from os import path
from threading import Thread
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager

from kivy.lang import Builder

from src.front.components.dialogs import ConfirmAction
from src.front.components.widget import BathymetryGraph, InvalidFileFormat

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
        self._file_manager: MDFileManager = MDFileManager(
            exit_manager=self.exit_file_manager, 
            select_path=self._select_path,
            selector="file"
        )
        self._graph = None
        self._water_level: float = None

        self._project = MDApp.get_running_app().project
        self._need_load_from_backup: bool = True


    def _select_path(self, file_path: str) -> None:
        """
            Check selected file.
        """
        self.load_graph(file_path)
        self.exit_file_manager()

        return
    
    def _load_bathymetry(self) -> None:
        if self._project.steps_done["bathymetry"]:
            data = self._project.bathymetry
            self._water_level = data["water_level"]

            Clock.schedule_once(lambda dt: self._display_loaded_bathymetry(data["x"], data["y"]))
        
        return
    
    def _display_loaded_bathymetry(self, x: list, y: list) -> None:
        self.load_graph((x, y))
        self.children[0].ids.water_level.text = str(self._water_level)

        return
    
    def _save_bathymetry(self) -> None:
        MDApp.get_running_app().project.bathymetry = {
            "x": self._graph.x_coordinates,
            "y": self._graph.y_coordinates,
            "water_level": self._water_level
        }

        return
    
    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """

        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(6)

    def on_enter(self, *args) -> None:
        if self._need_load_from_backup:
            Thread(target=self._load_bathymetry).start()

    def go_back(self) -> None:
        self.manager.current = "video_configuration"

    def open_file_manager(self) -> None:
        """
            Called to open the file manager
        """
        self._file_manager.show(path.expanduser('~'))

    def load_graph(self, bathymetry: str | tuple) -> None:
        try:
            if self._graph is None:
                self._graph = BathymetryGraph(bathymetry)

                self.children[0].ids.content.clear_widgets()
                self.children[0].ids.content.add_widget(self._graph.generate_image_widget())
                self.children[0].ids.control_button.disabled = False

        except InvalidFileFormat:
            ConfirmAction(
                title="The bathymetry isn't provided in a suitable typesetting !",
                text="Please check the documentation for more information on how to typeset your bathymetry",
                confirm_text="I understand"
            ).open()

        except UnicodeDecodeError:
            ConfirmAction(
                title="The bathymetry isn't provided in a suitable encoding !",
                text="Please use UTF-8 encoded file",
                confirm_text="I understand"
            ).open()

    def exit_file_manager(self, *args) -> None:
        """
            Called when leaving the file manager
        """
        self._file_manager.close()
    
    def remove_graph(self) -> None:
        self._graph = None
        self.children[0].ids.control_button.disabled = True
        self.children[0].ids.content.clear_widgets()
        self.children[0].ids.content.add_widget(self.children[0].ids.upload_button)

    def set_water_level(self, value: int | float) -> bool:
        if value == "" or value is None:
            self.children[0].ids.water_level.error = True
            self.children[0].ids.water_level.helper_text = "Water Level is required"
            self._water_level = None
            return False
        
        try:
            value = float(value)

        except ValueError:
            self.children[0].ids.water_level.error = True
            self.children[0].ids.water_level.helper_text = "Water Level should be a number"
            return False
        
        if value <= 0:
            self.children[0].ids.water_level.error = True
            self.children[0].ids.water_level.helper_text = "Water Level cannot be less than or equal to 0"
            return True
        
        self._water_level = value
        return True
    
    def validate_bathymetry(self) -> None:

        if self._graph is None or not self.set_water_level(self._water_level):
            return

        Thread(target=self._save_bathymetry).start()
        self.manager.current = "beacons"