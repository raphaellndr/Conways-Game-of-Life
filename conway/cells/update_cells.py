import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def update_cell(i: int, j: int, counter: int, duplication: np.ndarray) -> None:
    """
    Method that updates the cell depending on the results of the 3 rules.

    :param duplication:
    :param i: line index
    :param j: column index
    :param counter: number of neighboring living cells
    :return:
    """
    if counter == 3:
        duplication[i][j] = 1
    if counter < 2 or counter > 3:
        duplication[i][j] = 0


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

    def update_cells(self) -> None:
        start = time.time()

        grid = self.universe
        duplication = grid.copy()

        positions = np.argwhere(grid == 1)
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
            min_y = max(y-1, 0)
            max_y = min(y+2, self.max_y)
            min_x = max(x-1, 0)
            max_x = min(x+2, self.max_x)
            sum_of_cells = 0
            for i in range(min_x, max_x):
                for j in range(min_y, max_y):
                    if i == x and j == y:
                        continue
                    sum_of_cells += grid[i, j]

            update_cell(x, y, int(sum_of_cells), duplication)

        self.universe = duplication

        print(f"Elapsed time: {time.time() - start}")

    def animate(self, i: int) -> np.ndarray:
        self.update_cells()
        self.im.set_data(self.universe)
        return self.im

    def run(self, speed: int) -> None:
        _ = animation.FuncAnimation(self.fig, self.animate, interval=speed, repeat=True)
        plt.show()


