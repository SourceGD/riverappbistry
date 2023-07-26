from os import path

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager

from kivy.metrics import dp
from kivy.lang import Builder

from libs.components.dialogs.confirm_action.confirm_action import ConfirmAction
from libs.components.widget.bathymetry_graph.bathymetry_graph import BathymetryGraph, InvalidFileFormat

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
            ext=[".csv", ".txt", ".dat"],
            selector="file"
        )
        self.graph = None

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(6)

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
        if path.splitext(file_path)[1] in [".csv", ".txt", ".dat"]:
            try:
                if self.graph is None:
                    self.graph = BathymetryGraph(file_path)

                    self.exit_file_manager()
                    self.children[0].ids.content.clear_widgets()
                    self.children[0].ids.content.add_widget(self.graph.generate_image_widget())
                    self.children[0].ids.control_button.disabled = False

            except InvalidFileFormat:
                ConfirmAction(
                    title="Wrong File Format",
                    text="The bathymetry file has a specific format !\nMore information in the documentation.",
                    confirm_text="I understand"
                )

                return self.dialog.open()

        else:
            ConfirmAction(
                title="Wrong File",
                text="The bathymetry file can only be a csv, a txt or a dat !",
                confirm_text="I understand"
            )

            self.dialog.open()

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
    