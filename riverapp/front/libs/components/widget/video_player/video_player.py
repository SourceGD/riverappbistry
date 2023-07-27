from os import path
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT

from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.uix.video import Video
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"video_player.kv"))

class RiverAppVideoPlayer(MDRelativeLayout):
    _current_time = StringProperty("0:00")
    _time_duration = StringProperty("0:00")
    _duration = NumericProperty()
    
    hide = BooleanProperty(False)
    source = StringProperty()
    state = StringProperty("play")

    def __init__(self, source: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = source
        self.set__duration()
        self.set__time_duration()

    def on_parent(self, widget, parent) -> None:
        if parent is None:
            self.ids.video.unload()

    def on_source(self, instance, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"source must be a string: {value}")

        if value == "":
            raise ValueError(f"source is mandatory: {value}")
        
        if not path.exists(value):
            raise FileNotFoundError(f"the file {value} was not found")

    def on_state(self, instance, value:str) -> None:
        if value not in ["play", "pause", "stop"]:
            raise ValueError(f"Unknown state. Available states are [play, pause, stop] : {value}")
        
        if value == "play":
            self.ids.video.state = "play"
        
        if value == "pause":
            self.ids.video.state = "pause"

        if value == "stop":
            self.ids.video.state = "stop"

    def change_slider_value(self, instance, value) -> None:
        position = (value / self._duration) * 100
        self.ids.slider.value = position
        self.set__current_time(value)
        self.update_timer()

    def play_pause(self, button) -> None:
        if button.icon != "replay":
            if button.icon == "play":
                button.icon = "pause"
                self.state = "play"

            else:
                button.icon = "play"
                self.state = "pause"

        else:
            button.icon = "pause"
            self.ids.video.reload()

    def on_off_volume(self, button) -> None:
        if button.icon == "volume-high":
            button.icon = "volume-off"
            self.ids.video.volume = 0

        else:
            button.icon = "volume-high"
            self.ids.video.volume = 1

    def set__duration(self) -> None:
        try:
            video = VideoCapture(self.source)
            self._duration = round(video.get(CAP_PROP_FRAME_COUNT) / video.get(CAP_PROP_FPS))
        
        except ZeroDivisionError:
            raise ZeroDivisionError(
                f"Could not get the fps from {self.source}. Make sure the video is in a format supported by opencv "
            )

    def set__time_duration(self) -> None:
        minutes = int(self._duration / 60) if self._duration / 60 >= 1 else 0
        seconds = int(self._duration - minutes * 60)
        self._time_duration = f"{minutes}:{str(seconds).zfill(2)}"

    def set__current_time(self, value: float) -> None:
        minutes = int(value / 60) if value / 60 >= 1 else 0
        seconds = int(value - minutes * 60)
        self._current_time = f"{minutes}:{str(seconds).zfill(2)}"

    def update_timer(self) -> None:
        self.ids.timer.text = f"{self._current_time} / {self._time_duration}"

    def hide_controls(self, *args) -> None:
        self.hide = True
        self.remove_widget(self.ids.controls)
    
    def unhide_controls(self, *args) -> None:
        self.hide = False
        self.add_widget(self.ids.controls)

class Videos(Video):

    def _on_eos(self, *largs) -> None:
        self.parent.ids.play_pause_button.icon = "replay"
        if self.parent.hide:
            self.parent.unhide_controls()

    def on_parent(self, widget, parent) -> None:
        self.bind(position=parent.change_slider_value)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.hide:
                self.parent.unhide_controls()
            
            else:
                if touch.pos[1] > self.parent.ids.video.height / 4:
                    self.parent.hide_controls()