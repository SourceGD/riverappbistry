import pytest

from back_fixtures import saving_project_data, all_video_configs, all_bathy_configs


def test_video_configuration_setter(saving_project_data, all_video_configs):
    spd = saving_project_data
    with pytest.raises(FileExistsError):
        spd.video_configuration = all_video_configs["bad_video_config"]
    with pytest.raises(TypeError):
        spd.video_configuration = all_video_configs["bad_start_time_format_config"]
    with pytest.raises(TypeError):
        spd.video_configuration = all_video_configs["bad_end_time_format_config"]
    with pytest.raises(TypeError):
        spd.video_configuration = all_video_configs["bad_frequency_format_config"]
    with pytest.raises(ValueError):
        spd.video_configuration = all_video_configs["bad_start_time_value"]
    with pytest.raises(ValueError):
        spd.video_configuration = all_video_configs["bad_end_time_value"]
    with pytest.raises(ValueError):
        spd.video_configuration = all_video_configs["bad_frequency_value"]
    with pytest.raises(ValueError):
        spd.video_configuration = all_video_configs["greater_start_time_than_end_time"]

    spd.video_configuration = all_video_configs["good_video_config"]
    assert spd.video_configuration == all_video_configs["good_video_config"]
    return


def test_bathymetry_setter(saving_project_data, all_bathy_configs):
    spd = saving_project_data
    with pytest.raises(TypeError):
        spd.bathymetry = all_bathy_configs["bad_bathy_format"]
    with pytest.raises(ValueError):
        spd.bathymetry = all_bathy_configs["bad_bathy_values_count"]
    with pytest.raises(ValueError):
        spd.bathymetry = all_bathy_configs["bad_bathy_values"]
    with pytest.raises(ValueError):
        spd.bathymetry = all_bathy_configs["bad_bathy_water_level"]

    spd.bathymetry = all_bathy_configs["good_bathy"]
    assert spd.bathymetry == all_bathy_configs["good_bathy"]
    return


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



