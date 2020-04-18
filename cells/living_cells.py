import random
import numpy as np


class LivingCells:
    def __init__(self, universe: np.ndarray):
        """
        Init Constructor.
        :param universe: the blank grid we want to initialize with "living cells"
        """
        self.universe = universe

    def random_init(self, random_init_length: int) -> np.ndarray:
        """
        Method that implements a random initialization for the Conway's
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

    def beacon(self) -> np.ndarray:
        """
        Method that implements a Beacon oscillator.
        :return: universe with a beacon at its center
        """
        grid = self.universe
        beacon = [[1, 1, 0, 0],
                  [1, 1, 0, 0],
                  [0, 0, 1, 1],
                  [0, 0, 1, 1]]
        if len(grid) % 2 == 0:
            grid[int((len(grid) - len(beacon)) / 2):(
                    len(grid) - int((len(grid) - len(beacon)) / 2)),
            int((len(grid) - len(beacon)) / 2):(
                    len(grid) - int((len(grid) - len(beacon)) / 2))] = beacon
        else:
            grid[int((len(grid) - len(beacon)) / 2):(
                    len(grid) - int((len(grid) - len(beacon)) / 2 + 1)),
            int((len(grid) - len(beacon)) / 2):(
                    len(grid) - int((len(grid) - len(beacon)) / 2 + 1))] = beacon
        return grid

    def blinker(self) -> np.ndarray:
        """
        Method that implements a Blinker oscillator.
        :return: universe with a blinker at its center
        """
        grid = self.universe
        blinker = [1, 1, 1]
        if len(grid) % 2 == 0:
            grid[int(len(grid) / 2) - 1, int(len(grid) / 2) - 1:int(len(grid) / 2) + 2] = blinker
        else:
            grid[int(len(grid) / 2), int(len(grid) / 2) - 1:int(len(grid) / 2) + 2] = blinker
        return grid

    def toad(self) -> np.ndarray:
        """
        Method that implements a Toad oscillator.
        :return: universe with a toad at its center
        """
        grid = self.universe
        toad = [[0, 1, 1, 1],
                [1, 1, 1, 0]]

        grid[int(len(grid) / 2) - 1:int(len(grid) / 2) + 1,
            int((len(grid) - len(toad[0])) / 2):int((len(grid) - len(toad[0])) / 2) + 4] = toad

        return grid
