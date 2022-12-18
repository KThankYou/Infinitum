from Infinitum.Core.Bootstrapper import boot


import pygame
import os


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def init():
    pygame.init()
    boot.boot()