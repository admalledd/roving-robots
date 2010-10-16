import os

import pygame
from pygame.locals import *

import map
import tiles
import input
import lib

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
        self.blank = False
        
        
    def draw(self,screen,rect):
        if self.lable:
            self.surf.blit(self.lable,self.lable_pos)
        if self.tbox:
            self.tbox.draw(self.surf)
        self.surf.blit(self.img,(0,0))
        screen.blit(self.surf,rect)
    def event_engine(self,events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                print 'happy days!'
                
        self
    def link_up(self):
        pass
    def link_down(self):
        pass
    def link_left(self):
        pass
    def link_right(self):
        pass
    
    #properties--> block locations
    #block locations are thusly defined: tuple of (x,y) position of next block.
    @lib.decorators.propget
    def dblock(self):
        return self._dblock
    @lib.decorators.propset
    def dblock(self,value):
        if self.__loc[1] >= value:
            print 'warning, you made a mistake idiot!! fix it! <<dblock.propset>>'
        self._dblock = value
    @lib.decorators.propget
    def ublock(self):
        pass
    @lib.decorators.propget
    def lblock(self):
        pass
    @lib.decorators.propget
    def rblock(self):
        pass
    @lib.decorators.propget
    def loc(self):
        return self.__loc
    @lib.decorators.propset
    def loc(self,value):
        self.__loc = value
    
    #action stuff
    def action(self,robot):
        '''robotic action to take (turn, go fwd, scan/make desision)'''
        pass
    def next(self,robot):
        '''what is the next block? (give (x,y))'''
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
        
class bgnd_block(block):
    def __init__(self):
        block.__init__(self,os.path.join('gui','programmer','background_bgnd.png'))
        self.blank = True
        
class pfwd_block(block):
    def next(self,robot):
        return seld.dblock
        
class main_block(block):
    def __init__(self):
        block.__init__(self,os.path.join('gui','programmer','main_main.png'))
        
    def action(self,robot):
        '''do nothing, pass along. this is not the robot you are looking for'''
        pass
    
    def next(self,robot):
        return self.dblock
        
class interface(object):
    def __init__(self):
        self.fwd_spawn = (lib.common.load_img(os.path.join('gui','programmer','forward_pfwd.png')),
                          pygame.Rect((650,25),(80,80)) )
        
        self.spawns = {'pfwd':(self.fwd_spawn,pfwd_block)}
        
        self.main_block = main_block()
        
        
    def click_engine(self,pos):
        '''this is for the spawning and other thing within the interface
        it has nothing to do with the event engine of the pmap system...'''
        for key,value in self.spawns.items():
            if value[0][1].collidepoint(pos):
                print 'hit spawn'
                return value[1](value[0][0])
    def event_engine(self,events,pmap):
        '''the job of this function is to follow the path of the main_block, and pass the events down the line
        also utlizes the map.MAP system to find next block to run (yay me!)'''
        for event in events:
            pass
            
        next = self.main_block.event_engine(events)
        while next is not None:
            #is it OK for the event chain to be broken when a block starts to get dragged?
            next = pmap.map[next][0].event_engine(events)
    def draw(self, screen):
        #screen.blit(self.surf, self.rect)
        for key,value in self.spawns.items():
            screen.blit(value[0][0],value[0][1])
        
def create_programming_gui(screen):
    back_ground = screen.copy()
    pmap = map.MAP(r_c=(15,15),
                   sub_rect=pygame.Rect((0,0),(80,80)),
                   main_rect=pygame.Rect((0,0),(640,600)),
                   tclass=bgnd_block)
    pmap.show_grid = True
    intr = interface()
    while True:
        pygame.time.wait(10)
        
        screen.fill((0, 0, 0))
        #draw background (img of robots/terrain)
        screen.blit(back_ground,(0,0))
        
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return None
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    pmap.loc =pmap.loc[0]+1, pmap.loc[1]
                elif event.key == K_RIGHT:
                    pmap.loc =pmap.loc[0]-1, pmap.loc[1]
                elif event.key == K_UP:
                    pmap.loc =pmap.loc[0], pmap.loc[1]+1
                elif event.key == K_DOWN:
                    pmap.loc =pmap.loc[0], pmap.loc[1]-1
            elif event.type == MOUSEBUTTONDOWN and event.button==1:
                print event.pos
                pmap.click_engine(event.pos)
                ret = intr.click_engine(event.pos)
                if ret:
                    pmap.map[(0,0)][0] = ret
                    pmap.render()
        intr.event_engine(events,pmap)
        
        intr.draw(screen)
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