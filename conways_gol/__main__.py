import click

from conways_gol.cells import living_cells_initialization, update_cells
from conways_gol.cells import update_cells_multiprocessing, update_cells_threading
from conways_gol.grid import grid_maker


@click.command()
@click.option("--grid_size", "-gs", "grid_size", type=int, default=100)
@click.option("--speed", "-s", "speed", type=float, default=0.005)
@click.option("--random_init", "-ri", "random_init", is_flag=True)
@click.option("--random_init_length", "-ril", "random_init_length", type=int, default=10)
@click.option("--beacon", "-bc", "beacon", is_flag=True)
@click.option("--blinker", "-bl", "blinker", is_flag=True)
@click.option("--toad", "-t", "toad", is_flag=True)
@click.option("--pulsar", "-p", "pulsar", is_flag=True)
@click.option("--gosper_glider_gun", "-ggg", "gosper_glider_gun", is_flag=True)
def main(grid_size: int,
         speed: int,
         random_init: bool,
         random_init_length: int,
         beacon: bool,
         blinker: bool,
         toad: bool,
         pulsar: bool,
         gosper_glider_gun: bool) -> None:

    universe = grid_maker.Grid(grid_size).build_grid()

    if random_init:
        random_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).random_init(random_init_length=random_init_length)
        matrix = update_cells_multiprocessing.UpdateCells(universe=random_initialization)
        matrix.run(speed)
    else:
        if beacon:
            beacon_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).beacon()
            matrix = update_cells_multiprocessing.UpdateCells(universe=beacon_initialization)
            matrix.run(speed)
        elif blinker:
            blinker_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).blinker()
            matrix = update_cells_multiprocessing.UpdateCells(universe=blinker_initialization)
            matrix.run(speed)
        elif toad:
            toad_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).toad()
            matrix = update_cells_multiprocessing.UpdateCells(universe=toad_initialization)
            matrix.run(speed)
        elif pulsar:
            pulsar_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).pulsar()
            matrix = update_cells_multiprocessing.UpdateCells(universe=pulsar_initialization)
            matrix.run(speed)
        elif gosper_glider_gun:
            ggg_initialization = living_cells_initialization.LivingCellsInitialization(universe=universe).gosper_glider_gun()
            matrix = update_cells_multiprocessing.UpdateCells(universe=ggg_initialization)
            matrix.run(speed)


if __name__ == '__main__':
    main()
