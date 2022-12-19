from Infinitum.Core.APIHandler.APIHandler import APIHandler
from multiprocessing import Queue

import pygame

class DesktopWindowManager:
    def __init__(self, Threader) -> None:
        self.__threader = Threader
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
                surf.fill((255, 255, 255))
                
                disp.blit(surf, (0,0))
                pygame.display.flip()
        pygame.quit()

def init(Threader):
    dwm = DesktopWindowManager(Threader)
    dwm.draw()