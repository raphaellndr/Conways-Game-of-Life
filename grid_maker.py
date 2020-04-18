import numpy as np


class Grid:
    def __init__(self, grid_size: int):
        self.grid_size = grid_size

    def build_grid(self) -> np.ndarray:
        size = self.grid_size
        universe = np.zeros((size, size))
        return universe


