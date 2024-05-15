import pytest

from src.back.project_data_management import is_directory_valid, get_project_save_file, download_project
from back_fixtures import testing_project_path


def test_download_project(testing_project_path):
    with pytest.raises(ValueError):
        download_project("", "")
    with pytest.raises(ValueError):
        download_project("/unknown/path", "")
    with pytest.raises(ValueError):
        download_project("/unknown/path", "/unknown/path")

    pass


def test_is_directory_valid(testing_project_path):
    with pytest.raises(ValueError):
        is_directory_valid("")
    with pytest.raises(ValueError):
        is_directory_valid("/unknown/path")
    assert is_directory_valid(testing_project_path) is True
    return


def test_get_project_save_file(testing_project_path):
    with pytest.raises(FileNotFoundError):
        get_project_save_file("tests/riverapp_test/test_ressources/empty_directory/")
    assert get_project_save_file(testing_project_path) == f"{testing_project_path}/testing_project.json"
    return
