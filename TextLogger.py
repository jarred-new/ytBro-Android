from kivy.app import App
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

class TextLogger:
    def __init__(self, log_widget):
        self.log_widget = log_widget

    def debug(self, msg):
        self.append_log(msg)

    def warning(self, msg):
        self.append_log("WARNING: " + str(msg))

    def error(self, msg):
        self.append_log("ERROR: " + str(msg))

    def append_log(self, text):
        # yt-dlp may run in another thread,
        # so update Kivy through Clock.
        Clock.schedule_once(
            lambda dt: self._append_log(str(text))
        )

    def _append_log(self, text):
        self.log_widget.text += text + "\n"
        self.log_widget.cursor = (0, len(self.log_widget.text))
        self.log_widget.scroll_y = 0

