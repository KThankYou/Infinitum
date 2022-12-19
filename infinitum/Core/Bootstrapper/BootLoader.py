# Handle normal boot
from Infinitum.Core.Threading.Threading import ThreadHandler
from Infinitum.Core.DesktopWindowManager import DWM

def init():
    Threader = ThreadHandler()
    WinManager = DWM.init(Threader=Threader)
    return WinManager