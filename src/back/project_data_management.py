from os import path, mkdir
from shutil import rmtree
from json import dump, load
from re import match
from definitions import PROJECT_DEFAULT_STRUCT

def create_project(project_name: str, save_directory: str) -> None:

    if not match(r'^[a-zA-Z0-9-_]+$', project_name):
        raise ValueError(f"Invalid folder name. Use only letters, numbers, hyphens and underscores : {project_name}")
    
    if not match(r'^[a-zA-Z0-9-_/:\\]+$', save_directory):
        raise ValueError(f"Invalid save_directory path")
    
    folder_path = path.join(save_directory, project_name)

    if path.exists(folder_path):
        raise FileExistsError(f"{project_name} already exists")
    
    mkdir(folder_path)

    with open(path.join(folder_path, f"{project_name}.json"), "w") as json_file:
        data = PROJECT_DEFAULT_STRUCT
        data["project_name"] = project_name
        dump(data, json_file, indent=4)

    return 

def delete_projects(project_directory: str) -> None:
    check_path(project_directory)

    rmtree(project_directory)

    return


def save_project(project_directory: str, json_data: dict) -> None:
    
    save_file = check_path(project_directory)
    check_data_format(PROJECT_DEFAULT_STRUCT, json_data)

    with open(save_file, "w") as json_file:
        dump(json_data, json_file, indent=4)

    return 

def load_project(project_directory: str) -> dict :

    save_file = check_path(project_directory)
    
    with open(save_file, "r") as json_file:
        data = load(json_file)

    return data

def check_path(folder_path: str) -> str:

    if not match(r'^[a-zA-Z0-9-_/:\\]+$', folder_path):
        raise ValueError(f"Invalid path")
    
    if not path.exists(folder_path) or not path.isdir(folder_path):
        raise ValueError(f"Directory not found : {path}")
    
    save_file_path = path.join(folder_path, f"{path.basename(folder_path)}.json")

    if not path.exists(save_file_path):
        raise FileNotFoundError(f"Could not find the save file : {save_file_path}")
    
    return save_file_path

def check_data_format(data_format: dict, data: dict) -> None:
    if not isinstance(data_format, dict):
        raise TypeError(f"data_format should be a dict : {data_format}")
    
    if not isinstance(data, dict):
        raise TypeError(f"data should be a dict : {data}")
    
    keys_format = set(data_format.keys())
    keys_data = set(data.keys())

    if keys_format != keys_data:
        raise ValueError(f"The data format doesn't respect the wanted format")
    
    for key in keys_format:
        if isinstance(data_format[key], dict) and isinstance(data[key], dict):
            check_data_format(data_format[key], data[key])
        
        elif (isinstance(data_format[key], dict) and not isinstance(data[key], dict)) or not isinstance(data_format[key], dict) and isinstance(data[key], dict):
            raise ValueError(f"The data format doesn't respect the wanted format")
        
    return
    
    
