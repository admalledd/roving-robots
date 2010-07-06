
import pygame
from pygame.locals import *

import lib

class MOUSE(object):
    def __init__(self):
        self.prev_selected = None
        self.cur_sel = None
    @lib.decorators.propget
    def cur_selected(self):
        
        return self.cur_sel

    @lib.decorators.propset
    def cur_selected(self, value):
        self.prev_selected = self.cur_sel
        self.cur_sel = value

mouse=MOUSE()