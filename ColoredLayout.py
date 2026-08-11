from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

class ColoredLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Add the drawing instructions to canvas.before
        with self.canvas.before:
            self.bg_color = get_color_from_hex('#DDA756')
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
        # Bind the rectangle updates to layout resizing events
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
