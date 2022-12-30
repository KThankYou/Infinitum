# Handle normal boot
#from Infinitum.Core.Threading.Threading import ThreadHandler
from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Core.DesktopWindowManager.DWM import start
from Infinitum.Sys.Login.Login import Login

def init():
    if not FileManager.check_install(r'.\Infinitum.vc'): return False
    exit_code = 2
    while exit_code == 2:
        login = Login()
        pwd = login.main()
        exit_code = start(pwd = pwd)
    return True