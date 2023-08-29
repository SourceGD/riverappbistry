from os import path

ROOT_DIR = path.dirname(path.abspath(__file__))
CONFIG_DIR = path.join(ROOT_DIR, 'config')
PROJECTS_DIR = path.join(ROOT_DIR, "projects")

PROJECT_DEFAULT_STRUCT = {
    "project_name": "",
    "steps_done": {
        "video_configuration" : 0,
        "bathymetry" : 0,
        "beacons" : 0,
    },

    "video_configuration": {
        "video" : "",
        "start_time": 0,
        "end_time": 0,
        "frequency": 0
    },

    "bathymetry" : {
        "x": [],
        "y": [],
        "water_level": 0
    },

    "beacons" : {
        "points": [],
        "p1_to_p2" : 0,
        "p2_to_p3": 0,
        "p3_to_p4": 0,
        "p4_to_p1": 0
    },

    "piv": {
        "filters": [],
        "piv_file_data": ""
    },

    "post_process": {
        "masks": []
    },

    "transect": {
        "points": [],
        "transect_file_data": ""
    }
}

PROJECT_STEPS = ["video_configuration", "bathymetry", "beacons", "filter_video", "piv"]
