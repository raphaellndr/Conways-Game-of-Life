import numpy as np


class Grid:
    def __init__(self, grid_size: int):
        """
        Grid Constructor.
        :param grid_size: size of the grid
        """
        self.grid_size = grid_size

    def build_grid(self) -> np.ndarray:
        """
        Method that creates the starting blank grid in order to begin the
        Conway's Game-of-Life.
        :return: blank grid called the "universe"
        """
        size = self.grid_size
        universe = np.zeros((size, size))
        return universe


