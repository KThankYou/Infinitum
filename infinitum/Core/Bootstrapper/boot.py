#Context switch for normal or first time boot
from Infinitum.Core.Bootstrapper import BootLoader, InstallBoot

import pygame
import os

def boot():
    pygame.init()
    installed = os.path.exists(r'.\Infinitum.vc') and BootLoader.init()
    if not installed:
        install = InstallBoot.Installer()
        install.main()
    pygame.quit()