from Infinitum.Core.Fonts.IOHandler import Button, TextHandler
from typing import Tuple
import pygame

class _Process:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def draw(self) -> pygame.Surface:
        raise NotImplementedError

    def handle_event(self) -> None:
        raise NotImplementedError

text = TextHandler()

class Frame:
    def __init__(self, process: _Process, border: bool = True, fullscreen: bool = False, name: str = None,
                pos: Tuple[int, int] = (0, 0), size: Tuple[int, int] = (0, 0), max_res: Tuple[int, int] = (1600, 900)) -> None:
        self.process = process
        self.border = border
        self.rect = pygame.Rect(*pos, *size)
        self.alive = True
        self.active = self.drag = False

        close_button = Button(' X ', Font= text.font, border = True, hover_color=pygame.Color('#C80815'), 
                                function=self.close, text_size=16, border_color=(200,200,200))
        mini_button = Button(' − ', Font= text.font, border = True, function=self.mini, text_size=16, border_color=(200,200,200))
        self.buttons = {'close': close_button, 'mini': mini_button}

        if self.border:
            self.rect.size = (self.rect.w+2, self.rect.h + 31)

        self.top_border = pygame.Rect(*self.rect.topleft, self.rect.right, 30)
        self.surf = pygame.Surface(self.rect.size)
        size = self.rect.size
        if self.border: 
            size = (max(self.rect.w-2, 0), max(self.rect.h-30, 0))
            self.surf.fill((0, 0, 0))
        self.display_surf = pygame.Surface(size)
        
    def draw(self) -> pygame.Surface:
        for process_surf in self.process.draw():
            pos = process_surf.get_rect()
            pos.center = self.display_surf.get_rect().center
            self.display_surf.blit(process_surf, pos)

            if self.border:
                button_offset = 30
                for button in self.buttons.values():
                    pos = self.top_border.topright
                    button.set_pos( *(pos[0] - button_offset, 0) )
                    self.surf.blit(button.draw(), button.get_rect())
                    button_offset += 30
            
            self.surf.blit(self.display_surf, (1, 30))
            return self.surf

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int], active: bool = True) -> None:
        if not active:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drag_offset = (event.pos[0] - self.rect.left, event.pos[1] - self.rect.top)
            self.drag = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.drag = False
        self.process.handle_event(event, mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse click occurred within the top border of the window
            if self.top_border.collidepoint(*self.drag_offset):
                # Check if the mouse click occurred within the boundaries of any buttons
                for button in self.buttons.values():
                    if button.get_rect().collidepoint(*self.drag_offset):
                        # Call the on_click method of the button
                        button.on_click()
                # Set the drag attribute to True and the drag_offset attribute to the offset between the top-left corner of the window and the mouse position
                self.drag = True
                self.drag_offset = (event.pos[0] - self.rect.left, event.pos[1] - self.rect.top)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Set the drag attribute to False when the mouse button is released
            self.drag = False
        elif event.type == pygame.MOUSEMOTION:
            if self.drag:
                # Update the position of the window based on the current mouse position and the drag_offset
                self.update_pos(x=event.pos[0] - self.drag_offset[0], y=event.pos[1] - self.drag_offset[1])

    def update_pos(self, x: int = None, y: int = None, w: int = None, h: int = None) -> None:
        self.rect.topleft = ((x, self.rect.x)[x is None], (y, self.rect.y)[y is None])
        self.rect.size = ((w, self.rect.size[0])[w is None] , (h, self.rect.size[1])[h is None])
    
    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def get_pos(self) -> Tuple[int, int]:
        return self.rect.topleft
    
    def get_size(self) -> Tuple[int, int]:
        return self.rect.size

    def mini(self) -> None:
        self.active = False
        self.rect.size = (0, 0)

    def close(self) -> None:
        self.alive = False

class _dummy_process:
    def __init__(self) -> None:
        self.running = True
        self.color = (0, 0, 0)
        self.colors = _dummy_process.COLORS()

    def draw(self) -> pygame.Surface:
        surf = pygame.Surface((480, 360))
        while self.running:
            surf.fill(self.color)
            yield surf

    def handle_event(self, *args, **kwargs):
        self.color = next(self.colors)
    
    @staticmethod
    def COLORS():
        while True:
            for i in ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)):
                yield i

_dummy_window1 = Frame(_dummy_process(), size=(480, 360))
_dummy_window2 = Frame(_dummy_process(), size=(480, 360))
