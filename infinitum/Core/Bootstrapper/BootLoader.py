# Handle normal boot
from Infinitum.Core.Threading.Threading import ThreadHandler
from Infinitum.Core.DesktopWindowManager import DWM
from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Sys.Login.login import Login
import pygame

def init():
    pygame.init()
    if not FileManager.check_install(r'.\Infinitum.vc'): return False
    login = Login()
    pwd = login.main()

    Threader = ThreadHandler()
    DWM.init(Threader=Threader, pwd = pwd)
    return True
    