from os import path, mkdir, getenv
from json import load, dumps, loads
from shutil import rmtree
import math
import requests
from requests.adapters import HTTPAdapter, Retry

from cv2 import VideoCapture, CAP_PROP_FPS
from dotenv import load_dotenv
from definitions import PROJECT_DEFAULT_STRUCT, PROJECTS_DIR

from src.utils import get_video_frame, utils
from libs.pyorc import CameraConfig, Video


class ProjectNotLoaded(Exception):
    pass


class SavingProjectData:
    def __init__(self) -> None:
        self._post_process: dict = None
        self._backup_file: str = None
        self._project_name: str = None
        self._steps_done: dict = None
        self._video_configuration: dict = None
        self._bathymetry: dict = None
        self._beacons: dict = None
        self._cam_config: dict = None
        self._filter_video: dict = None
        self._piv: dict = None

    @property
    def project_name(self) -> str:
        return self._project_name

    @property
    def steps_done(self) -> dict:
        return self._steps_done

    @property
    def video_configuration(self) -> dict:
        return self._video_configuration

    @video_configuration.setter
    def video_configuration(self, video_configuration: dict) -> None:
        if self._backup_file is None:
            raise ValueError("The project need to be loaded before adding data")

        if self._video_configuration == video_configuration:
            return

        if not isinstance(video_configuration, dict):
            raise TypeError(f"video_configuration should be a dict : {video_configuration}")

        self._check_missing_data(["video", "start_time", "end_time", "frequency"],
                                 video_configuration)

        if not path.exists(video_configuration["video"]):
            raise FileNotFoundError(f"The video was not found : {video_configuration['video']}")

        if not isinstance(video_configuration["start_time"], (int, float)):
            raise TypeError("start_time should be an int or a float")

        if not isinstance(video_configuration["end_time"], (int, float)):
            raise TypeError("end_time should be an int or a float")

        if not isinstance(video_configuration["frequency"], (int, float)):
            raise TypeError("frequency should be an int or a float")

        if video_configuration["start_time"] < 0:
            raise ValueError("start_time cannot be less than 0")

        if video_configuration["end_time"] < 0:
            raise ValueError("end_time cannot be less than 0")

        if video_configuration["frequency"] <= 0:
            raise ValueError("start_time cannot be less than or equal to 0")

        if video_configuration["start_time"] >= video_configuration["end_time"]:
            raise ValueError("start_time cannot be greater than end_time")

        self._video_configuration = video_configuration
        self._save_step("video_configuration", video_configuration)
        self.generate_cam_config()

        return

    @property
    def bathymetry(self) -> dict:
        return self._bathymetry

    @bathymetry.setter
    def bathymetry(self, bathymetry: dict) -> None:
        if self._backup_file is None:
            raise ValueError("The project need to be loaded before adding data")

        if self._bathymetry == bathymetry:
            return

        if not isinstance(bathymetry, dict):
            raise TypeError(f"bathymetry should be a dict : {bathymetry}")

        self._check_missing_data(["x", "y", "water_level"], bathymetry)

        if len(bathymetry["x"]) != len(bathymetry["y"]):
            raise ValueError("There are not as many x-coordinates as y-coordinates")

        for i in range(len(bathymetry["x"])):
            if (not isinstance(bathymetry["x"][i], (int, float))
                    or not isinstance(bathymetry["y"][i], (int, float))):
                raise ValueError("All coordinates must be numbers")

        if not isinstance(bathymetry["water_level"], (float, int)):
            raise TypeError("Mean water Level should be a number")

        if bathymetry["water_level"] <= 0:
            raise ValueError("Water Level cannot be less than or equal to 0")

        self._bathymetry = bathymetry
        self._save_step("bathymetry", bathymetry)
        self.generate_cam_config()

        return

    @property
    def beacons(self) -> dict:
        return self._beacons

    @beacons.setter
    def beacons(self, beacons: dict) -> None:
        if self._backup_file is None:
            raise ValueError("The project need to be loaded before adding data")

        if self._beacons == beacons:
            return

        if not isinstance(beacons, dict):
            raise TypeError(f"beacons should be a dict : {beacons}")

        self._check_missing_data(
            [
                "points",
                "p1_to_p2",
                "p2_to_p3",
                "p3_to_p4",
                "p4_to_p1",
                "p1_to_p3",
                "p2_to_p4"],
            beacons)

        if len(beacons["points"]) != 4:
            raise ValueError("Points should have 4 pairs of coordinates ")

        for coordinates in beacons["points"]:
            if len(coordinates) != 2:
                raise ValueError("A point lacks the x-coordinate or y-coordinates or both")

            if not isinstance(coordinates[0], (int, float)) or not isinstance(coordinates[1],
                                                                              (int, float)):
                raise ValueError("Point coordinates should be numbers")

        if beacons["p1_to_p2"] <= 0 or beacons["p2_to_p3"] <= 0 or beacons["p3_to_p4"] <= 0 or \
                beacons["p4_to_p1"] <= 0 or beacons["p1_to_p3"] <= 0 or beacons["p2_to_p4"] <= 0:
            raise ValueError("Distance between points cannot be lass than or equal to 0")

        self._beacons = beacons
        self._save_step("beacons", beacons)
        self.generate_cam_config()

    @property
    def cam_config(self) -> dict:
        return self._cam_config

    @property
    def filter_video(self) -> dict:
        return self._filter_video

    @filter_video.setter
    def filter_video(self, filters: dict):
        self._save_step("filter_video", {})

    @property
    def piv(self) -> dict:
        if self._piv is None:
            return None

        data = self._piv
        data["file"] = path.abspath(path.join(PROJECTS_DIR, self._project_name, self._piv["file"]))
        return data

    def _save_step(self, step: str, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError("data should be a dict")

        with open(self._backup_file, "r") as json_file:
            saved_data = load(json_file)

        saved_data[step] = data
        saved_data["steps_done"][step] = True
        self._steps_done[step] = True

        with open(self._backup_file, "w") as json_file:
            json_file.write(dumps(saved_data, indent=4))


    def _check_backup_file_format(self, wanted_dict_format: dict, dict_format: dict) -> bool:
        if not isinstance(wanted_dict_format, dict):
            raise TypeError(f"wanted_dict_format should be a dict : {wanted_dict_format}")

        if not isinstance(dict_format, dict):
            raise TypeError(f"dict_format should be a dict : {dict_format}")

        keys_format = set(wanted_dict_format.keys())
        keys_data = set(dict_format.keys())
        if keys_format != keys_data:
            print("ValueError, The data format doesn't respect the wanted format")
            raise ValueError("The data format doesn't respect the wanted format 3")

        for key in keys_format:
            if key == "cam_config":
                continue

            if isinstance(wanted_dict_format[key], dict) and isinstance(dict_format[key], dict):
                self._check_backup_file_format(wanted_dict_format[key], dict_format[key])

            elif ((isinstance(wanted_dict_format[key], dict) and not isinstance(dict_format[key],
                                                                                dict))
                  or not isinstance(wanted_dict_format[key], dict) and isinstance(dict_format[key],
                                                                                  dict)):
                raise ValueError("The data format doesn't respect the wanted format 4")

        return True

    def _check_missing_data(self, wanted_data: list, data: dict) -> bool:

        if not isinstance(wanted_data, list):
            raise TypeError(f"wanted_data should be a list : {wanted_data}")

        if not isinstance(data, dict):
            raise TypeError(f"bathymetry should be a dict : {data}")

        missing_data = [key for key in wanted_data if key not in data.keys()]
        if missing_data:
            raise ValueError(f"Missing data : {missing_data}")

        return True

    def _convert_dist_to_dest_points(self, dist: list) -> list:
        if not isinstance(dist, list):
            raise TypeError(f"dist should be a list : {dist}")
        # Points coordinates computation
        # We consider first that P1 and P4 are vertically aligned and P4 as the  origin
        p1, p4 = [0, dist[3]], [0, 0]

        # Then we compute other coordinates using cosine law
        alpha = math.acos((dist[3] ** 2 + dist[5] ** 2 - dist[0] ** 2) / (2 * dist[3] * dist[5]))
        p2 = [dist[5] * math.sin(alpha), dist[5] * math.cos(alpha)]
        beta = math.acos((dist[3] ** 2 + dist[2] ** 2 - dist[4] ** 2) / (2 * dist[3] * dist[2]))
        p3 = [dist[2] * math.sin(beta), dist[2] * math.cos(beta)]
        return [[p2[0], p2[1]], [p3[0], p3[1]], [p4[0], p4[1]], [p1[0], p1[1]]]

    def generate_cam_config(self) -> bool:
        if (not self._steps_done["video_configuration"]
                or not self._steps_done["bathymetry"]
                or not self._steps_done["beacons"]):
            return False

        init_frame = get_video_frame(self.video_configuration["video"],
                                     self.video_configuration["start_time"])

        height, width = init_frame.shape[0:2]
        dst: list = self._convert_dist_to_dest_points([
            self._beacons["p4_to_p1"],
            self._beacons["p1_to_p2"],
            self._beacons["p2_to_p3"],
            self._beacons["p3_to_p4"],
            self._beacons["p2_to_p4"],
            self._beacons["p1_to_p3"]
        ])

        gcps: dict = {
            "src": self._beacons["points"],
            "dst": dst,
            "z_0": self._bathymetry["water_level"]
        }

        cam_config: CameraConfig = CameraConfig(
            height=height,
            width=width,
            gcps=gcps,
            lens_position=self._video_configuration["lens_position"]
            # lens_position=[1.25, 1.5, 3], # Position for PB from 45 degrees
            # lens_position=[1.25, 0.75, 3] # Position for PB from above at 90 degrees
            # lens_position=[7, -2, 3] # Position for VGC
            # the lens_position does not seem to be used for the process but has to be indicated
            # to avoid error/warnings
        )

        cam_config.set_bbox_from_corners(self._beacons["points"])
        self._save_step("cam_config", loads(cam_config.to_json()))
        self._cam_config = cam_config
        return True

    def generate_piv(self) -> bool:
        """
        Generates PIV data for a RiverApp project (potentially using an API)

        This function attempts to generate PIV (Particle Image Velocimetry) data
        for a RiverApp project. It performs the following checks before proceeding:

        - **Completion Check:** Ensures all prerequisite steps (`video_configuration`,
          `bathymetry`, `beacons`, `cam_config`, and `filter_video`) have been
          completed in the project workflow (`_steps_done` dictionary).

        If all checks pass, the function extracts video configuration data
        (including FPS, start and end frame) and performs PIV analysis using one
        of two methods:

          - **API Method (if internet available):**
            - Leverages an external API service (requires internet connection).
            - Uploads the project video file and configuration data (including FPS,
              start/end frames, frequency, water level, camera configuration, and
              project name) to the API.
            - The API service processes the PIV analysis on the video.
          - **Local Processing Method (if no internet):**
            - Uses the PyOrc library to process the video locally.
            - Performs normalization, projection, and PIV analysis on the video frames.
            - Saves the PIV data to a NetCDF file (`piv.nc`) within the project directory.

        Parameters
        ----------

        - None (function utilizes project data loaded from configuration file).

        Returns
        -------

        - `bool`: True if the PIV data is generated successfully, False otherwise

        Raises
        ------

        - `ValueError`: If the API key used for the external service is not correct
          (applicable only if the API method is used).

        Notes
        -----

        - This function utilizes the `requests` library for API communication (if applicable).
        - The function uses exponential backoff retry logic with a timeout for the API call.
        - This function utilizes the PyOrc library for local PIV processing (if no internet).
        - The function saves the PIV data (`"piv.nc"` file) and updates the project
          data structure (`_steps_done` and potentially others) to reflect completion
          of the PIV step.

        """
        if not self._steps_done["video_configuration"] or not self._steps_done["bathymetry"] \
                or not self._steps_done["beacons"] or not self._steps_done["cam_config"] \
                or not self._steps_done["filter_video"]:
            return False

        video: str = self._video_configuration["video"]
        fps: int = VideoCapture(video).get(CAP_PROP_FPS)
        start_frame: int = int(self._video_configuration["start_time"] * fps)
        end_frame: int = int(self._video_configuration["end_time"] * fps)

        if utils.check_internet():
            self._cam_config = loads(self._cam_config.to_json()) \
                if isinstance(self._cam_config, CameraConfig) \
                else self._cam_config
            params = {
                "fps": fps,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "freq": self._video_configuration["frequency"],
                "h_a": self._bathymetry["water_level"],
                "camera_config": self._cam_config,
                "project_name": self._project_name
            }
            load_dotenv()
            api_key = getenv("API_KEY")
            route_url = getenv("API_URL") + "/process-piv"
            files = {
                "file": (video, open(video, "rb"), 'application/octet-stream'),
                "data": ('data', dumps(params), 'application/json')
            }
            headers = {
                "X-API-KEY": api_key,
            }
            # TODO add exceptions
            s = requests.Session()
            retries = Retry(total=100, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
            s.mount('http://', HTTPAdapter(max_retries=retries))
            s.mount('https://', HTTPAdapter(max_retries=retries))
            response = s.post(route_url, files=files, headers=headers, timeout=(500, 500))
            if response.status_code == 401:
                raise ValueError("The API key is not correct")
            print("PROCESS PIV DURATION: ", response.text)
            s.close()
        else:
            pyorc_video: Video = Video(
                video,
                start_frame=start_frame,
                end_frame=end_frame,
                freq=self._video_configuration["frequency"],
                h_a=self._bathymetry["water_level"],
                camera_config=self._cam_config
            )

            da = pyorc_video.get_frames()
            # Apply previous steps filter here
            da_norm = da.frames.normalize()
            da_norm_proj = da_norm.frames.project()
            da_norm_proj.frames.get_piv().to_netcdf(
                path.join(PROJECTS_DIR, self._project_name, "piv.nc"))

        self._save_step("piv", {
            "file": "piv.nc",
            "need_update": False
        })

        return True

    def save_post_process(self, river_flow: float, transect_picture_path: str,
                          local_points: list) -> bool:
        """
        Saves post-processing results for a RiverApp project

        This function attempts to save the results of the post-processing step
        for a RiverApp project. It performs the following checks before saving:

        - **PIV Completion Check:** Ensures the PIV analysis step (`"piv"` key in
          `_steps_done`) has been completed before saving post-processing data.
          This is because post-processing typically relies on results from PIV analysis.
        - **Data Type Verification:** Ensures `river_flow` is a float,
          `transect_picture_path` is a string, and `local_points` is a list.

        If all checks pass, the function calls the internal `_save_step` function
        to save the provided post-processing data (`river_flow`, `transect_picture_path`,
        and `local_points`) under the `"post_process"` key in the project data
        structure. The saved data is likely stored in the project configuration
        file.

        Parameters
        ----------

        - `river_flow` (`float`): The calculated river flow rate.
        - `transect_picture_path` (`str`): Path to the image file representing the
          analyzed transect.
        - `local_points` (`list`): A list of local points extracted during
          post-processing (data format may vary).

        Returns
        -------

        - `bool`: True if the post-processing data is saved successfully, False
          otherwise (specifically if the PIV step was not completed).

        Raises
        ------

        - `TypeError`:
            - If `river_flow` is not a float.
            - If `transect_picture_path` is not a string.
            - If `local_points` is not a list.

        Notes
        -----

        - This function relies on the internal `_save_step` function to handle
          saving the data to the project configuration file.
        """
        if not self._steps_done["piv"]:
            return False

        if not isinstance(river_flow, float):
            raise TypeError(f"river_flow should be a number : {river_flow}")
        if not isinstance(transect_picture_path, str):
            raise TypeError(f"transect_picture_path should be a str : {transect_picture_path}")
        if not isinstance(local_points, list):
            raise TypeError(f"local_points should be a list : {local_points}")
        self._save_step("post_process", {
            "river_flow": river_flow,
            "transect_picture_path": transect_picture_path,
            "local_points": local_points
        })
        return True

    def load_project(self, project_dir: str) -> None:
        """
        Loads a RiverApp project from a project directory

        This function loads the configuration data for a RiverApp project from a
        specified project directory. It performs the following checks before loading
        the data:

        - **Data Type Verification:** Ensures `project_dir` is a string type.
        - **Directory Existence:** Verifies if the provided `project_dir` exists
          and is a directory.
        - **Project Configuration File:** Checks if the expected project configuration
          file (`project_name.json`) exists within `project_dir`.

        If all checks pass, the function opens the project configuration file and
        reads the project data as a JSON dictionary. The function then performs a
        format check using an internal function (`_check_backup_file_format`) to
        ensure the data structure matches the expected format (defined in
        `PROJECT_DEFAULT_STRUCT`).

        If the data format is valid, the function populates various class attributes
        with the loaded project data:

        - `_backup_file`: Path to the project configuration file.
        - `_project_name`: Name of the project (extracted from the directory name).
        - `_steps_done`: Steps completed in the project workflow (from loaded data).
        - `_video_configuration`: Video configuration data (from loaded data).
        - `_bathymetry`: Bathymetry data (from loaded data).
        - `_beacons`: Beacons data (from loaded data).
        - `_cam_config`: Camera configuration data (from loaded data).
        - `_filter_video`: Video filter configuration data (from loaded data).
        - `_piv`: PIV analysis configuration data (from loaded data).
        - `_post_process`: Post-processing configuration data (from loaded data).

        Parameters
        ----------

        - `project_dir` (`str`): The path to the directory containing the RiverApp project.

        Raises
        ------

        - `TypeError`: If `project_dir` is not a string type.
        - `FileNotFoundError`:
            - If the provided `project_dir` does not exist.
            - If the project configuration file is not found within `project_dir`.
        - `ValueError`: If the loaded project data format is invalid.

        Notes
        -----

        - This function utilizes the `os.path` module for path manipulation.
        - The function uses the `json` module to read and parse the project
          configuration file (JSON format).
        - An internal function (`_check_backup_file_format`) is used to validate
          the loaded data structure.

        """
        if not isinstance(project_dir, str):
            raise TypeError(f"project_dir should be a str : {project_dir}")

        if not path.exists(project_dir) or not path.isdir(project_dir):
            raise FileNotFoundError(f"project_dir was not found : {project_dir}")

        backup_file_path: str = path.join(project_dir, f"{path.basename(project_dir)}.json")

        if not path.exists(backup_file_path):
            raise FileNotFoundError(f"the backup file was not found : {backup_file_path}")

        with open(backup_file_path, "r") as json_file:
            project_data: dict = load(json_file)

        # Check if data format is correct
        try:
            self._check_backup_file_format(PROJECT_DEFAULT_STRUCT, project_data)
        except ValueError as exc:
            raise ValueError(f'CRASH : The backup file format is not correct{backup_file_path}') \
                from exc
        self._backup_file = backup_file_path
        self._project_name = path.basename(project_dir)
        self._steps_done = project_data["steps_done"]
        self._video_configuration = project_data["video_configuration"]
        self._bathymetry = project_data["bathymetry"]
        self._beacons = project_data["beacons"]
        self._cam_config = project_data["cam_config"]
        self._filter_video = project_data["filter_video"]
        self._piv = project_data["piv"]
        self._post_process = project_data["post_process"]

    def create_project(self, projects_dir: str, project_name: str):
        """
        Creates a new RiverApp project directory

        This function creates a new directory structure for a RiverApp project
        within a specified projects directory. It performs the following checks
        before creating the project:

        - **Data Type Verification:** Ensures both `projects_dir` and
          `project_name` are strings.
        - **Directory Existence:** Verifies if the provided `projects_dir` exists
          and is a directory.

        If all checks pass, the function creates the project directory structure:

        1. Creates a new directory within `projects_dir` named according to
           the provided `project_name`.
        2. Creates a project configuration file (`project_name.json`) within the
           newly created project directory.
        3. Writes the default project configuration data (stored in
           `PROJECT_DEFAULT_STRUCT`) to the project configuration file.
           The `project_name` key in the default data is updated with the
           provided `project_name`.

        Parameters
        ----------

        - `projects_dir` (`str`): The path to the directory containing RiverApp projects.
        - `project_name` (`str`): The name for the new RiverApp project.

        Raises
        ------

        - `TypeError`:
            - If `projects_dir` is not a string type.
            - If `project_name` is not a string type.
        - `FileNotFoundError`: If the provided `projects_dir` does not exist
          or is not a directory.
        - `FileExistsError`: If a directory with the provided `project_name`
          already exists within `projects_dir`.

        Notes
        -----

        - This function utilizes the `os.path` module for path manipulation.
        - The function uses `mkdir` to create the project directory.
        - The function writes the project configuration data to a JSON file
          using the `json` module with indentation for readability.

        """
        if not isinstance(projects_dir, str):
            raise TypeError(f"project_dir should be a str : {projects_dir}")

        if not isinstance(project_name, str):
            raise TypeError(f"project_name should be a str : {project_name}")

        if not path.exists(projects_dir) or not path.isdir(projects_dir):
            raise FileNotFoundError(f"project_dir was not found : {projects_dir}")

        project_directory: str = path.join(projects_dir, project_name)

        if path.exists(project_directory):
            raise FileExistsError(f"project_name is already taken : {project_name}")

        mkdir(project_directory)

        with open(path.join(project_directory, f"{project_name}.json"), "w") as json_file:
            data = PROJECT_DEFAULT_STRUCT
            data["project_name"] = project_name
            json_file.write(dumps(data, indent=4))

    def delete_project(self, project_dir: str):
        """
        Deletes a RiverApp project directory

        This function attempts to delete a directory containing a RiverApp project.
        It performs the following checks before deletion:

        - **Data Type Verification:** Ensures `project_dir` is a string type.
        - **Directory Existence:** Verifies if the provided `project_dir` exists and
          is a directory.
        - **Project Confirmation:** Checks if a project configuration file
          (.json file with the same name as the directory) exists within
          `project_dir`. This is used to confirm it's a valid RiverApp project directory.

        If all checks pass, the function removes the entire `project_dir` using
        `rmtree`.

        Parameters
        ----------

        - `project_dir` (`str`): The path to the directory containing the RiverApp project.

        Raises
        ------

        - `TypeError`: If `project_dir` is not a string type.
        - `FileNotFoundError`:
            - If the provided `project_dir` does not exist.
            - If the directory does not contain the expected project configuration file.

        Notes
        -----

        - This function utilizes the `os.path` module for path manipulation.
        - The function uses `rmtree` to recursively delete the project directory
          and its contents. Caution should be exercised as this is a permanent deletion.

        """
        if not isinstance(project_dir, str):
            raise TypeError(f"project_dir should be a str : {project_dir}")

        if not path.exists(project_dir) or not path.isdir(project_dir):
            raise FileNotFoundError(f"project_dir was not found : {project_dir}")

        if not path.exists(path.join(project_dir, f"{path.basename(project_dir)}.json")):
            raise FileNotFoundError("the directory is not a RiverApp project directory")

        rmtree(project_dir)
