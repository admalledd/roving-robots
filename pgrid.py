import os

import pygame
from pygame.locals import *

import map
import tiles
import input
import lib

class button(object):
    def __init__(self,type=None):
        if type==None:
            #get a random tile from the cache
            #to be depreciated...
            self.set_tile()
        self.walkable=False
        
        self.item = None
    def set_tile(self,type=None):
        if type is not None and len(type) < 4:
            raise Exception('tile type MUST be a four-charichtar length string!')
        self.type=type
        if type=='rand':
            #get a random tile from the cache
            self.surf=tile_cache.get(tile_cache.cache.keys()[int(random.random()*len(tile_cache.cache.keys()))])
        else:
            try:
                self.surf = tile_cache.get(type)
            except:
                self.surf = tile_cache.get('uuuu')
        if type == None:
            self.walkable = False
        elif type in  walkable:
            self.walkable = True
        else:
            self.walkable = False
            
    def draw(self,screen,rect):
        screen.blit(self.surf,rect)
        if self.item:
            self.item.draw(screen,rect)
    @lib.decorators.propget
    def walkable(self):
        if self.item:
            return False
        else:
            return self._walkable
    @lib.decorators.propset
    def walkable(self, value):
        self._walkable=value

class block(object):
    #non interface stuff
    def __init__(self,img,lable=None,num=None):
        '''example init:::
        block(os.path.join(~~~~~),pygame.font.render(~~~~~),1)
        
        we draw img's onto fake smaller surface so that we can use IT for an absilute topleft'''
        if type(img) == str:
            self.img = lib.common.load_img(img)
        else:
            self.img=img
        self.lable = lable
        self.lable_pos = 7,11
        self.surf = pygame.Surface((80,80))
        if num is not None:
            if isinstance(num,input.Input):
                self.tbox = num
            else:
                self.tbox = input.Input(y=y,maxlength=3, color=(255,0,0), prompt=' ', restricted='0123456789')
        else:
            #used to let us know NOT to try and render this section
            self.tbox = None
            
    def draw(self,screen,rect):
        if self.lable:
            self.surf.blit(self.lable,self.lable_pos)
        if self.tbox:
            self.tbox.draw(self.surf)
        self.surf.blit(self.img,(0,0))
        screen.blit(self.surf,rect)
    def process_events(self,events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                print 'happy days!'
    def link_up(self):
        pass
    def link_down(self):
        pass
    def link_left(self):
        pass
    def link_right(self):
        pass
    
    #properties--> block locations
    def dblock(self):
        pass
    
    def ublock(self):
        pass
    def lblock(self):
        pass
    def rblock(self):
        pass
        
    #action stuff
    def action(self,robot):
        pass
        
    def drag(self):
        '''cleans up object for a 'drop' '''
        pass
    def drop(self,pos):
        '''find any problems with the drop and cancle it if needed...'''
        pass
    def save(self):
        '''return a string which will allow recreation of this block (type,lable,num,pos,binding)'''
        pass
    def load(self,s):
        '''places block and recreates block based on "s" '''
        pass
        
class blank_block(block):
    def __init__(self):
        block.__init__(self,os.path.join('gui','programmer','blankblock_blnk.png'))
        
        
        
class interface(object):
    def __init__(self,robot):
        self.ro = robot
        if self.ro.code:
            self.code = self.ro.code
        else:
            self.code = code(self.ro)
    def click_engine(self,pos):
        pass
    @lib.decorators.disabled
    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        
def create_programming_gui(screen):
    back_ground = screen.copy()
    pmap = map.MAP(r_c=(160,121),
                   sub_rect=pygame.Rect((0,0),(80,80)),
                   main_rect=pygame.Rect((100,50),(600,500)),
                   tclass=blank_block)
    
    while True:
        pygame.time.wait(10)
        
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return None
            elif event.type == MOUSEBUTTONDOWN and event.button==1:
                pass
                #input.mouse.click_engine(event.pos)
        screen.blit(back_ground,(0,0))
        pmap.draw(screen)
        
        
        pygame.display.flip()




if __name__ == '__main__':
    pygame.init()
    lib.common.set_directory()
    lib.common.debug = 2
    screen = pygame.display.set_mode((800, 600))
    #load map tiles...
    tiles.find_tiles()
    
    create_programming_gui(screen)