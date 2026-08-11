from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ColorProperty
)
from kivy.metrics import dp


class TextCheckbox(BoxLayout):
    text = StringProperty("")
    active = BooleanProperty(False)

    # Separate colors
    text_color = ColorProperty((1, 1, 1, 1))
    check_color = ColorProperty((1, 1, 1, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(40)
        self.spacing = dp(8)

        # Text on the LEFT
        self.label = Label(
            text=self.text,
            color=self.text_color,
            halign="left",
            valign="middle",
            size_hint_x=1
        )

        # Checkbox on the RIGHT
        self.checkbox = CheckBox(
            color=self.check_color,
            active=self.active,
            size_hint_x=None,
            width=dp(40)
        )

        self.add_widget(self.label)
        self.add_widget(self.checkbox)

        # Synchronize properties
        self.bind(text=self._update_text)
        self.bind(text_color=self._update_text_color)
        self.bind(active=self._update_checkbox)

        self.checkbox.bind(active=self._checkbox_changed)

    def _update_text(self, instance, value):
        self.label.text = value

    def _update_text_color(self, instance, value):
        self.label.color = value

    def _update_checkbox(self, instance, value):
        if self.checkbox.active != value:
            self.checkbox.active = value

    def _checkbox_changed(self, checkbox, value):
        self.active = value
