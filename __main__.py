import click

import init
import grid_maker

import matplotlib.pyplot as plt


def show_grid(space):
    plt.imshow(space, cmap='binary')
    plt.show()


@click.command()
@click.option("--grid_size", "-gs", "grid_size", type=int, default=100)
@click.option("--init_length", "-il", "init_length", type=int, default=10)
def main(init_length: int, grid_size: int):
    universe = grid_maker.Grid(grid_size).build_grid()
    initialisation = init.Init(universe=universe).random_init(init_length)

    show_grid(initialisation)


if __name__ == '__main__':
    main()
