from os import path

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
        self.file_manager: MDFileManager = MDFileManager(
            exit_manager=self.exit_file_manager, 
            select_path=self.select_path,
            selector="file"
        )
        self.graph = None
        self.data = None
        self._app = MDApp.get_running_app()

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """

        if self._app.project_data is None:
            self.manager.current = "project"
            return
        
        self._app.root.ids["lollipop_progress_bar"].activate_lollipop(6)

    def on_enter(self, *args) -> None:
            if self.data is None:
                self.data = self._app.project_data["bathymetry"]
                if self.data["x"] and self.data["y"] :
                    self.load_graph((self.data["x"], self.data["y"]))

    def go_back(self) -> None:
        self.manager.current = "video_configuration"

    def open_file_manager(self) -> None:
        """
            Called to open the file manager
        """
        self.file_manager.show(path.expanduser('~'))

    def select_path(self, file_path: str) -> None:
        """
            Check selected file.
        """
        self.load_graph(file_path)
        self.exit_file_manager()

    def load_graph(self, bathymetry: str | tuple) -> None:
        try:
            if self.graph is None:
                self.graph = BathymetryGraph(bathymetry)

                self.children[0].ids.content.clear_widgets()
                self.children[0].ids.content.add_widget(self.graph.generate_image_widget())
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
        self.file_manager.close()
    
    def remove_graph(self) -> None:
        self.graph = None
        self.children[0].ids.control_button.disabled = True
        self.children[0].ids.content.clear_widgets()
        self.children[0].ids.content.add_widget(self.children[0].ids.upload_button)

    def send_bathymetry(self) -> None:

        if self.graph is None:
            return

        self._app.project_data["bathymetry"]["x"] = self.graph.x_coordinates
        self._app.project_data["bathymetry"]["y"] = self.graph.y_coordinates
        self._app.project_data["last_step_done"] = "bathymetry"
        
        self.manager.current = "beacons"
    