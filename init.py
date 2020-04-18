import random
import numpy as np


class Init:
    def __init__(self, universe: np.ndarray):
        self.universe = universe

    def random_init(self, init_length: int):
        grid = self.universe
        init = []
        for i in range(init_length):
            randomList = []
            for j in range(init_length):
                n = random.randint(0, 1)
                randomList.append(n)
            init.append(randomList)
        grid[int((len(self.universe) - init_length)/2):(len(self.universe) - int((len(self.universe) - init_length)/2)),
        int((len(self.universe) - init_length)/2):(len(self.universe) - int((len(self.universe) - init_length)/2))] = init
        return grid


