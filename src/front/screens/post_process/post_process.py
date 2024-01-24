from os import path
from threading import Thread, Event

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp

from kivy.lang import Builder

from src.front.components.dialogs import ConfirmAction

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
