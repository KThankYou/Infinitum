from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Core.DesktopWindowManager.Icons import Icon, _dummy_icon_gen
from typing import Tuple

import pygame

_bg = r'.\Infinitum\Core\DesktopWindowManager\default_bg.jpg'

class DesktopWindowManager:
    def __init__(self, Threader, pwd: str) -> None:
        self.FM = FileManager(r'.\Infinitum.vc', pwd) # Ignore
        self.__threader = Threader # Ignore
        self.bg = pygame.image.load(_bg)
        self.icons, self.windows = [], []
        self.grid = pygame.Rect(50, 50, 128, 128)

    def draw(self):
        pygame.init()
        fps = pygame.time.Clock()
        fps.tick(30)
        disp, quit = pygame.display.set_mode((1600, 900)), False
        surf = pygame.Surface((1600, 900))
        self.active = None
        #_dummy_icon_gen()
        for _ in range(2): self.add_icon(_dummy_icon_gen, process_size = (480, 360))
        while not quit:
            pygame.display.flip()
            self.windows = [window for window in self.windows if window.alive]
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
                    for window in self.windows:
                        if window.get_rect().collidepoint(*mouse_pos):
                            mouse_in_window = True
                            # Check if mouse is within a window, and if so, set that window to active
                            if event.button == 1:
                                self.active = window
                                self.windows.remove(self.active)
                                self.windows.append(self.active)
                            break
                    if not mouse_in_window:
                        self.active = None
                
                if self.active is None: self.handle_event(event, mouse_pos)
                else:
                    self.active.handle_event(event, mouse_pos)
                    # Update the position of the window if it is being dragged
                    if self.active.drag:
                        self.active.update_pos(x=mouse_pos[0] - window.drag_offset[0], y=mouse_pos[1] - window.drag_offset[1])

                # Draw all alive windows
                surf.blits(blit_sequence=((window.draw(), window.get_rect()) for window in self.windows if window.alive))

                disp.blit(surf, (0,0))
                pygame.display.update()
        pygame.quit()

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for icon in self.icons:
                if icon.rect.collidepoint(*mouse_pos):
                    self.windows.append(icon.launch())
    
    def add_icon(self, icon_gen: Icon, **kwargs):
        x, y = self.grid.topleft
        size = self.grid.h
        if x + size > 1500: x, y = - 100, y + 150
        grid = self.grid
        self.grid = pygame.Rect(x + 150, y, size, size)
        kwargs['rect'] = grid
        self.icons.append(icon_gen(**kwargs))

def init(Threader, pwd: str):
    dwm = DesktopWindowManager(Threader, pwd)
    dwm.draw()