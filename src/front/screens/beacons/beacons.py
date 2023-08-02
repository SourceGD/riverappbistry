from os import path

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp

from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"beacons.kv"))

class BeaconsMobileView(MDScreen):
    """
        Class containing the mobile view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class BeaconsTabletView(MDScreen):
    """
        Class containing the tablet view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class BeaconsDesktopView(MDScreen):
    """
        Class containing the desktop view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class Beacons(MDResponsiveLayout,MDScreen):
    
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "beacons"
        self.mobile_view: BeaconsMobileView = BeaconsMobileView()
        self.tablet_view: BeaconsTabletView = BeaconsTabletView()
        self.desktop_view: BeaconsDesktopView = BeaconsDesktopView()

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(5)

    def go_back(self) -> None:
        self.manager.current = "bathymetry"