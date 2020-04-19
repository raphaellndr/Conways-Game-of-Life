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

    def update_cells(self) -> np.ndarray:
        grid = self.universe
        duplication = grid.copy()
        size = len(grid)
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
        grid = duplication
        return duplication
