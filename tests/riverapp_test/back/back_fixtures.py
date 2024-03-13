import pytest
import json
from os import path
from src.back import SavingProjectData
from libs import pyorc


# FIXTURES FOR TESTING SAVING_PROJECT_DATA.PY
@pytest.fixture
def directory_path():
    return "../test_ressources/VGC1/"


@pytest.fixture
def bathymetry():
    with open("../test_ressources/bathy.json", "r") as f:
        bathymetry = json.load(f)
    return bathymetry


@pytest.fixture
def cam_config_json(directory_path):
    cam_config = {}
    with open(directory_path + "cam_config.json", "r") as f:
        cam_config = json.load(f)
    return cam_config


@pytest.fixture
def video(cam_config_json, directory_path):
    start_frame = 25
    end_frame = 30
    video = pyorc.Video(directory_path + "VGC1.mp4", start_frame=start_frame, end_frame=end_frame)
    video.camera_config = cam_config_json
    return video


# FIXTURES FOR TESTING BACK/SAVING_PROJECT_DATA.PY


@pytest.fixture
def saving_project_data():
    spd = SavingProjectData()
    with open("../test_ressources/testing_project/default_config.json", "r") as f:
        default_json = json.load(f)
    with open("../test_ressources/testing_project/testing_project.json", "w") as f:
        json.dump(default_json, f, indent=4)

    current_dir = path.dirname(path.abspath(__file__))
    current_dir = path.join(current_dir, "../test_ressources/testing_project")
    spd.load_project(current_dir)
    return spd


@pytest.fixture
def all_video_configs():
    return {
        "good_video_config": {
            "video": "../test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": 30,
            "frequency": 1
        },
        "bad_video_config": {
            "video": "unknown/path.mp4",
            "start_time": -1,
            "end_time": -1,
            "frequency": -1
        },
        "bad_video_configuration_format_config": [
            "video",
            "start_time",
            "end_time",
            "frequency"
        ],
        "bad_start_time_format_config": {
            "video": "../test_ressources/VGC1/VGC1.mp4",
            "start_time": "25",
            "end_time": 30,
            "frequency": 1
        },
        "bad_end_time_format_config": {
            "video": "../test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": "25",
            "frequency": 1
        },
        "bad_frequency_format_config": {
            "video": "../test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": 30,
            "frequency": "1"
        },
        "bad_start_time_value": {
            "video": "../test_ressources/VGC1/VGC1.mp4",
            "start_time": -1,
            "end_time": 30,
            "frequency": 1
        },
        "bad_end_time_value": {
            "video": "../test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": -1,
            "frequency": 1
        },
        "bad_frequency_value": {
            "video": "../test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": 30,
            "frequency": -1
        },
        "greater_start_time_than_end_time": {
            "video": "../test_ressources/VGC1/VGC1.mp4",
            "start_time": 30,
            "end_time": 25,
            "frequency": 1
        }
    }


@pytest.fixture
def good_bathy():
    return {
        "x": [
            0.0,
            0.35,
            0.6,
            0.8,
            1.2,
            1.5
        ],
        "y": [
            1.44,
            0.29,
            0.28,
            0.3,
            0.13,
            0.14
        ],
        "water_level": 0.44
    }


@pytest.fixture
def bad_bathy_format():
    return []


@pytest.fixture
def bad_bathy_values_count():
    return {
        "x": [
            0.0,
            0.35,
            0.6,
            0.8,
            1.2,
            1.5
        ],
        "y": [
            1.44,
            0.29,
            0.28,
            0.3,
            0.13,
        ],
        "water_level": 0.44
    }


@pytest.fixture
def bad_bathy_values():
    return {
        "x": [
            0.0,
            0.35,
            0.6,
            0.8,
            1.2,
            1.5
        ],
        "y": [
            1.44,
            0.29,
            "0.28",
            0.3,
            0.13,
            0.14
        ],
        "water_level": 0.44
    }


@pytest.fixture
def bad_bathy_water_level():
    return {
        "x": [
            0.0,
            0.35,
            0.6,
            0.8,
            1.2,
            1.5
        ],
        "y": [
            1.44,
            0.29,
            0.28,
            0.3,
            0.13,
            0.14
        ],
        "water_level": -0.44
    }


@pytest.fixture
def all_bathy_configs():
    return {
        "good_bathy": {
            "x": [
                0.0,
                0.35,
                0.6,
                0.8,
                1.2,
                1.5
            ],
            "y": [
                1.44,
                0.29,
                0.28,
                0.3,
                0.13,
                0.14
            ],
            "water_level": 0.44
        },
        "bad_bathy_format": [],
        "bad_bathy_values_count": {
            "x": [
                0.0,
                0.35,
                0.6,
                0.8,
                1.2,
                1.5
            ],
            "y": [
                1.44,
                0.29,
                0.28,
                0.3,
                0.13,
            ],
            "water_level": 0.44
        },
        "bad_bathy_values": {
            "x": [
                0.0,
                0.35,
                0.6,
                0.8,
                1.2,
                1.5
            ],
            "y": [
                1.44,
                0.29,
                "0.28",
                0.3,
                0.13,
                0.14
            ],
            "water_level": 0.44
        },
        "bad_bathy_water_level": {
            "x": [
                0.0,
                0.35,
                0.6,
                0.8,
                1.2,
                1.5
            ],
            "y": [
                1.44,
                0.29,
                0.28,
                0.3,
                0.13,
                0.14
            ],
            "water_level": -0.44
        }
    }
