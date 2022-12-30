from Infinitum.Core.DesktopWindowManager.Window import Frame
from Infinitum.Core.Fonts.SimpleIO import Button
from Infinitum.commons import empty_surf
from typing import List, Tuple, Dict
import pygame


class _Dropdown:
    def __init__(self, width: int, height: int, buttons: List[Button],
                gap_color: Tuple[int, int, int], gap_size: int, *args, **kwargs) -> None:
        self.rect = pygame.Rect(0, 0, width, 0)
        self.default_height = height
        self.surf = empty_surf
        self.gap_color = gap_color
        self.gap_size = gap_size
        self.buttons = self.__get_rects(buttons)
        self.refresh()
    
    def refresh(self) -> None:
        self.surf = pygame.Surface((self.rect.w, (self.default_height)*len(self.buttons) + self.gap_size))
        self.surf.fill(self.gap_color)
        surf = pygame.Surface((self.rect.w, self.default_height))
        for button, rect in self.buttons.items():
            surf.fill(button.box_color)
            surf.blit(button.draw(), (0, 0))
            self.surf.blit(surf, rect)

    def __get_rects(self, buttons: List[Button]) -> Dict[Button, pygame.Rect]:
        self.rect.y, self.rect.height = 0, self.default_height + self.gap_size
        buttons_dict = {}
        for button in buttons:
            buttons_dict[button] = self.rect.copy()
            self.rect.y = self.rect.h
            self.rect.h += self.default_height + self.gap_size
        return buttons_dict

    def draw(self) -> pygame.Surface:
        while True: yield self.surf

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int], abs_pos: pygame.Rect, *args, **kwargs) -> None:
        for button, rect in self.buttons.items():
            collision = rect.collidepoint(mouse_pos[0], mouse_pos[1] - abs_pos.y + rect.y)
            if collision and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button.on_click()

class DropDownMenu:
    def __init__(self, pos: Tuple[int, int], width: int = 200, height: int = 30, dropup: bool = False, 
                buttons: List[Button] = [], gap_color: Tuple[int, int, int] = (0, 0, 0), gap_size: int = 2) -> None:
        if dropup: buttons = buttons[::-1]
        menu = _Dropdown(width, height, buttons, gap_color = gap_color, gap_size= gap_size)
        self.window = Frame(process=_Dropdown, border=False, size=(width, menu.rect.y), 
                    width=width, height=height, buttons=buttons, gap_color=gap_color, gap_size=gap_size)
        if dropup: pos = pos[0], pos[1]-self.window.rect.bottom
        self.window.update_pos(*pos)
        self.rect = pygame.Rect(*pos, width, self.window.rect.h)
        self.visible = False

    def draw(self) -> pygame.Surface:
        return self.window.draw()

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]):
        self.window.handle_event(event, mouse_pos, active=True, abs_pos = self.rect)
        self.visible = False