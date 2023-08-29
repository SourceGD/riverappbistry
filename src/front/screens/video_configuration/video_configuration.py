from os import path
from threading import Thread
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager

from kivy.metrics import dp
from kivy.animation import Animation
from kivy.lang import Builder

from src.front.components.dialogs import ConfirmAction
from src.front.components.widget import RiverAppVideoPlayer

Builder.load_file(path.join(path.dirname(__file__),"video_configuration.kv"))

class VideoConfigurationMobileView(MDScreen):
    """
        Class containing the mobile view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class VideoConfigurationTabletView(MDScreen):
    """
        Class containing the tablet view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class VideoConfigurationDesktopView(MDScreen):
    """
        Class containing the desktop view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """

class VideoConfiguration(MDResponsiveLayout,MDScreen):
    """
        Class managing the App video configuration.
    """

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "video_configuration"
        self.mobile_view: VideoConfigurationMobileView = VideoConfigurationMobileView()
        self.tablet_view: VideoConfigurationTabletView = VideoConfigurationTabletView()
        self.desktop_view: VideoConfigurationDesktopView = VideoConfigurationDesktopView()
        self._file_manager: MDFileManager = MDFileManager(
            exit_manager=self.exit_file_manager, 
            select_path=self._select_path,
            ext=[".mp4", ".avi"],
            selector="file"
        )
        self._project = MDApp.get_running_app().project
        self._theme_cls = MDApp.get_running_app().theme_cls
        self._need_load_from_backup: bool = True

        self._video_reader: RiverAppVideoPlayer = None
        self._video_path: str = None

        self._start_time: float = None
        self._end_time: float = None
        self._frequency: int = None

    def _select_path(self, file_path: str) -> None:
        """
            Check selected file.
        """

        if path.splitext(file_path)[1] in [".mp4", ".avi"]: 
            self.exit_file_manager()
            self.load_video(file_path)

        else:
            ConfirmAction(
                title="Wrong File",
                text="The video can only be a mp3 or an avi !",
                confirm_text="I understand"
            ).open()

    def _load_configuration(self) -> None:
        if self._project.steps_done["video_configuration"]:
            data = self._project.video_configuration

            self._start_time = data["start_time"]
            self._end_time = data["end_time"]
            self._frequency = data["frequency"]
            self._video_path = data["video"]

            Clock.schedule_once(lambda dt: self._display_loaded_configuration(data))

        return 
    
    def _display_loaded_configuration(self, video_configuration: dict) -> None:
        self.children[0].ids.start_time.text = str(video_configuration["start_time"])
        self.children[0].ids.end_time.text = str(video_configuration["end_time"])
        self.children[0].ids.frequency.text = str(video_configuration["frequency"])
        self.load_video(video_configuration["video"])
        
        return
        
    def _save_video_configuration(self) -> None:
    
        MDApp.get_running_app().project.video_configuration = {
            "video": self._video_path,
            "start_time": self._start_time,
            "end_time": self._end_time,
            "frequency": self._frequency
        }

        return
    
    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """

        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(7)

    def on_enter(self, *args) -> None:
        if self._need_load_from_backup:
            Thread(target=self._load_configuration).start()

    def on_pre_leave(self, *args) -> None:
        """
            Called just before the user leave the screen.
        """
        if self._video_reader is not None:
            self._video_reader.state = "pause"

    def go_back(self) -> None:
        self.manager.current = "projects"

    def open_file_manager(self) -> None:
        """
            Called to open the file manager
        """
        self._file_manager.show(path.expanduser('~'))

    def load_video(self, video_path: str) -> None:
        self._video_reader = RiverAppVideoPlayer(
                source=video_path,
                size_hint= (1, None),
                height=(self.height - 2 * dp(64)) / 2,
                y=(self.height - 2 * dp(64)) / 2
                )
        self._video_path = video_path
        self.children[0].ids.video_upload.disabled = True
        self.children[0].ids.bottom_buttons.remove_is_disabled = False
        self.children[0].add_widget(self._video_reader)

    def exit_file_manager(self, *args) -> None:
        """
            Called when leaving the file manager
        """
        self._file_manager.close()

    def remove_video(self) -> None:
        self.children[0].remove_widget(self._video_reader)
        self._video_reader = None
        self._video_path = None
        self.children[0].ids.video_upload.disabled = False
        self.children[0].ids.bottom_buttons.remove_is_disabled = True

    def set_start_time(self, value: int | float) -> bool:

        if value == "" or value is None:
            self.children[0].ids.start_time.error = True
            self.children[0].ids.start_time.helper_text = "Start Time is required"
            self._start_time = None
            return False
        
        try:
            value = float(value)

        except ValueError:
            self.children[0].ids.start_time.error = True
            self.children[0].ids.start_time.helper_text = "Start Time should be a number"
            return False
        
        if value < 0:
            self.children[0].ids.start_time.error = True
            self.children[0].ids.start_time.helper_text = "Start Time cannot be less than 0"
            return False
        
        if self._end_time is not None and value >= self._end_time:
            self.children[0].ids.start_time.error = True
            self.children[0].ids.start_time.helper_text = "Start Time cannot be greater than End Time"
            return False

        self._start_time = value
        return True
    
    def set_end_time(self, value: int | float) -> bool:

        if value == "" or value is None:
            self.children[0].ids.end_time.error = True
            self.children[0].ids.end_time.helper_text = "End Time is required"
            self._end_time = None
            return False
        
        try:
            value = float(value)

        except ValueError:
            self.children[0].ids.end_time.error = True
            self.children[0].ids.end_time.helper_text = "End Time should be a number"
            return False
        
        if value < 0:
            self.children[0].ids.end_time.error = True
            self.children[0].ids.end_time.helper_text = "End Time cannot be less than 0"
            return False
        
        if self._start_time is not None and value <= self._start_time:
            self.children[0].ids.end_time.error = True
            self.children[0].ids.end_time.helper_text = "End Time cannot be smaller than Start Time"
            return False

        self._end_time = value
        return True

    def set_frequency(self, value: int | float) -> bool:

        if value == "" or value is None:
            self.children[0].ids.frequency.error = True
            self.children[0].ids.frequency.helper_text = "Frequency is required"
            self._frequency = None
            return False
        
        try:
            value = int(value)

        except ValueError:
            self.children[0].ids.frequency.error = True
            self.children[0].ids.frequency.helper_text = "Frequency should be a number"
            return False
        
        if value <= 0:
            self.children[0].ids.frequency.error = True
            self.children[0].ids.frequency.helper_text = "Start Frequency cannot be less than or equal to 0"
            return False

        self._frequency = value
        return True
    
    def validate_video_configuration(self) -> None:

        if self._video_path is None or not path.exists(self._video_path):
            error_flash = Animation(md_bg_color=self._theme_cls.error_color, duration=0.1)
            revert_to_normal = Animation(md_bg_color=self._theme_cls.bg_normal, duration=0.45)
            error_flash.bind(on_complete=lambda *_: revert_to_normal.start(self.children[0].ids.video_upload))
            error_flash.start(self.children[0].ids.video_upload)
            return 
        
        if self.set_start_time(self._start_time) and \
            self.set_end_time(self._end_time) and \
            self.set_frequency(self._frequency) :
            
            Thread(target=self._save_video_configuration).start()
            self._need_load_from_backup = False
            self.manager.current = "bathymetry"

        return