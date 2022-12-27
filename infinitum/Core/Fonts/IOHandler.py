from typing import Tuple, Callable, Pattern

import pygame, re, sys

_FONT = {
    'OpenSans': r'.\Infinitum\Core\Fonts\OpenSans\OpenSans-VariableFont_wdth,wght.ttf',
    
    }

_P = re.compile(r'(\n|[^\s]+)|(?: ( +) )')

class TextHandler:
    def __init__(self, font: str = 'OpenSans', starting: Tuple = (0, 0)) -> None:
        if font not in _FONT: raise ValueError('Font Does not exist')
        self.font = _FONT[font]
        self.underline = self.bold = self.italic = False
        self.__default_pos = self.pointer = starting

    # U = underline, B = bold, I = Italic, S = Strikethrough
    def write(self, 
        text: str, color: tuple | pygame.Color, surface: pygame.Surface, size: int = None, width: bool = None,
        U: bool = False, B: bool = False, I: bool = False, S: bool = False, newline_width: int = 20) -> None:

        if not isinstance(size, int) or size <= 0: raise ValueError('Size must be a positive integer')

        font = pygame.font.Font(self.font, size)
        font.set_underline(U); font.set_bold(B); font.set_italic(I); font.set_strikethrough(S)

        lines, line, line_height = [], '', font.get_linesize()

        # Set the width to the width of the surface if it is not provided
        if width is None: width = surface.get_width()*.95
        elif width <= 0: raise ValueError('Width must be a positive integer')
        
        # Split the text into words
        words = [max(word) for word in _P.findall(text)]
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
            surface.blit(rendered_line, (self.pointer[0], self.pointer[1] + y))
            y += line_height

        while lines and lines[-1] == '': lines.pop()

        # Set the position of the TextHandler object to the final position of the rendered text
        self.pointer = self.pointer[0], self.pointer[1] + y + newline_width

    def set_pos(self, x: int = 0, y: int = 0) -> None: self.pointer = (x, y)

    def get_pos(self) -> Tuple[int]: return self.pointer

    def reset_pos(self) -> None: self.pointer = self.__default_pos

def NOTHING(*args, **kwargs) -> None: return #Does Nothing

class Button:
    def __init__(self, 
            text: str, Font: str, text_color: Tuple[int] = (255, 255, 255), box_color: Tuple[int] = (0, 0, 0),
            function: Callable = NOTHING, margin: Tuple[int] = (7, 7), text_size: Tuple[int] = 20, pos = (0, 0),
            hover_color: Tuple[int] = (200, 200, 200)) -> None:
        # Box_gap is the distance between the borders of the box and the text in px
        self.text, self.function, self.text_color = text, function, text_color
        self.margin, self.text_size, self.font = margin, text_size, Font
        self.box_color, self.pos = box_color, pos
        self.rect = pygame.Rect(0,0,0,0)
        self.hover_color, self.hover = hover_color, False

    def on_click(self, generator = False, *args, **kwargs):
        return self.function if generator else self.function(*args, **kwargs)

    def draw(self) -> Tuple[pygame.Surface]:
        FONT = pygame.font.Font(self.font, self.text_size)
        # Create an empty surface for the button
        button_surface = pygame.Surface((FONT.size(self.text)[0] + self.margin[0] * 2, self.text_size + self.margin[1] * 2))
        button_surface.fill(self.box_color if not self.hover else self.hover_color)
        # Render the button text
        text = FONT.render(self.text, True, self.text_color)

        # Calculate the position of the text on the button surface
        text_x = (button_surface.get_width() - text.get_width()) // 2
        text_y = (button_surface.get_height() - text.get_height()) // 2

        # Blit the rendered text onto the button surface
        button_surface.blit(text, (text_x, text_y)) 

        # Update the rect attribute to represent the boundaries of the button surface
        self.rect = pygame.Rect(self.pos, button_surface.get_size())

        # Return the button surface and a rectangle representing the button
        return button_surface

    def get_pos(self) -> Tuple[int]:
        return self.pos

    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def set_pos(self, x: int = None, y: int = None) -> None:
        self.pos = (x or self.pos[0], y or self.pos[1])

class TextBox:
    def __init__(self, 
                 placeholder: str, font: str, text_color: Tuple[int] = (0, 0, 0), box_color: Tuple[int] = (255, 255, 255),
                 size: Tuple[int] = (100, 30), text_size: Tuple[int] = 20, pos = (0, 0), password: bool = False) -> None:
        self.placeholder = placeholder
        self.font = font
        self.text_color = text_color
        self.box_color = box_color
        self.size = size
        self.text_size = text_size
        self.pos = pos
        self.text = ''
        self.active = False
        self.pulse = True
        self.password = password

    def draw(self) -> pygame.Surface:
        # Set the font and font size
        font = pygame.font.Font(self.font, self.text_size)
        
        # If the text attribute is empty, use the placeholder text
        display_text = self.text or self.placeholder
        if self.text and self.password:
            display_text = '*'*len(self.text)
        # Calculate the width and height of the text box based on the font size
        text_width, text_height = font.size(display_text)
        box_width, box_height = self.size
        
        # Create the text box surface
        surf = pygame.Surface(self.size)
        
        # Fill the text box surface with the box color
        surf.fill(self.box_color)
        
        # Render the text onto the text box surface
        text_surface = font.render(display_text + '|'*(self.active and self.pulse), True, self.text_color)
        self.pulse = not self.pulse

        # Calculate the position of the text within the text box
        text_x = (box_width - text_width) // 2
        text_y = (box_height - text_height) // 2
        
        # Blit the text onto the text box surface
        surf.blit(text_surface, (text_x, text_y))
                
        return surf
    
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
        self.pos = (x or self.pos[0], y or self.pos[1])

    def get_pos(self) -> Tuple[int, int]:
        return self.pos

    def set_size(self, w: int = None, h: int = None):
        self.size = (w or self.size[0], h or self.size[1])
    
    def get_size(self) -> Tuple[int, int]:
        return self.size
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(*self.pos, *self.size)

    def get_text(self):
        return self.text
