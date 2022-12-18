from Infinitum.Core.Bootstrapper import Boot


import pygame
import os


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def init():
    pygame.init()
    for i in Boot.boot():
        print(i)