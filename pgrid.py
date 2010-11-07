import os
import logging

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
    @lib.decorators.propget
    def dblock(self):
        pass
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

class pfwd_block(block):
    def next(self,robot):
        return self.dblock
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
        
    def click_engine(self,pos):
        for key,value in self.spawns.items():
            print key
            if value[0][1].collidepoint(pos):
                print 'hit spawn'
                return value[1](value[0][0])
    
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
    pmap.render()
    intr = interface()
    while True:
        pygame.time.wait(10)
        
        screen.fill((0, 0, 0))
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
        #blit background FIRST! (it my just so happen to cover up your other stuff...)
        screen.blit(back_ground,(0,0))
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