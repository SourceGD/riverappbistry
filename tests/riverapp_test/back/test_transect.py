import json

import pytest
from os import path
import numpy as np
import xarray as xr
import pandas as pd


from libs import pyorc
from src.back.transect import delimiter_points_bathy, all_points_bathy, transect_plot, transect


@pytest.fixture
def sample_video_path():
    return "../test_ressources/VGC1/VGC1.mp4"


@pytest.fixture
def bathymetry():
    with open("../test_ressources/bathy.json", "r") as f:
        bathymetry = json.load(f)
    return bathymetry


@pytest.fixture
def piv_path():
    return "../test_ressources/VGC1/piv.nc"


@pytest.fixture
def masked_piv_path():
    return "../test_ressources/VGC1/piv_masked.nc"

@pytest.fixture
def cam_config_json():
    cam_config = {}
    with open("../test_ressources/VGC1/cam_config.json", "r") as f:
        cam_config = json.load(f)
    return cam_config

@pytest.fixture
def delimiter_points_path():
    return "../test_ressources/delimiter_points_bathy_results.txt"


@pytest.fixture
def video(cam_config_json, sample_video_path):
    start_frame = 25
    end_frame = 30
    video = pyorc.Video(sample_video_path, start_frame=start_frame, end_frame=end_frame)
    video.camera_config = cam_config_json
    return video



def test_delimiter_points_bathy(video, delimiter_points_path):
    tst = delimiter_points_bathy(video.camera_config)
    delimiter_points = np.loadtxt(delimiter_points_path)
    assert tst.any() == delimiter_points.any()
    # TODO verify a case where it should not be equal
    return


def test_all_points_bathy(video, bathymetry, masked_piv_path):
    delimiter_points = delimiter_points_bathy(video.camera_config)
    tst = all_points_bathy(bathymetry, delimiter_points, xr.open_dataset(masked_piv_path))
    expected = pd.read_csv("../test_ressources/all_points_bathy_results.csv")

    assert tst.any() == expected.any()
    # TODO verify a case where it should not be equal
    return


def test_transect_plot():
    # TODO
    pass


def test_transect():
    # TODO

    pass
