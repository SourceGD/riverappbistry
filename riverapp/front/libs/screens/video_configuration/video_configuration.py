from os import path

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager

from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.lang import Builder


from libs.components.dialogs.confirm_action.confirm_action import ConfirmAction
from libs.components.widget.video_player.video_player import RiverAppVideoPlayer

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
    start_time = NumericProperty(0)
    end_time = NumericProperty(1)
    frequency = NumericProperty(1)
    video_path = StringProperty()

    _start_time_is_valid = BooleanProperty(True)
    _end_time_is_valid = BooleanProperty(True)
    _frequency_is_valid = BooleanProperty(True)
    _video_reader = None

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "video_configuration"
        self.mobile_view: VideoConfigurationMobileView = VideoConfigurationMobileView()
        self.tablet_view: VideoConfigurationTabletView = VideoConfigurationTabletView()
        self.desktop_view: VideoConfigurationDesktopView = VideoConfigurationDesktopView()
        self.file_manager: MDFileManager = MDFileManager(
            exit_manager=self.exit_file_manager, 
            select_path=self.select_path,
            ext=[".mp4", ".avi"],
            selector="file"
        )
        self.dialog: ConfirmAction = None

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(7)

    def on_pre_leave(self, *args) -> None:
        """
            Called just before the user leave the screen.
        """
        if self._video_reader is not None:
            self._video_reader.state = "pause"
            
    def open_file_manager(self) -> None:
        """
            Called to open the file manager
        """
        self.file_manager.show(path.expanduser('~'))

    def select_path(self, file_path: str) -> None:
        """
            Check selected file.
        """

        if path.splitext(file_path)[1] in [".mp4", ".avi"]: 
            self.exit_file_manager()
            self._video_reader = RiverAppVideoPlayer(
                source=file_path,
                size_hint= (1, None),
                height=(self.height - 2 * dp(64)) / 2,
                y=(self.height - 2 * dp(64)) / 2
                )
            self.video_path = file_path
            self.children[0].ids.video_upload.disabled = True
            self.children[0].ids.remove_video.disabled = False
            self.children[0].add_widget(self._video_reader)
            

        else:
            self.dialog= ConfirmAction(
                title="Wrong File",
                text="The video can only be a mp3 or an avi !",
                confirm_text="I understand"
            )

            self.dialog.open()

    def exit_file_manager(self, *args) -> None:
        """
            Called when leaving the file manager
        """
        self.file_manager.close()

    def remove_video(self) -> None:
        self.children[0].remove_widget(self._video_reader)
        self._video_reader = None
        self.video_path = ""
        self.children[0].ids.video_upload.disabled = False
        self.children[0].ids.remove_video.disabled = True

    def set_start_time(self, value: str | int | float) -> None:
        """
            Check then set the start time input
        """
        if not value and value != 0:
            self.start_time = -9999
            self.children[0].ids.start_time_input.error = True
            self.children[0].ids.start_time_input.helper_text = "Start Time is required"
            self._start_time_is_valid = False
            return

        try:
            self.start_time = float(value)
            self._start_time_is_valid = True

            if self.start_time < 0:
                self.children[0].ids.start_time_input.error = True
                self.children[0].ids.start_time_input.helper_text = "Start Time cannot be negative"
                self._start_time_is_valid = False

            if self.start_time > self.end_time:
                self.children[0].ids.start_time_input.error = True
                self.children[0].ids.start_time_input.helper_text = "Start Time is greater than End Time"
                self._start_time_is_valid = False

        except ValueError:
            self.start_time = -9999
            self.children[0].ids.start_time_input.error = True
            self.children[0].ids.start_time_input.helper_text = "Start Time should be a float"
            self._start_time_is_valid = False

    def set_end_time(self, value: str | int | float) -> None:
        """
            Check then set the end time input
        """
        if not value and value != 0:
            self.end_time = -9999
            self.children[0].ids.end_time_input.error = True
            self.children[0].ids.end_time_input.helper_text = "End Time is required"
            self._end_time_is_valid = False
            return
        
        try:
            self.end_time = float(value)
            self._end_time_is_valid = True

            if self.end_time < 0:
                self.children[0].ids.end_time_input.error = True
                self.children[0].ids.end_time_input.helper_text = "End Time cannot be negative"
                self._end_time_is_valid = False

            if self.end_time < self.start_time:
                self.children[0].ids.end_time_input.error = True
                self.children[0].ids.end_time_input.helper_text = "Start Time is greater than End Time"
                self._end_time_is_valid = False

        except ValueError:
            self.end_time = -9999
            self.children[0].ids.end_time_input.error = True
            self.children[0].ids.end_time_input.helper_text = "Start Time should be a float"
            self._end_time_is_valid = False

    def set_frequency(self, value: str | int | float) -> None:
        """
            Check then set the frequency input
        """
        if not value and value != 0:
            self.frequency = -9999
            self.children[0].ids.frequency_input.error = True
            self.children[0].ids.frequency_input.helper_text = "Frequency is required"
            self._frequency_is_valid = False
            return
        
        try:
            self.frequency = int(value)
            self._frequency_is_valid = True

            if self.frequency < 1:
                self.children[0].ids.frequency_input.error = True
                self.children[0].ids.frequency_input.helper_text = "Frequency must be greater than 1"
                self._frequency_is_valid = False

        except ValueError:
            self.frequency = -9999
            self.children[0].ids.frequency_input.error = True
            self.children[0].ids.frequency_input.helper_text = "Frequency must be an int"
            self._frequency_is_valid = False

    def send_video_configuration(self) -> None:
        self.set_start_time(self.start_time)
        self.set_end_time(self.end_time)
        self.set_frequency(self.frequency)

        if not path.exists(self.video_path) or self.video_path == "":
            app_theme_color = MDApp.get_running_app().theme_cls

            error_flash = Animation(md_bg_color=app_theme_color.error_color, duration=0.1)
            revert_to_normal = Animation(md_bg_color=app_theme_color.bg_normal, duration=0.45)
            error_flash.bind(on_complete=lambda *_: revert_to_normal.start(self.children[0].ids.video_upload))
            error_flash.start(self.children[0].ids.video_upload)

            return 
        
        if self._start_time_is_valid and self._end_time_is_valid and self._frequency_is_valid :
            # Launch Save Process + Swicth to next screen
            print(f"""\n
                start_time : {self.start_time} \n
                end_time : {self.end_time} \n
                freq : {self.frequency}\n
                video : {self.video_path}
                """)
            
            self.manager.current = "bathymetry"
        