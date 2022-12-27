# Handle normal boot
from Infinitum.Core.Threading.Threading import ThreadHandler
from Infinitum.Core.DesktopWindowManager import DWM
from Infinitum.Core.Storage.FileManager import FileManager

def init():
    FM = FileManager(r'.\Infinitum.vc')
    if not FM.MBT.config['installed']: return False
    Threader = ThreadHandler()
    DWM.init(Threader=Threader)
    return True