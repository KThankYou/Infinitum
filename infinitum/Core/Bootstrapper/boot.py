#Context switch for normal or first time boot

from Infinitum.Core.Bootstrapper import BootLoader, InstallBoot
import os

def boot():
    installed = os.path.exists(r'.\Infinitum.vc') and BootLoader.init()
    if not installed:
        install = InstallBoot.Installer()
        install.main()