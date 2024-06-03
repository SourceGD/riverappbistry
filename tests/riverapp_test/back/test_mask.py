import json

import pytest
import xarray as xr
from os import path, remove
from src.back.mask import apply_mask, mask_and_plot
from libs.pyorc import CameraConfig, Video
from back_fixtures import saving_project_data, empty_spd, check_backup_file_format, testing_project_path


def test_apply_mask():
    dataset = xr.open_dataset("tests/riverapp_test/test_ressources/mask_testing/piv.nc")
    mask = apply_mask(dataset)
    expected_dataset = xr.open_dataset("tests/riverapp_test/test_ressources/VGC1/piv_masked.nc")
    assert mask.any() == expected_dataset.any()
    return


def test_mask_and_plot(empty_spd, check_backup_file_format, testing_project_path):
    if path.exists("tests/riverapp_test/test_ressources/mask_testing/piv_masked.nc"):
        remove("tests/riverapp_test/test_ressources/mask_testing/piv_masked.nc")
    dataset = xr.open_dataset("tests/riverapp_test/test_ressources/mask_testing/piv.nc")
    spd = empty_spd
    default_json = check_backup_file_format
    with open(testing_project_path + "/testing_project.json", "w") as f:
        json.dump(default_json, f, indent=4)
    current_dir_base = path.dirname(path.abspath(__file__))
    current_dir = path.join(current_dir_base, "../test_ressources/testing_project")
    spd.load_project(current_dir)

    start_frame = int(5 * spd.video_configuration['start_time'])
    end_frame = int(5 * spd._video_configuration['end_time'])
    video = Video(spd._video_configuration['video'], start_frame=start_frame, end_frame=end_frame,
                  camera_config=spd.cam_config)

    mask_and_plot("tests/riverapp_test/test_ressources/mask_testing/", dataset, video)
    expected_dataset = xr.open_dataset("tests/riverapp_test/test_ressources/VGC1/piv_masked.nc")
    current_dataset = xr.open_dataset("tests/riverapp_test/test_ressources/mask_testing/piv_masked.nc")
    assert current_dataset.any() == expected_dataset.any()
    return
