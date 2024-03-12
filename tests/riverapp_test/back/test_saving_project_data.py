import json

import pytest
from os import path
import numpy as np
import xarray as xr
import pandas as pd
from src.back import SavingProjectData

@pytest.fixture
def saving_project_data():
    spd = SavingProjectData()
    return spd


def test_video_configuration_setter():
    # TODO
    pass


def test_bathymetry_setter():
    # TODO
    pass


def test_beacons_setter():
    # TODO
    pass


def test_save_step():
    # TODO
    pass


def test_check_backup_file_format():
    # TODO
    pass


def test_check_missing_data():
    # TODO
    pass


def test_convert_dist_to_dest_points():
    # TODO
    pass


def test_generate_cam_config():
    # TODO
    pass


def test_generate_piv():
    # TODO
    pass


def test_save_post_process():
    # TODO
    pass


def test_load_project():
    # TODO
    pass


def test_create_project():
    # TODO
    pass


def test_delete_project():
    # TODO
    pass



