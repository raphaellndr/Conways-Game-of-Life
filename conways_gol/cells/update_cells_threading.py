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
        self.positions: typing.List[np.ndarray] = []

        self.threads: typing.List[threading.Thread] = []

        self.__is_alive = True
        self.speed: float = 0.0001

        self._init_threads()

        self.update_ok: int = 0
        self.mutex_positions = threading.Lock()
        self.mutex_end_update = threading.Lock()
        self.cond_looking_for_positions = threading.Condition()
        self.event_compute_results = threading.Event()

    def _init_threads(self):
        # Create new threads
        thread0 = threading.Thread(target=self.update_cells)
        thread1 = threading.Thread(target=self.looking_for_positions, args=(0,))
        thread2 = threading.Thread(target=self.looking_for_positions, args=(1,))
        thread3 = threading.Thread(target=self.looking_for_positions, args=(2,))
        thread4 = threading.Thread(target=self.looking_for_positions, args=(3,))

        # Add threads to thread list
        self.threads.append(thread1)
        self.threads.append(thread2)
        self.threads.append(thread3)
        self.threads.append(thread4)
        self.threads.append(thread0)

    def _run_threads(self):
        # Start new threads
        for t in self.threads:
            t.start()
            time.sleep(0.25)

        # Wait for all threads to complete
        try:
            speed = max(10, min(int(self.speed*1000), 1000))
            self.run_animation(speed)
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
                self.update_ok = 0
                self.event_compute_results.set()

    def looking_for_positions(self, position_id: int):
        while self.__is_alive:
            with self.cond_looking_for_positions:
                self.cond_looking_for_positions.wait()

            positions = self.positions[position_id]
            for pos in positions:
                x, y = pos
                min_y = max(y - 1, 0)
                max_y = min(y + 2, self.max_y)
                min_x = max(x - 1, 0)
                max_x = min(x + 2, self.max_x)
                new_pos = np.array(
                    [[i, j] for i in range(min_x, max_x) for j in range(min_y, max_y) if i != x or j != y])
                for new in new_pos:
                    if not any(np.equal(positions, new).all(axis=-1)):
                        positions = np.concatenate((positions, np.expand_dims(new, axis=0)))

            with self.mutex_positions:
                self.positions[position_id] = positions

            self.end_update()

    def update_cells(self):
        while self.__is_alive:
            duplication = self.universe.copy()
            positions = np.argwhere(self.universe == 1)
            positions = np.array_split(positions, len(self.threads) - 1)

            self.positions = [position for position in positions]

            with self.cond_looking_for_positions:
                self.cond_looking_for_positions.notifyAll()
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
            time.sleep(self.speed)

    def animate(self, i: int) -> np.ndarray:
        self.im.set_data(self.universe)
        return self.im

    def run_animation(self, speed: int) -> None:
        _ = animation.FuncAnimation(self.fig, self.animate, interval=speed, repeat=True)
        plt.show()

    def run(self, speed: float) -> None:
        self.speed = speed
        self._run_threads()
