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
from src.back import SavingProjectData

class RiverApp(MDApp):

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

        self.project: SavingProjectData = SavingProjectData()
        
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
        
if __name__=="__main__":
    RiverApp().run()