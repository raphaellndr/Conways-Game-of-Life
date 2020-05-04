Conway's Game of Life
=====================

|license| |python|

This project is a Python personal implementation of the well-known "`Game of Life <https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life>`_",
written using object-oriented programming.
Although is not said to be fully optimized, multithreading is being used to speed up the program, and other methods such
as multiprocessing or the use of `Ray <https://github.com/ray-project/ray>`_ are currently being implemented.

Requirements
============

Before running the code, you should consider using a virtual environment. To do so, you can either use conda or pip :

Using pip :
-----------

- verify that pip is installed :

.. code-block:: console

    $ pip --version

if not, `install it <https://pip.pypa.io/en/stable/installing/>`_.

When it is done, let's continue the installation :

- install pipenv :

.. code-block:: console

    $ pip install --user pipenv

- once it is installed and well configured, run your environment :

.. code-block:: console

    $ pipenv shell

Using conda :
-------------

- verify that conda is installed :

.. code-block:: console

    $ conda --version

if not, `install Anaconda <https://www.anaconda.com/products/individual>`_.

- then, create your conda environment and launch it:

.. code-block:: console

    $ conda create -n my_env
    $ conda activate my_env

Run the code
============

Before you can have some fun "playing" Conway's Game of Life, you should at least know how to run the code. So here are all
the commands yet implemented.

Main commands :
---------------

- choose the grid size (int, default to 100) :

.. code-block:: console

    $ python -m my_module -gs grid_size

- choose the speed (float, default to 0.005), which is the time between two updates :

.. code-block:: console

    $ python -m my_module -gs grid_size -s speed

Choose your start :
-------------------

- random init (bool, default to False if not chosen) and its length (int, default to 10) :

.. code-block:: console

    $ python -m my_module -gs grid_size -ri -ril random_init_length

- oscillators :

.. code-block:: console

    $ python -m my_module -gs grid_size -beacon
    $ python -m my_module -gs grid_size -blinker
    $ python -m my_module -gs grid_size -toad
    $ python -m my_module -gs grid_size -gosper_glider_gun

What's next ?
=============

The future of this project is to, once significantly/fully optimized, try to make some PyQT in order to create a "Conway's
Game of Life app". Thanks for reading this far and stay tuned !

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/raphaellndr/Conways-Game-of-Life/blob/master/LICENSEfe

.. |python| image:: https://img.shields.io/github/pipenv/locked/python-version/raphaellndr/Conways-Game-of-Life
    :target: https://www.python.org/downloads/release/python-376/
