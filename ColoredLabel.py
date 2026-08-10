from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class ColoredLabel(Label):
    def __init__(self, bg_color=(1, 0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect_color = Color(*bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Example Usage
# return ColoredLabel(text="Hello", bg_color=(0, 0.6, 0.2, 1))
