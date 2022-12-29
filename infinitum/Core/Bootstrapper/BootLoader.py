# Handle normal boot
#from Infinitum.Core.Threading.Threading import ThreadHandler
from Infinitum.Core.DesktopWindowManager import DWM
from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Sys.Login.main import Login
import pygame

def init():
    pygame.init()
    if not FileManager.check_install(r'.\Infinitum.vc'): return False
    login = Login()
    #pwd = login.main()
    pwd = 'Kiran@2003'

    DWM.init(pwd = pwd)
    return True
    