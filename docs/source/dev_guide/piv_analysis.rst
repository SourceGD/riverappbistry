.. _piv_analysis:

##############################################
PIV (Particle Image Velocimetry) Analysis
##############################################
This screen appears when the PIV analysis is processing.

There is nothing much too display as screen example here since the PIV launches when switching from the filters screen.
When entering the screen, the application will check if the piv has been already computer by checking if the "need_update" field is set to True.

.. note::
    This need_update field need to be removed, it is possible to check if the PIV has already be done by checking the steps_done objet in the json configuration file of the project, as it has been done for the rest of the steps.

If an update is needed, the application will start a thread and launch the ``_piv_calculation`` function.
This function call the ``generate_piv`` function from the back/save_project_data.py file. (This is another misconception, this function has nothing to do in this file)

This generate piv function is one of the most important function of the application.
First, it verifies that all previous steps have been done.
If you are using the api version the following steps happen (You obviously need a running version of the API to do so):
It checks if internet is available, if so, it will use the API to process the PIV analysis.
If so, it prepares all the data needed and sends it to the ``/process-piv`` route. An API key is needed from the .env file to access this route. The IP of the API host machine is also needed, these are set in a .env file in the root of the application.
The content of the env file is presented as follows:

.. code-block:: env

    API_URL=http://93.127.202.193:5000
    API_KEY=qborm0w93U5UTKwomMp4MGjq0ivgY/QJIXkGVOWZUIA=

The API will then process the PIV analysis and return a 200 response code if the PIV processed well.
If the API is not available, the application will process the PIV analysis locally. (The piv.nc file will thus be stored locally in the project folder)

If you are not using the API version, the application will directly process the PIV analysis locally.


The cancel_piv function does not work yet, this is a problem with the way Kivy handles threads.

Here is a summary of the functions used in this screen:

From the front-end:

* ``_piv_calculation``: Launches the PIV calculation in a thread.
* ``cancel_piv``: Cancels the PIV calculation. (not working)
* ``on_enter``: Checks if the PIV has already been done and if not, launches the PIV calculation.

From the back-end:

* ``generate_piv``: Prepares the data and sends it to the API or processes it locally.