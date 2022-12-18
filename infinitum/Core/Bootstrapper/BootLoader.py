# Handle normal boot
from Infinitum.Core.Threading.Threading import ThreadHandler
from Infinitum.Core.DesktopWindowManager import DWM

def init():
    primary = ThreadHandler()
    WinManager = primary.create_process(function = DWM.init, sudo = True, Threader = primary,)
    WinManager.start()
    return WinManager