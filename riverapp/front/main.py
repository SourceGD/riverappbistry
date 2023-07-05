from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config

from libs.components.dialogs.confirm_action.confirm_action import ConfirmAction

from json import load
from os import path

class RiverApp(MDApp):

    def __init__(self, **kwargs) -> None:
        super(RiverApp, self).__init__(**kwargs)
        Config.set('kivy', 'exit_on_escape', '0')

        Window.bind(on_request_close=self._on_request_close)

        # class variables #
        self.title: str ='RiverApp'
        self._exit_dialog: ConfirmAction = None
        
        # App colors & theme
        self.theme_cls.colors = self._load_colors_config()
        self.theme_cls.primary_palette = "Teal"

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
        """
        with open(path.join(path.dirname(__file__),"assets/theming/colors.json")) as colors_config_file:
            config: dict = load(colors_config_file)
        return config

if __name__=="__main__":
    RiverApp().run()