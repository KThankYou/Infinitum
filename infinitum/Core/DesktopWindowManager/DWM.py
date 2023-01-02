from Infinitum.Sys.Taskbar.Taskbar import Taskbar, SHUTDOWN, RESTART
from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Sys.AppManager.AppMan import AppMan
from Infinitum.Core.Misc.TYPEHINTS import Frame, Icon

from typing import Tuple, List

import pygame

_bg = r'.\Infinitum\Core\DesktopWindowManager\default_bg.jpg'

class DesktopWindowManager:
    def __init__(self, pwd: str, display: pygame.Surface = None, windows: List[Frame] = [], icons: List[Icon] = []) -> None:
        self.FM = FileManager(r'.\Infinitum.vc', pwd)
        self.bg = pygame.transform.smoothscale(pygame.image.load(_bg), display.get_size())
        self.icons, self.windows = list(icons), list(windows)
        self.grid = pygame.Rect(50, 50, 128, 128)
        self.display = display
        self.AppMan = AppMan(self.FM, max_res = display.get_size())
        self.taskbar = Taskbar(install=self.AppMan.install)
        self.windows.append(self.taskbar)


    def main(self):
        fps, quit = pygame.time.Clock(), False
        fps.tick(30)
        surf = pygame.Surface((1600, 900))
        self.active = None
        while not quit:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    break
                
                surf.blit(self.bg, (0, 0))
                mouse_pos = pygame.mouse.get_pos()

                # Draw all icons
                for icon in self.icons: icon.draw(surf, icon.rect)

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
                    except SHUTDOWN: return self.shutdown(0)
                    except RESTART: return self.shutdown(2)
                    # Update the position of the window if it is being dragged
                    if (self.taskbar not in (self.active, window)) and self.active.drag:
                        self.active.update_pos(x=mouse_pos[0] - window.drag_offset[0], y=mouse_pos[1] - window.drag_offset[1])
                if self.taskbar.power_options.visible: surf.blit(self.taskbar.power_options.draw(), self.taskbar.power_options.rect)
                # Draw all alive windows
                windows, process_num = [], 0
                for window in self.windows:
                    if window.alive:
                        process_num += 1
                        windows.append(window)
                        surf.blit(window.draw(), window.get_rect())
                self.windows = windows
                self.taskbar.process_num = process_num

                self.display.blit(surf, (0,0))
                pygame.display.update()
                self.get_apps()

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for icon in self.icons:
                if icon.rect.collidepoint(*mouse_pos):
                    process = icon.launch(self.FM.temp())
                    self.windows.append(process)
                    self.taskbar.add_process(icon.image, process)
    
    def add_icon(self, icon: Icon):
        x, y = self.grid.topleft
        size = self.grid.h
        if x + size > 1500: x, y = - 100, y + 150
        grid = self.grid
        self.grid = pygame.Rect(x + 150, y, size, size)
        icon.rect = grid
        self.icons.append(icon)
    
    def shutdown(self, code = 0):
        self.FM.close()
        return code
    
    def get_apps(self):
        apps = self.FM.get_apps()
        if len(apps) == len(self.icons): return 
        installed = {i.name: True for i in self.icons}
        for name, metadata in apps.items():
            if not installed.get(name, False):
                self.add_icon(self.AppMan.get_icon(metadata))


def start(display: pygame.Surface, pwd: str):
    dwm = DesktopWindowManager(pwd, display = display)
    return dwm.main()
    
 