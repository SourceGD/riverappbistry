from os import path
from threading import Thread, Event
from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from src.front.components.dialogs import ConfirmAction

Builder.load_file(path.join(path.dirname(__file__), "piv.kv"))


class PivMobileView(MDScreen):
    """
        Class containing the mobile view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """


class PivTabletView(MDScreen):
    """
        Class containing the tablet view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """


class PivDesktopView(MDScreen):
    """
        Class containing the desktop view of this screen.
        The class is empty because it is not possible to do otherwise
        to use the MDResponsiveLayout.
    """


class Piv(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name: str = "piv"
        self.mobile_view: PivMobileView = PivMobileView()
        self.tablet_view: PivTabletView = PivTabletView()
        self.desktop_view: PivDesktopView = PivDesktopView()

        self._project = MDApp.get_running_app().project
        self._lauch_piv: bool = True
        self._piv_thread: Thread = None
        self._stop_piv_flag: Event = Event()

    def _piv_calculation(self) -> None:

        try:
            self._project.generate_piv()
            print("PIV done")
            # self.cancel_piv()
        except Exception:
            ConfirmAction(
                title="PIV error",
                text="Someting went wrong with the analysis. Please restart the App",
                confirm_text="I understand",
            ).open()
            self.children[0].ids.progress.stop()
            return
        return

    def to_post_processing(self) -> None:
        self.manager.current = "post_process"

    def on_pre_enter(self, *args) -> None:
        """
            Called just before the screen appear to the user.
            Update the left progress bar to Video.
        """
        MDApp.get_running_app().root.ids["lollipop_progress_bar"].activate_lollipop(4)

        if not self._project.piv["need_update"]:
            self._lauch_piv = False

    def on_enter(self, *args) -> None:

        if self._lauch_piv:
            self.children[0].ids.progress.start()
            thread = Thread(target=self._piv_calculation)
            thread.start()
            # wait for 1 minute
            # TODO Find a way to fix the fact that we can't touch the window while the thread is running

            thread.join()
            self.to_post_processing()

            print("in on_enter piv.py")

        else:
            self.to_post_processing()
        return

    def on_leave(self, *args) -> None:
        if self.children:
            self.children[0].ids.progress.stop()

    def cancel_piv(self) -> None:
        self._stop_piv_flag.set()
        self._piv_thread.join()
        print("uwu")

        self._stop_piv_flag.clear()
