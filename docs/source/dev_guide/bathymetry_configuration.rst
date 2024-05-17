.. _bathymetry_configuration:

######################################
Bathymetry Configuration
######################################

The bathymetry configuration screen allows the user to configure the bathymetry data, as well as the mean water level at the time of the measurements.
This screen also lets the user select the surface coefficient, which can make the results vary.

When entering the screen, the application checks if the bathymetry data is already loaded by calling ``_load_bathymetry``.
If so, bathymetry plot is displayed on the screen by calling ``_display_loaded_bathymetry``
, which itself calls ``load_graph``, which will process the bathymetry graph plot and display it as a widget.
If not, the user is prompted to upload the bathymetry data.

When the user clicks on the "Upload bathymetry" button, the application opens the file manager using ``open_file_manager``.
When the user has chosen the file, the application calls ``_select_path``, which will load the graph of the bathymetry data and display it as a widget.

The user can then select the mean water level at the time of the measurements by entering the value in the text box.

When validating the entered data, the application calls ``validate_bathymetry``.

This screen uses custom widgets such as BathymetryGraph, which can be found in src/front/components/widget/bathymetry_graph.
This documentation will not cover this code in detail because it basic file reading, so you should get along with it.

The other components like ConfirmAction are basically small Kivy components, we will also not develop in this documentation.

Below is an example of a loaded bathymetry, as well as an example of the bathymetry file format supported.

.. figure:: ../_static/bathy_configuration.png
    :align: center

    Bathymetry Configuration Screen


.. code-block:: text

    x,y
    0,1.66
    0.2,0.61
    0.4,0.57
    0.6,0.53
    0.8,0.51
    1,0.48
    1.2,0.47
    1.4,0.43
    1.6,0.37
    1.8,0.33
    2,0.29
    2.2,0.23
    2.4,0.17
    2.6,0.07
    2.8,0.05
    3,0.07
    3.2,0.01
    3.4,0
    3.6,0.05
    3.8,0.08
    4,0.1
    4.2,0.08
    4.4,0.1
    4.6,0.05
    4.8,0.08
    5,0.09
    5.2,0.13
    5.4,0.15
    5.6,0.14
    5.8,0.18
    6,0.16
    6.2,0.17
    6.4,0.25
    6.6,0.27
    6.8,0.32
    7,0.4
    7.2,0.46
    7.4,0.43
    7.6,0.73
    7.8,1.38

