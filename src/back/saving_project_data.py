import json
import time
from os import path, mkdir
from json import load, dumps, loads
from shutil import rmtree
import math

import requests
from dask.diagnostics import ProgressBar
from cv2 import VideoCapture, CAP_PROP_FPS

from definitions import PROJECT_DEFAULT_STRUCT, PROJECTS_DIR

from src.utils import get_video_frame
from libs.pyorc import CameraConfig, Video


class ProjectNotLoaded(Exception):
    pass


class SavingProjectData():
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
            raise ProjectNotLoaded(f"The project need to be loaded before adding data")

        if self._video_configuration == video_configuration:
            return

        if not isinstance(video_configuration, dict):
            return TypeError(f"video_configuration should be a dict : {video_configuration}")

        self._check_missing_data(["video", "start_time", "end_time", "frequency"], video_configuration)

        if not path.exists(video_configuration["video"]):
            raise FileExistsError(f"The video was not found : {video_configuration['video']}")

        if not isinstance(video_configuration["start_time"], (int, float)):
            raise TypeError(f"start_time should be an int or a float")

        if not isinstance(video_configuration["end_time"], (int, float)):
            raise TypeError(f"end_time should be an int or a float")

        if not isinstance(video_configuration["frequency"], (int, float)):
            raise TypeError(f"frequency should be an int or a float")

        if video_configuration["start_time"] < 0:
            raise ValueError(f"start_time cannot be less than 0")

        if video_configuration["end_time"] < 0:
            raise ValueError(f"end_time cannot be less than 0")

        if video_configuration["frequency"] <= 0:
            raise ValueError(f"start_time cannot be less than or equal to 0")

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
            raise ProjectNotLoaded(f"The project need to be loaded before adding data")

        if self._bathymetry == bathymetry:
            return

        if not isinstance(bathymetry, dict):
            raise TypeError(f"bathymetry should be a dict : {bathymetry}")

        self._check_missing_data(["x", "y", "water_level"], bathymetry)

        if len(bathymetry["x"]) != len(bathymetry["y"]):
            raise ValueError("There are not as many x-coordinates as y-coordinates")

        for i in range(len(bathymetry["x"])):
            if not isinstance(bathymetry["x"][i], (int, float)) or not isinstance(bathymetry["y"][i], (int, float)):
                raise ValueError("All coordinates must be numbers")

        if not isinstance(bathymetry["water_level"], (float, int)):
            raise TypeError("Water Level should be a number")

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
            raise ProjectNotLoaded(f"The project need to be loaded before adding data")

        if self._beacons == beacons:
            return

        if not isinstance(beacons, dict):
            return TypeError(f"beacons should be a dict : {beacons}")

        self._check_missing_data(["points", "p1_to_p2", "p2_to_p3", "p3_to_p4", "p4_to_p1", "p1_to_p3", "p2_to_p4"],
                                 beacons)

        if len(beacons["points"]) != 4:
            raise ValueError("Points should have 4 pairs of coordinates ")

        for coordinates in beacons["points"]:
            if len(coordinates) != 2:
                raise ValueError(f"A point lacks the x-coordinate or y-coordinates or both")

            if not isinstance(coordinates[0], (int, float)) or not isinstance(coordinates[1], (int, float)):
                raise ValueError(f"Point coordinates should be numbers")

        if beacons["p1_to_p2"] <= 0 or beacons["p2_to_p3"] <= 0 or beacons["p3_to_p4"] <= 0 or beacons["p4_to_p1"] <= 0:
            raise ValueError(f"Distance between points cannot be lass than or equal to 0")

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
    def filter_video(self, filter_video: dict) -> None:
        self._save_step("filter_video", {})
        return

    @property
    def piv(self) -> dict:
        if self._piv is None:
            return None

        data = self._piv
        data["file"] = path.abspath(path.join(PROJECTS_DIR, self._project_name, self._piv["file"]))
        return data

    def _save_step(self, step: str, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"data should be a dict")

        with open(self._backup_file, "r") as json_file:
            saved_data = load(json_file)

        saved_data[step] = data
        saved_data["steps_done"][step] = True
        self._steps_done[step] = True

        with open(self._backup_file, "w") as json_file:
            json_file.write(dumps(saved_data, indent=4))

        return

    def _check_backup_file_format(self, wanted_dict_format: dict, dict_format: dict) -> bool:
        if not isinstance(wanted_dict_format, dict):
            raise TypeError(f"wanted_dict_format should be a dict : {wanted_dict_format}")

        if not isinstance(dict_format, dict):
            raise TypeError(f"dict_format should be a dict : {dict_format}")

        keys_format = set(wanted_dict_format.keys())
        keys_data = set(dict_format.keys())
        if keys_format != keys_data:
            print("ValueError, The data format doesn't respect the wanted format")
            raise ValueError(f"The data format doesn't respect the wanted format")

        for key in keys_format:
            if key == "cam_config":
                continue

            if isinstance(wanted_dict_format[key], dict) and isinstance(dict_format[key], dict):
                self._check_backup_file_format(wanted_dict_format[key], dict_format[key])

            elif (isinstance(wanted_dict_format[key], dict) and not isinstance(dict_format[key],
                                                                               dict)) or not isinstance(
                    wanted_dict_format[key], dict) and isinstance(dict_format[key], dict):
                raise ValueError(f"The data format doesn't respect the wanted format")

        return True

    def _check_missing_data(self, wanted_data: list, data: dict) -> bool:

        if not isinstance(wanted_data, list):
            return TypeError(f"wanted_data should be a list : {wanted_data}")

        if not isinstance(data, dict):
            return TypeError(f"bathymetry should be a dict : {data}")

        missing_data = [key for key in wanted_data if key not in data.keys()]
        if missing_data:
            raise ValueError(f"Missing data : {missing_data}")

        return True

    def _convert_dist_to_dest_points(self, dist: list) -> list:
        # Points coordinates computation
        # We consider first that P1 and P4 are vertically aligned and P4 as the  origin
        P1, P4 = [0, dist[3]], [0, 0]

        # Then we compute other coordinates using cosine law
        alpha = math.acos((dist[3] ** 2 + dist[5] ** 2 - dist[0] ** 2) / (2 * dist[3] * dist[5]))
        P2 = [dist[5] * math.sin(alpha), dist[5] * math.cos(alpha)]
        beta = math.acos((dist[3] ** 2 + dist[2] ** 2 - dist[4] ** 2) / (2 * dist[3] * dist[2]))
        P3 = [dist[2] * math.sin(beta), dist[2] * math.cos(beta)]

        return [[P2[0], P2[1]], [P3[0], P3[1]], [P4[0], P4[1]], [P1[0], P1[1]]]

    def generate_cam_config(self) -> bool:
        if not self._steps_done["video_configuration"] or not self._steps_done["bathymetry"] or not self._steps_done[
            "beacons"]:
            return False

        init_frame = get_video_frame(self.video_configuration["video"], self.video_configuration["start_time"])

        height, width = init_frame.shape[0:2]
        print("=================================================================================")
        print(height," " ,width)
        print("=================================================================================")
        dst: list = self._convert_dist_to_dest_points([
            self._beacons["p1_to_p2"],
            self._beacons["p2_to_p3"],
            self._beacons["p3_to_p4"],
            self._beacons["p4_to_p1"],
            self._beacons["p1_to_p3"],
            self._beacons["p2_to_p4"]
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
            lens_position=[7, -2, 3]
            # the lens_position does not seem to be used for the process but has to be indicated to avoid error/warnings
        )

        cam_config.set_bbox_from_corners(self._beacons["points"])
        self._save_step("cam_config", loads(cam_config.to_json()))
        self._cam_config = cam_config
        return True

    def generate_piv(self) -> bool:
        if not self._steps_done["video_configuration"] or not self._steps_done["bathymetry"] \
                or not self._steps_done["beacons"] or not self._steps_done["cam_config"] \
                or not self._steps_done["filter_video"]:
            return False

        video: str = self._video_configuration["video"]
        fps: int = VideoCapture(video).get(CAP_PROP_FPS)
        start_frame: int = int(self._video_configuration["start_time"] * fps)
        end_frame: int = int(self._video_configuration["end_time"] * fps)
        print("=====================================")
        print(self._cam_config)
        self._cam_config = loads(self._cam_config.to_json()) if isinstance(self._cam_config, CameraConfig) else self._cam_config
        params = {
            "fps": fps,
            "start_frame": start_frame,
            "end_frame": end_frame,
            "freq": self._video_configuration["frequency"],
            "h_a": self._bathymetry["water_level"],
            "camera_config": self._cam_config,
            "project_name": self._project_name
        }
        # TODO change the route_url by using a .env file
        route_url = "http://localhost:5000/process-piv"
        files = {
            "file": (video, open(video, "rb"), 'application/octet-stream'),
            "data": ('data', dumps(params), 'application/json')
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }

        response = requests.post(route_url, files=files)
        print(response.text)


        # TODO: if no internet connection, use the following code, if there is one use the api
        # pyorc_video: Video = Video(
        #     video,
        #     start_frame=start_frame,
        #     end_frame=end_frame,
        #     freq=self._video_configuration["frequency"],
        #     h_a=self._bathymetry["water_level"],
        #     camera_config=self._cam_config
        # )
        #
        # da = pyorc_video.get_frames()
        # #Apply previous steps filter here
        # da_norm = da.frames.normalize()
        # da_norm_proj = da_norm.frames.project()
        # piv = da_norm_proj.frames.get_piv().to_netcdf(path.join(PROJECTS_DIR, self._project_name, "piv.nc"))
        self._save_step("piv", {
            "file": "piv.nc",
            "need_update": False
        })

        return True

    def save_post_process(self, river_flow: float, transect_picture_path: str) -> None:
        self._save_step("post_process", {
            "river_flow": river_flow,
            "transect_picture_path": transect_picture_path
        })
        return

    def load_project(self, project_dir: str) -> None:
        print(project_dir)
        if not isinstance(project_dir, str):
            raise ValueError(f"project_dir should be a str : {project_dir}")

        if not path.exists(project_dir) or not path.isdir(project_dir):
            raise FileNotFoundError(f"project_dir was not found : {project_dir}")

        backup_file_path: str = path.join(project_dir, f"{path.basename(project_dir)}.json")

        if not path.exists(backup_file_path):
            raise FileNotFoundError(f"the backup file was not found : {backup_file_path}")

        with open(backup_file_path, "r") as json_file:
            project_data: dict = load(json_file)

        # Check if data format is correct
        self._check_backup_file_format(PROJECT_DEFAULT_STRUCT, project_data)
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
        return

    def create_project(self, projects_dir: str, project_name: str) -> None:
        if not isinstance(projects_dir, str):
            raise ValueError(f"project_dir should be a str : {projects_dir}")

        if not isinstance(project_name, str):
            raise ValueError(f"project_name should be a str : {project_name}")

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

        return

    def delete_project(self, project_dir: str) -> None:
        if not isinstance(project_dir, str):
            raise ValueError(f"project_dir should be a str : {project_dir}")

        if not path.exists(project_dir) or not path.isdir(project_dir):
            raise FileNotFoundError(f"project_dir was not found : {project_dir}")

        if not path.exists(path.join(project_dir, f"{path.basename(project_dir)}.json")):
            raise FileNotFoundError(f"the directory is not a RiverApp project directory")

        rmtree(project_dir)

        return