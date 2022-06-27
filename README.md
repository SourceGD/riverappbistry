# RiverApp

RiverApp is a python app dedicated to estimating the debit of a river based on a video. Take a movie of your river from the top, give it some insight of the bathymetry, and here you go !

## Installation procedure

Install the packages in a dedicated environment. To to do, there are multiple possibilities:

With the conda `.yml` file:

```
conda env create -f environment.yml
conda activate riverApp
```
or simply with
```
conda create --name riverApp python=3.8 --file requirements.txt -c conda-forge
conda activate riverApp
```

You can also install all packages using pip, with the file `requirementsPip.txt` (beta).