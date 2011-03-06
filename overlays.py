'''
overlay classes and mechanisms
includes items and animators

'''

import pygame
import os
import random
import logging
logger=logging.getLogger('overlays')


import lib


class overlay(object):
    def __init__(self):
        ##must have a self.surf first, crated by the overlay elsewhere...
        self.rect=self.surf.get_rect()
    def update(self,screen,loc,center,ms,map):
        self.rect.center=center
        screen.blit(self.surf,self.rect)
    def __getstate__(self):
        state=self.__dict__.copy()
        state.pop('surf')
        if 'frames' in state:
            state.pop('frames')
        return state
    def __setstate__(self,state):
        self.__dict__.update(state)
        self.frames = tuple((lib.common.load_img(*file) for file in self.files))
        if len(self.frames) ==1:
            self.surf = self.frames[0]
        else:
            self.surf = self.frames[self.cur]
            
class item(overlay):
        pass
        
class energy(item):
    def __init__(self):
        self.files=(
                    ('items','energy','capsule3.png'),
                    ('items','energy','capsule1.png'),
                    ('items','energy','capsule2.png')
                   )
        
        self.frames=tuple((lib.common.load_img(*file) for file in self.files))
        self.surf=self.frames[0]
        self.value = random.randint(0,100)
        item.__init__(self)
        self.cur=0
        self.time=0
        
    def update(self,screen,loc,center,ms,map):
        self.rect.center=center
        screen.blit(self.surf,self.rect)
        
        self.time+=ms
        if self.time > 250:
            self.cur+=1
            self.time=0
        if self.cur>len(self.frames)-1:
            self.cur=0
        self.surf = self.frames[self.cur]
        
class metal(item):
    def __init__(self):
        self.files=(('items','scrap-metal.png'),)
        self.surf = lib.common.load_img(*self.files[0])
        self.value = random.randint(0,100)
        item.__init__(self)
        
class datalog(item):
    def __init__(self):
        self.surf = pygame.Surface((50,50))
        self.value = 'test item!'
        
        

    
    
    