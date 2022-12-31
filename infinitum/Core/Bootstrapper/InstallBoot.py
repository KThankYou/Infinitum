#Handle First time boot
from Infinitum.Core.Bootstrapper.text import welcome, user_details, installation, installation_alt, install_success, install_fail
from Infinitum.Core.Fonts.SimpleIO import TextHandler, Button, TextBox
from Infinitum.Core.Storage.FileManager import FileManager
from Infinitum.CONSTANTS import Pattern_Password
from Infinitum.commons import empty_surf

from typing import Tuple

import pygame
import sys

text_color, button_color, X = (251,230,255), (118,0,183), 1150

def draw_text(txt: str, font: pygame.font.Font, color: Tuple, surface: pygame.Surface, x: int, y: int, styles = None):
    textobj = font.render(txt, 1, color, styles)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Installer:
    def __init__(self) -> None:
        self.FM = None
        self.bg = pygame.transform.smoothscale(pygame.image.load(r'.\Infinitum\Core\Bootstrapper\installer.jpg'), (1600, 900))
        self.context = None
        self.username = self.password = ''
        self.error = None

    def main(self) -> None:
        pygame.init()
        fps = pygame.time.Clock()
        fps.tick(30)
        display = pygame.display.set_mode((1600, 900))
        
        contexts = {1: self.phase1, 2: self.phase2, 3: self.phase3, 4: self.phase4}
        self.context = contexts[1]
        while True:
            pygame.display.flip()
            for screen in self.context():
                display.blit(screen, (0, 0))
                pygame.display.update()

    def phase1(self): #Welcome_Screen
        self.text, finished = TextHandler(starting=(70, 44)), False
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
                self.text.print(text, text_color, surf, modifier = text_type)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.context = self.phase4_alt
                        finished = True
                    if event.key == pygame.K_RETURN:
                        self.context = self.phase2
                        finished = True
            yield surf

    def phase2(self): #Username, password etc
        self.username = self.password = ''
        self.text, finished = TextHandler(starting=(70, 44)), False
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
                self.text.print(text, text_color, surf, modifier = text_type)

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
                        self.username, self.password = text_box1.get_text(), text_box2.get_text()
                    
                for button in buttons:
                    button_rect = button.get_rect()
                    button.hover = button_rect.collidepoint(mouse_pos)
                    if button.hover:
                        surf.blit(button.draw(), button.get_pos())
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.context = button.on_click(generator=True)
                            finished = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.context = self.phase4_alt
                        finished = True
                    if event.key == pygame.K_RETURN:
                        self.context = self.phase3
                        finished = True

            yield surf

    def phase3(self): #Confirmation
        if not self.username or not Pattern_Password.search(self.password): 
            self.context, finished = self.phase3_alt, True
            return empty_surf

        self.text, finished = TextHandler(starting=(70, 44)), False
        text_color, button_color = (251,230,255), (118,0,183)
        
        button1 = Button('Back <', self.text.font, box_color = button_color, function = self.phase2)
        button2 = Button('Next >', self.text.font, box_color = button_color, function = self.phase4)
        button3 = Button('Cancel', self.text.font, box_color = button_color, function = self.phase4_alt)
        while not finished:
            self.text.reset_pos()
            surf = pygame.Surface((1600, 900))

            surf.blit(self.bg, (0,0)) # Draw Background

            for text_type, text in installation:
                self.text.print(text, text_color, surf, modifier = text_type)

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
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.context = self.phase4_alt
                        finished = True
                    if event.key == pygame.K_RETURN:
                        self.context = self.phase4
                        finished = True

            yield surf

    def phase3_alt(self): #Invalid Username/Password
        self.text, finished = TextHandler(starting=(70, 44)), False
        text_color, button_color = (251,230,255), (118,0,183)
        button1 = Button('Back <', self.text.font, box_color = button_color, function = self.phase2)
        button2 = Button('Next >', self.text.font, box_color = button_color, function = self.phase2)
        button3 = Button('Cancel', self.text.font, box_color = button_color, function = self.phase4_alt)
        while not finished:
            self.text.reset_pos()
            surf = pygame.Surface((1600, 900))

            surf.blit(self.bg, (0,0)) # Draw Background

            #Write Welcome Header
            for text_type, text in installation_alt:
                self.text.print(text, text_color, surf, modifier = text_type)

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
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.context = self.phase4_alt
                        finished = True
                    if event.key == pygame.K_RETURN:
                        self.context = self.phase2
                        finished = True

            yield surf

    def phase4(self): #Installation Complete
        try:
            FM = FileManager.initial_setup(r'.\Infinitum.vc', self.username, self.password)
            FM.MBT.installed()
            FM.close()
        except Exception as e:
            self.error, self.context = e, self.phase4_alt
            return empty_surf


        self.text, finished = TextHandler(starting=(70, 44)), False
        
        button1 = Button('Back <', self.text.font, box_color = button_color)
        button2 = Button('Finish', self.text.font, box_color = button_color, function = self.phase5)
        button3 = Button('Cancel', self.text.font, box_color = button_color, function = self.phase5)
        while not finished:
            self.text.reset_pos()
            surf = pygame.Surface((1600, 900))

            surf.blit(self.bg, (0,0)) # Draw Background

            #Write Welcome Header
            for text_type, text in install_success:
                self.text.print(text, text_color, surf, modifier = text_type)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.context = self.phase5
                        finished = True
                    if event.key == pygame.K_RETURN:
                        self.context = self.phase5
                        finished = True
            yield surf

    def phase4_alt(self): # Installation Failed
        self.text, finished = TextHandler(starting=(70, 44)), False
        text_color, button_color = (251,230,255), (118,0,183)
        button1 = Button('Back <', self.text.font, box_color = button_color)
        button2 = Button('Next >', self.text.font, box_color = button_color, function = self.phase5)
        button3 = Button('Cancel', self.text.font, box_color = button_color, function = self.phase5)
        while not finished:
            self.text.reset_pos()
            surf = pygame.Surface((1600, 900))

            surf.blit(self.bg, (0,0)) # Draw Background

            #Write Welcome Header
            h1, t1 = install_fail[0]; h2, t2 = install_fail[1]
            self.text.print(t1, text_color, surf, modifier = h1)
            self.text.print(t2.format(self.error), text_color, surf, modifier = h2)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.context = self.phase5
                        finished = True
                    if event.key == pygame.K_RETURN:
                        self.context = self.phase5
                        finished = True
            yield surf
    
    def phase5(self): # quit
        pygame.quit()
        sys.exit()
