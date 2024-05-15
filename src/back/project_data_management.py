from os import path, walk
from re import match
from zipfile import ZipFile, ZIP_DEFLATED


def download_project(project_dir: str, output_zip_path: str):
    get_project_save_file(project_dir)
    is_directory_valid(output_zip_path)

    with ZipFile(path.join(
            output_zip_path, f"{path.basename(project_dir)}.zip"),
            "w", ZIP_DEFLATED) as zipfile:
        for folder_root, _, files in walk(project_dir):
            for file in files:
                file_path = path.join(folder_root, file)
                arcname = path.relpath(file_path, start=project_dir)
                zipfile.write(file_path, arcname)


def is_directory_valid(directory: str) -> bool:
    if not match(r'^[a-zA-Z0-9-._/:\\]+$', directory):
        raise ValueError("Invalid path")

    if not path.exists(directory) or not path.isdir(directory):
        raise ValueError(f"Directory not found : {directory}")

    return True


def get_project_save_file(project_dir: str) -> str:
    print(project_dir)
    is_directory_valid(project_dir)

    save_file_path = path.join(project_dir, f"{path.basename(project_dir)}.json")

    if not path.exists(save_file_path):
        raise FileNotFoundError(f"Could not find the save file : {save_file_path}")

    return save_file_path
