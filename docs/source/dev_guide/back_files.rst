.. _back_files:

#######################################
Back files and their respective uses
#######################################

This file will contain a list of the "back" files and where they are used.

Mask
---------------------------------------

The functions of this file are only used in the src/back/transect.py file to apply masks to the data received from the PIV analysis.
You can notice a commented plt.show() in the ``plot_result`` file, which displays the velocity field obtained thanks to the PIV.

Saving Project Data
---------------------------------------

This file contains all the functions needed to manage the project data stored in the json configuration files.

When a project is loaded, a SavingProjectData object is created and all the data is stored in this object.

This file handles all the getters and setters for this SavingProjectData objects. It also contains all the functions used to check if the format of some values is correct or not (e.g. backup file format, check if some data is missing from a given project dict, etc.).

The way the steps are handled is also managed by this file. Each time a setter is called, it registers it in the current loaded SavingProjectData object, and it directly writes it into the json file.

What is not correct about the organisation of this file is that it contains functions that should not be in this file. These functions are the following:

* ``_convert_dist_to_dest_points`` : converts beacons distances to points for the PIV analysis
* ``generate_piv`` : generates the PIV analysis, function already explained in the piv page


Transect
---------------------------------------

This file contains all the needed functions to process the PIV results and to plot the velocity field obtained, as well as the river discharge.
The functions are pretty much self-explanatory, you can take a look to the docstrings to understand what each function does.

Project data management and filter
---------------------------------------

The functions from theses files are either outdated or not used at all. They are not used in the current version of the software.