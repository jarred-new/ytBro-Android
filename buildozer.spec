[app]

title = YtBro

package.name = ytbro

package.domain = com.jarredapps

source.dir = .

version = 1.0

source.include_exts = py,png,jpg,jpeg,kv,atlas

requirements = python3==3.11.11,hostpython3==3.11.11,kivy,pyjnius,yt_dlp,requests

orientation = portrait

fullscreen = 0

icon.filename = %(source.dir)s/data/icon.png

presplash.filename = %(source.dir)s/data/presplash.png

presplash.color = #800000

android.api = 35

android.minapi = 24

android.archs = arm64-v8a

android.accept_sdk_license = True

android.entrypoint = org.kivy.android.PythonActivity

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

p4a.bootstrap = sdl2

# master is already the stable default.
p4a.branch = master

log_level = 2

warn_on_root = 1
