"""
This module provides functions for calculating and visualizing river transects
using velocimetry data and bathymetry information.

The core functionality revolves around the `transect` function, which takes
video, velocimetry data, bathymetry information, and local points defining
the desired transect as input and performs the following steps:

1. **Transect Point Delimitation:**
    - Extracts camera configuration information from the velocimetry data.
    - Calculates the image coordinates (in the rectified reference frame)
      that delimit the transect based on provided local points using the
      `delimiter_points_bathy` function.

2. **Bathymetry Data Processing:**
    - Reads bathymetry data from a dictionary.
    - Utilizes the calculated transect delimiters to extract relevant bathymetry
      points that fall within the transect boundaries using the
      `all_points_bathy` function.

3. **Transect Plot Generation:**
    - Calls the `transect_plot` function to create a plot visualizing the
      transect line overlaid on the video frame (in both local and camera
      projections) with color representing velocity information.
    - The `bathy_file["surface_coefficient"]` is used as a potential
      velocity correction factor during plotting.

4. **River Flow Calculation:**
    - Extracts the river flow value from the processed data using the
      `get_river_flow` method (functionality not detailed here).

Functions
---------

* `delimiter_points_bathy(cam_config, local_points)`:
    - Calculates image coordinates (in the rectified reference frame) for the
      transect delimiters based on camera configuration and provided local points.

* `all_points_bathy(bathy, bathy_delimeters, ds)`:
    - Calculates transect velocities across all bathymetry data points within
      specified delimiters using the velocimetry data in the provided xarray dataset.

* `transect_plot(ds_points, video, ds, directory, v_corr)`:
    - Generates a plot visualizing the river transect with overlaid velocimetry
      information in both local and camera projections.

* `transect(ds, video, directory, bathy_file, local_points)`:
    - The main function that performs the complete workflow for calculating
      and visualizing a river transect, returning the calculated river flow value.

External Dependencies
---------------------

- OpenCV (`cv2`) for perspective transformation (used by `delimiter_points_bathy`).
- pandas (`pd`) for data manipulation (used by `all_points_bathy`).
- Matplotlib (`plt`) for plotting (used by `transect_plot`).

Notes
-----

- This module assumes specific data structures for the velocimetry data (xarray
  dataset with a `velocimetry` variable) and bathymetry data (dictionary with
  keys "x" and "y" for horizontal coordinates).

"""

# File from older master thesis on pyorc_main
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


def delimiter_points_bathy(cam_config, local_points):
    """
    Delimit Transect Points using Camera Configuration

    This function calculates the image coordinates (in the rectified reference frame)
    that delimit the river transect based on provided local points and camera configuration.

    Parameters
    ----------

    - cam_config `CameraConfig`:
        An object containing the camera configuration
        information. This object is expected to have attributes named `gcps` which is a
        dictionary containing source and destination Ground Control Points (GCPs) used
        for camera calibration.

    - list `local_points`:
        A list containing two local points (2D coordinates) in the image plane
        that define the desired transect boundaries.
        These points are assumed to be provided in pixel coordinates.

    Returns
    -------

    - `list` of `list`:
        A list containing two elements, each being a list of length
        two representing the image coordinates (in the rectified reference frame)
        corresponding to the provided local points.

    Notes
    -----

    - This function relies on the OpenCV library (`cv2`) for perspective transformation.
    - The camera calibration information from `cam_config` is used to transform the
      provided local points from the image plane to the rectified reference frame.
    - This function assumes the `cam_config` object is valid and has the expected
      attributes.
    """

    # two points that delimit the transect for the VGC1 example
    #local_points = [[600, 1080], [2800, 1080]]
    # local_points = [[600, 1200], [2800, 1200]] # Petit bocq 90 degrees
    # local_points = [[494, 427], [1391, 465]]
    # convert local_points to the orthorectified referential
    m = np.array(cv2.getPerspectiveTransform(np.float32(cam_config.gcps['src']),
                                             np.float32(cam_config.gcps['dst'])))
    ret = cv2.perspectiveTransform(np.float32([local_points]), m)[0]

    return ret


def all_points_bathy(bathy, bathy_delimeters, ds):
    """
    Calculates Transect Velocities using Bathymetry and Delimiters

    This function calculates the transect velocities across all bathymetry data points
    within the specified delimiters.

    Parameters
    ----------

    - dict `bathy`:
        A dictionary containing bathymetry data. This dictionary
        is expected to have keys named "x" and "y" corresponding to the horizontal
        coordinates (assumed to be in meters) of each bathymetry point.

    - tuple of `list `bathy_delimeters`:
        A tuple containing two lists, each
        representing a delimiter point in the rectified reference frame. The first
        element defines the starting point and the second element defines the ending
        point of the transect. Each list is expected to have a length of two,
        representing the x and y coordinates of the point.

    - xarray.Dataset `ds`:
        An xarray dataset containing the velocimetry data.
        It's assumed that the dataset has a variable named `velocimetry` that provides
        the velocity information.

    Returns
    -------

    - `xarray.DataArray`:
        An xarray DataArray containing the calculated transect
        velocities along the specified transect line. The DataArray will have the same
        dimensions as the original `velocimetry` variable in the provided `ds` but
        with potentially different values along the transect line.

    Notes
    -----

    - This function uses pandas (`pd`) to convert the bathymetry dictionary to a
      DataFrame for easier manipulation.
    - The function interpolates points along a line defined by the provided delimiters.
      These interpolated points are then used to extract the corresponding velocities
      from the `velocimetry` variable in the `ds` using the `get_transect` method
      (functionality not detailed here).
    """

    bathy = pd.DataFrame.from_dict(bathy)
    x_bath = bathy["x"].values
    z_bath = bathy["y"].values

    c1, c2 = bathy_delimeters

    # interpolate points between both bathy_delimeters points
    x, y, z = np.empty((3, len(x_bath)))
    for idx, xb in enumerate(x_bath):
        lambd = xb / np.amax(x_bath)
        x[idx] = c1[0] + lambd * np.abs(c2[0] - c1[0])
        y[idx] = c1[1] + lambd * np.abs(c2[1] - c1[1])
        z[idx] = z_bath[idx]

    return ds.velocimetry.get_transect(x, y, z, rolling=4)


def transect_plot(ds_points, video, ds, directory, v_corr):
    """
    Generates Transect Plot with Velocity Information

    This function creates a plot visualizing the river transect with overlaid
    velocimetry data. It utilizes two different projections (local and camera)
    to display the information.

    Parameters
    ----------

    - xarray.Dataset `ds_points`:
        An xarray dataset containing the transect points.

    - pyorc.Video `video`:
        An object representing the video data. It's assumed
        this object has methods to access video frames.

    - xarray.Dataset `ds`:
        An xarray dataset containing the velocimetry data.

    - str `directory` :
        The directory path where the generated plot image
        will be saved.

    - float, optional `v_corr`:
        A velocity correction factor (default is 0.9).

    Returns
    -------

    - `xarray.DataArray`:
        The original `ds_points` dataset with
        additional information such as river discharge.

    Notes
    -----

    - This function utilizes Matplotlib (`plt`) for generating the plot.
    - The `get_q` method (from `transect` attribute of `ds_points`) is used to
      calculate discharge from the transect points with optional velocity correction.
      Missing values are filled using logarithmic interpolation ("log_interp").
    - The generated plot is saved as "plot_transect.jpg" in the specified directory.
    """

    ds_points_q = ds_points.transect.get_q(v_corr=v_corr, fill_method="log_interp")
    ax = plt.axes()
    ds_points_q["v_eff"].isel(quantile=2).plot(ax=ax, label="q")
    plt.legend()
    plt.grid()

    #################### plot velocimetry point results in local projection ########
    norm = Normalize(vmin=0, vmax=0.6, clip=False)
    ds_mean = ds.mean(dim="time", keep_attrs=True)
    p = video.get_frames(method="rgb").frames.project()[0].frames.plot(mode="local")

    ds_points_q.isel(quantile=2).transect.plot(
        ax=p.axes,
        mode="local",
        cmap="rainbow",
        scale=10,
        width=0.003,
        norm=norm,
        add_colorbar=True,
    )

    # to ensure streamplot understands the directions correctly, all values must
    # be flipped upside down and up-down velocities become down-up velocities.
    ds_mean.velocimetry.plot.streamplot(
        ax=p.axes,
        mode="local",
        density=3.,
        minlength=0.05,
        linewidth_scale=2,
        cmap="rainbow",
        norm=norm,
        add_colorbar=True
    )

    ########### extract mean velocity and plot in camera projection ###########
    # plot the rgb frame first. We use the "camera" mode to plot the camera perspective.
    norm = Normalize(vmin=0., vmax=0.8, clip=False)

    p = video.get_frames(method="rgb")[0].frames.plot(mode="camera")

    ds.mean(dim="time", keep_attrs=True).velocimetry.plot(
        ax=p.axes,
        mode="camera",
        cmap="rainbow",
        scale=200,
        width=0.001,
        alpha=0.3,
        norm=norm,
    )

    # plot velocimetry point results in camera projection
    ds_points_q.isel(quantile=2).transect.plot(
        ax=p.axes,
        mode="camera",
        cmap="rainbow",
        scale=100,
        width=0.003,
        norm=norm,
    )
    # store figure in a JPEG
    p.axes.figure.savefig(directory + "plot_transect.jpg", dpi=200)

    return ds_points_q


def transect(ds, video, directory, bathy_file, local_points):
    """
    Calculates and Plots River Transect Flow

    This function performs the complete workflow for calculating and visualizing
    a river transect:

    1. **Transect Point Delimitation:**
        - Extracts camera configuration information from the velocimetry variable
          in `ds`.
        - Calculates the image coordinates (in the rectified reference frame)
          that delimit the transect based on provided local points using the
          `delimiter_points_bathy` function.

    2. **Bathymetry Data Processing:**
        - Reads bathymetry data from the provided `bathy_file`.
        - Utilizes the calculated `bathy_delimiters` to extract relevant bathymetry
          points that fall within the transect boundaries using the
          `all_points_bathy` function.

    3. **Transect Plot Generation:**
        - Calls the `transect_plot` function to create a plot visualizing the
          transect line overlaid on the video frame (in both local and camera
          projections) with color representing velocity information.
        - The `bathy_file["surface_coefficient"]` is used as a potential
          velocity correction factor during plotting.

    4. **River Flow Calculation:**
        - Extracts the river flow value from the processed `ds_points_q` dataset
          using the `get_river_flow` method (functionality not detailed here).

    Parameters
    ----------

    - xarray.Dataset `ds`:
        An xarray dataset containing the velocimetry data.

    - pyorc.Video `video`:
        An object representing the video data. It's assumed
        this object has a `camera_config` attribute containing camera configuration
        information.

    - str `directory`:
        The directory path where the generated transect plot
        image will be saved.

    - dict `bathy_file`:
        A dictionary containing bathymetry data (assumed
        to have a structure similar to the output of `all_points_bathy`).

    - list of list `local_points`:
        A list containing two local points
        (2D coordinates) in the image plane that define the desired transect
        boundaries.

    Returns
    -------

    - `list`:
        The calculated river flow value for the specified transect in the form of a
        list of 5 quantiles.

    Notes
    -----

    - This function relies on several helper functions:
        - `delimiter_points_bathy` for calculating transect delimiters.
        - `all_points_bathy` for processing bathymetry data.
        - `transect_plot` for generating the transect visualization.
    """
    # video.camera_config = ds.velocimetry.camera_config
    bathy_delimiters = delimiter_points_bathy(video.camera_config, local_points)

    ds_points = all_points_bathy(bathy_file, bathy_delimiters, ds)
    ds_points_q = transect_plot(ds_points, video, ds, directory, bathy_file["surface_coefficient"])

    # print discharge for this transect
    ds_points_q.transect.get_river_flow()

    return ds_points_q["river_flow"]
