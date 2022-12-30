from Infinitum.commons import font_18 as font, font_name as FONT
from Infinitum.Core.DesktopWindowManager.Window import Frame
from Infinitum.Core.Fonts.CompoundIO import DropDownMenu
from Infinitum.Core.Fonts.SimpleIO import Button
from typing import Tuple, Dict
import pygame, datetime

class SHUTDOWN(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    @classmethod
    def _raise(cls, *args, **kwargs):
        raise SHUTDOWN

class RESTART(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    @classmethod
    def _raise(cls, *args, **kwargs):
        raise RESTART

_Shutdown = Button('Shutdown', Font=FONT, box_color=(200, 200, 200), text_size=14, function= SHUTDOWN._raise)
_Restart = Button('Restart', Font=FONT, box_color=(200, 200, 200), text_size=14, function= RESTART._raise)
_Install = Button('Install', Font=FONT, box_color=(200, 200, 200), text_size=14)
_default_power = pygame.image.load(r'.\Infinitum\Sys\Taskbar\default_power.png')

class Taskbar:
    def __init__(self, display_res: Tuple[int, int] = (1600, 900), thickness: int = 60, processes: Dict[Tuple[pygame.Surface, Frame], pygame.Rect] = {},
            color: Tuple[int, int, int] = (210, 210, 210), power_image: pygame.Surface = _default_power) -> None:
        self.rect = pygame.Rect(0, display_res[1]-thickness, display_res[0], thickness)
        self.surf = pygame.Surface(self.rect.size)
        self.processes = processes
        self.power_options = DropDownMenu(self.rect.topleft, dropup=True, buttons=[_Shutdown, _Restart, _Install])
        self.power_button_image = pygame.transform.smoothscale(power_image, (50, 50))
        self.power_button_rect = pygame.Rect((5, 5), (50, 50))
        self.color, self.alive = color, True

        self.refresh()

    def add_process(self, image: pygame.Surface, process: Frame) -> None:
        self.processes[(image, process)] = self.calculate_icon_position()
        self.process_num += 1
        
    def calculate_icon_position(self) -> Tuple[int, int]:
        return pygame.Rect(self.rect.left + 60*(len(self.processes)+1) + 10, 5, 50, 50)
    
    # Remove dead apps
    def refresh(self) -> None:
        processes = {}
        prev_rect = pygame.Rect(0, 5, 60, 50)
        self.process_num = 0
        for key, rect in self.processes.items():
            if key[1].alive:
                rect.left = prev_rect.right + 10
                processes[key] = rect
                prev_rect = rect
                self.process_num += 1
        self.processes = processes   

    def draw(self):
        if len(self.processes) != self.process_num: self.refresh()
        self.surf.fill(self.color)
        self.surf.blit(self.power_button_image, self.power_button_rect.topleft)

        for process, rect in self.processes.items():
            thumbnail, frame = process
            if frame.alive:
                thumbnail = pygame.transform.scale(thumbnail, (50, 50))
                self.surf.blit(thumbnail, rect)
        self.set_datetime()
        
        return self.surf

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]) -> None:
        collision_rect = pygame.Rect(0, 0, 50, 50)
        collision_rect.x, collision_rect.y = self.rect.x, self.rect.y
        if collision_rect.collidepoint(*mouse_pos) and event.type == event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.power_options.visible = True
        else:
            for _, frame in self.processes.keys():
                collision_rect.x = collision_rect.x+60
                if collision_rect.collidepoint(*mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if frame.minimize: frame.restore()
                    else: frame.mini()
    
    def set_datetime(self) -> None:
        now = datetime.datetime.now()
        time_text = font.render(now.strftime("%I:%M %p"), True, (0, 0, 0))
        date_text = font.render(now.strftime("%b %d, %Y"), True, (0, 0, 0))
        d_rect, t_rect = date_text.get_rect(), time_text.get_rect()
        d_rect.bottomright = self.rect.w-20, self.rect.h-5
        t_rect.centerx, t_rect.bottom = d_rect.centerx, d_rect.top
        self.surf.blit(time_text, t_rect)
        self.surf.blit(date_text, d_rect)

    def get_rect(self) -> pygame.Surface:
        return self.rect

