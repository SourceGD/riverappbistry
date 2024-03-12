import json

import pytest
from os import path
import numpy as np
import xarray as xr
import pandas as pd


from libs import pyorc
from src.back.transect import delimiter_points_bathy, all_points_bathy, transect_plot, transect


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


def test_delimiter_points_bathy(video, directory_path):
    tst = delimiter_points_bathy(video.camera_config)
    delimiter_points = np.loadtxt("../test_ressources/delimiter_points_bathy_results.txt")
    assert tst.any() == delimiter_points.any()
    # TODO verify a case where it should not be equal
    return


def test_all_points_bathy(video, bathymetry, directory_path):
    delimiter_points = delimiter_points_bathy(video.camera_config)
    all_points_ds = all_points_bathy(bathymetry, delimiter_points, xr.open_dataset(directory_path + "piv_masked.nc"))
    expected = pd.read_csv("../test_ressources/all_points_bathy_results.csv")

    assert all_points_ds.any() == expected.any()
    # TODO verify a case where it should not be equal
    return


def test_transect_plot(video, bathymetry, directory_path):
    delimiter_points = delimiter_points_bathy(video.camera_config)
    all_points_ds = all_points_bathy(bathymetry, delimiter_points, xr.open_dataset(directory_path + "piv_masked.nc"))
    ds = transect_plot(all_points_ds, video, xr.open_dataset(directory_path + "piv_masked.nc"), "../test_ressources/VGC1/")
    expected = pd.read_csv("../test_ressources/transect_plot_results.csv")
    assert ds.any() == expected.any()
    # TODO verify a case where it should not be equal
    return


def test_transect(video, directory_path, bathymetry):
    ds = xr.open_dataset(directory_path + "piv_masked.nc")
    ds_points_q = transect(ds, video, directory_path, bathymetry)
    ds_points_q = ds_points_q.to_dataframe()
    expected = pd.read_csv("../test_ressources/ds_points_q.csv", index_col=0)
    assert ds_points_q["river_flow"].any() == expected["river_flow"].any()
    # TODO verify a case where it should not be equal
    return
