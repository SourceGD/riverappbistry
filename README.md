RiverApp
========

Installation
------------

**RiverApp** uses Python 3.10. No help is provided if you are using another version.

### Installation from latest code base (Windows 64 bits)

To install **RiverApp** from the code base with Windows 64 bits , go through these steps.

First, clone the code with `git` and move into the cloned folder.

```
git clone https://forge.uclouvain.be/hydraulics-simulations/riverapp.git
cd riverapp
```

Setup the environment with all dependencies as follows : 

```
pip install libs/pyproj-3.3.1-cp310-cp310-win_amd64.whl 
pip install libs/Shapely-1.8.2-cp310-cp310-win_amd64.whl
pip install -r requirements.txt
pip install libs/Cartopy-0.20.2-cp310-cp310-win_amd64.whl
```

> **_note :_** the Windows binaries files for pyproj, shapely and cartopy are provided by Christoph Gohlke on this [page](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

> **_note 2 :_** this environments do not have the dependencies needed for testing and documenting

### Installation from latest code base (Windows 32 bites)

To install **RiverApp** from the code base with Windows 32 bits , go through these steps.

First, clone the code with `git` and move into the cloned folder.

```
git clone https://forge.uclouvain.be/hydraulics-simulations/riverapp.git
cd riverapp
```

Setup the environment with all dependencies as follows : 

```
pip install libs/pyproj-3.3.1-cp310-cp310-win32.whl
pip install libs/Shapely-1.8.2-cp310-cp310-win32.whl
pip install -r requirements.txt
pip install libs/Cartopy-0.20.2-cp310-cp310-win32.whl
```

> **_note :_** the Windows binaries files for pyproj, shapely and cartopy are provided by Christoph Gohlke on this [page](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

> **_note 2 :_** this environments do not have the dependencies needed for testing and documenting

Project organisation
--------------------
    .
    ├── README.md
    ├── environment.txt         <- TXT-file for setting up the project dependencies
    ├── main.py                 <- main file which launches RiverApp
    ├── definitions.py          <- set of constants useful for RiverApp
    ├── .gitlab-ci.yml          <- RiverApp CI/CD configuration file
    ├── assets                  <- RiverApp assets such as images, data, logos, etc.
        ├── ...
    ├── config                  <- RiverApp configurations
        ├── ...
    ├── docs                    <- Sphinx documentation source code
        ├── ...
    ├── examples                <- Sets of examples on how to use the project
        ├── pyorc_examples      <- Jupyter notebooks with examples how to use the PyOrc API
            ├── ...             
        ├── riverapp_examples   <- images, files & data on the results you can expect from RiverApp
            ├── ...
    ├── libs                    <- libraries within the project
        ├── pyorc               <- pyorc library
            ├── ...  
        ├── ...  
    ├── src                     <- RiverApp source code
        ├── back                <- calculation & data management source code
            ├── ...
        ├── front               <- interface source code
            ├── ...
        ├── utils               <- useful functions for the whole project
            ├── ...        
    ├── tests                   <- pytest suite
        ├── pyorc_tests         <- pytest functions on PyOrc source code
            ├── ...     
        ├── riverapp_tests      <- pytest functions on RiverApp source code