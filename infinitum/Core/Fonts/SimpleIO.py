from Infinitum.Core.Misc.CONSTANTS import Pattern_TextHandler

from typing import Tuple, Callable, List

import pygame
import sys

_FONT = {
    'OpenSans': r'.\Infinitum\Core\Fonts\OpenSans\OpenSans-VariableFont_wdth,wght.ttf',
    
    }


_KWARGS = {
        # U = underline, B = bold, I = Italic, S = Strikethrough
        
        # 0 = UBIS, 1 = UBI, 2 = U, 3 = UB, 4 = UI, 5 = BI, 6 = B+mini, 7 = mini
        'Header0': {'U': True, 'B': True, 'I': True, 'S': True, 'size': 44},
        'Header1': {'U': True, 'B': True, 'I': True, 'S': False, 'size': 44},
        'Header2': {'U': True, 'B': False, 'I': False, 'S': False, 'size': 44},
        'Header3': {'U': True, 'B': True, 'I': False, 'S': False, 'size': 44},
        'Header4': {'U': True, 'B': False, 'I': True, 'S': False, 'size': 44},
        'Header5': {'U': False, 'B': True, 'I': True, 'S': False, 'size': 44},
        'Header6': {'U': False, 'B': True, 'I': False, 'S': False, 'size': 32},
        'Header6': {'U': False, 'B': False, 'I': False, 'S': False, 'size': 32},

        # 0 = UBI, 1 = None, 2 = U, 3 = B, 4 = I, 5 = mini
        'Text0': {'U': True, 'B': True, 'I': True, 'S': False, 'size': 20},
        'Text1': {'U': False, 'B': False, 'I': False, 'S': False, 'size': 20},
        'Text2': {'U': True, 'B': False, 'I': False, 'S': False, 'size': 20},
        'Text3': {'U': False, 'B': True, 'I': False, 'S': False, 'size': 20},
        'Text4': {'U': False, 'B': False, 'I': True, 'S': False, 'size': 20},
        'Text5': {'U': False, 'B': False, 'I': True, 'S': False, 'size': 18},
        }

pygame.font.init()

class TextHandler:
    def __init__(self, font: str = 'OpenSans', starting: Tuple = (0, 0)) -> None:
        if font not in _FONT: raise ValueError('Font Does not exist')
        self.font = _FONT[font]
        self.underline = self.bold = self.italic = False
        self.__default_pos = self.pointer = starting

    # U = underline, B = bold, I = Italic, S = Strikethrough
    def write(self, text: str, color: tuple | pygame.Color, surface: pygame.Surface, size: int = None, width: bool = None,
        U: bool = False, B: bool = False, I: bool = False, S: bool = False, newline_width: int = 20, special_flags: List = 0) -> None:

        if not isinstance(size, int) or size <= 0: raise ValueError('Size must be a positive integer')

        font = pygame.font.Font(self.font, size)
        font.set_underline(U); font.set_bold(B); font.set_italic(I); font.set_strikethrough(S)

        lines, line, line_height = [], '', font.get_linesize()

        # Set the width to the width of the surface if it is not provided
        if width is None: width = surface.get_width()*.95
        elif width <= 0: raise ValueError('Width must be a positive integer')
        
        # Split the text into words
        words = [max(word) for word in Pattern_TextHandler.findall(text)]
        for word in words:
            # Check if the current word does not fit on the current line, or if the word is a newline character
            # then add the current line to the list of lines and reset the line
            if font.size(line + word)[0] > width - self.pointer[0] or word == '\n': 
                lines, line = lines + [line.strip('\n').strip(' ')], ''
            line += word + ' '

        # Add the last line to the list of lines
        lines.append(line.strip('\n').strip(' '))

        # Render the lines and blit them onto the surface
        y = 0
        for line in lines:
            # If the line is a newline character, skip it and just increase the y position
            if line == '': 
                y += newline_width
                continue
            rendered_line = font.render(line, True, color)
            surface.blit(rendered_line, (self.pointer[0], self.pointer[1] + y), special_flags=special_flags)
            y += line_height

        while lines and lines[-1] == '': lines.pop()

        # Set the position of the TextHandler object to the final position of the rendered text
        self.pointer = self.pointer[0], self.pointer[1] + y + newline_width

    def set_pos(self, x: int = 0, y: int = 0) -> None: 
        self.pointer = (x, y)

    def get_pos(self) -> Tuple[int]: 
        return self.pointer

    def reset_pos(self) -> None: 
        self.pointer = self.__default_pos
    
    #Wrapper for write and supports the formats in _KWARGS
    def print(self, text: str, color: tuple | pygame.Color, surface: pygame.Surface, 
            width: bool = None, modifier: str = 'Text1', newline_width: int = 20, special_flags: List = 0) -> None:
        self.write(text, color, surface, width = width, newline_width = newline_width, special_flags = special_flags, **_KWARGS[modifier])
    
    def get_rect(self, text: str, size: int = 20, bold: bool = False, modifier: str = None, center: pygame.Rect = None) -> pygame.Rect:
        if modifier:
            modifier = _KWARGS[modifier]
            size, bold = modifier['size'], modifier['B']
        font = pygame.font.Font(self.font, size)
        font.set_bold(bold)
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface.get_rect() if not center else text_surface.get_rect(center = center.center)

def NOTHING(*args, **kwargs) -> None: return #Does Nothing

class Button:
    def __init__(self, 
            text: str, Font: str, text_color: Tuple[int] = (255, 255, 255), box_color: Tuple[int] = (0, 0, 0),
            function: Callable = NOTHING, margin: Tuple[int] = (7, 7), text_size: Tuple[int] = 20, pos = (0, 0), border_size: int = 1,
            hover_color: Tuple[int] = (200, 200, 200), border: bool = False, border_color: Tuple[int, int, int] = (0, 0, 0)) -> None:

        font = pygame.font.Font(Font, text_size)
        self.text = text
        text_surf = font.render(text, True, text_color)
        self.box_color = box_color

        button_surface = pygame.Surface((font.size(text)[0] + margin[0] * 2, text_size + margin[1] * 2))
        button_surface_hover = pygame.Surface((font.size(text)[0] + margin[0] * 2, text_size + margin[1] * 2))
        button_surface.fill(box_color)
        button_surface_hover.fill(hover_color)
        if border:
            rect = button_surface.get_rect()
            pygame.draw.rect(button_surface, border_color, rect, border_size)
            pygame.draw.rect(button_surface_hover, border_color, rect, border_size)
        
        text_pos = ((button_surface.get_width() - text_surf.get_width()) // 2, (button_surface.get_height() - text_surf.get_height()) // 2)
        button_surface.blit(text_surf, text_pos) 
        button_surface_hover.blit(text_surf, text_pos) 

        self.rect = pygame.Rect(pos, button_surface.get_size())
        self.button_surface, self.button_surface_hover = button_surface, button_surface_hover
        self.function = function
        self.hover = False

    def on_click(self, generator = False, *args, **kwargs):
        return self.function if generator else self.function(*args, **kwargs)

    def __repr__(self) -> str:
        return f'Button({self.text})'

    def draw(self) -> Tuple[pygame.Surface]:
        # Return the button surface and a rectangle representing the button
        return (self.button_surface, self.button_surface_hover)[self.hover]

    def get_pos(self) -> Tuple[int]:
        return self.rect.topleft

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def set_pos(self, x: int = None, y: int = None) -> None:
        self.rect.topleft = (x or self.rect.x, y or self.rect.y)

class TextBox:
    def __init__(self, 
            placeholder: str, font: str, text_color: Tuple[int] = (0, 0, 0), box_color: Tuple[int] = (255, 255, 255),
            size: Tuple[int] = (100, 30), text_size: Tuple[int] = 20, pos = (0, 0), password: bool = False,
            border_size: int = 1, border: bool = False, border_color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        self.rect = pygame.Rect(*pos, *size)
        self.surf = pygame.Surface(size)
        self.active = False
        self.password = password
        self.border = border
        self.border_color = border_color
        self.border_size = border_size
        self.text = ''
        self.font = pygame.font.Font(font, text_size)
        self.box_color = box_color
        self.text_color = text_color
        self.placeholder = placeholder

    def draw(self) -> pygame.Surface:
        self.surf.fill(self.box_color)
        if self.border:
            rect = self.surf.get_rect()
            pygame.draw.rect(self.surf, (0,0,0), rect, 1)
        # If the text attribute is empty, use the placeholder text
        display_text = self.text or self.placeholder
        if self.text and self.password:
            display_text = '*'*len(self.text)

        # Calculate the width and height of the text box based on the font size
        text_width, text_height = self.font.size(display_text)
        box_width, box_height = self.rect.size

        # Render the text onto the text box surface
        text_surface = self.font.render(display_text + ('|' if self.active else ''), True, self.text_color)

        # Calculate the position of the text within the text box
        text_x = (box_width - text_width) // 2
        text_y = (box_height - text_height) // 2
        
        # Blit the text onto the text box surface
        self.surf.blit(text_surface, (text_x, text_y))
                
        return self.surf
    
    def typing(self) -> None:
        self.active = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.active = False
                    break
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.get_rect().collidepoint(*mouse_pos):
                    self.active = False
                    break

        return self.draw()
    
    def set_pos(self, x: int = None, y: int = None) -> None:
        self.rect.topleft = (x or self.rect.x, y or self.rect.y)

    def get_pos(self) -> Tuple[int, int]:
        return self.rect.topleft

    def set_size(self, w: int = None, h: int = None) -> None:
        self.rect.size = (w or self.rect.w, h or self.rect.h)
    
    def get_size(self) -> Tuple[int, int]:
        return self.rect.size
    
    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_text(self) -> str:
        return self.text


