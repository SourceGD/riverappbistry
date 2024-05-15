import pytest
from src.back.gcp_detection.gcp_detection import beacons_detection, GCP_detect, get_polar_angle_wrt_first_pt, sort_src
from back_fixtures import expected_gcp, expected_sorted_gcp
import numpy as np


def test_beacons_detection():
    with pytest.raises(ValueError):
        beacons_detection(1, 1)

    with pytest.raises(FileNotFoundError):
        beacons_detection("test", 1)
    # assert beacons_detection("tests/riverapp_test/test_ressources/PB.mp4", 1) == expected_image
    return


def test_GCP_detect(expected_gcp):
    with pytest.raises(ValueError):
        GCP_detect(1)
    with pytest.raises(FileNotFoundError):
        GCP_detect("test")
    with pytest.raises(IOError):
        GCP_detect("tests/riverapp_test/test_ressources/ds_points_q.csv")
    assert GCP_detect("tests/riverapp_test/test_ressources/PB.mp4") == expected_gcp
    return


def test_sort_src(expected_sorted_gcp):
    detected = GCP_detect("tests/riverapp_test/test_ressources/PB.mp4")
    assert sort_src(detected) == expected_sorted_gcp
    return


