import pygame
from pygame.locals import *
import math

from input import *
def dist(rect_a,rect_b):
    '''rect_a == top block to snap to
    rect_b    == bottom block to check'''
    return math.sqrt(((rect_a.midbottom[0]-rect_b.midtop[0])**2)+((rect_a.midbottom[1]-rect_b.midtop[1])**2))
class menu(object):
    def __init__(self):
        
        self.font = pygame.font.Font(None,48)
        
        self.clickable  =[ (button((300,160)
                                ,self.font.render('forward_spawn',True,(0,0,255)).convert_alpha()
                                ,self.font.render('forward_spawn',True,(255,0,00)).convert_alpha()
                                ,self.font.render('forward_spawn',True,(0,255,0)).convert_alpha()
                                )
                            ,self.spawn_fwd
                         ),
                         (button((300,240)
                                ,self.font.render('credits',True,(0,0,255)).convert_alpha()
                                ,self.font.render('credits',True,(255,0,0)).convert_alpha()
                                ,self.font.render('credits',True,(0,255,0)).convert_alpha()
                                )
                            ,self.credits
                         )
                         ]
        self.dragable   = [(drag_dock((300,300)
                                ,self.font.render('drag me',True,(0,0,255)).convert_alpha()
                                ,self.font.render('drag me',True,(255,0,0)).convert_alpha()
                                ,self.font.render('drag me',True,(0,255,0)).convert_alpha()
                                )
                         )
                         ]
        self.receptical = [dock_button((500,200)
                                ,self.font.render('mount me',True,(0,0,255)).convert_alpha()
                                ,self.font.render('mount me',True,(255,0,0)).convert_alpha()
                                ,self.font.render('mount me',True,(0,255,0)).convert_alpha()
                                )
                          ]
        
        self.dock_dist = 15
        
        self.surf = pygame.Surface((800, 600))
    def add_drag_btn(self, btn):
        self.dragable.append(btn)
        
    def remove_drag_btn(self,btn):
        self.dragable.remove(btn)
        del btn    
    
    def events(self,events):
        '''TODO: drag/click through to ONLY one button...'''
        for btn,func in self.clickable:
            var =  btn.events(events)
            if var:
                func(btn)
        for btn in self.dragable:
            if btn.events(events):
                self.dragged(btn)
        for event in events:
            ##debug code stuff, remove for production
            if event.type == MOUSEBUTTONUP and event.button == 1:
                print event.pos
            ##
            if event.type == KEYDOWN:
                if event.key == K_1:
                    print self.dragable[0].mount
                    print self.receptical[0].docked_btn
                else:
                    print event
    def draw(self,screen):
        for btn,func in self.clickable:
            btn.draw(screen)
        
        for btn in self.dragable:
            btn.draw(screen)
           
        for btn in self.receptical:
            btn.draw(screen)
        
    def spawn_fwd(self,btn):
        print 'fwd spawned'
        b=drag_dock((300,300)
                   ,self.font.render('drag me',True,(0,0,255)).convert_alpha()
                   ,self.font.render('drag me',True,(255,0,0)).convert_alpha()
                   ,self.font.render('drag me',True,(0,255,0)).convert_alpha()
                 )  
        self.add_drag_btn(b)
        
    def credits(self,btn):
        print 'credits clicked'
    def dragged(self,btn):
        print 'button dragged'
        
        for b in self.dragable:
            if b.docked_btn:#has been docked, dont do the math then...
                continue
            elif hasattr(b,'is_dock') and b.is_dock:
                if dist(b.rect,btn.rect) <= self.dock_dist:
                    btn.rect.midtop=b.rect.midbottom
                    if b.dock(btn):
                        return
        for r in self.receptical:
            if not r.docked_btn:
                if dist(r.rect,btn.rect) <= self.dock_dist:
                    btn.rect.midtop=r.rect.midbottom
                    r.dock(btn)
                    return
        
        
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
