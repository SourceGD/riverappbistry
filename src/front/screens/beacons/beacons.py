from os import path
from threading import Thread
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp

from kivy.lang import Builder

from src.utils import video_to_image
from src.front.components.widget import ShapeOnImage
from src.back import beacons_detection

Builder.load_file(path.join(path.dirname(__file__), "beacons.kv"))


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


class Beacons(MDResponsiveLayout, MDScreen):

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "beacons"
        self.mobile_view: BeaconsMobileView = BeaconsMobileView()
        self.tablet_view: BeaconsTabletView = BeaconsTabletView()
        self.desktop_view: BeaconsDesktopView = BeaconsDesktopView()

        self._project = MDApp.get_running_app().project
        self._area_selection: ShapeOnImage = None

        self._P1_to_P2: float = None
        self._P2_to_P3: float = None
        self._P3_to_P4: float = None
        self._P4_to_P1: float = None
        self._P1_to_P3: float = None
        self._P2_to_P4: float = None

    def _load_beacons_selection(self) -> None:
        if self._project.steps_done["beacons"]:
            image = video_to_image(self._project.video_configuration["video"],
                                   self._project.video_configuration["start_time"])
            gcp = self._project.beacons["points"]
            self._P1_to_P2 = self._project.beacons["p1_to_p2"]
            self._P2_to_P3 = self._project.beacons["p2_to_p3"]
            self._P3_to_P4 = self._project.beacons["p3_to_p4"]
            self._P4_to_P1 = self._project.beacons["p4_to_p1"]
            self._P1_to_P3 = self._project.beacons["p1_to_p3"]
            self._P2_to_P4 = self._project.beacons["p2_to_p4"]

        else:
            image, gcp = beacons_detection(self._project.video_configuration["video"],
                                           self._project.video_configuration["start_time"])

        Clock.schedule_once(lambda dt: self._display_loaded_beacons(image, gcp))

        return

    def _display_loaded_beacons(self, image, gcp) -> None:
        self.display_beacons_selection(
            ShapeOnImage(image, gcp, shape_width=2, label_format="P")
        )
        self.children[0].ids.p1_to_p2.text = str(self._P1_to_P2) if self._P1_to_P2 is not None else ""
        self.children[0].ids.p2_to_p3.text = str(self._P2_to_P3) if self._P2_to_P3 is not None else ""
        self.children[0].ids.p3_to_p4.text = str(self._P3_to_P4) if self._P3_to_P4 is not None else ""
        self.children[0].ids.p4_to_p1.text = str(self._P4_to_P1) if self._P4_to_P1 is not None else ""
        self.children[0].ids.p1_to_p3.text = str(self._P1_to_P3) if self._P1_to_P3 is not None else ""
        self.children[0].ids.p2_to_p4.text = str(self._P2_to_P4) if self._P2_to_P3 is not None else ""

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(5)

    def on_enter(self, *args) -> None:
        if self._area_selection is None:
            Thread(target=self._load_beacons_selection()).start()

    def go_back(self) -> None:
        self.manager.current = "bathymetry"

    def display_beacons_selection(self, widget: ShapeOnImage) -> None:
        beacons_selection_layout = self.children[0].ids.beacons_selection

        if self._area_selection is not None:
            beacons_selection_layout.clear_widgets()

        beacons_selection_layout.add_widget(widget)
        self._area_selection = widget

        return

    def is_input_valid(self, input_id: int, value: float | int) -> bool:

        if value is not None or value == "":
            try:
                value = float(value)

            except ValueError:
                self.children[0].ids[input_id].error = True
                self.children[0].ids[input_id].helper_text = "The distance should be a number"

                return False

            if value < 0:
                self.children[0].ids[input_id].error = True
                self.children[0].ids[input_id].helper_text = "The distance can't be negative"
                return False

        else:
            self.children[0].ids[input_id].error = True
            self.children[0].ids[input_id].helper_text = "Mandatory input"
            return False

        if input_id == "p1_to_p2":
            self._P1_to_P2 = value

        elif input_id == "p2_to_p3":
            self._P2_to_P3 = value

        elif input_id == "p3_to_p4":
            self._P3_to_P4 = value

        elif input_id == "p4_to_p1":
            self._P4_to_P1 = value

        elif input_id == "p1_to_p3":
            self._P1_to_P3 = value

        elif input_id == "p2_to_p4":
            self._P2_to_P4 = value

        return True

    def validate_beacons(self) -> None:

        if (self.is_input_valid("p1_to_p2", self._P1_to_P2) and \
            self.is_input_valid("p2_to_p3", self._P2_to_P3) and \
            self.is_input_valid("p3_to_p4", self._P3_to_P4) and \
            self.is_input_valid("p4_to_p1", self._P4_to_P1)) and \
                self.is_input_valid("p1_to_p3", self._P1_to_P3) and \
                self.is_input_valid("p2_to_p4", self._P2_to_P4):
            Thread(target=self._save_beacons).start()
            self.manager.current = "filter_video"

        return

    def _save_beacons(self) -> None:
        MDApp.get_running_app().project.beacons = {
            "points": self._area_selection.get_points_coordinate(),
            "p1_to_p2": self._P1_to_P2,
            "p2_to_p3": self._P2_to_P3,
            "p3_to_p4": self._P3_to_P4,
            "p4_to_p1": self._P4_to_P1,
            "p1_to_p3": self._P1_to_P3,
            "p2_to_p4": self._P2_to_P4
        }
