import os
import logging
logger=logging.getLogger('programmer')

import pygame
from pygame.locals import *

import lib
import input

class block(object):
    #non interface stuff
    def __init__(self,img,lable=None,num=None):
        '''example init:::
        block(os.path.join(~~~~~),pygame.font.render(~~~~~),1)
        
        we draw img's onto fake smaller surface so that we can use IT for an absilute topleft'''
        ##TODO::: make "active" setting for textbox, and other settings???
        
        if type(img) in (str,tuple,list):
            if type(img) in (tuple,list):
                ##list of directories to join are passed along...
                self.img = lib.common.load_img(*img)
            else:
                ##string name (already passed through os.path.join?)
                self.img = lib.common.load_img(img)
        else:
            self.img=img
        
        self.lable = lable
        if lable:
            self.lable_pos = lable.get_rect()
            self.lable_pos.midtop = 39,10
            
        self.surf = pygame.Surface((80,80),pygame.SRCALPHA)
        self.drag_rect=pygame.Rect((0,0),(10,10))
        
        if num is not None:
            if isinstance(num,input.Input):
                self.tbox = num
            else:
                self.tbox = input.Input(y=40,x=40,maxlength=3, color=(255,0,0), prompt='#:', restricted='0123456789')
            self._old_tbox_value = ''
        else:
            #used to let us know NOT to try and render this section
            self.tbox = None
        
        self.active = False
        
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
        
        #can this block be dragged? (override in sub classes!)
        self.draggable = False
        self.color = (255,255,0)#outline color
    def draw(self,screen,rect):
        
        self.surf.blit(self.img,(0,0))
        if self.lable:
            self.surf.blit(self.lable,self.lable_pos)
        if self.tbox:
            self.tbox.draw(self.surf,self.active)
            
        screen.blit(self.surf,rect)
        
    def event_engine(self,events,pmap,loc):
        '''run by every tile in the grid,so dont take TOO long.
        
        notes:::
            1: use self.active for events that should only happen when a tile is currently selected as "active" eg: text_box update
            
            2: if sub classes wish to over-ride this, fine, just call it to do background stuff. (unless you want a block to ignore you)
            '''
        
        if self.tbox and self.active:
            self.tbox.update(events,True)
            if self._old_tbox_value != self.tbox.value:
                self._old_tbox_value = self.tbox.value
                pmap.render()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pass
            elif event.type == MOUSEBUTTONDOWN and event.button==1:
                if self.tbox:
                    if self.tbox.rect.collidepoint(self._rel_click(pmap,event.pos)):
                        self.active = True
                    else:
                        self.active = False
    ##link block decorators:::
    ##if "set", tey set themselves to other, and also set other.xblock to self(or none if unlinking)
    @lib.decorators.propget
    def dblock(self):
        return self._dblock
    @lib.decorators.propset
    def dblock(self,other):
        if other is None:
            #set the other block's corrisponing to None as well...
            #use name in self because other is None right now...
            try:
                self._dblock._ublock = None
            except AttributeError as e:
                pass
        else:
            other._ublock = self
        self._dblock = other
        
    @lib.decorators.propget
    def ublock(self):
        return self._ublock
    @lib.decorators.propset
    def ublock(self,other):
        if other is None:
            #set the other block's corrisponing to None as well...
            try:
                self._ublock._dblock = None
            except AttributeError as e:
                pass
        else:
            other._dblock = self
        self._ublock = other
        
    @lib.decorators.propget
    def lblock(self):
        return self._lblock
    @lib.decorators.propset
    def lblock(self,other):
        if other is None:
            #set the other block's corrisponing to None as well...
            try:
                self._lblock._rblock = None
            except AttributeError as e:
                pass
        else:
            other._rblock = self
        self._lblock = other
        
    @lib.decorators.propget
    def rblock(self):
        return self._rblock
    @lib.decorators.propset
    def rblock(self,other):
        if other is None:
            #set the other block's corrisponing to None as well...
            try:
                self._rblock._lblock = None
            except AttributeError as e:
                pass
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
    
    def check_drag_click(self,pmap,mouse_pos,map_pos):
        '''see if click registers on this tiles self.click_rect'''
        
        return self.drag_rect.collidepoint(self._rel_click(pmap,mouse_pos,map_pos))
        
    def _rel_click(self,pmap,mouse_pos,map_pos=None):
        if map_pos is None:
            map_pos = pmap.click_engine(mouse_pos)
        if map_pos == self.loc:
            return (mouse_pos[0]%pmap.sub_rect.width,mouse_pos[1]%pmap.sub_rect.height)
        else:
            return (-1,-1)
    def drag(self,pmap):
        '''cleans up object for a 'drop' '''
        self.dblock = None
        self.ublock = None
        self.lblock = None
        self.rblock = None
        pmap.map[self.loc][0] = bgnd_block()
        return self
        
    def able_drop(self,pos,pmap):
        '''find any problems with the drop and return False if obstructed.
        else return True'''
        pass
    def drop(self,pos,pmap):
        '''finalize a drop. actually places block on grid'''
        pass
    def __getstate__(self):
        state=self.__dict__.copy()
        state.pop('lable')
        state.pop('surf')
        state.pop('img')
        #if not isinstance(self,bgnd_block):
        #    print self,self.dblock
        return state
    def __setstate__(self,state):
        self.__dict__.update(state)
        if hasattr(self,'text'):
            self.lable=lib.common.font.render(*self.text).convert_alpha()
        else:
            self.lable = None
        self.img=lib.common.load_img(*self.file)
        self.surf = pygame.Surface((80,80),pygame.SRCALPHA)
        #if not isinstance(self,bgnd_block):
        #    print self,self.dblock
            
class bgnd_block(block):
    def __init__(self):
        self.file=('gui','programmer','background_bgnd.png')
        block.__init__(self,self.file)
        self.link_down  = False
        self.link_up    = True
        self.blank = True
        self.loc = (0,0)
    def event_engine(self,events,pmap,loc):
        '''we are a blank block, dont care none about them events'''
        pass
class vertical_block(block):
    def __init__(self,img,lable=None,num=None):
        block.__init__(self,img,lable,num)
        self.link_up   = True
        self.link_down = True
        self.draggable = True
        
        
    def next(self,robot):
        if self.dblock:
            return self.dblock
        else:
            return False
        
    def able_drop(self,pos,pmap):
        #firstly: check for up block
        up=pos[0],pos[1]-1
        if up[1] < 0:
            logger.debug('we are at the top, cant place block here!')
            return False
        if not pmap.map[up][0].link_down:
            logger.debug('block above cant be linked downwards, cant place block there!')
            return False
            
        #secondly: check for down block:
        down=pos[0],pos[1]+1
        #we dont care about running off the map if down is off, because this block is able to "end" code
        #but lets check IF there even IS a block there...
        if pmap.map.has_key(down):
            if not pmap.map[down][0].link_up:
                logger.debug('block below doesnt allow linking')
                return False
        return True
        
    def drop(self,pos,pmap):
        if self.able_drop(pos,pmap):
            pmap.map[pos][0]=self
            up=pos[0],pos[1]-1
            pmap.map[up][0].dblock = self
        
            down=pos[0],pos[1]+1
            pmap.map[down][0].ublock = self
        else:
            raise Error('must be able to place block before drop')
        self.loc=pos
        
class pfwd_block(vertical_block):
    def __init__(self):
        self.file=('gui','programmer','blank_vert.png')
        img=lib.common.load_img(*self.file)
        self.text=('Forward',True,(255,0,0))
        lable = lib.common.font.render(*self.text).convert_alpha()
        num=True
        vertical_block.__init__(self,img,lable,num)
        
    def action(self,robot):
        try:times=int(self.tbox.value)
        except:times=1
        for i in range(times):
            robot.move_fwd()
        
class trnl_block(vertical_block):
    def __init__(self):
        self.file = ('gui','programmer','blank_vert.png')
        img=lib.common.load_img(*self.file)
        self.text=('Turn Left',True,(255,0,0))
        lable = lib.common.font.render(*self.text).convert_alpha()
        vertical_block.__init__(self,img,lable)
        
    def action(self,robot):
        robot.turn('left')

class trnr_block(vertical_block):
    def __init__(self):
        self.file = ('gui','programmer','blank_vert.png')
        img=lib.common.load_img(*self.file)
        self.text=('Turn Right',True,(255,0,0))
        lable = lib.common.font.render(*self.text).convert_alpha()
        vertical_block.__init__(self,img,lable)
        
    def action(self,robot):
        robot.turn('right')
        
class main_block(block):
    def __init__(self,loc):
        self.file=('gui','programmer','main_main.png')
        block.__init__(self,self.file)
        self.link_down=True
        self.loc=loc
    def action(self,robot):
        '''do nothing, pass along. this is not the robot you are looking for'''
        pass
    
    def next(self,robot):
        if self.dblock:
            return self.dblock
        else:
            return False
        