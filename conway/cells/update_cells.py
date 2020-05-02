import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
import multiprocessing
from multiprocessing import Process

# python -m conway -gs 100 -ri -ril 50


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

    def thread(self, slice: np.ndarray):
        for pos in slice:
            x, y = pos
            min_y = max(y - 1, 0)
            max_y = min(y + 2, self.max_y)
            min_x = max(x - 1, 0)
            max_x = min(x + 2, self.max_x)
            new_pos = np.array(
                [[i, j] for i in range(min_x, max_x) for j in range(min_y, max_y) if i != x or j != y])
            for new in new_pos:
                if not any(np.equal(slice, new).all(axis=-1)):
                    slice = np.concatenate((slice, np.expand_dims(new, axis=0)))

        for position in slice:
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

    def update_cells(self) -> None:

        duplication = self.universe.copy()
        positions = np.argwhere(self.universe == 1)
        split = np.array_split(positions, 4)



        slice1 = split[0]
        slice2 = split[1]
        slice3 = split[2]
        slice4 = split[3]

        processes = list()

        # Create new processes
        process1 = Process(target=self.thread, args=(slice1,))
        process2 = Process(target=thread, args=(slice2,))
        process3 = Process(target=thread, args=(slice3,))
        process4 = Process(target=thread, args=(slice4,))

        # Add processes to process list
        processes.append(process1)
        processes.append(process2)
        processes.append(process3)
        processes.append(process4)

        # Start new Processes
        for p in processes:
            p.start()

        # Wait for all processes to complete
        for p in processes:
            p.join()

        # threadLock = threading.Lock()
        # threads = []
        #
        # # Create new threads
        # thread1 = threading.Thread(target=thread, args=(slice1,))
        # thread2 = threading.Thread(target=thread, args=(slice2,))
        # thread3 = threading.Thread(target=thread, args=(slice3,))
        # thread4 = threading.Thread(target=thread, args=(slice4,))
        #
        # # Add threads to thread list
        # threads.append(thread1)
        # threads.append(thread2)
        # threads.append(thread3)
        # threads.append(thread4)
        #
        # # Start new Threads
        # for t in threads:
        #     t.start()
        #
        # # Wait for all threads to complete
        # for t in threads:
        #     t.join()

        # for pos in positions:
        #     x, y = pos
        #     min_y = max(y - 1, 0)
        #     max_y = min(y + 2, self.max_y)
        #     min_x = max(x - 1, 0)
        #     max_x = min(x + 2, self.max_x)
        #     new_pos = np.array([[i, j] for i in range(min_x, max_x) for j in range(min_y, max_y) if i != x or j != y])
        #     for new in new_pos:
        #         if not any(np.equal(positions, new).all(axis=-1)):
        #             positions = np.concatenate((positions, np.expand_dims(new, axis=0)))
        #
        # for position in positions:
        #     x, y = position
        #     min_y = max(y - 1, 0)
        #     max_y = min(y + 2, self.max_y)
        #     min_x = max(x - 1, 0)
        #     max_x = min(x + 2, self.max_x)
        #     sum_of_cells = 0
        #     for i in range(min_x, max_x):
        #         for j in range(min_y, max_y):
        #             if i == x and j == y:
        #                 continue
        #             sum_of_cells += self.universe[i, j]
        #
        #     if sum_of_cells == 3:
        #         duplication[x][y] = 1
        #     if sum_of_cells < 2 or sum_of_cells > 3:
        #         duplication[x][y] = 0

        self.universe = duplication

    def animate(self, i: int) -> np.ndarray:
        self.update_cells()
        self.im.set_data(self.universe)
        return self.im

    def run(self, speed: int) -> None:
        _ = animation.FuncAnimation(self.fig, self.animate, interval=speed, repeat=True)
        plt.show()
