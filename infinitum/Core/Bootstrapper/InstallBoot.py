#Handle First time boot
from typing import Tuple
from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.Core.Fonts.IOHandler import TextHandler, Button, TextBox
from Infinitum.Core.Bootstrapper.text import welcome, user_details
import pygame, sys



def draw_text(txt: str, font: pygame.font.Font, color: Tuple, surface: pygame.Surface, x: int, y: int, styles = None):
    textobj = font.render(txt, 1, color, styles)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Installer:
    # U = underline, B = bold, I = Italic, S = Strikethrough
    KWARGS = {
        # 0 = UBIS, 1 = UBI, 2 = U, 3 = UB, 4 = UI, 5 = BI, 6 = B+mini
        'Header0': {'U': True, 'B': True, 'I': True, 'S': True, 'size': 44},
        'Header1': {'U': True, 'B': True, 'I': True, 'S': False, 'size': 44},
        'Header2': {'U': True, 'B': False, 'I': False, 'S': False, 'size': 44},
        'Header3': {'U': True, 'B': True, 'I': False, 'S': False, 'size': 44},
        'Header4': {'U': True, 'B': False, 'I': True, 'S': False, 'size': 44},
        'Header5': {'U': False, 'B': True, 'I': True, 'S': False, 'size': 44},
        'Header6': {'U': False, 'B': True, 'I': False, 'S': False, 'size': 32},

        # 0 = UBI, 1 = None, 2 = U, 3 = B, 4 = I
        'Text0': {'U': True, 'B': True, 'I': True, 'S': False, 'size': 20},
        'Text1': {'U': False, 'B': False, 'I': False, 'S': False, 'size': 20},
        'Text2': {'U': True, 'B': False, 'I': False, 'S': False, 'size': 20},
        'Text3': {'U': False, 'B': True, 'I': False, 'S': False, 'size': 20},
        'Text4': {'U': False, 'B': False, 'I': True, 'S': False, 'size': 20},
        
        }
    def __init__(self) -> None:
        self.FM = FileManager(r'.\Infinitum.vc')
        self.bg = pygame.image.load(r'.\Infinitum\Core\Bootstrapper\installer.jpg')
        self.context, self.installing = None, True

    def main(self) -> None:
        pygame.init()
        fps = pygame.time.Clock()
        fps.tick(30)
        display = pygame.display.set_mode((1600, 900))
        
        contexts = {1: self.phase1, 2: self.phase2, 3: self.phase3, 4: self.phase4}
        self.context = contexts[1]
        while self.installing:
            pygame.display.flip()
            for screen in self.context():
                display.blit(screen, (0, 0))
                pygame.display.update()
        pygame.quit()

    def phase1(self): #Welcome_Screen
        finished = False
        self.text, X = TextHandler(starting=(70, 44)), 1150
        text_color, button_color = (251,230,255), (118,0,183)
        button1 = Button('Back <', self.text.font, box_color = button_color)
        button2 = Button('Next >', self.text.font, box_color = button_color, function = self.phase2)
        button3 = Button('Cancel', self.text.font, box_color = button_color, function = self.phase4_alt)
        while not finished:
            self.text.reset_pos()
            surf = pygame.Surface((1600, 900))

            surf.blit(self.bg, (0,0)) # Draw Background

            #Write Welcome Header
            for text_type, text in welcome:
                self.text.write(text, text_color, surf, **Installer.KWARGS[text_type])

            row_offset = self.text.get_pos()[1]
            button1.set_pos(X, row_offset)
            button2.set_pos(X + 100, row_offset)
            button3.set_pos(X + 195, row_offset)
            
            surf.blit(button1.draw(), button1.get_pos())
            surf.blit(button2.draw(), button2.get_pos())
            surf.blit(button3.draw(), button3.get_pos())

            buttons = (button1, button2, button3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                mouse_pos = pygame.mouse.get_pos()

                for button in buttons:
                    button_rect = button.get_rect()
                    button.hover = button_rect.collidepoint(mouse_pos)
                    if button.hover:
                        
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.context = button.on_click(generator=True)
                            finished = True
                    

            yield surf

    def phase2(self): #Username, password etc
        finished = False
        self.text, X = TextHandler(starting=(70, 44)), 1150
        text_color, button_color = (251,230,255), (118,0,183)
        
        button1 = Button('Back <', self.text.font, box_color = button_color, function = self.phase1)
        button2 = Button('Next >', self.text.font, box_color = button_color, function = self.phase3)
        button3 = Button('Cancel', self.text.font, box_color = button_color, function = self.phase4_alt)

        text_box1 = TextBox(font = self.text.font, placeholder = 'Username', size = (200, 30))
        text_box2 = TextBox(font = self.text.font, placeholder = 'Password', size = (200, 30), password=True)

        while not finished:
            self.text.reset_pos()
            surf = pygame.Surface((1600, 900))

            surf.blit(self.bg, (0,0)) # Draw Background

            for text_type, text in user_details:
                self.text.write(text, text_color, surf, **Installer.KWARGS[text_type])

            row_offset = self.text.get_pos()[1]

            text_box1.set_pos(70, row_offset)
            text_box2.set_pos(70, row_offset + 60)

            row_offset += 180

            button1.set_pos(X, row_offset)
            button2.set_pos(X + 100, row_offset)
            button3.set_pos(X + 195, row_offset)

            buttons = (button1, button2, button3)
            text_boxes = (text_box1, text_box2)

            for box in text_boxes: surf.blit(box.draw(), box.get_pos())
            for button in buttons: surf.blit(button.draw(), button.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                mouse_pos = pygame.mouse.get_pos()

                for box in text_boxes:
                    box_rect = box.get_rect()
                    box.active = box_rect.collidepoint(mouse_pos)
                    if event.type == pygame.MOUSEBUTTONDOWN and box.active:
                        while box.active:
                            surf.blit(box.typing(), box.get_pos())
                            yield surf
                    
                for button in buttons:
                    button_rect = button.get_rect()
                    button.hover = button_rect.collidepoint(mouse_pos)
                    if button.hover:
                        surf.blit(button.draw(), button.get_pos())
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.context = button.on_click(generator=True)
                            finished = True

            yield surf

    def phase3(self): #Installation in Progress
        self.installing = False #TODO: remove this

    def phase4(self): #Installation Complete
        self.installing = False

    def phase4_alt(self): # Installation Failed
        self.installing = False
        yield pygame.Surface((0,0))