from Infinitum.Core.Fonts.SimpleIO import TextHandler, TextBox, Button
from Infinitum.Core.Storage.FileManager import FileManager as FM

import hashlib
import pygame
import sys 

_bg = r'.\Infinitum\Sys\Login\login_default.png'
_pfp = r'.\Infinitum\Sys\Login\login_default_pfp.png'

box_color, box_hover, text_color = (200, 200, 200), (162,26,0), (25,25,25)

def _hash(string: str) -> str:
    return hashlib.sha256(hashlib.sha256(string.encode()).hexdigest().encode()).hexdigest()

class Login:
    def __init__(self, display: pygame.Surface) -> None:
        self.bg = pygame.image.load(_bg)
        self.password = ''
        config = FM.get_config(r'.\Infinitum.vc')
        self.username = config['username']
        self.pwd_hash = config['password']

        self.DISPLAY = display

        # Circular pfp
        pfp = pygame.image.load(_pfp)
        size = pfp.get_size()
        self.pfp = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.ellipse(self.pfp, (255, 255, 255, 255), (0, 0, *size))
        self.pfp.blit(pfp, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def main(self) -> None:
        fps = pygame.time.Clock()
        fps.tick(30)

        while not self.password:
            pygame.display.flip()
            for screen in self.draw():
                self.DISPLAY.blit(screen, (0, 0))
                pygame.display.update()
        return self.password

    def draw(self) -> pygame.Surface:
        self.text, finished = TextHandler(starting=(70, 44)), False
        
        login_button = Button('LOGIN', self.text.font, box_color = box_color, hover_color = box_hover, text_color = text_color, text_size=20, function=self.check_password)
        password_box = TextBox(placeholder='Password', font=self.text.font, size=(200, 30), password=True, box_color=box_color, text_color=text_color)

        err_msg = ''

        while not finished:
            self.text.reset_pos()
            surf = pygame.Surface(self.DISPLAY.get_size())

            surf.blit(self.bg, (0,0)) # Draw Background

            surf_rect = surf.get_rect()

            pfp_rect = self.pfp.get_rect(center = (surf_rect.centerx, surf_rect.centery - 50))
            surf.blit(self.pfp, pfp_rect) # Draw pfp
            
            msg = 'Welcome ' + self.username
            msg_rect = self.text.get_rect(msg, modifier='Header6')
            msg_rect.center = (pfp_rect.centerx, pfp_rect.bottom + 30 )
            self.text.set_pos(*msg_rect.topleft)
            self.text.print(msg, color=(255, 255, 255), surface=surf, modifier='Header6') # Write Username

            box_rect = password_box.get_rect()
            box_rect.center = (surf_rect.centerx, msg_rect.bottom + 30)
            surf.blit(password_box.draw(), box_rect)
            
            button_rect = login_button.get_rect()
            button_rect.center = (surf_rect.centerx, box_rect.bottom + 40)
            surf.blit(login_button.draw(), button_rect)

            if err_msg:
                msg_rect = self.text.get_rect(err_msg, modifier='Text3')
                msg_rect.center = (pfp_rect.centerx, button_rect.bottom + 30)
                self.text.set_pos(*msg_rect.topleft)
                self.text.print(err_msg, color=(255, 255, 255), surface=surf, modifier='Text3')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                mouse_pos = pygame.mouse.get_pos()

                login_button.hover = button_rect.collidepoint(mouse_pos)
                if login_button.hover:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        check_pass = login_button.on_click()
                        if check_pass: finished = True
                        else: err_msg = 'Incorrect Password, please try again'

                password_box.active = box_rect.collidepoint(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN and password_box.active:
                    err_msg = ''
                    while password_box.active:
                        surf.blit(password_box.typing(), box_rect)
                        yield surf
                    self.password = password_box.get_text()
            yield surf
    
    def check_password(self) -> bool:
        return _hash(self.password) == self.pwd_hash
        