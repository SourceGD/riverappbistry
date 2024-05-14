# File from older master thesis on pyorc_main
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


# todo add user input interface to get the two points, defining the edge points of the transect,
#  one on each side of the river
def delimiter_points_bathy(cam_config, local_points):
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


# todo add user input to precise the factor correlation of how much varies
#  the velocity with the depth (v_corr variable)
def transect_plot(ds_points, video, ds, directory, v_corr):
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
    # video.camera_config = ds.velocimetry.camera_config
    bathy_delimiters = delimiter_points_bathy(video.camera_config, local_points)

    ds_points = all_points_bathy(bathy_file, bathy_delimiters, ds)
    ds_points_q = transect_plot(ds_points, video, ds, directory, bathy_file["surface_coefficient"])

    # print discharge for this transect
    ds_points_q.transect.get_river_flow()

    return ds_points_q["river_flow"]
