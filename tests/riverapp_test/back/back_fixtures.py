import pytest
import json
from os import path
from src.back import SavingProjectData
from src.utils import video_to_image
from libs import pyorc


@pytest.fixture
def testing_project_path():
    return "tests/riverapp_test/test_ressources/testing_project"


# FIXTURES FOR TESTING BACK/TRANSECT.PY
@pytest.fixture
def directory_path():
    return "tests/riverapp_test/test_ressources/VGC1/"


@pytest.fixture
def bathymetry():
    with open("tests/riverapp_test/test_ressources/bathy.json", "r") as f:
        bathymetry = json.load(f)
    return bathymetry


@pytest.fixture
def cam_config_json(directory_path):
    with open(directory_path + "cam_config.json", "r") as f:
        cam_config = json.load(f)
    return cam_config


@pytest.fixture
def local_points():
    return [[494, 427], [1391, 465]]


@pytest.fixture
def video(cam_config_json, directory_path):
    start_frame = 25
    end_frame = 30
    video = pyorc.Video(directory_path + "VGC1.mp4", start_frame=start_frame, end_frame=end_frame)
    video.camera_config = cam_config_json
    return video


# FIXTURES FOR TESTING BACK/gcp_detection/gcp_detection.py
@pytest.fixture
def expected_gcp():
    return [[212, 665], [193, 236], [958, 51], [989, 572]]


@pytest.fixture
def expected_sorted_gcp():
    return [[989, 572], [958, 51], [193, 236], [212, 665]]


# TODO Find why this fixture generates a segfault
@pytest.fixture
def expected_image(expected_gcp):
    return video_to_image("tests/riverapp_test/test_ressources/PB.mp4", 19)

# FIXTURES FOR TESTING BACK/SAVING_PROJECT_DATA.PY
@pytest.fixture
def saving_project_data():
    spd = SavingProjectData()
    with open("tests/riverapp_test/test_ressources/testing_project/default_config.json", "r") as f:
        default_json = json.load(f)
    with open("tests/riverapp_test/test_ressources/testing_project/testing_project.json", "w") as f:
        json.dump(default_json, f, indent=4)

    current_dir = path.dirname(path.abspath(__file__))
    current_dir = path.join(current_dir, "../test_ressources/testing_project")
    spd.load_project(current_dir)
    return spd


@pytest.fixture
def empty_spd():
    return SavingProjectData()


@pytest.fixture
def all_video_config():
    return {
        "good_video_config": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
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
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": "25",
            "end_time": 30,
            "frequency": 1
        },
        "bad_end_time_format_config": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": "25",
            "frequency": 1
        },
        "bad_frequency_format_config": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": 30,
            "frequency": "1"
        },
        "bad_start_time_value": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": -1,
            "end_time": 30,
            "frequency": 1
        },
        "bad_end_time_value": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": -1,
            "frequency": 1
        },
        "bad_frequency_value": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
            "end_time": 30,
            "frequency": -1
        },
        "greater_start_time_than_end_time": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": 30,
            "end_time": 25,
            "frequency": 1
        },
        "missing_data": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": 25,
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
        },
        "bad_bathy_water_level_type": {
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
            "water_level": "Not a number"
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
            "p1_to_p2": 7.6,
            "p2_to_p3": 6.69,
            "p3_to_p4": 7.82,
            "p4_to_p1": 6.65,
            "p1_to_p3": 10.1,
            "p2_to_p4": 10.29
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


@pytest.fixture
def check_missing_data_config():
    return {
        "wanted_data": ["video", "start_time", "end_time", "frequency"],
        "bad_wanted_data": ["video", "start_time", "end_time", "frequency", "bad_data"],
    }


@pytest.fixture
def check_backup_file_format():
    return {
        "project_name": "vgc",
        "steps_done": {
            "video_configuration": True,
            "bathymetry": True,
            "beacons": True,
            "cam_config": True,
            "filter_video": True,
            "piv": True,
            "post_process": True
        },
        "video_configuration": {
            "video": "tests/riverapp_test/test_ressources/VGC1/VGC1.mp4",
            "start_time": 25.0,
            "end_time": 30.0,
            "frequency": 1,
            "lens_position": [
                7.0,
                -2.0,
                3.0
            ]
        },
        "bathymetry": {
            "x": [
                0.0,
                0.35,
                0.6,
                0.8,
                1.2,
                1.5,
                1.8,
                2.1,
                2.4,
                2.7,
                2.85,
                3.2,
                3.6,
                3.85,
                4.1,
                4.35,
                4.6,
                4.8,
                5.0,
                5.2,
                5.4,
                5.6,
                5.84,
                6.0
            ],
            "y": [
                1.44,
                0.29,
                0.28,
                0.3,
                0.13,
                0.14,
                0.1,
                0.11,
                0.04,
                0.11,
                0.11,
                0.055,
                0.0,
                0.05,
                0.02,
                0.07,
                0.06,
                0.11,
                0.07,
                0.09,
                0.13,
                0.08,
                0.06,
                1.44
            ],
            "water_level": 0.44,
            "surface_coefficient": 0.85
        },
        "beacons": {
            "points": [
                [
                    1527,
                    126
                ],
                [
                    1449,
                    749
                ],
                [
                    207,
                    650
                ],
                [
                    765,
                    165
                ]
            ],
            "p1_to_p2": 7.6,
            "p2_to_p3": 6.69,
            "p3_to_p4": 7.82,
            "p4_to_p1": 6.65,
            "p1_to_p3": 10.1,
            "p2_to_p4": 10.29
        },
        "cam_config": {
            "height": 1080,
            "width": 1920,
            "resolution": 0.01,
            "lens_position": [
                7.0,
                -2.0,
                3.0
            ],
            "gcps": {
                "src": [
                    [
                        1527,
                        126
                    ],
                    [
                        1449,
                        749
                    ],
                    [
                        207,
                        650
                    ],
                    [
                        765,
                        165
                    ]
                ],
                "dst": [
                    [
                        6.646518768729957,
                        7.60485294117647
                    ],
                    [
                        6.689999818092734,
                        0.0015601023017917583
                    ],
                    [
                        0,
                        0
                    ],
                    [
                        0,
                        7.82
                    ]
                ],
                "h_ref": 0.0,
                "z_0": 0.44
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
            "bbox": "POLYGON ((6.667613781127995 7.837302559629649, 6.689716101460062 -0.0026662851704344, -0.0002573132991914 -0.0215265559639981, -0.0223596336312588 7.818442288836085, 6.667613781127995 7.837302559629649))"
        },
        "filter_video": {},
        "piv": {
            "file": "piv.nc",
            "need_update": False
        },
        "post_process": {
            "river_flow": "1.52",
            "transect_picture_path": "/media/andreas/LaCie Andreas/Memoire/riverapp/projects/vgc/plot_transect.jpg",
            "local_points": [
                [
                    448,
                    504
                ],
                [
                    1400,
                    536
                ]
            ]
        }
    }
