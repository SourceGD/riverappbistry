from dask.diagnostics import ProgressBar


def process_piv(directory, video):

    # project the frames with orthorectification and process PIV analysis

    # extracting gray scaled frames
    da = video.get_frames()
    # normalize to add contrast
    da_norm = da.frames.normalize()
    # project the frames into orthorectified plane
    da_norm_proj = da_norm.frames.project()
    # PIV process
    piv = da_norm_proj.frames.get_piv()

    # store in file to reuse later and avoid the process time execution
    delayed_obj = piv.to_netcdf(directory + "piv.nc", compute=False)
    with ProgressBar():
        results = delayed_obj.compute()
