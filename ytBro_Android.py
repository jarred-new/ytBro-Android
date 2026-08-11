from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
#from kivy.uix.checkbox import CheckBox

import threading
import yt_dlp
import os

from ColoredLabel import ColoredLabel
from ColoredLayout import ColoredLayout
from TextCheckbox import TextCheckbox

class YtBro(App):
    def build(self):
        pd = 18 # Padding
        
        layout = ColoredLayout(
        	orientation='vertical',
        	padding=[pd, pd, pd, pd],
            spacing=35
        )
        # Note: to change color, go to the ColoredLayout.py file
        
        logoLayout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=222
        )
        
        logo = ColoredLabel(
            text="[b]YtBro[/b]", 
            markup=True,
            bg_color=(0.7, 0, 0, 1),
            font_size=88           
        )
        
        slogan = ColoredLabel(
            text="YouTube Downloader by Jarred (Powered by yt-dlp)", 
            bg_color=(0.7, 0, 0, 1),
            font_size=45
        )
        
        logoLayout.add_widget(logo)
        logoLayout.add_widget(slogan)
        layout.add_widget(logoLayout)
        
        urlInput = TextInput(
            hint_text="Enter your YouTube or any kind of URL",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(urlInput)
        
        settingsLabel = Label(
            text="[b]Settings:[/b]",
            markup=True,
            font_size=45,
            size_hint_x=0.163,
            size_hint_y=None,
            height=20,
            color=(0,0,0,1)
        )
        layout.add_widget(settingsLabel)
        
        playlist = TextCheckbox(
            text="Download Playlist",
            text_color=(0,0,0,1),
            check_color=(0.9,0,0,1)
        )
        layout.add_widget(playlist)
        
        audio = TextCheckbox(
            text="Download Audio Only",
            text_color=(0,0,0,1),
            check_color=(0.9,0,0,1)
        )
        layout.add_widget(audio)
        
        selectPath_button = Button(
            text='Select Download Path', 
            size_hint_y=0.1
        )
        layout.add_widget(selectPath_button)
        
        download_button = Button(
            text='Download', 
            size_hint_y=0.1
        )
        layout.add_widget(download_button)
        
        log = TextInput(
            multiline=True,
            readonly=True
        )
        layout.add_widget(log)
        
        return layout

if __name__ == '__main__':
    YtBro().run()