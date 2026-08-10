from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import yt_dlp
from ColoredLabel import ColoredLabel

class YtBro(App):
    def build(self):
        pd = 10
        
        layout = BoxLayout(
        	orientation='vertical',
        	padding=[pd, pd, pd, pd],
        	spacing=pd+25
        )
        
        #logo = Label(
        #    text="YtBro",
        #    size_hint_y=0.5
        #)
        
        logo = ColoredLabel(
            text="YtBro", 
            bg_color=(0.7, 0, 0, 1)
        )
        
        layout.add_widget(logo)
        
        download_button = Button(
            text='Download', 
            size_hint_y=0.2
        )
        layout.add_widget(download_button)
        
        return layout

if __name__ == '__main__':
    YtBro().run()