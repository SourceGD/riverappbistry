# RiverApp

RiverApp is a python app dedicated to estimating the debit of a river based on a video. Take a movie of your river from the top, give it some insight of the bathymetry, and here you go !

## Installation procedure (recommended with Windows OS) [V]

Install the packages in a dedicated environment. To to do, there are multiple possibilities:

### With the conda `environment.yml` file:

```
conda env create -f environment_14-03-22_windows.yml
conda activate riverApp
garden install matplotlib
garden install graph
```

### With the 'requirements.txt' file:

```
conda create --name riverApp python=3.8 --file requirements.txt -c conda-forge
conda activate riverApp 
garden install matplotlib
garden install graph
```

### With pip using 'requirementsPip.txt' file:
You can also install all packages using pip, with the file `requirementsPip.txt` (beta). 
Note that this method is obsolete for this project and is therefore not recommended

## Installation procedure (recommended with Linux OS)

Install the packages in a dedicated environment. To to do, there are multiple possibilities:

### With the conda `environment.yml` file:

```
conda env create -f environment_14-03-22_linux.yml
conda activate riverApp
garden install matplotlib
garden install graph
```

The garden installation might get you an error of type 'Permission denied'. In that case, go to the directory hosting your environment (should look like '*/anaconda3/envs/riverApp/bin')
```
chmod u=rwx garden
garden install matplotlib
garden install graph
```

### With the 'requirements.txt' file:

In the file 'requirements.txt' , comment the line 'pywin32==304'

```
conda create --name riverApp python=3.8 --file requirements.txt -c conda-forge
conda activate riverApp 
garden install matplotlib
garden install graph
```

The garden installation might get you an error of type 'Permission denied'. In that case, go to the directory hosting your environment (should look like '*/anaconda3/envs/riverApp/bin')
```
chmod u=rwx garden
garden install matplotlib
garden install graph
```

### With pip using 'requirementsPip.txt' file:
You can also install all packages using pip, with the file `requirementsPip.txt` (beta). 
Note that this method is not robust since it doesn't deal with dependencies. It is therefore not recommended.

```
conda create --name riverApp python=3.8 
conda activate riverApp  
pip install -r requirementsPip.txt
garden install matplotlib
garden install graph
```

The garden installation might get you an error of type 'Permission denied'. In that case, go to the directory hosting your environment (should look like '*/anaconda3/envs/riverApp/bin')
```
chmod u=rwx garden
garden install matplotlib
garden install graph
```


## Installation procedure (recommended with Mas OS) [V]
No specific procedure, use a Virtual Machine to use a Linux OS.
