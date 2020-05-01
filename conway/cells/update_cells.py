import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def test(i: int, j: int, counter: int, duplication: np.ndarray) -> None:
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
    if counter == 2:
        pass
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
        grid = self.universe
        duplication = grid.copy()
        size = len(grid)

        positions = np.argwhere(grid == 1)
        for pos in positions:
            x, y = pos
            new_pos = np.array([[x+i, y+j] for i in range(-1, 2) for j in range(-1, 2) if i != j])
            for new in new_pos:
                if not any(np.equal(positions, new).all(axis=-1)):
                    positions = np.concatenate((positions, np.expand_dims(new, axis=0)))

        # ones_pos_t = positions.T
        # ones_pos_t = (ones_pos_t[0], ones_pos_t[1])

        for position in positions:
            x, y = position
            print(f"x: {x}, y: {y}")
            min_y = max(y-1, 0)
            max_y = min(y+1, self.max_y)
            min_x = max(x-1, 0)
            max_x = max(x+1, self.max_x)
            for i in range(min_x, max_x):
                for j in range(min_y, max_y):
                    print(i, y)
            # print(x, y)

        exit(0)

        # print(np.where(grid == 1))
        # print(grid[np.where(grid == 1)])
        for i in range(size):
            for j in range(size):
                living_cells_counter = 0
                # top left hand corner
                if i == 0 == j:
                    if grid[i][j + 1] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j + 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)
                # top right hand corner
                elif i == 0 and j == size - 1:
                    if grid[i][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j - 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)
                # bottom left hand corner
                elif i == size - 1 and j == 0:
                    if grid[i][j + 1] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j + 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)
                # bottom right hand corner
                elif i == size - 1 == j:
                    if grid[i][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j - 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)
                # top side
                elif i == 0 and (j != 0 and j != size - 1):
                    if grid[i][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i][j + 1] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j + 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)
                # bottom side
                elif i == size - 1 and (j != 0 and j != size - 1):
                    if grid[i][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i][j + 1] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j + 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)
                # left side
                elif j == 0 and (i != 0 and i != size - 1):
                    if grid[i][j + 1] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j + 1] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j + 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)
                # right side
                elif j == size - 1 and (i != 0 and i != size - 1):
                    if grid[i][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j - 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)
                # rest of the grid
                else:
                    if grid[i][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i][j + 1] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i - 1][j + 1] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j - 1] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j] == 1:
                        living_cells_counter += 1
                    if grid[i + 1][j + 1] == 1:
                        living_cells_counter += 1
                    test(i, j, living_cells_counter, duplication)

        self.universe = duplication

    def animate(self, i: int) -> np.ndarray:
        self.update_cells()
        self.im.set_data(self.universe)
        return self.im

    def run(self, speed: int) -> None:
        _ = animation.FuncAnimation(self.fig, self.animate, interval=speed, repeat=True)
        plt.show()


