import pytest
import json

from os import path

from back_fixtures import saving_project_data, empty_spd, all_video_config, all_bathy_config, all_beacons_config, check_missing_data_config, check_backup_file_format


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
    return


def test_check_backup_file_format(saving_project_data, check_backup_file_format):
    spd = saving_project_data
    dict_format = check_backup_file_format
    with open("tests/riverapp_test/test_ressources/testing_project/default_config.json", "r") as file:
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


def test_check_missing_data(saving_project_data, all_video_config, check_missing_data_config):
    spd = saving_project_data
    video_config = all_video_config["good_video_config"]
    with pytest.raises(TypeError):
        spd._check_missing_data("not a list", video_config)
    with pytest.raises(TypeError):
        spd._check_missing_data([], "not a dict")
    with pytest.raises(ValueError):
        spd._check_missing_data(check_missing_data_config["bad_wanted_data"], video_config)
    with pytest.raises(ValueError):
        spd._check_missing_data(check_missing_data_config["wanted_data"], all_video_config["missing_data"])

    assert spd._check_missing_data(check_missing_data_config["wanted_data"], video_config) is True

    return


def test_convert_dist_to_dest_points(saving_project_data, all_beacons_config):
    spd = saving_project_data
    good_beacons = all_beacons_config["good_beacons"]
    beacons_list = [good_beacons["p4_to_p1"], good_beacons["p1_to_p2"], good_beacons["p2_to_p3"], good_beacons["p3_to_p4"], good_beacons["p2_to_p4"], good_beacons["p1_to_p3"]]
    expected_result = [[6.646518768729957, 7.60485294117647], [6.689999818092734, 0.0015601023017917583], [0, 0], [0, 7.82]]
    with pytest.raises(TypeError):
        spd._convert_dist_to_dest_points("not a list")
    assert spd._convert_dist_to_dest_points(beacons_list) == expected_result
    assert len(spd._convert_dist_to_dest_points(beacons_list)) == 4
    assert isinstance(spd._convert_dist_to_dest_points(beacons_list), list) is True
    return


def test_generate_cam_config(saving_project_data, check_backup_file_format):
    spd = saving_project_data
    expected_config = check_backup_file_format
    spd.video_configuration = expected_config["video_configuration"]
    assert spd.generate_piv() is False
    spd.bathymetry = expected_config["bathymetry"]
    assert spd.generate_cam_config() is False
    spd.beacons = expected_config["beacons"]
    assert spd.generate_cam_config() is True
    assert spd.cam_config.height == expected_config["cam_config"]["height"]
    assert spd.cam_config.width == expected_config["cam_config"]["width"]
    assert spd.cam_config.window_size == expected_config["cam_config"]["window_size"]
    assert spd.cam_config.resolution == expected_config["cam_config"]["resolution"]
    assert spd.cam_config.gcps == expected_config["cam_config"]["gcps"]
    assert spd.cam_config.lens_position == expected_config["cam_config"]["lens_position"]
    assert spd.cam_config.dist_coeffs == expected_config["cam_config"]["dist_coeffs"]
    assert spd.cam_config.camera_matrix == expected_config["cam_config"]["camera_matrix"]
    assert str(spd.cam_config.bbox) == expected_config["cam_config"]["bbox"]

    return


def test_generate_piv(saving_project_data, check_backup_file_format):
    spd = saving_project_data
    expected_config = check_backup_file_format
    spd.video_configuration = expected_config["video_configuration"]
    assert spd.generate_piv() is False
    spd.bathymetry = expected_config["bathymetry"]
    assert spd.generate_piv() is False
    spd.beacons = expected_config["beacons"]
    assert spd.generate_piv() is False
    spd.filter_video = expected_config["filter_video"]
    # assert spd.generate_piv() is True

    # TODO check that the PIV is producing the expected file
    # At the moment pytest cannot access to projects folder so it is impossible to check the file
    pass


def test_save_post_process(saving_project_data, check_backup_file_format):
    spd = saving_project_data
    spd.steps_done["piv"] = True
    expected_config = check_backup_file_format
    with pytest.raises(TypeError):
        spd.save_post_process(1, ["not a string"], expected_config["post_process"]["local_points"])
    with pytest.raises(TypeError):
        spd.save_post_process(1, "not a string", "not a list")
    with pytest.raises(TypeError):
        spd.save_post_process("not a float", 1, expected_config["post_process"]["local_points"])
    assert spd.save_post_process(float(expected_config["post_process"]["river_flow"]), expected_config["post_process"]["transect_picture_path"], expected_config["post_process"]["local_points"]) is True
    spd.steps_done["post_process"] = 0
    spd.save_post_process(0.0, "", [])
    return


def test_load_project(empty_spd):
    spd = empty_spd
    with open("tests/riverapp_test/test_ressources/test_check_backup_file_format.json", "r") as f:
        default_json = json.load(f)
    with open("tests/riverapp_test/test_ressources/testing_project/testing_project.json", "w") as f:
        json.dump(default_json, f, indent=4)

    current_dir = path.dirname(path.abspath(__file__))
    current_dir = path.join(current_dir, "../test_ressources/testing_project")

    with pytest.raises(TypeError):
        spd.load_project(["Not a string"])
    with pytest.raises(FileNotFoundError):
        spd.load_project("/unknown/path")

    spd.load_project(current_dir)
    assert spd.video_configuration == default_json["video_configuration"]
    assert spd.bathymetry == default_json["bathymetry"]
    assert spd.beacons == default_json["beacons"]
    assert spd.filter_video == default_json["filter_video"]
    assert spd.cam_config["height"] == default_json["cam_config"]["height"]
    assert spd.cam_config["width"] == default_json["cam_config"]["width"]
    assert spd.cam_config["window_size"] == default_json["cam_config"]["window_size"]
    assert spd.cam_config["resolution"] == default_json["cam_config"]["resolution"]
    assert spd.cam_config["gcps"] == default_json["cam_config"]["gcps"]
    assert spd.cam_config["lens_position"] == default_json["cam_config"]["lens_position"]
    assert spd.cam_config["dist_coeffs"] == default_json["cam_config"]["dist_coeffs"]
    assert spd.cam_config["camera_matrix"] == default_json["cam_config"]["camera_matrix"]
    assert str(spd.cam_config["bbox"]) == default_json["cam_config"]["bbox"]
    assert spd.steps_done == default_json["steps_done"]
    return


def test_create_project():
    # TODO
    pass


def test_delete_project():
    # TODO
    pass
