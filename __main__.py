import click
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from .cells import living_cells_initialization
from .cells import update_cells
from .grid import grid_maker


def show_grid(universe: np.ndarray) -> None:
    fig = plt.figure()
    plt.imshow(universe, cmap='binary')
    plt.show()


beacon_initialization = None


@click.command()
@click.option("--grid_size", "-gs", "grid_size", type=int, default=100)
@click.option("--random_init", "-ri", "random_init", type=bool, default=False)
@click.option("--random_init_length", "-ril", "random_init_length", type=int, default=10)
@click.option("--beacon", "-beacon", "beacon", type=bool, default=False)
@click.option("--blinker", "-blinker", "blinker", type=bool, default=False)
@click.option("--toad", "-toad", "toad", type=bool, default=False)
def main(grid_size: int, random_init: bool, random_init_length: int, beacon: bool, blinker: bool, toad: bool) -> None:
    global beacon_initialization

    universe = grid_maker.Grid(grid_size).build_grid()

    if random_init:
        random_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).random_init(random_init_length=random_init_length)
        show_grid(random_initialization)
    else:
        if beacon:
            beacon_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).beacon()
            fig = plt.figure()
            im = plt.imshow(beacon_initialization, cmap='binary')

            def animate(i):
                global beacon_initialization
                beacon_initialization = update_cells.UpdateCells(universe=beacon_initialization).update_cells()
                im.set_data(beacon_initialization)
                return im

            anim = animation.FuncAnimation(fig, animate, interval=500, repeat=True)
            plt.show()
        if blinker:
            blinker_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).blinker()
            print(blinker_initialization)
            for i in range(10):
                update = show_matrix(blinker_initialization)
                blinker_initialization = update
                show_grid(update)
        if toad:
            toad_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).toad()
            print(toad_initialization)
            for i in range(10):
                update = show_matrix(toad_initialization)
                toad_initialization = update
                show_grid(update)


if __name__ == '__main__':
    main()