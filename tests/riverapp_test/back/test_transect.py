import json

import pytest
from os import path
import numpy as np
import xarray as xr
import pandas as pd

from libs import pyorc
from src.back.transect import delimiter_points_bathy, all_points_bathy, transect_plot, transect
from back_fixtures import directory_path, bathymetry, video, cam_config_json, local_points


def test_delimiter_points_bathy(video, directory_path, local_points):
    tst = delimiter_points_bathy(video.camera_config, local_points)
    delimiter_points = np.loadtxt("tests/riverapp_test/test_ressources/delimiter_points_bathy_results.txt")
    assert tst.any() == delimiter_points.any()
    # TODO verify a case where it should not be equal
    return


def test_all_points_bathy(video, bathymetry, directory_path, local_points):
    delimiter_points = delimiter_points_bathy(video.camera_config, local_points)
    all_points_ds = all_points_bathy(bathymetry, delimiter_points, xr.open_dataset(directory_path + "piv_masked.nc"))
    expected = pd.read_csv("tests/riverapp_test/test_ressources/all_points_bathy_results.csv")

    assert all_points_ds.any() == expected.any()
    # TODO verify a case where it should not be equal
    return


def test_transect_plot(video, bathymetry, directory_path, local_points):
    delimiter_points = delimiter_points_bathy(video.camera_config, local_points)
    all_points_ds = all_points_bathy(bathymetry, delimiter_points, xr.open_dataset(directory_path + "piv_masked.nc"))
    ds = transect_plot(all_points_ds, video, xr.open_dataset(directory_path + "piv_masked.nc"),
                       "tests/riverapp_test/test_ressources/VGC1/", bathymetry["surface_coefficient"])
    expected = pd.read_csv("tests/riverapp_test/test_ressources/transect_plot_results.csv")
    assert ds.any() == expected.any()
    # TODO verify a case where it should not be equal
    return


def test_transect(video, directory_path, bathymetry, local_points):
    ds = xr.open_dataset(directory_path + "piv_masked.nc")
    ds_points_q = transect(ds, video, directory_path, bathymetry, local_points)
    ds_points_q = ds_points_q.to_dataframe()
    expected = pd.read_csv("tests/riverapp_test/test_ressources/ds_points_q.csv", index_col=0)
    assert ds_points_q["river_flow"].any() == expected["river_flow"].any()
    # TODO verify a case where it should not be equal
    return
