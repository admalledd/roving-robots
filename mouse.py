
import pygame
from pygame.locals import *

import lib
import map
import programmer

class MOUSE(object):
    def __init__(self):
        self.prev_selected = None
        self.cur_sel = None
        self.active = 
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