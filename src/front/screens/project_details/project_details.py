from os import path
from threading import Thread
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp

from kivy.lang import Builder

from src.front.components.dialogs import ConfirmAction
from definitions import PROJECT_STEPS

Builder.load_file(path.join(path.dirname(__file__),"project_details.kv"))

class ProjectDetailsMobileView(MDScreen):
    """
        Class containing the mobile view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class ProjectDetailsTabletView(MDScreen):
    """
        Class containing the tablet view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class ProjectDetailsDesktopView(MDScreen):
    """
        Class containing the desktop view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class ProjectDetails(MDResponsiveLayout, MDScreen):


    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "project_details"
        self.mobile_view: ProjectDetailsMobileView = ProjectDetailsMobileView()
        self.tablet_view: ProjectDetailsTabletView = ProjectDetailsTabletView()
        self.desktop_view: ProjectDetailsDesktopView = ProjectDetailsDesktopView()
        self.next_step = PROJECT_STEPS[0]

    def _display_steps_done(self) -> None:
        self.next_step = next((key for key in PROJECT_STEPS if not MDApp.get_running_app().project.steps_done[key]), None)
        print(self.next_step)
        if self.next_step is None and MDApp.get_running_app().project.steps_done["post_process"]:
            Clock.schedule_once(lambda dt: self.children[0].ids.rl_progress_bar.activate_lollipop(1))
            return
        if self.next_step is not None:
            Clock.schedule_once(lambda dt: self.children[0].ids.rl_progress_bar.activate_lollipop(8 - PROJECT_STEPS.index(self.next_step)))
        
        return
    
    def on_enter(self, *args) -> None:
        Thread(target=self._display_steps_done).start()

    def continue_project(self, *args) -> None:
        if self.next_step is None and not MDApp.get_running_app().project.steps_done["post_process"]:
            # Screen do not exist yet
            self.manager.current = "video_configuration"
        elif MDApp.get_running_app().project.steps_done["post_process"]:
            self.manager.current = "post_process"
        else:
            self.manager.current = self.next_step

    def go_back(self) -> None:
        self.manager.current = "projects"
