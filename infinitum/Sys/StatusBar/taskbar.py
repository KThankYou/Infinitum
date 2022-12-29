from Infinitum.Core.DesktopWindowManager.Window import Frame
from Infinitum.Core.Fonts.IOHandler import Button, DropdownMenu, TextHandler
from typing import Tuple, Dict
import pygame, datetime

text = TextHandler()
_Shutdown = Button('Shutdown', Font=text.font, box_color=(200, 200, 200), text_size=18)
_Restart = Button('Restart', Font=text.font, box_color=(200, 200, 200), text_size=18)
_Lock = Button('Lock', Font=text.font, box_color=(200, 200, 200), text_size=18)
font = pygame.font.Font(text.font, 18)
_default_power = pygame.image.load(r'.\Infinitum\Sys\StatusBar\default_power.png')

class Taskbar:
    def __init__(self, display_res: Tuple[int, int] = (1600, 900), thickness: int = 60, processes: Dict[Tuple[pygame.Surface, Frame], pygame.Rect] = {},
            color: Tuple[int, int, int] = (210, 210, 210), power_image: pygame.Surface = _default_power) -> None:
        self.rect = pygame.Rect(0, display_res[1]-thickness, display_res[0], thickness)
        self.surf = pygame.Surface(self.rect.size)
        self.processes = processes
        self.power_options = DropdownMenu(self.rect.topleft, 0, 0, dropup=True, buttons=[_Shutdown, _Restart, _Lock])
        self.power_button_image = pygame.transform.smoothscale(power_image, (50, 50))
        self.power_button_rect = pygame.Rect((5, 5), (50, 50))
        self.color, self.alive = color, True
        self.power_options_visible = False
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
        
        self.power_options.set_pos((self.rect.right - self.power_options.width - 5, 5))
        if self.power_options_visible: 
            self.surf.blit(self.power_options.draw(), self.power_options.pos)
        
        self.set_datetime()
        
        return self.surf

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]) -> None:
        collision_rect = pygame.Rect(0, 0, 50, 50)
        collision_rect.x, collision_rect.y = self.rect.x, self.rect.y
        if collision_rect.collidepoint(*mouse_pos):
            self.power_options_visible = not self.power_options_visible
        else:
            for _, frame in self.processes.keys():
                collision_rect.x, collision_rect.y = self.rect.x+60, self.rect.y
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

