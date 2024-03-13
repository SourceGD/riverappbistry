import pytest
import json
from os import path
from src.back import SavingProjectData
from libs import pyorc


# FIXTURES FOR TESTING BACK/SAVING_PROJECT_DATA.PY
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
def all_video_config():
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
def all_bathy_config():
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


@pytest.fixture
def all_beacons_config():
    return {
        "good_beacons": {
            "points": [
                [
                    1518,
                    122
                ],
                [
                    1449,
                    749
                ],
                [
                    203,
                    658
                ],
                [
                    770,
                    161
                ]
            ],
            "p1_to_p2": 6.65,
            "p2_to_p3": 7.6,
            "p3_to_p4": 6.69,
            "p4_to_p1": 7.82,
            "p1_to_p3": 10.29,
            "p2_to_p4": 10.1
        },
        "bad_beacons_format": [],
        "bad_beacons_pair_count": {
            "points": [
                [
                    1518,
                    122
                ],
                [
                    1449,
                    749
                ],
                [
                    203,
                    658
                ]
            ],
            "p1_to_p2": 6.65,
            "p2_to_p3": 7.6,
            "p3_to_p4": 6.69,
            "p4_to_p1": 7.82,
            "p1_to_p3": 10.29,
            "p2_to_p4": 10.1
        },
        "bad_beacons_point_lacking_coordinate": {
            "points": [
                [
                    1518,
                    122
                ],
                [
                    1449,
                    749
                ],
                [
                    203,
                    658
                ],
                [
                    770
                ]
            ],
            "p1_to_p2": 6.65,
            "p2_to_p3": 7.6,
            "p3_to_p4": 6.69,
            "p4_to_p1": 7.82,
            "p1_to_p3": 10.29,
            "p2_to_p4": 10.1
        },
        "bad_beacons_values": {
            "points": [
                [
                    1518,
                    122
                ],
                [
                    1449,
                    749
                ],
                [
                    203,
                    658
                ],
                [
                    770,
                    "161"
                ]
            ],
            "p1_to_p2": 6.65,
            "p2_to_p3": 7.6,
            "p3_to_p4": 6.69,
            "p4_to_p1": 7.82,
            "p1_to_p3": 10.29,
            "p2_to_p4": 10.1
        },
        "bad_beacons_impossible_distance": {
            "points": [
                [
                    1518,
                    122
                ],
                [
                    1449,
                    749
                ],
                [
                    203,
                    658
                ],
                [
                    770,
                    161
                ]
            ],
            "p1_to_p2": 6.65,
            "p2_to_p3": 7.6,
            "p3_to_p4": 6.69,
            "p4_to_p1": 7.82,
            "p1_to_p3": 0,
            "p2_to_p4": 10.1
        }
    }
