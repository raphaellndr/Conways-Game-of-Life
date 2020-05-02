from multiprocessing import Process
import time
import threading
import typing

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


# python -m conway -gs 100 -ri -ril 50
# python -m conway -gs 10 -bc


class UpdateCells:
    def __init__(self, universe: np.ndarray):
        """
        UpdateCells Constructor.

        :param universe: the blank grid we want to initialize with "living cells"
        """
        self.universe = universe
        self.fig = plt.figure()
        self.im = plt.imshow(universe, cmap='binary')
        self.max_x = universe.shape[0]
        self.min_x = 0
        self.max_y = universe.shape[1]
        self.min_y = 0
        self.slices: typing.List[np.ndarray] = []
        self.positions: typing.List[np.ndarray] = []

        self.threads: typing.List[threading.Thread] = []

        self.__is_alive = True

        self._init_threads()

        self.update_ok: int = 0
        self.mutex = threading.Lock()
        self.mutex_end_update = threading.Lock()
        self.barrier_looking_for_positions = threading.Barrier(len(self.threads) - 1)
        self.event_end_of_compute = threading.Event()
        self.event_compute_results = threading.Event()

    def _init_threads(self):
        # Create new threads
        thread0 = threading.Thread(target=self.update_cells_v2)
        thread1 = threading.Thread(target=self.looking_for_positions, args=(1,))
        thread2 = threading.Thread(target=self.looking_for_positions, args=(2,))
        thread3 = threading.Thread(target=self.looking_for_positions, args=(3,))
        thread4 = threading.Thread(target=self.looking_for_positions, args=(4,))

        # Add threads to thread list
        self.threads.append(thread0)
        self.threads.append(thread1)
        self.threads.append(thread2)
        self.threads.append(thread3)
        self.threads.append(thread4)

    def _run_threads(self):
        # Start new Threads
        for t in self.threads:
            t.start()

        # Wait for all threads to complete
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            self.__is_alive = False
            for t in self.threads:
                t.join()

    def end_update(self):
        with self.mutex_end_update:
            self.update_ok += 1
            if self.update_ok == len(self.threads) - 1:
                print("YOLO")
                self.update_ok = 0
                self.event_compute_results.set()

                self.event_end_of_compute.wait()
                self.event_end_of_compute.clear()

    def looking_for_positions(self, position_id: int):
        while self.__is_alive:
            print(f"looking_for_positions, waiting: {position_id}")
            self.barrier_looking_for_positions.wait()

            positions = self.positions[position_id]
            if position_id == 0:
                print(len(positions))
            for pos in positions:
                x, y = pos
                min_y = max(y - 1, 0)
                max_y = min(y + 2, self.max_y)
                min_x = max(x - 1, 0)
                max_x = min(x + 2, self.max_x)
                new_pos = np.array([[i, j] for i in range(min_x, max_x) for j in range(min_y, max_y) if i != x or j != y])
                for new in new_pos:
                    if not any(np.equal(positions, new).all(axis=-1)):
                        positions = np.concatenate((positions, np.expand_dims(new, axis=0)))
            if position_id == 0:
                print(len(positions))
            with self.mutex:
                self.positions[position_id] = positions

            self.end_update()

    def update_cells_v2(self):
        while self.__is_alive:
            print("update_cells_v2")
            duplication = self.universe.copy()
            positions = np.argwhere(self.universe == 1)
            print(positions.shape)
            positions = np.array_split(positions, len(self.threads))

            self.positions = [position for position in positions]

            self.event_compute_results.wait()
            self.event_compute_results.clear()

            positions = self.positions[0]
            for position in self.positions[1:]:
                positions = np.concatenate((positions, position))
            # Remove duplicates
            positions = np.unique(positions, axis=0)

            for position in positions:
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
            print(self.universe)

            self.event_end_of_compute.set()

    def update_cells_v1(self) -> None:
        duplication = self.universe.copy()
        positions = np.argwhere(self.universe == 1)

        for pos in positions:
            x, y = pos
            min_y = max(y - 1, 0)
            max_y = min(y + 2, self.max_y)
            min_x = max(x - 1, 0)
            max_x = min(x + 2, self.max_x)
            new_pos = np.array([[i, j] for i in range(min_x, max_x) for j in range(min_y, max_y) if i != x or j != y])
            for new in new_pos:
                if not any(np.equal(positions, new).all(axis=-1)):
                    positions = np.concatenate((positions, np.expand_dims(new, axis=0)))

        for position in positions:
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

    def animate(self, i: int) -> np.ndarray:
        self.update_cells()
        self.im.set_data(self.universe)
        return self.im

    def run_v1(self, speed: int) -> None:
        _ = animation.FuncAnimation(self.fig, self.animate, interval=speed, repeat=True)
        plt.show()

    def run_v2(self) -> None:
        self._run_threads()
