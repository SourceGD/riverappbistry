from os import path

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
        self.project = None

    def on_pre_enter(self, *args) -> None:
        self.project = MDApp.get_running_app().project_data

        if self.project is None:
            ConfirmAction(
                title="Error while loading project",
                text="Please retry",
                confirm_text="I understand"
            ).open()

            self.go_back()

    def on_enter(self, *args) -> None:
        if self.project is not None: 
            if self.project["last_step_done"] in PROJECT_STEPS:
                self.children[0].ids.rl_progress_bar.activate_lollipop(7 - PROJECT_STEPS.index(self.project["last_step_done"]))

    def continue_project(self, *args) -> None:
        step = self.project["last_step_done"]
        if step not in PROJECT_STEPS:
            self.manager.current = "video_configuration"
        
        else:
            next_step_index = PROJECT_STEPS.index(step) + 1 if PROJECT_STEPS.index(step) + 1 < len(PROJECT_STEPS) else len(PROJECT_STEPS) - 1
            self.manager.current = PROJECT_STEPS[next_step_index]

    def go_back(self) -> None:
        self.manager.current = "projects"