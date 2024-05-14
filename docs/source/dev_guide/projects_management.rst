.. _projects_management:

########################################
Projects Management
########################################

Before beginning, here is how the application generally works:
Each project is a directory containing a ``project.json`` file, which contains
the project's metadata. The project's files are stored in the ``projects`` directory.

The front part is managed by the Kivy screen manager, which allows the developer to make switches between screens when needed.

Here is an example of a project configuration file (some fields have been reduced for readability purposes):

.. code-block:: json

    {
    "project_name": "sample_tests",
    "steps_done": {
        "video_configuration": true,
        "bathymetry": true,
        "beacons": true,
        "cam_config": true,
        "filter_video": true,
        "piv": true,
        "post_process": true
    },
    "video_configuration": {
        "video": "/home/andreas/examples/limelette-milieu-copaux-23-04-2024.mp4",
        "start_time": 39.0,
        "end_time": 44.0,
        "frequency": 1,
        "lens_position": [
            3.65,
            -6.2438,
            3.7349
        ]
    },
    "bathymetry": {
        "x": [
            0.0,
            0.2,
            0.4,
            0.6,
            0.8,
            1.0,
            1.2,
            1.4,
            1.6,
            1.8,
            2.0
        ],
        "y": [
            1.66,
            0.61,
            0.57,
            0.53,
            0.51,
            0.48,
            0.47,
            0.43,
            0.37,
            0.33,
            0.29
        ],
        "water_level": 0.83,
        "surface_coefficient": 0.85
    },
    "beacons": {
        "points": [
            [
                1367,
                364
            ],
            [
                1663,
                784
            ],
            [
                450,
                660
            ],
            [
                774,
                338
            ]
        ],
        "p1_to_p2": 6.646,
        "p2_to_p3": 7.975,
        "p3_to_p4": 7.25,
        "p4_to_p1": 7.49,
        "p1_to_p3": 9.55,
        "p2_to_p4": 11.155
    },
    "cam_config": {
        "height": 1080,
        "width": 1920,
        "resolution": 0.01,
        "lens_position": [
            3.65,
            -6.2438,
            3.7349
        ],
        "gcps": {
            "src": [
                [
                    1367,
                    364
                ],
                [
                    1663,
                    784
                ],
                [
                    450,
                    660
                ],
                [
                    774,
                    338
                ]
            ],
            "dst": [
                [
                    7.392572977941942,
                    6.045855172413794
                ],
                [
                    7.954574845481449,
                    -0.5704068965517247
                ],
                [
                    0,
                    0
                ],
                [
                    0,
                    7.25
                ]
            ],
            "h_ref": 0.0,
            "z_0": 0.83
        },
        "window_size": 25,
        "dist_coeffs": [
            [
                0.0
            ],
            [
                0.0
            ],
            [
                0.0
            ],
            [
                0.0
            ]
        ],
        "camera_matrix": [
            [
                1920.0,
                0.0,
                960.0
            ],
            [
                0.0,
                1920.0,
                540.0
            ],
            [
                0.0,
                0.0,
                1.0
            ]
        ],
        "bbox": "POLYGON ((7.626857841131374 7.562373199765359, 7.956502771006525 -0.5709492591199159, 0.0330080414045315 -0.8920898357673299, -0.296636888470621 7.241232623117945, 7.626857841131374 7.562373199765359))"
    },
    "filter_video": {},
    "piv": {
        "file": "piv.nc",
        "need_update": false
    },
    "post_process": {
        "river_flow": 2.87,
        "transect_picture_path": "/media/andreas/LaCie Andreas/Memoire/riverapp/projects/sample_tests/plot_transect.jpg",
        "local_points": [
            [
                585,
                600
            ],
            [
                1436,
                600
            ]
        ]
    }
    }

Each screen has its own object in the project configuration file.
The ``steps_done`` allows the application to know where the user stopped the last time he worked on the project.

For each screen we will develop what means each field of the current screen section.

How does the projects management screen works
----------------------------------------------

When entering the screen, the application will look for all sub-directories in the projects directory (function ``_load_project_list``).
From this moment, the user can select a project to work on.
The application will use the project class function ``load_project`` to load the project configuration file.
If the configuration file is not found or corrupted, the application will return an error the the user.

The user can also create a new project by clicking the plus sign button, which will call ``open_new_project_dialogs`` and open a modal,
then the user can enter a project name and click on the create button. This will check if the project name is not already taken and create a new project directory with a ``project.json`` file containing the project metadata.

If the user decides to delete a project, he can click on the trash icon button, which will call the function ``_del_project``..

This screen does not call "back-end" functions, only for the download features (which does not work).

When the user has clicked on a project that loaded successfully, the application will switch the screen manager to the project_details screen.

To sum up the different functions used in this screen:

From the front-end:

* **open_del_project_dialogs**: opens the new project modal
* **_check_and_create_new_project**: checks if the project name is not already taken and creates a new project
* **_del_project**: deletes the project
* **_load_project_list**: loads the project list
* **set_list_projects**: set the view of the project list on the application screen
* **select_project**: selects the project and switches the screen manager to the project_details screen if the project is loaded successfully
* **open_download_file_manager**: opens the download file modal to let the user choose where to download the file
* **select_download_destination**: used in open_download_file_manager to select the download destination
* **exit_download_file_manager**: same thing

From the back-end:

* **download_project**: function from project_data_management to download the project, but not working.