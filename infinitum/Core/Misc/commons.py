# some common stuff a few files use
# moved here as to give slightly more performance

from Infinitum.Core.Fonts.SimpleIO import TextHandler
import pygame

empty_surf = pygame.Surface((0, 0))
empty_rect = pygame.Rect(0, 0, 0, 0)
text = TextHandler()
font_name = text.font
font_12 = pygame.font.Font(font_name, 12)
font_18 = pygame.font.Font(font_name, 18)
font_21 = pygame.font.Font(font_name, 21)

class CONTINUE(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)