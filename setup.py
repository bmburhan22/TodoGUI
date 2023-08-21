import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["PIL",'itertools','tempfile', 'tkinter']}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "TODO List",
    version = "1.0",
    author= 'Casper',
    description = "TODO List Program by Casper. Discord casper.exe_ casper.exe#6764",
    options = {"build_exe": build_exe_options},
    executables = [Executable("todo.py", base=base)]
)