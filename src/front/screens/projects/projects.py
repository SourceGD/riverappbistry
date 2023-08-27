from os import path, listdir
from threading import Thread

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager

from kivy.lang import Builder
from kivy.clock import Clock

from definitions import PROJECTS_DIR
from src.front.components.card import ProjectCard
from src.front.components.card import NoResults
from src.front.components.dialogs import ConfirmAction

from src.back import create_project, delete_projects, load_project, download_project

Builder.load_file(path.join(path.dirname(__file__),"projects.kv"))

class ProjectsMobileView(MDScreen):
    """
        Class containing the mobile view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class ProjectsTabletView(MDScreen):
    """
        Class containing the tablet view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class ProjectsDesktopView(MDScreen):
    """
        Class containing the desktop view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class Projects(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "projects"
        self.mobile_view: ProjectsMobileView = ProjectsMobileView()
        self.tablet_view: ProjectsTabletView = ProjectsTabletView()
        self.desktop_view: ProjectsDesktopView = ProjectsDesktopView()
        self.projects: list = None
        self.no_results : NoResults = None
        self._new_project_dialogs: ConfirmAction = None
        self._del_project_dialogs: ConfirmAction = None
        self._download_project: str = None
        self._download_file_manager: MDFileManager = MDFileManager(
            exit_manager=self.exit_download_file_manager, 
            select_path=self.select_download_destination,
            selector="folder"
        )

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(8)

    def on_enter(self, *args) -> None:
        Thread(target=self._load_project_list()).start()
    
    def open_new_project_dialogs(self) -> None:
        if self._new_project_dialogs is None:
            self._new_project_dialogs = ConfirmAction(
                title="New Project",
                confirm_text="New",
                type="custom",
                content_cls=MDTextField(
                    hint_text="Project Name",
                    helper_text_mode="on_error"
                ),
                confirm_callback=self._check_and_create_new_project
            )
        
        self._new_project_dialogs.open()

    def open_del_project_dialogs(self, project_name: str) -> None:
        self._del_project_dialogs = ConfirmAction(
            title="Delete project",
            text= f"Are you sure you want to delete the project {project_name} ? This action is irreversible.",
            confirm_text= "Delete",
            confirm_callback=lambda x:self._del_project(project_name=project_name)
        )

        self._del_project_dialogs.open()

    def _check_and_create_new_project(self, *args) -> None:
        if self._new_project_dialogs is None:
            return
        self._new_project_dialogs.buttons[1].disabled = True

        project_name = self._new_project_dialogs.content_cls.text

        try:
            create_project_thread = Thread(target=create_project(project_name, PROJECTS_DIR))
            create_project_thread.start()
            create_project_thread.join()

        except (ValueError, FileExistsError) as error:
            self._new_project_dialogs.buttons[1].disabled = False
            self._new_project_dialogs.content_cls.error = True
            self._new_project_dialogs.content_cls.helper_text = str(error)
            return
        
        self._new_project_dialogs.buttons[1].disabled = False 
        self._new_project_dialogs.dismiss()
        self.select_project(project_name)

    def _del_project(self, project_name:str, *args) -> None:
        if self._del_project_dialogs is None:
            return
        
        try:
            delete_projects_thread = Thread(target=delete_projects(path.join(PROJECTS_DIR, project_name)))
            delete_projects_thread.start()
            delete_projects_thread.join()

        except (ValueError, FileExistsError):
            pass

        self._del_project_dialogs.dismiss()
        self._load_project_list()

    def _load_project_list(self) -> None:

        if self.no_results is not None:
            Clock.schedule_once(lambda x: self.children[0].remove_widget(self.no_results))

        self.projects = [project_name for project_name in listdir(PROJECTS_DIR)] if path.exists(PROJECTS_DIR) else []

        if self.projects == []:
            if self.no_results is None:
                self.no_results = NoResults(
                    title= "No Project",
                    text="No Projects were found within the application",
                )
                
            Clock.schedule_once(lambda x: self.children[0].ids.no_results.add_widget(self.no_results))

        
        Clock.schedule_once(self.set_list_projects)
        return 
    

    def set_list_projects(self, querry: str="", search: bool = False) -> None:

        def add_project_item(name: str) -> None:
            self.children[0].ids.project_recycle_view.data.append(
                {
                    "viewclass": "ProjectCard",
                    "title": name,
                    "on_release": lambda: self.select_project(name),
                    "delete_callback": lambda: self.open_del_project_dialogs(name),
                    "download_callback": lambda: self.open_download_file_manager(name)
                    
                }
            )
        
        self.children[0].ids.project_recycle_view.data = []
        for project_name in self.projects:
            if search:
                if querry in project_name:
                    add_project_item(project_name)
            else:
                add_project_item(project_name)
    
    def select_project(self, project_name: str) -> None:

        try:
            project_data=Thread(target=self._load_project_data(project_name))
            project_data.start()
            project_data.join()

        except (ValueError, FileNotFoundError):
            ConfirmAction(
                title="Error",
                text="Something went wrong while loading the project. Please retry",
                confirm_text="I understand"
            ).open()

            return

        self.manager.current = "project_details"
        
    def _load_project_data(self, project_name: str) -> None:
        data = load_project(path.join(PROJECTS_DIR, project_name))
        MDApp.get_running_app().project_data = data
        return
    
    def open_download_file_manager(self, project_to_download: str = "") -> None:
        """
            Called to open the file manager
        """
        self._download_project = project_to_download
        self._download_file_manager.show(path.expanduser('~'))

    def select_download_destination(self, folder_path: str) -> None:
        try:
            Thread(target=download_project(path.join(PROJECTS_DIR, self._download_project), folder_path)).start()

        except ValueError:  
            ConfirmAction(
                title="Download error",
                text="The requested download folder is not found or is invalid",
                confirm_text="I understand"
            ).open()
        
        except FileNotFoundError:
            ConfirmAction(
                title="Download error",
                text="An error occured while downloading the project. Please retry !",
                confirm_text="I understand"
            ).open()

        except PermissionError :
            ConfirmAction(
                title="Download error",
                text="RiverApp do not have the permission to save the project at the request folder.",
                confirm_text="I understand"
            ).open()

        self.exit_download_file_manager()

    def exit_download_file_manager(self, *args) -> None:
        """
            Called when leaving the file manager
        """
        self._download_project = None
        self._download_file_manager.close()