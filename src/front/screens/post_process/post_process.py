from os import path
from threading import Thread, Event
from pprint import pprint
from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp

from kivy.lang import Builder

from libs import pyorc
from src.back import transect, mask_and_plot
import xarray as xr


Builder.load_file(path.join(path.dirname(__file__), "post_process.kv"))


class PostProcessMobileView(MDScreen):
    """
        Class containing the mobile view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """


class PostProcessTabletView(MDScreen):
    """
        Class containing the tablet view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """


class PostProcessDesktopView(MDScreen):
    """
        Class containing the desktop view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """


class PostProcess(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "post_process"
        self.mobile_view: PostProcessMobileView = PostProcessMobileView()
        self.tablet_view: PostProcessTabletView = PostProcessTabletView()
        self.desktop_view: PostProcessDesktopView = PostProcessDesktopView()

        self._project = MDApp.get_running_app().project

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(3)
        print("on_pre_enter post processing")

    def on_enter(self, *args) -> None:
        print("on_enter post processing")
        return

    def on_leave(self, *args) -> None:
        print("on_leave post processing")
        return

    def on_button_press(self, *args) -> None:
        start_frame = int(5 * self._project._video_configuration['start_time'])
        end_frame = int(5 * self._project._video_configuration['end_time'])
        video = pyorc.Video(self._project._video_configuration['video'], start_frame=start_frame, end_frame=end_frame)
        video.camera_config = self._project.cam_config
        print("on_button_press post processing")
        obj_vars = vars(self._project)
        pprint(obj_vars)
        piv_path = self._project._backup_file.strip(self._project.project_name+".json") + "piv.nc"
        dataset = xr.open_dataset(piv_path)
        mask_and_plot(self._project._backup_file.strip(self._project.project_name+".json"), dataset, video)

        masked_dataset = xr.open_dataset(self._project._backup_file.strip(self._project.project_name+".json") + "piv_masked.nc")

        bathy_path = self._project._video_configuration['video'].strip("") + "bathy_format_riverApp.txt"
        transect(masked_dataset, video, self._project._backup_file.strip(self._project.project_name+".json"), "/media/andreas/LaCie Andreas/Mémoire/riverapp/examples/riverapp_examples/VGC1/bathy_format_riverApp.txt")
        return
