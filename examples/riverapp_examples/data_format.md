Informations about the format of the different data files required for the run of riverApp

# Load files in the appropriate directory (recommended)

First, create a folder in **./examples/riverapp_examples/your_river/**
	where **your_river** is the name of your dataset
Note that everything you add in the **riverapp_examples** will be ignored by git thanks to **.gitignore**

The three following files must exists in order to launch the process
	- **./examples/riverapp_examples/your_river/video.mp4**
	- **./examples/riverapp_examples/your_river/dimension.txt**
	- **./examples/riverapp_examples/your_river/bathymetry.txt**
	
# Files format

## video file
Should be a video of the river with four visible tags.

## dimension file
A file containing one line with the 6 distances :
	**L_AB, L_BC, L_CD, L_DA, L_AC, L_DB**
where these distances refers to the distances between the reference points A,B,C and D (A top left corner then clockwise order)
Note that the number should be separated with a comma (=,)
Note that a line starting with '#' will be ignored

## bathymetry file
A file containing the (x,y) coordinates refering to the depth of the river along a section of the river
	**x1,y1**
	**X2,y2**
	...
Note that the the first line of that file should be 'x,y'
Note that the x-coord refer to the coordinate along the section of the river
              y-coord refer to the depth of the river
Note that the number should be separated with a comma (=,)
