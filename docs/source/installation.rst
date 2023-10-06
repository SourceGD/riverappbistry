.. _installation:

============
Installation
============

**RiverApp** uses Python 3.10. No help is provided if you are using another version.

.. _install_win64:

Latest code base (Windows 64 bites)
===================================

To install **RiverApp** from the code base with Windows 64 bits , go through these steps.

First, clone the code with `git` and move into the cloned folder.

.. code-block:: console

    $ git clone https://forge.uclouvain.be/hydraulics-simulations/riverapp.git
    $ cd riverapp

Setup the environment with all dependencies as follows : 

.. code-block:: console

    $ pip install libs/pyproj-3.3.1-cp310-cp310-win_amd64.whl 
    $ pip install libs/Shapely-1.8.2-cp310-cp310-win_amd64.whl
    $ pip install -r requirements.txt
    $ pip install libs/Cartopy-0.20.2-cp310-cp310-win_amd64.whl

.. note::

    This environments do not have the dependencies needed for testing and documenting

    The Windows binaries files for pyproj, shapely and cartopy are provided by Christoph Gohlke on this BinariesSourcePage_

.. _install_win32:

Latest code base (Windows 32 bites)
===================================

To install **RiverApp** from the code base with Windows 32 bits , go through these steps.

First, clone the code with `git` and move into the cloned folder.

.. code-block:: console

    $ git clone https://forge.uclouvain.be/hydraulics-simulations/riverapp.git
    $ cd riverapp

Setup the environment with all dependencies as follows : 

.. code-block:: console

    $ pip install libs/pyproj-3.3.1-cp310-cp310-win32.whl
    $ pip install libs/Shapely-1.8.2-cp310-cp310-win32.whl
    $ pip install -r requirements.txt
    $ pip install libs/Cartopy-0.20.2-cp310-cp310-win32.whl

.. note::
    This environments do not have the dependencies needed for testing and documenting

    The Windows binaries files for pyproj, shapely and cartopy are provided by Christoph Gohlke on BinariesSourcePage_

.. _BinariesSourcePage: https://www.lfd.uci.edu/~gohlke/pythonlibs/