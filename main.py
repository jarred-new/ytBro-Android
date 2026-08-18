from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
#from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.utils import platform

#from kivy.uix.checkbox import CheckBox

from functools import partial

import threading
import yt_dlp
import os
import urllib.parse
#from sys import platform

from ColoredLabel import ColoredLabel
from ColoredLayout import ColoredLayout
from TextCheckbox import TextCheckbox
from TextLogger import TextLogger

from jnius import autoclass, cast
from android import activity


# Android Java classes
PythonActivity = autoclass(
    "org.kivy.android.PythonActivity"
)

Intent = autoclass(
    "android.content.Intent"
)

DocumentsContract = autoclass(
    "android.provider.DocumentsContract"
)

Uri = autoclass(
    "android.net.Uri"
)

isPlaylist = False
isAudio = False


class YtBro(App):

    def build(self):

        pd = 18  # Padding

        # Default download directory
        #if platform == "android":
            #self.downloadPath = "/storage/emulated/0/Download"
        #else:
            #self.downloadPath = os.path.expanduser("~/Downloads")
        
        self.downloadPath = os.path.join(
        self.user_data_dir,
            "downloads"
            )

        os.makedirs(
            self.downloadPath,
            exist_ok=True
            )

        self.downloadUri = None
        
        # --------------------------------------------------
        # MAIN LAYOUT
        # --------------------------------------------------

        self.layout = ColoredLayout(
            orientation='vertical',
            padding=[pd, pd, pd, pd],
            spacing=35
        )

        # Note: to change color, go to the ColoredLayout.py file

        # --------------------------------------------------
        # LOGO
        # --------------------------------------------------

        self.logoLayout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=222
        )

        self.logo = ColoredLabel(
            text="[b]YtBro[/b]",
            markup=True,
            bg_color=(0.7, 0, 0, 1),
            font_size=88
        )

        self.slogan = ColoredLabel(
            text="YouTube Downloader by Jarred (Powered by yt-dlp)",
            bg_color=(0.7, 0, 0, 1),
            font_size=45
        )

        self.logoLayout.add_widget(self.logo)
        self.logoLayout.add_widget(self.slogan)

        self.layout.add_widget(self.logoLayout)

        # --------------------------------------------------
        # URL INPUT
        # --------------------------------------------------

        self.urlInput = TextInput(
            hint_text="Enter your YouTube or any kind of URL",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.urlInput)

        # --------------------------------------------------
        # SETTINGS
        # --------------------------------------------------

        self.settingsLabel = Label(
            text="[b]Settings:[/b]",
            markup=True,
            font_size=45,
            size_hint_x=0.163,
            size_hint_y=None,
            height=20,
            color=(0, 0, 0, 1)
        )

        self.layout.add_widget(self.settingsLabel)

        # Playlist checkbox
        self.playlist = TextCheckbox(
            text="Download Playlist",
            text_color=(0, 0, 0, 1),
            check_color=(0.9, 0, 0, 1)
        )

        self.playlist.bind(
            active=self.on_playlist_changed
        )

        self.layout.add_widget(self.playlist)

        # Audio checkbox
        self.audio = TextCheckbox(
            text="Download Audio Only",
            text_color=(0, 0, 0, 1),
            check_color=(0.9, 0, 0, 1)
        )

        self.audio.bind(
            active=self.on_audio_changed
        )

        self.layout.add_widget(self.audio)

        # --------------------------------------------------
        # DOWNLOAD PATH
        # --------------------------------------------------

        self.pathLabel = Label(
            text="Download Path:\n" + self.downloadPath,
            color=(0, 0, 0, 1),
            font_size=30,
            size_hint_y=None,
            height=55
        )

        self.layout.add_widget(self.pathLabel)

        self.selectPath_button = Button(
            text='Select Download Path',
            size_hint_y=0.1
        )

        self.selectPath_button.bind(
            on_press=self.select_download_path
        )

        self.layout.add_widget(
            self.selectPath_button
        )

        # --------------------------------------------------
        # DOWNLOAD BUTTON
        # --------------------------------------------------

        self.download_button = Button(
            text='Download',
            size_hint_y=0.1
        )

        self.download_button.bind(
            on_press=self.start_download
        )

        self.layout.add_widget(
            self.download_button
        )

        # --------------------------------------------------
        # LOG
        # --------------------------------------------------

        self.log = TextInput(
            multiline=True,
            readonly=True
        )

        self.layout.add_widget(self.log)

        self.logger = TextLogger(self.log)
        
        #if platform == 'android':
            #try:
                #from android import activity
                #activity.bind(on_activity_result=self.on_activity_result)
            #except Exception as e:
                #self.logger.error("Skipping activity binding: Not running inside a compiled APK or something. Please report this to the developer...")   
        
        return self.layout

    # ======================================================
    # CHECKBOX EVENTS
    # ======================================================

    def on_audio_changed(self, checkbox, value):

        global isAudio

        isAudio = value

    def on_playlist_changed(self, checkbox, value):

        global isPlaylist

        isPlaylist = value

    # ======================================================
    # SELECT DOWNLOAD PATH
    # ======================================================

    def select_download_path(self, instance):
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)

        # Allow the application to retain permission
        flags = (
            Intent.FLAG_GRANT_READ_URI_PERMISSION
            | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
        )

        intent.addFlags(flags)

        PythonActivity.mActivity.startActivityForResult(
            intent,
            1001
        )
        
    def saf_uri_to_path(self, uri):
        uri_string = str(uri.toString())
    
        document_id = (
            DocumentsContract.getTreeDocumentId(uri)
        )
    
        self.logger.debug("SAF URI:", uri_string)
        self.logger.debug("Document ID:", document_id)
    
        # Internal/shared storage
        if document_id.startswith("primary:"):
    
            relative_path = document_id.split(
                ":",
                1
            )[1]
    
            if relative_path:
                return "/storage/emulated/0/" + relative_path
    
            return "/storage/emulated/0"
    
        # Other storage providers cannot safely be
        # converted into a normal filesystem path.
        return None
    
    def on_activity_result(self, request_code, result_code, intent):
        if request_code != 1001:
            return
    
        if result_code != -1:
            self.logger.debug(
                "Folder selection cancelled."
            )
            return
    
        if intent is None:
            self.logger.error(
                "No folder selection result."
            )
            return
    
        uri = intent.getData()
        
        if uri is not None:
        
            path = self.saf_uri_to_path(uri)
        
            if path is not None:
        
                self.downloadPath = path
        
                self.logger.debug(
                    "Download path:",
                    self.downloadPath
                )
        
            else:
        
                self.logger.warning(
                    "Selected location is SAF-only:"
                )
        
                self.logger.debug(
                    uri.toString()
                )
    
        # Persist permission
        flags = (
            intent.getFlags()
            &
            (
                Intent.FLAG_GRANT_READ_URI_PERMISSION
                |
                Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            )
        )
    
        try:
    
            resolver = (
                PythonActivity.mActivity
                .getContentResolver()
            )
    
            resolver.takePersistableUriPermission(
                uri,
                flags
            )
    
            self.logger.debug(
                "SAF permission persisted."
            )
    
        except Exception as e:
    
            self.logger.error(
                "Could not persist SAF permission: " +
                str(e)
            )
    
        # Display URI
        self.pathLabel.text = (
            "Download Path:\n" +
            self.downloadPath
        )
    
    # ======================================================
    # START DOWNLOAD
    # ======================================================

    def start_download(self, instance):

        url = self.urlInput.text.strip()

        if not url:
            self.logger.error(
                "Please enter a URL."
            )
            return

        if not os.path.isdir(self.downloadPath):
            self.logger.error(
                "Download path does not exist."
            )
            return

        self.logger.debug(
            "Starting download..."
        )

        self.logger.debug(
            "URL: " + url
        )

        self.logger.debug(
            "Download path: " +
            self.downloadPath
        )

        # Don't run yt-dlp directly on the
        # Kivy UI thread.
        threading.Thread(
            target=self.download,
            args=(
                url,
                self.downloadPath
            ),
            daemon=True
        ).start()

    # ======================================================
    # YT-DLP DOWNLOAD
    # ======================================================

    def download(self, url, download_path):

        global isAudio, isPlaylist

        ydl_opts = {

            # Video or audio
            "format":
                "best[height<=1080]/best"
                if not isAudio
                else
                "bestaudio/best",

            # Logger
            "logger": self.logger,
            
            # Playlist
            "noplaylist": not isPlaylist,

            # Console output
            "js_runtimes": {"deno": {}},
            "force_ipv4": True,
            "verbose": True,
            #"quiet": False,
            "no_warnings": True,

            # Save to selected folder
            "outtmpl": os.path.join(
                download_path,
                "%(title)s.%(ext)s"
            ),

            # Progress
            "progress_hooks": [
                self.download_progress
            ],
        }

        try:

            self.logger.debug(
                "Downloading..."
            )

            with yt_dlp.YoutubeDL(
                ydl_opts
            ) as ydl:

                ydl.download([url])

            self.logger.debug(
                "Download completed."
            )

        except Exception as e:

            self.logger.error(
                str(e)
            )

    # ======================================================
    # DOWNLOAD PROGRESS
    # ======================================================

    def download_progress(self, data):

        if data["status"] == "downloading":

            percent = data.get(
                "_percent_str",
                ""
            ).strip()

            speed = data.get(
                "_speed_str",
                ""
            ).strip()

            eta = data.get(
                "_eta",
                ""
            )

            self.logger.append_log(
                f"{percent} | "
                f"{speed} | "
                f"ETA: {eta}"
            )

        elif data["status"] == "finished":

            self.logger.append_log(
                "Download finished. Processing..."
            )


app = YtBro()


def on_activity_result(
    request_code,
    result_code,
    intent
):

    app.on_activity_result(
        request_code,
        result_code,
        intent
    )


activity.bind(
    on_activity_result=on_activity_result
)


if __name__ == '__main__':
    app.run()