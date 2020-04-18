import init
import grid_maker

import matplotlib.pyplot as plt


def show_grid(space):
    plt.imshow(space, cmap='binary')
    plt.show()


def main():
    universe = grid_maker.Grid(grid_size=6).build_grid()
    initialisation = init.Init(universe=universe).random_init(init_length=4)

    show_grid(initialisation)


if __name__ == '__main__':
    main()
