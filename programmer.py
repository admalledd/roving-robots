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
        self.surf = pygame.Surface((80,80),pygame.SRCALPHA)
        self.drag_rect=pygame.Rect((0,0),(10,10))
        
        if num is not None:
            if isinstance(num,input.Input):
                self.tbox = num
            else:
                self.tbox = input.Input(y=40,x=20,maxlength=3, color=(255,0,0), prompt=' ', restricted='0123456789')
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
        
    def draw(self,screen,rect):
        
        self.surf.blit(self.img,(0,0))
        if self.lable:
            self.surf.blit(self.lable,self.lable_pos)
        if self.tbox:
            self.tbox.draw(self.surf)
            
        screen.blit(self.surf,rect)
        
    def event_engine(self,events,pmap,loc):
        '''run by every tile in the grid,so dont take TOO long.
        
        notes:::
            1: use self.active for events that should only happen when a tile is currently selected as "active" eg: text_box update
            
            2: if sub classes wish to over-ride this, fine, just call it to do background stuff. (unless you want a block to ignore you)
            '''
        for event in events:
            if event.type == KEYDOWN:
                if self.tbox and self.active:
                    self.tbox.update(events,True)
                elif event.key == K_RETURN:
                    pass
            elif event.type == MOUSEBUTTONDOWN and event.button==1:
                if self.tbox:
                    if self._surf_click(self.tbox.rect,pmap,event.pos,loc):
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
        
        return self._surf_click(self.drag_rect,pmap,mouse_pos,map_pos)
        
    def _surf_click(self,rect,pmap,mouse_pos,map_pos):
        return rect.collidepoint(mouse_pos[1]%pmap.sub_rect.height,mouse_pos[0]%pmap.sub_rect.width)
    
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
        self.blank = True
    def event_engine(self,events,pmap,loc):
        '''we are a blank block, dont care none about them events'''
        pass
class pfwd_block(block):
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
        
        self.main_block = main_block()
        
        
    def click_engine(self,pos):
        '''this is for the spawning and other thing within the interface
        it has nothing to do with the event engine of the pmap system...'''
        for key,value in self.spawns.items():
            if value[0][1].collidepoint(pos):
                logger.debug('hit spawn')
                return value[1](value[0][0])
    def event_engine(self,events,pmap):
        '''pass all events to all tiles, and also update this interface.'''
        #for event in events:
        #    pass
            
        for tile,loc in pmap.tile_gen():
            tile[0].event_engine(events,pmap,loc)
        
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
        if isinstance(cur,bgnd_block):
            #looks like we have a bgblock, exit loop
            cur = False
            
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
    
    clock = pygame.time.Clock()
    _fps=0
    while True:
        clock.tick(30)
        if int(clock.get_fps()) != _fps:
            _fps = int(clock.get_fps())
            
        #blit background FIRST! (it my just so happen to cover up your other stuff...)
        screen.fill((0, 0, 0))
        #draw background (img of robots/terrain)
        screen.blit(back_ground,(0,0))
        
        #lag drawing by one loop, allaowing events to draw OVER screen...
        intr.draw(screen)
        pmap.draw(screen)
        events = pygame.event.get()
        
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
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
                ##TODO::: use the blocks own event_engine to do dragging? (click only in block.drag_rect?)
                
                elif input.mouse.cur_sel is None and \
                     (map_pos != (-1,-1)) and \
                     pmap.map[map_pos][0].draggable and \
                     pmap.map[map_pos][0].check_drag_click(pmap,event.pos,map_pos):
                    #we have no mouse item
                    #map pos is good
                    #button CAN be dragged...
                    #click hits drag location on tile
                    input.mouse.cur_sel = pmap.map[map_pos][0].drag(pmap)
                    pmap.render()
                    
                ##ok... we FINALY finished darg+drop, now to avtive/inactive:
                #elif input.mouse.cur_sel is None and \
                #     (map_pos != (-1,-1)):
                #    input.mouse.active = 
                
                elif map_pos == (-1,-1):
                    #we are off the map, lets check if the interface needs anything...
                    
                    #try to make a button, remove whatever is __in__ the mouse right now
                    ret = intr.click_engine(event.pos)
                    if ret:
                        input.mouse.cur_sel = ret
                        
                
        intr.event_engine(events,pmap)
        if input.mouse.cur_sel:
            input.mouse.cur_sel.draw(screen,input.mouse.cur_pos())
        
        
        pygame.display.flip()




if __name__ == '__main__':
    pygame.init()
    lib.common.debug(2)
    screen = pygame.display.set_mode((800, 600))
    #load map tiles...
    tiles.find_tiles()
    
    create_programming_gui(screen)