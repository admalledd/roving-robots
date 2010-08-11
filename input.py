
import pygame
from pygame.locals import *

import lib
import map
import programmer

class MOUSE(object):
    def __init__(self):
        self.prev_selected = None
        self.cur_sel = None
        self.active = 'map'
    @lib.decorators.propget
    def cur_selected(self):
        
        return self.cur_sel

    @lib.decorators.propset
    def cur_selected(self, value):
        self.prev_selected = self.cur_sel
        self.cur_sel = value
    def click_engine(self,pos):
    
        self.cur_selected = map.map.click_engine(pos)
        if lib.common.debug > 0:
            print "cur:%s   prev:%s"%(mouse.cur_selected,mouse.prev_selected)
mouse=MOUSE()


class button(object):
    def __init__(self,center,text_norm,text_high=None,text_click=None):
        
        self.text_norm = text_norm
        
        if text_high:
            self.text_high = text_high
            if text_click:
                self.text_click = text_click
            else:
                self.text_click = text_high
        else:
            self.text_high = text_norm
            
        
        self.surf = self.text_norm
        self.click_tmp=False
        self.clicked=False
        
        self.rect = self.text_norm.get_rect()
        self.rect.center = center
        
        self.is_dock = False
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
            self.clicked = False
            return True
    def draw(self,surf):
        surf.blit(self.surf,self.rect)
        
class dock_button(button):
    def __init__(self,center,text_norm,text_high=None,text_click=None):
        super(dock_button,self).__init__(center,text_norm,text_high,text_click)
        
        self.docked_btn = None
        self.is_dock = True
        
    def dock(self,btn):
        if self.docked_btn:
            return False
        else:
            self.docked_btn = btn
            self.docked_btn.mount = self
            
    def remove(self):
        '''to be defined, remove all docked items as well (eg we delete the entire dragged tree...)'''
        if hasattr(self.docked_btn,'remove'):
            self.docked_btn.remove()
        del self.dock
        del self
        
    def draw(self,surf):
        super(dock_button,self).draw(surf)
        ##TODO::: 
        if self.docked_btn:
            self.docked_btn.draw(surf,True)
        
class drag_button(button):
    def __init__(self,center,text_norm,text_high=None,text_click=None):
        super(drag_button,self).__init__(center,text_norm,text_high,text_click)
        
        self.mount=None
    def events(self,events):
        tmp = super(drag_button,self).events(events)
        for event in events:
            if  event.type == MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if self.click_tmp == True:
                        self.rect.center= event.pos
        return tmp
    def draw(self,surf,dock_override=False):
        if self.mount:
            if not dock_override:
                return None
        
        surf.blit(self.surf,self.rect)
        pygame.draw.rect(surf, (255,255,255), self.rect, 1)
        
class fwd_btn(drag_button  , dock_button):
    
    
    def draw(self,surf,dock_override=False):
        if self.mount:
            if not dock_override:
                return None
        if self.docked_btn:
            self.docked_btn.draw(surf,True)
        surf.blit(self.surf,self.rect)
        pygame.draw.rect(surf, (255,255,255), self.rect, 1)
        