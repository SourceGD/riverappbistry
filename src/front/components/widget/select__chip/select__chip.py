from os import path

from kivymd.uix.chip import MDChip

from kivy.animation import Animation

class SelectChip(MDChip):
    _no_ripple_effect = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self.set_chip_bg_color)
        self.bind(active=self.set_chip_text_color)
        self.icon_check_color = self.theme_cls.opposite_text_color
        self.text_color = self.theme_cls.text_color

    def set_chip_bg_color(self, instance_chip, active_value: int):
        '''
        Will be called every time the chip is activated/deactivated.
        Sets the background color of the chip.
        '''

        self.md_bg_color = (
            self.theme_cls.primary_color
            if active_value
            else (
                self.theme_cls.bg_darkest
            )
        )

    def set_chip_text_color(self, instance_chip, active_value: int):
        Animation(
            color=self.theme_cls.opposite_text_color if active_value else self.theme_cls.text_color, d=0.2
        ).start(self.ids.label)