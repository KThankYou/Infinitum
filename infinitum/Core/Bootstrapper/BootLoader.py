# Handle normal boot
from Infinitum.Core.Threading.Threading import ThreadHandler
from Infinitum.Core.DesktopWindowManager import DWM
from Infinitum.Core.Storage.FileManager import FileManager

def init():
    if not FileManager.check_install(r'.\Infinitum.vc'): return False
    Threader = ThreadHandler()
    DWM.init(Threader=Threader)
    return True
    