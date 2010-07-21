import pygame
from pygame.locals import *
import math

from input import button,drag_button
def dist(rect_a,rect_b):
    '''rect_a == top block to snap to
    rect_b    == bottom block to check'''
    return math.sqrt(((rect_a.midbottom[0]-rect_b.midtop[0])**2)+((rect_a.midbottom[1]-rect_b.midtop[1])**2))
class menu(object):
    def __init__(self):
        
        self.font = pygame.font.Font(None,48)
        
        self.clickable  =[ (button((300,160)
                                ,self.font.render('start game',True,(0,0,255)).convert_alpha()
                                ,self.font.render('start game',True,(255,0,00)).convert_alpha()
                                ,self.font.render('start game',True,(0,255,0)).convert_alpha()
                                )
                            ,self.start
                         ),
                         (button((300,240)
                                ,self.font.render('credits',True,(0,0,255)).convert_alpha()
                                ,self.font.render('credits',True,(255,0,0)).convert_alpha()
                                ,self.font.render('credits',True,(0,255,0)).convert_alpha()
                                )
                            ,self.credits
                         )
                         ]
        self.dragable   = [(drag_button((300,300)
                                ,self.font.render('drag me',True,(0,0,255)).convert_alpha()
                                ,self.font.render('drag me',True,(255,0,0)).convert_alpha()
                                ,self.font.render('drag me',True,(0,255,0)).convert_alpha()
                                )
                         )
                         ]
        self.receptical = []
        
        
        
        self.hub_img = self.font.render('mount me',True,(0,0,255)).convert_alpha()
        self.hub_rect = self.hub_img.get_rect()
        self.hub_rect.topleft = (500,200)
        
        
        self.surf = pygame.Surface((800, 600))
    def add_click_btn(self, btn, func):
        self.clickable.append(btn)
        
    def add_drag_btn(self, btn):
        self.dragable.append(btn)
        
    def add_receptical_btn(self,btn):
        self.receptical.append(btn)
        
    def events(self,events):
        for btn,func in self.clickable:
            var =  btn.events(events)
            if var:
                func(btn)
        for btn in self.dragable:
            if btn.events(events):
                self.dragged(btn)
        for event in events:
            if event.type == MOUSEBUTTONUP and event.button == 1:
                print event.pos
    
    def draw(self,screen):
        for btn,func in self.clickable:
            btn.draw(screen)
        
        for btn in self.dragable:
            btn.draw(screen)
            
        screen.blit(self.hub_img,self.hub_rect)
        pygame.draw.rect(screen, (255,255,255), self.hub_rect, 1)
        
        
    def start(self,btn):
        print 'start clicked'
    def credits(self,btn):
        print 'credits clicked'
    def dragged(self,btn):
        print 'button dragged'
        
        d = dist(self.hub_rect,btn.rect)#find distance between midtop and midbottom
        print d
        if d < 15:
            btn.rect.midtop=self.hub_rect.midbottom
        
        
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
                import sys
                sys.exit()
        me.events(events)
        me.draw(screen)
        
        pygame.display.flip()
