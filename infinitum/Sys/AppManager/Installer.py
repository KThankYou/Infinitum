from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Core.Storage.Metadata import Metadata
from Infinitum.Core.DesktopWindowManager.Icons import Icon
from Infinitum.TYPEHINTS import _Process

from tkinter import filedialog
from typing import List, Tuple

import importlib
import tkinter
import tomllib
import shutil
import sys
import os

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

'''
# Infinitum Installer config(infinstall.toml):
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

# Name of the file with process class which has 
# a generator draw() which yields a pygame.Surface and
# a method handle_event(event: pygame.event.Event, mouse_pos: Tuple[int, int], keys: pygame.key.ScancodeWrapper) to handle events
target = "<name of file>" 

# It must be integers in the form width x height, ex 1280x720
width = <width>
height = <height>

# Must be a boolean value. Indicates whether the program should use the max resolution or not. 
# If this is set to True, resolution will be ignored
fullscreen = <bool>

# Must be a boolean value. Indicates whether the program should have borders or not
# Borders are basically the frame of the window with the start, stop etc
borders = <bool>

# This name will be displayed on the Icon and the title bar of the window frame
name = "<name of app>"

# This is the image which will be used as the icon
image = "<path to image>"

# Must be a boolean value. Set if the window should be draggable or not.
# If set to True then a rect will be passed to process.handle_event(rect = pygame.Rect)
# whose x, y will be the topleft part of the window
draggable = <bool>

# Must be a boolean value. Set if the window should be resizeable or not.
# If set to True then an will be passed to process.handle_event
# which has an event.type == pygame.VIDEORESIZE
resizeable = <bool>

'''

class Installer:
    def __init__(self, FM: FileManager, max_res: Tuple[int, int] = (1600, 900),paths: List[str] = []) -> None:
        self.FileManager = FM
        self.paths = list(paths)
        self.max_res = max_res
    
    def install(self):
        folder_path = filedialog.askdirectory()
        config_file_path = os.path.join(folder_path, 'infinstall.toml')
        with open(config_file_path, 'rb') as file: data = tomllib.load(file)

        sys.path.append(folder_path)
        importlib.import_module(data['target']).Process

        working_dir = self.FileManager.temp()
        zip_file = os.path.join(working_dir.name, *(data['target'].split('\\')))
        path = shutil.make_archive(zip_file, 'zip', folder_path)

        app_path = self.FileManager.make_folder(f"{data['name']}", r'.\Apps', overwrite = True)

        handle = self.FileManager.write_open(data['name'], app_path)
        with open(path, 'rb') as zip: handle.write(zip.read())
        handle.close()
        
        working_dir.cleanup()

    def get_icon(self, metadata: Metadata) -> Icon:
        data, path = self.FileManager.read(metadata), self.FileManager.temp()
        self.paths.append(path)
        with open(os.path.join(path.name, 'setup.zip'), 'wb') as drive:
            drive.write(data)
        shutil.unpack_archive(os.path.join(path.name, 'setup.zip'), path.name, 'zip')
        sys.path.insert(1, path.name)
        config_file_path = os.path.join(path.name, 'infinstall.toml')
        with open(config_file_path, 'rb') as file: data = tomllib.load(file)
        
        Process: _Process = importlib.import_module(data['target']).Process
        resolution = (data['width'], data['height'])
        image_path = os.path.join(path.name, *(data['image'].split('\\')))
        return Icon(**{'process': Process, 'name': data['name'], 'process_size': resolution, 'image': image_path,
                    'fullscreen': data['fullscreen'], 'max_res': self.max_res, 'cwd': path.name, 
                    'draggable': data['draggable'], 'resizeable': data['resizeable']})
