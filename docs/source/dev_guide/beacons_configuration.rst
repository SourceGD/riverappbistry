.. _beacons_configuration:

#############################################
Beacons Configuration
#############################################

The beacons configuration file allows the user to chose the research are in which the PIV analysis will be processed.
The user has to move the beacons to define the area in the following order:

* P4 in top-left
* P3 in top-right
* P2 in bottom-right
* P1 in bottom-left

If this order is not respected, the application will not be able to process the PIV analysis.

The user also has to enter each distance between the beacons in the corresponding text box.
The more precise these parameters are, the more accurate the PIV analysis will be.

When entering, the app will check if the beacons configurations already occurred on the current project, and if so it will load the registered beacons positions, as well as the encoded distances.
The area selection is made using a custom widget "ShapeOnImage", available in front/components/widget/ and allow the user to move draggable points. Thus the widget draws the lines between the points.

This widget is the only specific part of this screen, the rest being basic fields to enter the distances.
When validating the entries, the application will check if all entries are of the valid format (positive float) and if the beacons are in the correct order.

.. figure:: ../_static/beacons_configuration.png
   :align: center
   :alt: Beacons Configuration

Since there is nothing new about this screen, we will not detail the code here. You can refer to the first configuration files to understand the form handling.
