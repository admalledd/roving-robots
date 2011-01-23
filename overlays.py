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
    def __init__(self,tmp):
        self.ticktime = tmp
        ##must have a self.surf first, crated by the overlay elsewhere...
        self.rect=self.surf.get_rect()
    def update(self,screen,loc,center,ms,map):
        self.rect.center=center
        screen.blit(self.surf,self.rect)
        
        
class item(overlay):
        pass
        
class energy(item):
    def __init__(self):
        self.frames=(
                    lib.common.load_img('items','energy','capsule3.png'),
                    lib.common.load_img('items','energy','capsule1.png'),
                    lib.common.load_img('items','energy','capsule2.png')
                    )
        self.surf=self.frames[0]
        self.value = random.randint(0,100)
        item.__init__(self,2500)
        self.cur=0
    def update(self,screen,loc,center,ms,map):
        self.rect.center=center
        screen.blit(self.surf,self.rect)
        self.cur+=1
        if self.cur>len(self.frames)-1:
            self.cur=0
        self.surf = self.frames[self.cur]
class metal(item):
    def __init__(self):
        self.surf = lib.common.load_img('items','scrap-metal.png')
        self.value = random.randint(0,100)
        item.__init__(self,1000)
        
class datalog(item):
    def __init__(self):
        self.surf = pygame.Surface ((50,50))
        self.value = 'test item!'
        
        

def test(map):
    return
    
    
    