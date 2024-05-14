import copy
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt


# File from debraye thesis
def apply_mask(ds):
    # copy ds object and apply mask on it
    # here it is just an example of a series of mask to apply
    # it is advised to first start with mask applied on individual values (minmax, corr),
    # then gradually move to masks that require analysis of all values in time (variance, count)
    # spatial masks
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
    # plt.show()


# here the idea is that the user can choose which filter he wants to apply
# after clicking on a button, he can observe the resulting plot and decide
# whether to continue the process or to change the masking of PIV result
# todo add interface to select filters the users wants to add and see the resulting plot
def mask_and_plot(directory, ds, video):
    video.camera_config = ds.velocimetry.camera_config
    da_rgb_proj = video.get_frames(method="rgb").frames.project()
    mask = apply_mask(ds)
    plot_result(da_rgb_proj, mask)

    # when the user is happy with the masking result store it
    mask.velocimetry.set_encoding()
    mask.to_netcdf(directory + "piv_masked.nc")
