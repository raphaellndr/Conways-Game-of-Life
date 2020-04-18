import click

import init
import grid_maker

import matplotlib.pyplot as plt


def show_grid(space):
    plt.imshow(space, cmap='binary')
    plt.show()


@click.command()
@click.option("--grid_size", "-gs", "grid_size", type=int, default=100)
@click.option("--random_init", "-ri", "random_init", type=bool, default=False)
@click.option("--random_init_length", "-ril", "random_init_length", type=int, default=10)
def main(grid_size: int, random_init: bool, random_init_length: int):
    universe = grid_maker.Grid(grid_size).build_grid()

    if random_init:
        random_initialisation = init.Init(universe=universe).random_init(random_init_length=random_init_length)
        show_grid(random_initialisation)
    else:
        pass


if __name__ == '__main__':
    main()
