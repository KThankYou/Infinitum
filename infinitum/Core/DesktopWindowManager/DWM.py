from Infinitum.Sys.Taskbar.Taskbar import Taskbar, SHUTDOWN, RESTART
from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Sys.AppManager.AppMan import Installer, Uninstaller
from Infinitum.Core.Misc.TYPEHINTS import Frame, Icon
from Infinitum.Core.Misc.commons import CONTINUE

from typing import Tuple, List

import pygame

_bg = r'.\Assets\default_bg.jpg'

class DesktopWindowManager:
    def __init__(self, pwd: str, display: pygame.Surface = None, windows: List[Frame] = [], icons: List[Icon] = []) -> None:
        self.FM = FileManager(r'.\Infinitum.vc', pwd)
        self.bg = pygame.transform.smoothscale(pygame.image.load(_bg), display.get_size())
        self.icons, self.windows = list(icons), list(windows)
        self.grid = pygame.Rect(50, 50, 128, 128)
        self.display = display
        self.active = None
        self.installer = Installer(self.FM, max_res = display.get_size())
        self.uninstaller = Uninstaller(self.FM, self, self.installer)
        self.taskbar = Taskbar(install=self.installer.install, uninstaller = self.uninstaller.uninstaller)
        self.uninstaller.update_pos(*self.taskbar.power_options.rect.bottomleft)
        self.windows.append(self.taskbar)
        self.surf = pygame.Surface(self.FM.get_res(self.FM.drive_path))

    def main(self) -> None:
        fps, quit = pygame.time.Clock(), False
        fps.tick(30)
        self.active = None
        while not quit:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    break
                
                self.surf.blit(self.bg, (0, 0))
                mouse_pos = pygame.mouse.get_pos()

                # Draw all icons
                for icon in self.icons: icon.draw(self.surf, icon.rect)

                # Set active window to None if mouse is clicked outside any windows
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_in_window = False
                    for index in range(-1, -len(self.windows)-1, -1):
                        window = self.windows[index]
                        if window.get_rect().collidepoint(*mouse_pos):
                            mouse_in_window = True
                            # Check if mouse is within a window, and if so, set that window to active
                            if event.button == 1:
                                self.active = window
                                self.windows.remove(self.active)
                                self.windows.append(self.active)
                            break
                    
                    else:
                        if self.taskbar.power_options.visible:
                            if self.taskbar.power_options.rect.collidepoint(*mouse_pos) and event.button == 1:
                                self.active = self.taskbar.power_options
                                mouse_in_window = True
                            else: 
                                self.taskbar.power_options.visible = False

                    if not mouse_in_window:
                        self.active = None

                if self.active is None: self.handle_event(event, mouse_pos)
                else:
                    try: self.active.handle_event(event, mouse_pos)
                    except SHUTDOWN: 
                        #self.FM.MFT.consolidate()
                        self.FM.flush()
                        return self.shutdown(0)
                    except RESTART: return self.shutdown(2)
                    except CONTINUE: continue
                    # Update the position of the window if it is being dragged
                    if (self.taskbar not in (self.active, window)) and self.active.drag:
                        self.active.update_pos(x=mouse_pos[0] - window.drag_offset[0], y=mouse_pos[1] - window.drag_offset[1])
                self.refresh()
            self.refresh()

    def refresh(self) -> None:
        # Draw all alive windows and remove dead ones
        windows, process_num = [], 0
        for window in self.windows:
            if window.alive and window:
                process_num += 1
                windows.append(window)
                self.surf.blit(window.draw(), window.get_rect())

        if self.taskbar.power_options.visible: 
            self.surf.blit(self.taskbar.power_options.draw(), self.taskbar.power_options.rect)
        
        # Stuff for optimization, makes it so that the taskbar only redraws if necessary
        self.windows = windows
        self.taskbar.process_num = process_num

        self.display.blit(self.surf, (0,0))
        pygame.display.update()
        self.get_apps()

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for icon in self.icons:
                if icon.rect.collidepoint(*mouse_pos):
                    process = icon.launch(self.installer.paths[icon.name].name)
                    self.windows.append(process)
                    self.taskbar.add_process(icon.image, process)
    
    def add_icon(self, icon: Icon) -> None:
        x, y = self.grid.topleft
        size = self.grid.h
        if x + size > 1500: x, y = - 100, y + 150
        grid = self.grid
        self.grid = pygame.Rect(x + 150, y, size, size)
        icon.rect = grid
        self.icons.append(icon)
    
    def shutdown(self, code = 0) -> int:
        self.FM.close()
        return code
    
    def get_apps(self) -> None:
        apps = self.FM.get_apps()
        if len(apps) == len(self.icons): return 
        installed = {i.name: True for i in self.icons}
        for name, metadata in apps.items():
            if not installed.get(name, False):
                self.add_icon(self.installer.get_icon(metadata))
        self.update_icons()

    def update_icons(self):
        icons, self.icons = self.icons, []
        self.grid = pygame.Rect(50, 50, 128, 128)
        for icon in icons:
            self.add_icon(icon)

def start(display: pygame.Surface, pwd: str) -> int:
    dwm = DesktopWindowManager(pwd, display = display)
    return dwm.main()
    
 