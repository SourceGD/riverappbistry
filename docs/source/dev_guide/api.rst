.. _api:

##################################
API
##################################

The api is a Flask application used to process the PIV analysis on a given setup and process the calculated river flow,
as well as the transects.
It is a RESTful API that can be used to upload data, process it and retrieve the results.



Endpoints documentation
-------------------------------------

The API is composed of the following endpoints:

Process PIV
################
[POST] http://exampleapiurl.com/process-piv

POST endpoint to process the PIV data
The endpoint expects a JSON object with the following structure as query parameters:

* **fps** - The frames per second of the video
* **start_frame** - The frame number to start the PIV analysis
* **end_frame** - The frame number to end the PIV analysis
* **freq** - The frequency of the PIV analysis
* **h_a** - The water level at the moment of the video
* **camera_config** - The camera configuration used to record the video
* **project_name** - The name of the project to process the PIV data

The endpoint also expects a file with the video to process.


example below:

.. code-block:: python

    params = {
        "fps": 1,
        "start_frame": 25,
        "end_frame": 30,
        "freq": self._video_configuration["frequency"],
        "h_a": self._bathymetry["water_level"],
        "camera_config": self._cam_config,
        "project_name": self._project_name
    }

    files = {
        "file": (video, open(video, "rb"), 'application/octet-stream'),
        "data": ('data', dumps(params), 'application/json')
    }
    headers = {
        "X-API-KEY": api_key,
    }

The endpoint expected responses are:

* 200 - The PIV data was processed successfully
* 400 - The request was malformed

Process Transects
########################
[GET] http://exampleapiurl.com/process-transects
GET endpoint to process the transects and retrieve the resulting image, as well as the calculated river flow

The endpoint expects the following query parameters:

* **video_name** - The path of the video file to process
* **project_name** - The name of the project to process the transects
* **video**: all data contained in the pyorc video object
* **bathymetry**: object containing the bathymetry data
* **local_points**: list of the two points that define the transect vector

example below:

.. code-block:: python

    params = {
        "video_name": video.fn,
        "project_name": self._project.project_name,
        "video": {
            "start_frame": int(video.start_frame),
            "end_frame": int(video.end_frame),
            "freq": int(video.freq),
            "h_a": video.h_a,
            "camera_config": json_camera_config
        },
        "bathymetry": self._project._bathymetry,
        "local_points": self._area_selection.get_points_coordinate()
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
    }

The endpoint expected responses are:

* 200 - The transects were processed successfully
* 400 - The request was malformed

API installation and configuration
-------------------------------------

To install the API, you need to follow the steps below:

1. Clone the repository on the machine/server that will host the API
2. Install docker and docker-compose on the machine (https://docs.docker.com/engine/install/) (https://docs.docker.com/compose/install/)
3. Create a .env file in the root of the repository with the following content:

.. code-block:: bash

    # You might want to change the API_KEY to a more secure one, it's up to you.
    API_KEY=qborm0w93U5UTKwomMp4MGjq0ivgY/QJIXkGVOWZUIA=

4. run the following command to build the docker image, container and start the container:

.. code-block:: bash

    docker-compose up --build -d

5. Once the container is running, you can access the API on the machine url on port 5000
6. Verify the API is running by accessing the docker container using the following command:

.. code-block:: bash

    docker exec -ti riverapp-web-1 bash
    lsof -i :5000
    # If something is running on port 5000, it should be the api.

7. IF the API is not running, run the api using the following command and launch a piv to test the api:

.. code-block:: bash

    python app.py

8. If the app runs correctly, you can access the API on the machine url on port 5000. To run the api in container background and be able to exit the container, run the following command:

.. code-block:: bash

    nohup python app.py &

9. Since Flask tends to produce a memory leak on heavy requests, the only solution found at the moment is to use a cron to restart the api every X hours (The owner chooses which suits the best). To do so, run the following command:

.. code-block:: bash

    crontab -e
    # Add the following line to the crontab file
    1 * * * * kill -9 `lsof -t -i:5000`;nohup python app.py &


Security
--------
The API is secured using an API key that is stored in the .env file. The API key is used to authenticate the requests to the API.
Currently, the API is not using any other security measures, but there is some ideas to implement in the future:

* Cypher the API key in the .env file
* Use a JWT token to authenticate the requests
* Use a more secure way to store the API key
* Secure server using a TLS certificate



