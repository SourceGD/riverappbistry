from os import path
from threading import Thread
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp

from kivy.lang import Builder

from src.utils import video_to_image

Builder.load_file(path.join(path.dirname(__file__),"filter_video.kv"))

class FilterVideoMobileView(MDScreen):
    """
        Class containing the mobile view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class FilterVideoTabletView(MDScreen):
    """
        Class containing the tablet view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class FilterVideoDesktopView(MDScreen):
    """
        Class containing the desktop view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class FilterVideo(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "filter_video"
        self.mobile_view: FilterVideoMobileView = FilterVideoMobileView()
        self.tablet_view: FilterVideoTabletView = FilterVideoTabletView()
        self.desktop_view: FilterVideoDesktopView = FilterVideoDesktopView()

        self._project = MDApp.get_running_app().project
        self._need_load_from_backup: bool = True

    def _load_video_preview(self) -> None:
        image = video_to_image(self._project.video_configuration["video"], self._project.video_configuration["start_time"])
        Clock.schedule_once(lambda dt: self.children[0].ids.preview.add_widget(image))
        return
     
    def _save_filter_video(self) -> None:
        self._project.filter_video = {}
        return
    
    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(4)

    def on_enter(self, *args) -> None:
        if self._need_load_from_backup:
            Thread(target=self._load_video_preview()).start()

    def go_back(self) -> None:
        self.manager.current = "beacons"
    
    def to_piv(self) -> None:
        Thread(target=self._save_filter_video).start()
        self.manager.current = "piv"