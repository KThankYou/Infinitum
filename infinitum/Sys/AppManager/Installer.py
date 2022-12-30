from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Sys.AppManager.AppMon import AppMon
from tkinter import filedialog
import tkinter, importlib, os
import configparser


tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing


'''
# Infinitum Installer config(infinstall.py):
#
# Any line starting with # is a comment
# 
# <> means placeholder and it must be replaced with appropriate values
# 
# The installer config must be in the uppermost level of the program directory
# Meaning the folder where the config is stored and everything inside it will be stored
# into the Infinitum.vc
#
# The Order of these variables does not matter but all must exist

# Path of the file with process class which has 
# a generator draw() which yields a pygame.Surface and
# a method handle_event(event: pygame.event.Event, mouse_pos: Tuple[int, int], keys: pygame.key.ScancodeWrapper) to handle events
path = "<path of file>" 

# It must be integers in the form width x height
resolution = (<width>, <height>)

# Must be a boolean value. Indicates whether the program should use the max resolution or not. 
# If this is set to True, resolution will be ignored
fullscreen = <bool>

# Must be a boolean value. Indicates whether the program should have borders or not
# Borders are basically the frame of the window with the start, stop etc
borders = <bool>

# Must be a boolean value. Indicates whether the program is drag-able or not.
# Set this to False if your program has mouse dragging or is fullscreen
drag_able = <bool>

# This name will be displayed on the Icon and the title bar of the window frame
name = "<name of app>"

'''

class Installer:
    def __init__(self, FM: FileManager, appMon: AppMon) -> None:
        self.FileManager = FM
        self.AppMon = appMon
    
    def install(self):
        folder_path = filedialog.askdirectory()
        importlib.import_module(os.path.join(folder_path, 'infinstall.py'))