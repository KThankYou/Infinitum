from Infinitum.Core.APIHandler.APIHandler import APIHandler
from multiprocessing import Queue

import pygame

class DesktopWindowManager:
    def __init__(self, _queue: Queue, _EXIT: Queue, Threader) -> None:
        self.__queue, self.__exit, self.__threader = _queue, _EXIT, Threader
        self.__api = APIHandler()

    def draw(self):
        pygame.init()
        fps = pygame.time.Clock()
        fps.tick(30)
        disp, quit = pygame.display.set_mode((1600, 900)), False
        while not quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit = True; break
                
                surf = pygame.Surface((1600, 900))
                surf.blit(pygame.image.load(r'C:\Users\K-PC\Videos\The Witcher 3\The Witcher 3 Screenshot 2022.12.16 - 18.49.57.18.png'), (0, 0))
                
                disp.blit(surf, (0,0))
                pygame.display.flip()
        pygame.quit()

def init(_queue: Queue, _EXIT: Queue, Threader):
    dwm = DesktopWindowManager(_queue, _EXIT, Threader)
    dwm.draw()