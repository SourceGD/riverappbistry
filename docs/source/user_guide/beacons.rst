.. _beacons:

##########################################
Beacons configuration
##########################################

This screen allows you to configure the beacons that will define the area of research for the PIV analysis,
which will calculate the velocity field of the river. The beacons should be placed on the GCP (Ground Control Points)
beacons that should have been placed during the measurements.

If the GCP are visible enough for the camera, the beacons should be already placed in the correct order, right on the GCPs.
If not please move the points as needed.

To allow the PIV to process as it should, you have to put the beacons in the following order:

* P4 in top left
* P3 in top right
* P2 in bottom right
* P1 in bottom left

Then you have to fill the text fields with every distances between the beacons. The distances should be in meters.
If you have GPS positions of the beacons, this is way better because the distances will be more accurate,
but if you did measure the distances by hand it should also work properly.

Once you are done with the beacons, you can validate them by clicking on the "Validate" button.

.. figure:: ../_static/beacons_configuration.png
    :align: center
    :alt: Beacons configuration

    Beacons configuration screen