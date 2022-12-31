from Infinitum.Core.DesktopWindowManager.Window import Frame, _dummy_process
from Infinitum.TYPEHINTS import _Process
from Infinitum.commons import font_18 as font, empty_rect

from typing import Tuple

import pygame

default_icon = r'.\Infinitum\Core\DesktopWindowManager\default_thumb.png'
default_image = pygame.image.load(default_icon)


class Icon:
    def __init__(self, process: _Process, name: str = 'name_placeholder', process_size: Tuple[int, int] = (0, 0), 
    image: str = None, rect: pygame.Rect = empty_rect, fullscreen: bool = False, max_res: Tuple[int, int] = (1600, 900),
    draggable: bool = True, resizeable: bool = True, *args, **kwargs) -> None:
        self.image = default_image if image is None else pygame.image.load(image)
        self.image = pygame.transform.smoothscale(self.image, (128, 128))
        self.process = process
        self.name = name[:15]
        self.text = font.render(self.name, True, (0, 0, 0))
        self.rect = rect
        self.active = False
        self.process_size = process_size
        self.fullscreen = fullscreen
        self.max_res = max_res
        self.draggable = draggable
        self.resizeable = resizeable

        self.args, self.kwargs = args, kwargs

    def launch(self, working_dir: str) -> Frame:
        # Create a new window using the process associated with this icon
        window = Frame(self.process, name=self.name, size=self.process_size, fullscreen = self.fullscreen, 
                max_res = self.max_res, working_dir = working_dir, draggable = self.draggable,
                resizeable = self.resizeable, *self.args, **self.kwargs)
        return window

    def draw(self, surf: pygame.Surface, rect: pygame.Rect) -> pygame.Surface:
        surf.blit(self.image, rect)
        surf.blit(self.text, self.rect.bottomleft)
    
    def set_psize(self, x: int = None, y: int = None):
        self.process_size = ((x, self.process_size[0])[x is None], (y, self.process_size[1])[y is None])

    def update_pos(self, x: int = None, y: int = None, w: int = None, h: int = None) -> None:
        self.rect.topleft = ((x, self.rect.x)[x is None], (y, self.rect.y)[y is None])
        self.rect.size = ((w, self.rect.size[0])[w is None] , (h, self.rect.size[1])[h is None])

def _dummy_icon_gen(*args, **kwargs) -> Icon:
    return Icon(_dummy_process, name='dummy icon', *args, **kwargs)