.. _video_configuration.rst:

###################################
Video Configuration
###################################

This screen contains the video configuration of the project, which means:

* The chose of the video file
* Start time: the second of the video from which you want to start the analysis. Be careful that if the second is after a minute, you still have to write it in seconds, for example: 1m30 = 90s.
* End time: the second of the video where you want to stop the analysis. The same rule applies as for the start time.
* Frequency: the number of frames per second you want to analyze. The number that gave the better results while testing the application is simply 1.
* The lens position: the position of the camera used to film the chosen video, this parameter begins to be sensitive when the difference with reality is more than 10cms. The [x, y, z] position starts from the bottom left beacon, which means that if the bottom left beacon is in front left of the camera, the x will be positive and the y negative. The z is the height of the camera from the ground. There is no default value since the parameter changes for every measuring setup. The parameter has to be entered as a string of 3 coordinates separated by ",", for example "7,-2,3".

.. figure:: ../_static/video_configuration.png
   :align: center

This screen uses a custom video player imported from src.front.components.widgets, this was made because the player was needed for the user to decide which part of the video to use.

When entering the screen, the ``_load_configuration`` function checks if the step has already be done, if so, it loads the existing configuration.
The fact that it has already be done does not stop the user to edit the configuration.
Once it is loaded, the ``_display_loaded_configuration`` function is called to display the configuration on the screen.

When the user clicks on the "Upload video" button, the ``open_file_manager`` function is called, which opens a file manager to select the video file.
When the file is selected, the ``_select_path`` function checks if the file correspond to accepted formats, if so, it saves the path in the configuration and displays the video player on the screen by calling ``load_video``.

The ``set_start_time``, ``set_end_time``, ``set_frequency`` and ``set_lens_position`` functions are called when the user changes the corresponding values, they check if the values are corresponding the right types and values and save the new values in the configuration.

Then, when the user presses the "Validate" button, the ``validate_video_configuration`` is called, which checks if all the values are correct and saves the configuration in the configuration file using ``_save_video_configuration``.

The user can also remove the video if if wants to change the current video

Finally, the ``go_back`` function is called when the user presses the "Back" button, it saves the configuration and goes back to the previous screen.

Once again, no functions from the backend are called in this screen, we will see later that these functions are almost exclusively there for the heavy processes.

To sum up the functions of this screen:

* **_select_path**: checks if the selected file is a video file and saves the path in the configuration
* **_load_configuration**: checks if the step has already be done and if so, loads the existing configuration
* **_display_loaded_configuration**: displays the loaded configuration on the screen
* **_save_video_configuration**: saves the configuration in the configuration file
* **go_back**: go back to previous screen without saving the configuration
* **open_file_manager**: opens a file manager to select the video file
* **load_video**: loads the video player on the screen
* **exit_file_manager**: closes the file manager
* **remove_video**: removes the video from the screen and the configuration
* **set_start_time**: saves the new start time in the configuration
* **set_end_time**: saves the new end time in the configuration
* **set_frequency**: saves the new frequency in the configuration
* **set_lens_position**: saves the new lens position in the configuration
* **validate_video_configuration**: checks if all the values are correct and saves the configuration in the configuration file
