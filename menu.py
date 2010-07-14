import pygame
from pygame.locals import *

class button(object):
    def __init__(self,text_norm,text_high=None,text_click=None):
        
        self.text_norm = text_norm
        
        if text_high:
            self.text_high = text_high
        else:
            self.text_high = None
            
        if text_click:
            self.text_click = text_click
        else:
            self.text_click = None
        
        self.surf = self.text_norm
        self.click_tmp=False
        self.clicked=False
        
        self.rect = self.text_norm.get_rect()
        
        
    def events(self,events):
        for event in events:
            if event.type == MOUSEMOTION:#hoverover button
                if self.rect.collidepoint(event.pos):
                    if self.surf is self.text_norm:
                        self.surf = self.text_high
                else:
                    self.surf = self.text_norm
            elif event.type == MOUSEBUTTONDOWN:#click and hold over button
                if self.rect.collidepoint(event.pos):
                    self.surf = self.text_click
                    self.click_tmp=True
                else:
                    self.click_tmp=False
            elif event.type == MOUSEBUTTONUP:#click,hold,and release over button
                if self.rect.collidepoint(event.pos):
                    if self.click_tmp:
                        self.clicked = True#variable for things to use to see if clicked...
                        self.click_tmp=False
                else:
                    self.click_tmp=False
                    self.clicked=False
        if self.clicked == True:
            return True
    def draw(self,pos,surf):
        self.rect.center= pos
        surf.blit(self.surf,self.rect)
        
        
class menu(object):
    def __init__(self):
        
        self.font = pygame.font.Font(None,48)
        self.buttons = ( (button(self.font.render('start game',True,(0,0,255)).convert_alpha()
                                ,self.font.render('start game',True,(255,0,00)).convert_alpha()
                                ,self.font.render('start game',True,(0,255,0)).convert_alpha()
                                )
                            ,(300,160)
                         ),
                         (button(self.font.render('credits',True,(0,0,255)).convert_alpha()
                                ,self.font.render('credits',True,(255,0,00)).convert_alpha()
                                ,self.font.render('credits',True,(0,255,0)).convert_alpha()
                                )
                            ,(300,240)
                         )
                       )
        
        self.surf = pygame.Surface((800, 600))
    def events(self,events):
        for btn,pos in self.buttons:
            btn.events(events) 
        for event in events:
            if event.type == MOUSEBUTTONUP and event.button == 1:
                print self.buttons[0][0].clicked
    def render(self):
        for btn,pos in self.buttons:
            btn.draw(pos,self.surf)
        #self.opt1.draw((300,160),self.surf)
        
    def draw(self,screen):
        self.render()
        screen.blit(self.surf,(0,0))
        
        
if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    me = menu()
    
    
    while True:
        pygame.time.wait(10)
        
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                break
        me.events(events)
        me.draw(screen)
        
        pygame.display.flip()
