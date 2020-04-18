import random
import numpy as np


class Init:
    def __init__(self, universe: np.ndarray):
        """
        Init Constructor.
        :param universe: the blank grid we want to initialize with "living cells"
        """
        self.universe = universe

    def random_init(self, random_init_length: int):
        """
        Functions that implements a random initialization for the Conway's
        Game-of-Life.
        :param random_init_length: length of the random initialization
        :return: grid with a random centered initialization
        """
        grid = self.universe
        init = []
        for i in range(random_init_length):
            randomList = []
            for j in range(random_init_length):
                n = random.randint(0, 1)
                randomList.append(n)
            init.append(randomList)
        grid[int((len(self.universe) - random_init_length) / 2):(
                len(self.universe) - int((len(self.universe) - random_init_length) / 2)),
        int((len(self.universe) - random_init_length) / 2):(
                len(self.universe) - int((len(self.universe) - random_init_length) / 2))] = init
        return grid
