# Handle normal boot
from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Core.DesktopWindowManager.DWM import start
from Infinitum.Sys.Login.Login import Login

import pygame

def init():
    if not FileManager.check_install(r'.\Infinitum.vc'): return False
    display = pygame.display.set_mode(FileManager.get_res(r'.\Infinitum.vc'))
    exit_code = 2
    while exit_code == 2:
        login = Login(display)
        pwd = login.main()
        exit_code = start(display, pwd = pwd)
    return True