""" Module for masking and visualizing velocimetry data.

    This module provides functions for applying masking techniques to velocimetry data and
    visualizing the results. It aims to assist in identifying and removing erroneous data points
    to improve data quality.

    Functions
    ---------
    - `apply_mask(ds)`: Applies a series of masking techniques to a velocimetry dataset (`ds`) to
      identify and remove potentially erroneous data points.

    - `plot_result(da_rgb_proj, mask)`: Visualizes the masked velocimetry data overlaid on the first
      RGB frame of a projected dataset.

    - `mask_and_plot(directory, ds, video)`: Iteratively masks and visualizes velocimetry data,
      allowing user interaction to refine masking and save results.
"""

import copy
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt


# File from debray thesis
def apply_mask(ds):
    """
        Applies a series of masks to a velocimetry dataset (`ds`) to identify and remove potentially
        erroneous data points.

        This function iteratively applies various masking techniques to create a new dataset
        with improved data quality. It's recommended to start with masks targeting individual values
        (e.g., min/max, correlation) and gradually progress to masks requiring analysis of all
        values across time (e.g., variance, count).

        Parameters:
        -----------
        xarray.Dataset ds :
            The velocimetry dataset to be masked. It's assumed to contain a 'velocimetry' data
            variable with appropriate dimensions (e.g., time, space).

        Returns:
        --------
        xarray.Dataset:
            A new dataset (`ds_mask`) with the same structure as the input dataset, where erroneous
            data points have been masked out (replaced with NaNs).

        Raises:
        -------
        ValueError:
            If the input dataset (`ds`) does not contain a 'velocimetry' data variable.

        Notes:
        -------
        * The masking techniques employed within this function are primarily focused on identifying
          outliers and inconsistencies in velocimetry data.

        * Consider customizing the mask parameters
          (e.g., correlation threshold, window size for rolling mean) based on your specific dataset
          and data quality requirements.

        Examples
        --------

        >>> ds_masked = apply_mask(ds.copy())  # Create a copy to avoid modifying original data

        """
    ds_mask = copy.deepcopy(ds)
    ds_mask.velocimetry.mask.corr(inplace=True)
    ds_mask.velocimetry.mask.minmax(inplace=True)
    ds_mask.velocimetry.mask.rolling(inplace=True)
    ds_mask.velocimetry.mask.outliers(inplace=True)
    ds_mask.velocimetry.mask.variance(inplace=True)
    ds_mask.velocimetry.mask.angle(angle_tolerance=0.5 * np.pi)
    ds_mask.velocimetry.mask.count(inplace=True)
    ds_mask.velocimetry.mask.window_mean(wdw=2, inplace=True, tolerance=0.5, reduce_time=True)

    return ds_mask


def plot_result(da_rgb_proj, mask):
    """
        Visualizes the masked velocimetry data overlaid on the first RGB frame of a projected
        dataset.

        This function creates a combined visualization of the velocimetry data, highlighting areas
        masked out due to potential errors. It takes two xarray DataArrays as input:

        - `da_rgb_proj`: An xarray DataArray representing the first RGB frame from a projected
          dataset. It's assumed to have dimensions (frames, height, width, channels) and contain RGB
          color information.

        - `mask`: An xarray DataArray representing the masked velocimetry data. It's assumed to have
          dimensions compatible with the velocimetry data in `da_rgb_proj`,
          with values indicating masked (NaN) and unmasked regions.

        The function performs the following steps:

        1. Plots the first RGB frame from `da_rgb_proj`.

        2. Calculates the mean of the `mask` DataArray along the temporal dimension (`"time"`),
        preserving attributes using `keep_attrs=True`.

        3. Overlays the masked velocimetry data from `mask.velocimetry` on top of the existing plot
        using the `pyorc.velocimetry.plot` method. This method offers various customization options
        for the visualization.

            - `ax=p.axes`: Specifies the existing axes from the RGB frame plot for overlaying.

            - `alpha=0.4`: Sets the transparency of the masked velocimetry layer
              (0.0 fully transparent, 1.0 fully opaque).

            - `cmap="rainbow"`: Selects the colormap for visualizing the masked regions
              (customizable).

            - `scale=20`: Scales the magnitude of the velocity vectors (adjust based on your data).

            - `width=0.0015`: Sets the width of the velocity vectors
              (adjust based on desired visibility).

            - `norm=Normalize(vmax=0.6, clip=False)`: Normalizes the colormap values
              (adjust `vmax` as needed).

            - `add_colorbar=True`: Adds a colorbar to the plot for interpreting masked region
              intensities.

        4. **(Optional)** Displays the plot using `plt.show()` (uncomment only during development).

        Parameters:
        -----------
        da_rgb_proj : `xarray.DataArray`
            An xarray DataArray representing the first RGB frame from a projected dataset.
            It's assumed to have dimensions (frames, height, width, channels) and contain RGB color
            information.
        mask : `xarray.DataArray`
            An xarray DataArray representing the masked velocimetry data.
            It's assumed to have dimensions compatible with the velocimetry data in `da_rgb_proj`,
            with values indicating masked (NaN) and unmasked regions.

        Returns:
        --------
        None

        Notes:
        -------
        * This function relies on the `pyorc` library for velocimetry plotting functionalities.
        * Ensure `da_rgb_proj` and `mask` have compatible spatial dimensions for overlaying.
        * Experiment with the `pyorc.velocimetry.plot` method's arguments to customize the
          visualization as needed for your specific data.

    """

    # first rgb frame
    p = da_rgb_proj[0].frames.plot()

    # mean on temporal axis
    mask = mask.mean(dim="time", keep_attrs=True)

    # add on top the masked velocimetry
    mask.velocimetry.plot(
        ax=p.axes,
        alpha=0.4,
        cmap="rainbow",
        scale=20,
        width=0.0015,
        norm=Normalize(vmax=0.6, clip=False),
        add_colorbar=True
    )
    # UNCOMMENT ONLY WHEN DEVELOPING
    plt.show()


# here the idea is that the user can choose which filter he wants to apply
# after clicking on a button, he can observe the resulting plot and decide
# whether to continue the process or to change the masking of PIV result
# todo add interface to select filters the users wants to add and see the resulting plot
def mask_and_plot(directory, ds, video):
    """
        Iteratively masks and visualizes velocimetry data, allowing user interaction to
        refine masking and save results.

        This function provides a user-interactive workflow for masking velocimetry data.
        It takes three arguments:

        - `directory`: (str) The directory path where the masked data will be saved.
        - `ds`: (xarray.Dataset) The velocimetry dataset containing the data to be masked.
        - `video`: (pyorc Video) A video object representing the data source for visualization.

        The function performs the following steps:

        1. Sets the camera configuration of the `video` object to match that of the velocimetry
        data in `ds.velocimetry.camera_config` (ensures consistent visualization).
        2. Extracts the first RGB frame from the video using `video.get_frames(method="rgb")`
        and projects it using `frames.project()`. This creates a projected RGB DataArray
        (`da_rgb_proj`) for visualization.
        3. Applies masking to the velocimetry data in `ds` using the `apply_mask` function.
        The resulting masked data is stored in the `mask` DataArray.
        4. Visualizes the masked velocimetry data overlaid on the first RGB frame using the
        `plot_result` function. This allows the user to see the impact of masking on the data.
        5. Set encoding for the masked velocimetry data and save it to a NetCDF file in the project
        folder

        Parameters
        ----------
        directory : str
            The directory path where the masked data will be saved.
        ds : xarray.Dataset
            The velocimetry dataset containing the data to be masked.
        video : pyorc Video
            A video object representing the data source for visualization.

        Returns
        -------
        None

        Notes
        -----

        - This function relies on the `pyorc` library for video and velocimetry functionalities.
        - The user interface for selecting filters and saving results is yet to be implemented.

        Examples
        --------

        >>> mask_and_plot(directory, ds, video)
    """

    video.camera_config = ds.velocimetry.camera_config
    da_rgb_proj = video.get_frames(method="rgb").frames.project()
    mask = apply_mask(ds)
    plot_result(da_rgb_proj, mask)

    # when the user is happy with the masking result store it
    mask.velocimetry.set_encoding()
    mask.to_netcdf(directory + "piv_masked.nc")
