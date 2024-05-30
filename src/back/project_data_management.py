"""
File and Archiving Utilities

This module provides functions for archiving and managing project directories.

Functions
---------

* `download_project(project_dir: str, output_zip_path: str)`:
    - Creates a ZIP archive of a project directory.
    - Validates input paths and handles potential errors.

* `is_directory_valid(directory: str) -> bool`:
    - Validates a directory path for existence and valid characters.
    - Raises exceptions for invalid paths.

* `get_project_save_file(project_dir: str) -> str` (Optional):
    - Potentially retrieves or validates a project's save file path.
    - The specific behavior depends on the implementation.

Notes
-----

- This module relies on the following external libraries:
    - `os`
    - `re`
    - `zipfile`
"""

from os import path, walk
from re import match
from zipfile import ZipFile, ZIP_DEFLATED


def download_project(project_dir: str, output_zip_path: str):
    """
        Downloads a project directory by creating a compressed archive (ZIP file).

        This function takes two arguments:

        - `project_dir` (str): The path to the project directory to be downloaded (archived).
        - `output_zip_path` (str): The path where the compressed archive (ZIP file) will be saved.

        The function performs the following steps:

        1. Validates the project directory using `get_project_save_file(project_dir)`. This function
            likely checks if the directory exists and is accessible (implementation details depend
            on your specific `get_project_save_file` function).

        2. Validates the output ZIP path using `is_directory_valid(output_zip_path)`.
            This function likely checks if the target directory exists and has write permissions
            (implementation details depend on your specific `is_directory_valid` function).

        3. Creates a ZIP archive using `ZipFile` with the specified output path and compression
            method (ZIP_DEFLATED). The archive filename is constructed by combining the project
            directory's base name with '.zip' and placed within the `output_zip_path`.

        4. Iterates through the project directory structure using `os.walk(project_dir)`.
            - For each file encountered:
                - Constructs the full file path (`file_path`).

                - Calculates the relative path within the project directory (`arcname`) using
                  `path.relpath`. This ensures the files are stored within the archive structure
                  reflecting their original location in the project directory.

                - Adds the file to the ZIP archive using `zipfile.write(file_path, arcname)`.

        Returns
        -------

        - None

        Raises
        ------

        `OSError` :
            or related exceptions in case of file system errors during ZIP creation or file access.

        Notes
        -----

        - This function relies on the `os` module for file system operations and
          path manipulation.

        Examples
        --------

        >>> download_project(project_dir, output_zip_path)
        """
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
    """
        Validates a directory path, checking for validity and existence.

        This function verifies whether a given path represents a valid and accessible directory.
        It performs the following checks:

        1. **Regular Expression Match:** The function uses a regular expression
        (`r'^[a-zA-Z0-9-._/:\\]+$'`) to ensure the directory path contains only allowed characters
        (alphanumeric, hyphens, underscores, periods, slashes, colons, and backslashes).
        This helps prevent potential issues with invalid path components.

        2. **Directory Existence and Type:** It uses `path.exists` and `path.isdir`
        from the `os.path` module to verify if the path points to an existing directory.
        If not, it raises a `ValueError` indicating the directory cannot be found.

        Parameters
        ----------

        - str `directory` :
            The path to the directory to be validated.

        Returns
        -------

        - `bool`:
            True if the directory path is valid and exists, False otherwise
            (though the function always raises an exception on invalidity).

        Raises
        ------

        - `ValueError`:
            Raised with an informative message if the directory path is invalid
            (due to character restrictions or non-existence).

        Notes
        -----

        - This function relies on the `os.path` module for path validation and checks.

        Examples
        --------

        >>> is_directory_valid(directory)
    """
    if not match(r'^[a-zA-Z0-9-._/:\\]+$', directory):
        raise ValueError("Invalid path")

    if not path.exists(directory) or not path.isdir(directory):
        raise ValueError(f"Directory not found : {directory}")

    return True


def get_project_save_file(project_dir: str) -> str:
    """
        Retrieves (or potentially validates) a project's save file path.

        This function's exact behavior depends on its implementation details, but it likely performs
         the following actions:

        1. **Validates Directory Path:** It calls `is_directory_valid(project_dir)` to ensure the
            provided path points to a valid and accessible directory.

        2. **Constructs Save File Path:** The function constructs a potential save file path by
            joining the `project_dir` with the base name of the directory appended with '.json'.
            This suggests the function might be looking for a JSON file associated with the project.

        3. **Checks Save File Existence:** It uses `path.exists` to verify if the constructed save
            file path actually exists. If not, it raises a `FileNotFoundError` indicating the file could
            not be found.

        Parameters
        ----------

        - `project_dir` (str): The path to the project directory.

        Returns
        -------

        - `str`: The path to the project's save file (if it exists and is valid).

        Raises
        ------

        - `ValueError`:
            Potentially raised by `is_directory_valid` if the project directory path
            is invalid.
        - `FileNotFoundError`:
            Raised if the constructed save file path does not exist.

        Notes
        -----

        - The specific behavior and purpose of this function might require clarification based on
          its actual implementation.
        - This function relies on the `os.path` module for path manipulation and existence checks.

        Examples
        --------

        >>> save_file_path = get_project_save_file(project_dir)
        """
    print(project_dir)
    is_directory_valid(project_dir)

    save_file_path = path.join(project_dir, f"{path.basename(project_dir)}.json")

    if not path.exists(save_file_path):
        raise FileNotFoundError(f"Could not find the save file : {save_file_path}")

    return save_file_path
