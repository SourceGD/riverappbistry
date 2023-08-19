from os import environ, path
from json import load
from threading import Thread
from definitions import CONFIG_DIR, PROJECTS_DIR

environ["KIVY_VIDEO"] = "ffpyplayer"
environ["KIVY_AUDIO"] = "ffpyplayer"

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import DictProperty

from src.front.riverapp_controller import RiverappController
from src.front.components.dialogs import ConfirmAction
from src.back import save_project

class RiverApp(MDApp):

    project_data: DictProperty = DictProperty()

    def __init__(self, **kwargs) -> None:
        super(RiverApp, self).__init__(**kwargs)
        Config.set('kivy', 'exit_on_escape', '0')

        Window.bind(on_request_close=self._on_request_close)
        Window.minimum_width, Window.minimum_height = 300, 600

        # class variables #
        self.title: str ='RiverApp'
        self._exit_dialog: ConfirmAction = None
        
        # App colors & theme
        self.theme_cls.colors = self._load_colors_config()
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Orange"

    def _on_request_close(self, *args) -> bool:
        """
            Display a dialog to make sure the user want to leave the app
        """
        if not self._exit_dialog:
            self._exit_dialog = ConfirmAction(
                title="Exit RiverApp",
                text="Are you sure you want to exit RiverApp ?",
                confirm_text="Exit",
                confirm_callback=self.stop
            )

        self._exit_dialog.open()
        return True
    
    def _load_colors_config(self) -> dict:
        """
            Load the colors config file needed for RiverApp and return a dict with the data
            More information about color definiton here : https://kivymd.readthedocs.io/en/1.1.1/themes/color-definitions/ 
                & https://github.com/kivymd/KivyMD/blob/master/kivymd/color_definitions.py
        """
        with open(path.join(path.dirname(__file__), CONFIG_DIR, "color_definitions.json")) as colors_config_file:
            config: dict = load(colors_config_file)
        return config
    
    def build(self) -> None:
        return RiverappController()

    def on_project_data(self, instance, value: dict) -> None:
        if value is None:
            return

        error_dialogs: ConfirmAction = ConfirmAction(
                title="Save error",
                text="An error occured while saving. Go back & revalidate the previous step to make sure it's saved.",
                confirm_text="I understand"
            )
        
        if not isinstance(value, dict):
            error_dialogs.open()
            return
        
        try:
            if value["project_name"] == "":
                error_dialogs.open()
                return

            Thread(target=save_project(path.join(PROJECTS_DIR, value["project_name"]), value)).start()

        except (KeyError, ValueError, FileNotFoundError, TypeError):
            error_dialogs.open()
            return

        
if __name__=="__main__":
    RiverApp().run()