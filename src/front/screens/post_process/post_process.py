from os import path
from threading import Thread, Event
from pprint import pprint

from kivy.clock import Clock
from kivy.uix.label import Label
from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp
from kivy.uix.image import Image


from kivy.lang import Builder

from libs import pyorc
from src.back import transect, mask_and_plot, saving_project_data
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
        app = MDApp.get_running_app()
        video = self.set_video()
        river_flow = self.process_and_plot_transects(video)
        self.deactivate_display_button()
        self.load_image()
        avg_flow = self.update_river_flow_label(river_flow)
        self._project.save_post_process(avg_flow, self._project._backup_file.strip(self._project.project_name + ".json") + "plot_transect.jpg")

        return

    def deactivate_display_button(self, *args) -> None:
        self.children[0].ids.display_transects_button.disabled = True
        self.children[0].ids.display_transects_button.opacity = 0


    def go_back(self):
        print("go back to projects")
        print("=========================================")
        self.manager.current = "projects"

    def load_image(self):
        image = Image(source=(self._project._backup_file.strip(self._project.project_name + ".json") + "plot_transect.jpg"), fit_mode="contain")
        Clock.schedule_once(lambda dt: self.children[0].ids.transects_layout.add_widget(image))
        return

    def update_river_flow_label(self, river_flow) -> float:
        avg = str(round(float(river_flow.mean()) * -1, 2))
        label = Label(text="Calculated river flow is " + avg + "m³/s", color=(0, 0, 0, 1))
        Clock.schedule_once(lambda dt: self.children[0].ids.river_flow_label.add_widget(label))
        return avg

    def set_video(self):
        start_frame = int(5 * self._project._video_configuration['start_time'])
        end_frame = int(5 * self._project._video_configuration['end_time'])
        video = pyorc.Video(self._project._video_configuration['video'], start_frame=start_frame, end_frame=end_frame)
        video.camera_config = self._project.cam_config
        return video

    def process_and_plot_transects(self, video):
        piv_path = self._project._backup_file.strip(self._project.project_name + ".json") + "piv.nc"
        dataset = xr.open_dataset(piv_path)
        mask_and_plot(self._project._backup_file.strip(self._project.project_name + ".json"), dataset, video)
        masked_dataset = xr.open_dataset(
        self._project._backup_file.strip(self._project.project_name + ".json") + "piv_masked.nc")
        river_flow = transect(masked_dataset, video, self._project._backup_file.strip(self._project.project_name + ".json"),
        self._project._bathymetry)
        return river_flow