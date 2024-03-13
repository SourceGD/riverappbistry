import pytest
import json

from back_fixtures import saving_project_data, all_video_config, all_bathy_config, all_beacons_config


def test_video_configuration_setter(saving_project_data, all_video_config):
    spd = saving_project_data
    with pytest.raises(FileExistsError):
        spd.video_configuration = all_video_config["bad_video_config"]
    with pytest.raises(TypeError):
        spd.video_configuration = all_video_config["bad_start_time_format_config"]
    with pytest.raises(TypeError):
        spd.video_configuration = all_video_config["bad_end_time_format_config"]
    with pytest.raises(TypeError):
        spd.video_configuration = all_video_config["bad_frequency_format_config"]
    with pytest.raises(ValueError):
        spd.video_configuration = all_video_config["bad_start_time_value"]
    with pytest.raises(ValueError):
        spd.video_configuration = all_video_config["bad_end_time_value"]
    with pytest.raises(ValueError):
        spd.video_configuration = all_video_config["bad_frequency_value"]
    with pytest.raises(ValueError):
        spd.video_configuration = all_video_config["greater_start_time_than_end_time"]

    spd.video_configuration = all_video_config["good_video_config"]
    assert spd.video_configuration == all_video_config["good_video_config"]
    return


def test_bathymetry_setter(saving_project_data, all_bathy_config):
    spd = saving_project_data
    with pytest.raises(TypeError):
        spd.bathymetry = all_bathy_config["bad_bathy_format"]
    with pytest.raises(ValueError):
        spd.bathymetry = all_bathy_config["bad_bathy_values_count"]
    with pytest.raises(ValueError):
        spd.bathymetry = all_bathy_config["bad_bathy_values"]
    with pytest.raises(ValueError):
        spd.bathymetry = all_bathy_config["bad_bathy_water_level"]

    spd.bathymetry = all_bathy_config["good_bathy"]
    assert spd.bathymetry == all_bathy_config["good_bathy"]
    return


def test_beacons_setter(saving_project_data, all_beacons_config):
    spd = saving_project_data
    with pytest.raises(TypeError):
        spd.beacons = all_beacons_config["bad_beacons_format"]
    with pytest.raises(ValueError):
        spd.beacons = all_beacons_config["bad_beacons_pair_count"]
    with pytest.raises(ValueError):
        spd.beacons = all_beacons_config["bad_beacons_point_lacking_coordinate"]
    with pytest.raises(ValueError):
        spd.beacons = all_beacons_config["bad_beacons_values"]
    with pytest.raises(ValueError):
        spd.beacons = all_beacons_config["bad_beacons_impossible_distance"]

    spd.beacons = all_beacons_config["good_beacons"]
    assert spd.beacons == all_beacons_config["good_beacons"]
    pass


def test_save_step(saving_project_data):
    spd = saving_project_data
    with pytest.raises(TypeError):
        spd._save_step("video_configuration", 1)
    with pytest.raises(TypeError):
        spd._save_step("video_configuration", [])
    with pytest.raises(ValueError):
        spd._save_step("not_existing_step", {})
    return


def test_check_backup_file_format(saving_project_data):
    spd = saving_project_data
    with open("../test_ressources/test_check_backup_file_format.json", "r") as file:
        dict_format = json.load(file)
    with open("../test_ressources/testing_project/default_config.json", "r") as file:
        wanted_dict_format = json.load(file)

    with pytest.raises(TypeError):
        spd._check_backup_file_format(dict_format, [])
    with pytest.raises(TypeError):
        spd._check_backup_file_format(dict_format, 1)
    with pytest.raises(ValueError):
        temp_dict_format = dict_format.copy()
        temp_dict_format["test_adding_a_key"] = {}
        spd._check_backup_file_format(temp_dict_format, dict_format)
    with pytest.raises(ValueError):
        temp_dict_format = dict_format.copy()
        temp_dict_format["filter_video"] = []
        spd._check_backup_file_format(temp_dict_format, dict_format)

    assert spd._check_backup_file_format(dict_format, wanted_dict_format) is True

    return


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
