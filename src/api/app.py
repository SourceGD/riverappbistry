"""
API-protected PIV and Transect Processing Flask Application

This Flask application provides two API endpoints for processing PIV (Particle Image
Velocimetry) data and calculating river transects. Both endpoints require a valid API key
for authentication.

Dependencies
------------

- Flask: Web framework for building the API.
- Werkzeug: Utility functions for Flask (including `secure_filename`).
- dotenv: Load environment variables from a `.env` file (for API key).
- base64: Encoding/decoding binary data to base64 strings (for image data).
- json: Encoding/decoding JSON data (for request/response handling).
- functools: Provides the `@wraps` decorator for preserving function metadata.
- time: Measures execution time for performance monitoring.
- logging: Records informational messages during processing.
- os: Operating system dependent functionalities (potentially used).
- gc: Garbage collection module for memory management.

Global Variables
----------------

- `UPLOAD_FOLDER`: Configures the upload folder path for video files.
- `OUTPUT_FOLDER`: Configures the output folder path for processing results.
- `required_api_key`: Stores the API key value loaded from the environment variable.

Endpoints
---------

1. **process_piv (POST /process-piv):**
    - Processes an uploaded video file for PIV analysis.
    - Expects a multipart form data request with a file part named 'file' containing the video
      and a JSON part named 'data' containing processing parameters.
    - Returns a JSON response with a success message, processing time, or an error message
      depending on the outcome.

2. **process_transects (GET /process-transects):**
    - Processes river transect data from a previously analyzed PIV result.
    - Expects a JSON request containing project name, video information (start/end frames,
      camera configuration), bathymetry data, and local points data.
    - Returns a JSON response with a success message, processing time, calculated river flow
      data (as a list), and a base64 encoded string of the generated transect plot image.

Module Functions
----------------

- `api_key_required(api_key)` (decorator):
    - Verifies the presence and validity of an API key in the request header.

Notes
-----

- This application assumes the existence of helper functions `mask_and_plot` and `transect`
  for specific processing steps (functionalities not detailed here).
- File path sanitization is performed on video paths received from the request data to avoid
  potential security issues.
- Garbage collection is triggered after processing to manage memory usage.
"""

import base64
import json
from functools import wraps
import time
import logging
import os
import gc

from dotenv import load_dotenv
from flask import Flask, request, send_file, jsonify, abort

from werkzeug.utils import secure_filename

import xarray as xr

from libs.pyorc import Video
from src.back.transect import transect
from src.back.mask import mask_and_plot


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

OUTPUT_FOLDER = 'outputs'
load_dotenv()
required_api_key = os.getenv("API_KEY")


# TODO cypher api-key
def api_key_required(api_key):
    """
    API Key Authentication Decorator

    This function is a decorator that verifies the presence and validity of an API key
    in the request header before allowing execution of the decorated function.

    Parameters
    ----------

    - `api_key` (str): The expected API key value for authentication.

    Returns
    -------

    - `function`: A decorator function that can be used to wrap other functions
      and enforce API key authentication.

    Raises
    ------

    - `KeyError`: If the 'X-API-KEY' header is not present in the request.
    - `HTTPException` (specifically `abort(401)`): If the provided API key in the
      'X-API-KEY' header does not match the expected `api_key` value.

    Notes
    -----

    - This decorator relies on the `request` object, likely provided by a web framework,
      to access the request headers.
    - The decorator uses the `@wraps` decorator from the `functools` module to preserve
      the decorated function's metadata (name, docstring, etc.).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.headers.get('X-API-KEY') and request.headers.get('X-API-KEY') == api_key:
                return f(*args, **kwargs)
            abort(401)

        return decorated_function

    return decorator


@app.route('/process-piv', methods=['POST'])
@api_key_required(required_api_key)
def process_piv():
    """
    API-protected PIV processing function

    This function processes a PIV (Particle Image Velocimetry) task on an uploaded video file.
    It requires a valid API key for access and performs the following steps:

    1. **File Upload Validation:**
        - Checks for the presence of a file part named 'file' in the request.
        - Verifies that a filename is provided and not empty.

    2. **File Storage and Data Extraction:**
        - Saves the uploaded file securely using `secure_filename`.
        - Extracts JSON data containing processing parameters from the request part named 'data'.
        - Creates a `Video` object (from the `pyorc` library) using the uploaded filename,
          start/end frames, frequency, height of the analysis area, and camera configuration
          provided in the JSON data.

    3. **PIV Processing:**
        - Records the start time for performance measurement.
        - Retrieves video frames using the `pyorc` library.
        - Applies normalization and projection steps to the retrieved frames
        - Performs PIV calculation on the processed frames and saves the results as a NetCDF file
          using the project name and 'piv.nc' as the filename.
        - Records the processing completion time.
        - Performs garbage collection for memory management.

    4. **Response:**
        - Returns a success message with the processing time in seconds and a 200 status code
          if processing is successful.
        - Returns an error message and a 400 status code if there are any issues with file
          upload or processing.

    Parameters
    ----------

    - None (function is decorated with `api_key_required` for API key authentication).

    Returns
    -------

    - `tuple` (str, int): A tuple containing a message string and an HTTP status code
      (200 for success, 400 for errors).

    Raises
    ------

    - Exceptions potentially raised by underlying libraries like `pyorc` or during file
      operations (not explicitly listed here).

    Notes
    -----

    - This function relies on the following libraries and configurations:
        - `request`: Web framework object for accessing request data (file uploads, JSON data).
        - `secure_filename`: Function to sanitize filenames for secure storage.
        - `app.config['UPLOAD_FOLDER']`: Application configuration for the upload folder path.
        - `OUTPUT_FOLDER`: Global variable defining the output folder path.
        - `pyorc`: Library for PIV processing (specific functionalities not detailed here).
        - `logging`: Library for logging informational messages.
        - `gc`: Garbage collection module for memory management.

    """
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace("_", "")))
        data = json.loads(request.files['data'].read())
        pyorc_video: Video = Video(
            # concat upload_folder+filename
            os.path.join(app.config['UPLOAD_FOLDER'], filename.replace("_", "")),
            start_frame=data["start_frame"],
            end_frame=data["end_frame"],
            freq=data["freq"],
            h_a=data["h_a"],
            camera_config=data["camera_config"]
        )
        # get start time
        start_time = time.time()
        da = pyorc_video.get_frames()
        # Apply previous steps filter here
        da_norm = da.frames.normalize()
        da_norm_proj = da_norm.frames.project()
        logging.info("Starting PIV")
        da_norm_proj.frames.get_piv().to_netcdf(
            os.path.join(OUTPUT_FOLDER, data["project_name"] + "_" + 'piv.nc'))
        end_time = time.time()
        logging.info("PIV done")
        gc.collect()
        return f'File processed successfully, piv lasted {end_time-start_time} seconds', 200

    return 'No file part', 400


@app.route('/process-transects', methods=['GET'])
@api_key_required(required_api_key)
def process_transects():
    """
    API-protected Transect Processing Function

    This function processes river transect data from a previously analyzed PIV (Particle Image
    Velocimetry) result. It requires a valid API key for access and performs the following:

    1. **Data retrieval:**
        - Extracts the request data as JSON format from the request object.
        - Sanitizes the video path provided in the request data to avoid format issues following
          different OS.
        - Creates a `Video` object (from the `pyorc` library) using the sanitized video path,
          start/end frames, and camera configuration retrieved from the request data.

    2. **Transect Processing:**
        - Records the start time for performance measurement.
        - Constructs the formatted output folder path based on the project name provided in the
          request data.
        - Opens the NetCDF file containing PIV results.
        - Calls the `mask_and_plot` function (functionality not detailed here) to perform
          masking and plotting operations on the PIV data, saving results in the output folder.
        - Opens the masked NetCDF file from the output folder.
        - Calls the `transect` function (functionality not detailed here) to calculate river flow
          using the masked dataset, `Video` object, output folder, bathymetry data, and local points
          provided in the request data.
        - Closes the masked dataset.
        - Records the processing completion time.
        - Converts the calculated river flow values to a list.

    3. **Response Generation:**
        - Sends the generated transect plot image ('plot_transect.jpg') located in the output folder
          as a response with the 'image/jpeg' mimetype.
        - Reads the transect plot image in binary format and converts it to a base64 encoded string
          for inclusion in the JSON response.
        - Prepares a dictionary containing a success message with processing time, the calculated
          river flow data as a list, and the base64 encoded image string.
        - Performs garbage collection for memory management.
        - Returns a JSON response containing the prepared dictionary.

    Parameters
    ----------

    - None (function is decorated with `api_key_required` for API key authentication).

    Returns
    -------

    - `JSON`: A JSON object containing a success message, river flow data as a list, and a
      base64 encoded string of the generated transect plot image.

    Raises
    ------

    - Exceptions potentially raised by underlying libraries like `pyorc` or during file operations
      (not explicitly listed here).

    Notes
    -----

    - This function relies on the following libraries and configurations:
        - `request`: Web framework object for accessing request data (JSON data).
        - `os` (potentially): Operating system dependent functionalities (commented out).
        - `UPLOAD_FOLDER`: Global variable defining the upload folder path.
        - `OUTPUT_FOLDER`: Global variable defining the output folder path.
        - `pyorc`: Library for PIV processing (specific functionalities not detailed here).
        - `xr`: Library for working with NetCDF files.
        - `mask_and_plot`: Function for masking and plotting PIV data (not detailed here).
        - `transect`: Function for calculating river flow using masked data (not detailed here).
        - `base64`: Library for base64 encoding (image to string conversion).
        - `gc`: Garbage collection module for memory management.
    """

    request_data = request.get_json()
    video_path = (request_data["video_name"].replace("/", "")
                  .replace("\\", "").replace("_", "").replace(":", "").lstrip("_"))
    pyorc_video: Video = Video(
        os.path.join(UPLOAD_FOLDER, video_path),
        start_frame=request_data["video"]["start_frame"],
        end_frame=request_data["video"]["end_frame"],
        camera_config=request_data["video"]["camera_config"]
    )
    start_time = time.time()
    formatted_output_folder = OUTPUT_FOLDER + "/" + request_data["project_name"] + "_"
    dataset = xr.open_dataset(OUTPUT_FOLDER + "/"
                              + request_data["project_name"]
                              + "_" + 'piv.nc')
    mask_and_plot(formatted_output_folder, dataset, pyorc_video)
    masked_dataset = xr.open_dataset(OUTPUT_FOLDER + "/"
                                     + request_data["project_name"]
                                     + "_" + "piv_masked.nc")
    river_flow = transect(masked_dataset,
                          pyorc_video,
                          formatted_output_folder,
                          request_data["bathymetry"],
                          request_data["local_points"])
    # os.remove(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_piv_masked.nc")
    # does not have the right on every computer,
    # TODO: find a way to bypass admin permissions (windows)
    masked_dataset.close()
    end_time = time.time()
    river_flow = river_flow.values.tolist()
    send_file(formatted_output_folder + 'plot_transect.jpg', mimetype='image/jpeg')
    # converting image to base64 to send it with other responses
    with (open(formatted_output_folder + 'plot_transect.jpg', "rb")
          as image_file):
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    data = {
        "Message": f"Transect processed successfully in {end_time - start_time} seconds",
        "river_flow": river_flow,
        "image": encoded_string
    }
    gc.collect()
    return jsonify(data)


if __name__ == '__main__':
    from waitress import serve

    serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=True)
