import pygame
import os
import random


import lib


class item(object):
    def __init__(self):
        pass
        
    def draw(self,screen,rect):
        r=self.surf.get_rect()
        r.center = rect.center
        
        screen.blit(self.surf,r)
class energy(item):
    def __init__(self):
        self.surf=lib.common.load_img(os.path.join('items','energy.png'))
        self.value = random.randint(0,100)
    
    
class metal(item):
    def __init__(self):
        self.surf = lib.common.load_img(os.path.join('items','scrap-metal.png'))
        self.value = random.randint(0,100)