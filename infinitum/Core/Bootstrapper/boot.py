#Context switch for normal or first time boot

from Infinitum.Core.Bootstrapper import BootLoader, InstallBoot

def boot():
    return BootLoader.init()