import multiprocessing
import os
import time
import typing
import psutil

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

PROCESSES: typing.List[multiprocessing.Process] = []
PAUSE: bool = False


class UpdateCells:
    def __init__(self, universe: np.ndarray):
        """
        UpdateCells Constructor.

        :param universe: the blank grid we want to initialize with "living cells"
        """

        print(f"__init__: {os.getpid()}")

        self.universe = universe
        self.real_shape = self.universe.shape
        self.__shared_universe = multiprocessing.Array("d", self.universe.size)
        self.__shared_universe[:] = self.universe.flatten()[:]

        self.fig = plt.figure()
        self.im = plt.imshow(universe, cmap='binary')

        self.max_x = universe.shape[0]
        self.min_x = 0
        self.max_y = universe.shape[1]
        self.min_y = 0

        manager = multiprocessing.Manager()
        self.positions: typing.List[np.ndarray] = manager.list()
        self.update_ok: manager.Value = manager.Value("i", 0)
        self.mutex_positions = manager.Lock()
        self.mutex_end_update = manager.Lock()
        self.cond_looking_for_positions = manager.Condition()
        self.event_compute_results = manager.Event()

        self.__is_alive = True
        self.speed: float = 0.0001

        self.iterations: int = 0

        self.list = list()

    def _init_processes(self):
        global PROCESSES

        # Create new processes and add each process to process list
        for i in range(multiprocessing.cpu_count() - 1):
            PROCESSES.append(multiprocessing.Process(
                target=looking_for_positions,
                args=(self,
                      i,
                      self.cond_looking_for_positions,
                      self.mutex_positions,
                      self.mutex_end_update,
                      self.event_compute_results,
                      self.positions,
                      self.update_ok
                      )
            ))
        PROCESSES.append(multiprocessing.Process(
            target=update_cells,
            args=(self, self.cond_looking_for_positions, self.event_compute_results, self.positions))
        )

    def _run_processes(self):
        global PROCESSES
        # Start new processes
        for p in PROCESSES:
            p.start()
            # m = psutil.Process(p.pid)
            # self.list.append(m)
            time.sleep(0.1)

        # Wait for all processes to complete
        try:
            speed = max(10, min(int(self.speed * 1000), 1000))
            self.run_animation(speed)
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            self.__is_alive = False
            for p in PROCESSES:
                p.join()

    @property
    def shared_universe(self) -> np.ndarray:
        shared_universe = self.__shared_universe[:]
        shared_universe = np.array(shared_universe)
        return np.reshape(shared_universe, self.real_shape)

    @staticmethod
    def end_update(
            mutex_end_update: multiprocessing.Lock,
            event_compute_results: multiprocessing.Event,
            update_ok: multiprocessing.Value
    ):
        """
        :param mutex_end_update:
        :param event_compute_results:
        :param update_ok:
        """

        # print(f"[{os.getpid()}] end_update value: {update_ok.value}")

        with mutex_end_update:
            update_ok.value += 1
            if update_ok.value == multiprocessing.cpu_count() - 1:
                # print(f"[{os.getpid()}] end_update: OK")
                update_ok.value = 0
                event_compute_results.set()

    def looking_for_positions(
            self,
            position_id: int,
            cond_looking_for_positions: multiprocessing.Condition,
            mutex_positions: multiprocessing.Lock,
            mutex_end_update: multiprocessing.Lock,
            event_compute_results: multiprocessing.Event,
            positions,
            update_ok
    ):
        """
        :param position_id:
        :param cond_looking_for_positions:
        :param mutex_positions:
        :param mutex_end_update:
        :param event_compute_results:
        :param positions:
        :param update_ok:
        """

        while self.__is_alive:
            # print(f"[{os.getpid()}] looking_for_positions: {position_id}")
            with cond_looking_for_positions:
                cond_looking_for_positions.wait()

            _positions = positions[position_id]
            for pos in _positions:
                x, y = pos
                min_y = max(y - 1, 0)
                max_y = min(y + 2, self.max_y)
                min_x = max(x - 1, 0)
                max_x = min(x + 2, self.max_x)
                new_pos = np.array(
                    [[i, j] for i in range(min_x, max_x) for j in range(min_y, max_y) if i != x or j != y])
                for new in new_pos:
                    if not any(np.equal(_positions, new).all(axis=-1)):
                        _positions = np.concatenate((_positions, np.expand_dims(new, axis=0)))

            with mutex_positions:
                positions[position_id] = _positions

            self.end_update(mutex_end_update, event_compute_results, update_ok)

    def update_cells(
            self,
            cond_looking_for_positions: multiprocessing.Condition,
            event_compute_results: multiprocessing.Event,
            positions
    ):
        """
        :param cond_looking_for_positions:
        :param event_compute_results:
        :param positions:
        """

        while self.__is_alive:
            # print(f"[{os.getpid()}] update_cells")
            duplication = self.universe.copy()
            _positions = np.argwhere(self.universe == 1)
            _positions = np.array_split(_positions, multiprocessing.cpu_count() - 1)

            positions[:] = [position for position in _positions]

            with cond_looking_for_positions:
                cond_looking_for_positions.notify_all()
            event_compute_results.wait()
            event_compute_results.clear()

            _positions = positions[0]
            for position in positions[1:]:
                _positions = np.concatenate((_positions, position))
            # Remove duplicates
            _positions = np.unique(_positions, axis=0)

            for position in _positions:
                x, y = position
                min_y = max(y - 1, 0)
                max_y = min(y + 2, self.max_y)
                min_x = max(x - 1, 0)
                max_x = min(x + 2, self.max_x)
                sum_of_cells = 0
                for i in range(min_x, max_x):
                    for j in range(min_y, max_y):
                        if i == x and j == y:
                            continue
                        sum_of_cells += self.universe[i, j]

                if sum_of_cells == 3:
                    duplication[x][y] = 1
                if sum_of_cells < 2 or sum_of_cells > 3:
                    duplication[x][y] = 0

            self.universe = duplication
            self.__shared_universe[:] = self.universe.flatten()[:]
            time.sleep(self.speed)

    def animate(self, i: int) -> np.ndarray:
        """
        :param i:
        :return:
        """
        if PAUSE:
            for process in self.list:
                process.suspend()
        if not PAUSE:
            # for process in self.list:
            #     process.resume()
            self.iterations += 1
            plt.title(f"Number of iterations : {self.iterations}")
            self.im.set_data(self.shared_universe)
            return self.im

    def run_animation(self, speed: int) -> None:
        """
        :param speed:
        """
        self.fig.canvas.mpl_connect('button_press_event', on_click)

        _ = animation.FuncAnimation(self.fig, self.animate, interval=speed, repeat=True)
        plt.show()

    def run(self, speed: float) -> None:
        """
        :param speed:
        """

        self.speed = speed
        self._init_processes()
        self._run_processes()


def looking_for_positions(
        matrix: UpdateCells,
        position_id: int,
        cond_looking_for_positions: multiprocessing.Condition,
        mutex_positions: multiprocessing.Lock,
        mutex_end_update: multiprocessing.Lock,
        event_compute_results: multiprocessing.Event,
        positions,
        update_ok
):
    """
    :param matrix:
    :param position_id:
    :param cond_looking_for_positions:
    :param mutex_positions:
    :param mutex_end_update:
    :param event_compute_results:
    :param positions:
    :param update_ok:
    :return:
    """

    return matrix.looking_for_positions(
        position_id,
        cond_looking_for_positions,
        mutex_positions,
        mutex_end_update,
        event_compute_results,
        positions,
        update_ok
    )


def update_cells(
        matrix: UpdateCells,
        cond_looking_for_positions: multiprocessing.Condition,
        event_compute_results: multiprocessing.Event,
        positions
):
    """
    :param matrix:
    :param cond_looking_for_positions:
    :param event_compute_results:
    :param positions:
    :return:
    """

    return matrix.update_cells(
        cond_looking_for_positions,
        event_compute_results,
        positions
    )


def on_click(event):
    global PAUSE
    PAUSE ^= True
