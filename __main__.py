import click

from .cells import living_cells
from .cells import update_cells
from .grid import grid_maker

import matplotlib.pyplot as plt


def show_grid(universe: grid_maker):
    fig = plt.figure()
    plt.imshow(universe, cmap='binary')
    plt.show()


@click.command()
@click.option("--grid_size", "-gs", "grid_size", type=int, default=100)
@click.option("--random_init", "-ri", "random_init", type=bool, default=False)
@click.option("--random_init_length", "-ril", "random_init_length", type=int, default=10)
@click.option("--beacon", "-beacon", "beacon", type=bool, default=False)
@click.option("--blinker", "-blinker", "blinker", type=bool, default=False)
@click.option("--toad", "-toad", "toad", type=bool, default=False)
def main(grid_size: int, random_init: bool, random_init_length: int, beacon: bool, blinker: bool, toad: bool) -> None:
    universe = grid_maker.Grid(grid_size).build_grid()

    if random_init:
        random_initialization = living_cells.LivingCells(universe=universe).random_init(random_init_length=random_init_length)
        show_grid(random_initialization)
    else:
        if beacon:
            beacon_initialization = living_cells.LivingCells(universe=universe).beacon()
            update = update_cells.UpdateCells(universe=beacon_initialization).update_cells()
            show_grid(update)
        if blinker:
            blinker_initialization = living_cells.LivingCells(universe=universe).blinker()
            update = update_cells.UpdateCells(universe=blinker_initialization).update_cells()
            show_grid(update)
        if toad:
            toad_initialization = living_cells.LivingCells(universe=universe).toad()
            update = update_cells.UpdateCells(universe=toad_initialization).update_cells()
            show_grid(update)


if __name__ == '__main__':
    main()
