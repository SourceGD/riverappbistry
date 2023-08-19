from os import path
from threading import Thread
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp

from kivy.lang import Builder

from src.front.components.widget import ShapeOnImage
from src.back import beacons_detection

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
        self._area_selection: ShapeOnImage = None
        self.P1_to_P2: float = None
        self.P2_to_P3: float = None
        self.P3_to_P4: float = None
        self.P4_to_P1: float = None
        self.P1_to_P3: float = None
        self.P2_to_P4: float = None

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(5)

    def on_enter(self, *args) -> None:
        if self._area_selection is None:
            Thread(target=self.load_beacons_selection()).start()

    def load_beacons_selection(self) -> None:
        data = beacons_detection("C:/Users/arnau/Desktop/riverapp/examples/riverapp_examples/VGC1/VGC1.mp4")
        print(data)
        layout = ShapeOnImage(data[0], data[1], shape_width=2, label_format= "P")
        self._area_selection = layout

        Clock.schedule_once(lambda dt: self.display_beacons_selection(layout))
        return
    
    def display_beacons_selection(self, widget: ShapeOnImage) -> None:
        if self._area_selection is not None:
            beacons_selection_layout = self.children[0].ids.beacons_selection
            beacons_selection_layout.clear_widgets()
            beacons_selection_layout.add_widget(widget)
            
    def go_back(self) -> None:
        self.manager.current = "bathymetry"

    def is_input_valid(self, input_id: int, value: float | int) -> bool:
        
        if value == "":
            value = None

        if value is not None:
            try:
                value = float(value)

            except ValueError:
                self.children[0].ids[input_id].error = True
                self.children[0].ids[input_id].helper_text = "The distance should be a number"

                return False
        
            if value < 0 :
                self.children[0].ids[input_id].error = True
                self.children[0].ids[input_id].helper_text = "The distance can't be negative"
                return False
        
        if value is None:
            self.children[0].ids[input_id].error = True
            self.children[0].ids[input_id].helper_text = "Mandatory input"
            return False
        
        if input_id == "p1_to_p2" :
            self.P1_to_P2 = value

        elif input_id == "p2_to_p3" :
            self.P2_to_P3 = value

        elif input_id == "p3_to_p4" :
            self.P3_to_P4 = value

        elif input_id == "p4_to_p1" :
            self.P4_to_P1 = value

        elif input_id == "p1_to_p3" :
            self.P1_to_P3 = value

        elif input_id == "p2_to_p4" :
            self.P2_to_P4 = value
            
        return True
    
    def validate(self) -> None:
        
        if not ( self.is_input_valid("p1_to_p2", self.P1_to_P2) and \
            self.is_input_valid("p2_to_p3", self.P2_to_P3) and \
            self.is_input_valid("p3_to_p4", self.P3_to_P4) and \
            self.is_input_valid("p4_to_p1", self.P4_to_P1) and \
            self.is_input_valid("p1_to_p3", self.P1_to_P3) and \
            self.is_input_valid("p2_to_p4", self.P2_to_P4)) :

            return
        
        points = self._area_selection.get_points_coordinate()
        print("OK")
        print(points)
