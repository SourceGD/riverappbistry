from os import path

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager

from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"bathymetry.kv"))

class BathymetryMobileView(MDScreen):
    """
        Class containing the mobile view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class BathymetryTabletView(MDScreen):
    """
        Class containing the tablet view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class BathymetryDesktopView(MDScreen):
    """
        Class containing the desktop view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class Bathymetry(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "bathymetry"
        self.mobile_view: BathymetryMobileView = BathymetryMobileView()
        self.tablet_view: BathymetryTabletView = BathymetryTabletView()
        self.desktop_view: BathymetryDesktopView = BathymetryDesktopView()

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(6)