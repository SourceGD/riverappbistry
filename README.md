# RiverApp

RiverApp is a python app dedicated to estimating the debit of a river based on a video. Take a movie of your river from the top, give it some insight of the bathymetry, and here you go !

## Installation procedure

Version de python=3.8

conda install:
  - numpy=1.18.5
  - scipy=1.5.0
  - matplotlib=3.2.2
  - opencv=4.0.1

conda install -c conda-forge:
  - kivy=1.11.0
  - kivy-garden=0.1.4
  - openpiv=0.23.4
  - imutils=0.5.3
  
garden install:
  - graph


Install the packages in a dedicated environment. You can do that in two codes of line with Anaconda:
'''
conda create --name riverApp python=3.8
conda activate riverApp
conda install --file requirements.txt -c conda-forge
'''

You can also install all packages using pip, with the file 'requirementsPip.txt'.