from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition

class DummyScreen(MDScreen):
    """
        Initial RiverApp screen. 
        Its purpose is to ensure that the other screens are fully loaded.
    """

    def on_enter(self, *args):
        """
            Trigger when the screen is displayed and change to the main screen
            one frame later.
        """
        Clock.schedule_once(self.switch_screen, 2)

    def switch_screen(self, *args):
        """
            Change current screen to video_configuration screen with no 
            transistion.
        """
        self.manager.transition = NoTransition()
        self.manager.current = "video_configuration"
