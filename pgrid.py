import os
import logging
logger=logging.getLogger('pgrid')

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
        ##TODO::: make "active" setting for textbox, and other settings???
        
        if type(img) == str:
            self.img = lib.common.load_img(img)
        else:
            self.img=img
        self.lable = lable
        self.lable_pos = 7,11
        self.surf = pygame.Surface((80,80))
        self.surf = self.surf.convert_alpha()
        if num is not None:
            if isinstance(num,input.Input):
                self.tbox = num
            else:
                self.tbox = input.Input(y=y,maxlength=3, color=(255,0,0), prompt=' ', restricted='0123456789')
        else:
            #used to let us know NOT to try and render this section
            self.tbox = None
        #nothing can link by default to a default block, use a subclass!
        self.link_down  = False
        self.link_up    = False
        self.link_left  = False
        self.link_right = False
        #block-linkers:
        self._dblock=None
        self._ublock=None
        self._rblock=None
        self._lblock=None
        
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
    
    ##link block decorators:::
    ##if "set", tey set themselves to other, and also set othe.xblock to self(or none if unlinking)
    @lib.decorators.propget
    def dblock(self):
        return self._dblock
    @lib.decorators.propset
    def dblock(self,other):
        #x=down
        #y=up
        if other is None:
            #set the other block's corrisponing to None as well...
            self._dblock._ublock = None
        else:
            other._ublock = self
        self._dblock = other
        
    @lib.decorators.propget
    def ublock(self):
        return self._ublock
    @lib.decorators.propset
    def ublock(self,other):
        #x=down
        #y=up
        if other is None:
            #set the other block's corrisponing to None as well...
            self._ublock._dblock = None
        else:
            other._dblock = self
        self._ublock = other
        
    @lib.decorators.propget
    def lblock(self):
        return self._lblock
    @lib.decorators.propset
    def lblock(self,other):
        #x=down
        #y=up
        if other is None:
            #set the other block's corrisponing to None as well...
            self._lblock._rblock = None
        else:
            other._rblock = self
        self._lblock = other
        
    @lib.decorators.propget
    def rblock(self):
        return self._rblock
    @lib.decorators.propset
    def rblock(self,other):
        #x=down
        #y=up
        if other is None:
            #set the other block's corrisponing to None as well...
            self._rblock._lblock = None
        else:
            other._lblock = self
        self._rblock = other
        
        
    ##location properties
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
        '''what is the next block? (give (x,y) or instance?)'''
        pass
    
        
    def drag(self):
        '''cleans up object for a 'drop' '''
        pass
    def able_drop(self,pos,pmap):
        '''find any problems with the drop and return False if obstructed.
        else return True'''
        pass
    def drop(self,pos,pmap):
        '''finalize a drop. actually places block on grid'''
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
        self.link_down  = False
        self.link_up    = True
        
class pfwd_block(block):
    def __init__(self,img,lable=None,num=None):
        block.__init__(self,img,lable,num)
        self.link_up   = True
        self.link_down = True
    
    def next(self,robot):
        if self.dblock and (isinstance(self.dblock,bgnd_block)==False):
            return self.dblock
        else:
            return False
        
    def able_drop(self,pos,pmap):
        #firstly: check for up block
        up=pos[0],pos[1]-1
        if up[1] < 0:
            print '#we are at the top, cant place block here!'
            return False
        if not pmap.map[up][0].link_down:
            print '#link_down is false, cant place block there!'
            return False
            
        #secondly: check for down block:
        down=pos[0],pos[1]+1
        #we dont care about running off the map if down is off, because this block is able to "end" code
        #but lets check IF there even IS a block there...
        if pmap.map.has_key(down):
            if not pmap.map[down][0].link_up:
                print '#block below doesnt allow linking'
                return False
        return True
        
    def drop(self,pos,pmap):
        pmap.map[pos][0]=self
        up=pos[0],pos[1]-1
        pmap.map[up][0].dblock = self
        
        down=pos[0],pos[1]+1
        pmap.map[down][0].ublock = self
        
        
class main_block(block):
    def __init__(self):
        block.__init__(self,os.path.join('gui','programmer','main_main.png'))
        self.link_down=True
    def action(self,robot):
        '''do nothing, pass along. this is not the robot you are looking for'''
        pass
    
    def next(self,robot):
        if self.dblock:
            return self.dblock
        else:
            return False
        
class interface(object):
    def __init__(self):
        self.fwd_spawn = (lib.common.load_img(os.path.join('gui','programmer','forward_pfwd.png')),
                          pygame.Rect((650,25),(80,80)) )
        
        self.spawns = {'pfwd':(self.fwd_spawn,pfwd_block)}
        
    def click_engine(self,pos):
        for key,value in self.spawns.items():
            if value[0][1].collidepoint(pos):
                print 'hit spawn'
                return value[1](value[0][0])
    
    def draw(self, screen):
        #screen.blit(self.surf, self.rect)
        for key,value in self.spawns.items():
            screen.blit(value[0][0],value[0][1])
def get_code(pmap):
    cur = pmap.map[(0,0)][0]
    while cur:
        print cur
        ##todo:: pass robot instance
        cur = cur.next(None)
def create_programming_gui(screen):
    back_ground = screen.copy()
    pmap = map.MAP(r_c=(15,15),
                   sub_rect=pygame.Rect((0,0),(80,80)),
                   main_rect=pygame.Rect((0,0),(640,600)),
                   tclass=bgnd_block)
    pmap.show_grid = True
    
    intr = interface()
    pmap.map[(0,0)][0]=main_block()
    pmap.render()
    while True:
        pygame.time.wait(10)
        
        #blit background FIRST! (it my just so happen to cover up your other stuff...)
        screen.fill((0, 0, 0))
        screen.blit(back_ground,(0,0))
        
        #lag drawing by one loop, allaowing events to draw OVER screen...
        intr.draw(screen)
        pmap.draw(screen)
        
        
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
                
                elif event.key == K_SPACE:
                    get_code(pmap)
            elif event.type == MOUSEBUTTONDOWN and event.button==1:
                map_pos = pmap.click_engine(event.pos)
                logger.info("%s:::%s"%(event.pos,map_pos))
                #drop button
                if input.mouse.cur_sel and (map_pos != (-1,-1)):
                    
                    if input.mouse.cur_sel.able_drop(map_pos,pmap):
                        input.mouse.cur_sel.drop(map_pos,pmap)
                        
                        #pmap.map[map_pos][0] = input.mouse.cur_sel
                        
                        input.mouse.cur_sel = None
                    pmap.render()
                #try to make a button, remove whatever is __in__ the mouse right now
                ret = intr.click_engine(event.pos)
                if ret:
                    input.mouse.cur_sel = ret
        
        if input.mouse.cur_sel:
            input.mouse.cur_sel.draw(screen,input.mouse.cur_pos())
        
        
        pygame.display.flip()




if __name__ == '__main__':
    pygame.init()
    lib.common.debug = 2
    screen = pygame.display.set_mode((800, 600))
    #load map tiles...
    tiles.find_tiles()
    
    create_programming_gui(screen)