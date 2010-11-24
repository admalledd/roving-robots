import os
import logging
logger=logging.getLogger('programmer')

import pygame
from pygame.locals import *

import map
import input
import lib
import blocks
MAIN_BLOCK=(5,0)
class remover(object):
    def __init__(self):
        self.surf = lib.common.load_img(os.path.join('gui','programmer','trash.png'))
    def draw(self,surf,rect):
        surf.blit(self.surf,rect)


class interface(object):
    def __init__(self,pmap):
        self.inmap = map.MAP(r_c=(1,15),
                             sub_rect=pygame.Rect((0,0),(80,80)),
                             main_rect=pygame.Rect((700,0),(80,560)),
                             tclass=blocks.bgnd_block
                            )
                       
        self.inmap.map[(0,1)][0] = blocks.pfwd_block()
        self.inmap.map[(0,2)][0] = blocks.trnl_block()
        self.inmap.map[(0,3)][0] = blocks.trnr_block()
        
        self.inmap.show_grid=True
        
        self.inmap.render()
        
        
        pmap.map[(5,0)][0]=blocks.main_block(MAIN_BLOCK)
        
    def click_engine(self,pos):
        '''this is for the spawning and other thing within the interface
        it has nothing to do with the event engine of the pmap system...'''
        #for key,value in self.spawns.items():
        #    if value[0][1].collidepoint(pos):
        #        logger.debug('hit spawn:%s'%key)
        #        return value[1]()
        
        logger.debug('running intr.click_engine')
        intr_button = self.inmap.click_engine(pos)
        
        if intr_button != (-1,-1):
            if isinstance(self.inmap.map[intr_button][0],blocks.block):
                input.mouse.cur_sel = self.inmap.map[intr_button][0].__class__()
                
    def event_engine(self,events,pmap):
        '''pass all events to all tiles, and also update this interface.'''
        #for event in events:
        #    pass
            
        for tile,loc in pmap.tile_gen():
            tile[0].event_engine(events,pmap,loc)
        
    def draw(self, screen):
        #for key,value in self.spawns.items():
            #value[0][0].draw(screen,value[0][1])
        self.inmap.draw(screen)
def create_programming_gui(screen,pmap):
    back_ground = screen.copy()
    if pmap == None:
        pmap = map.MAP(r_c=(15,15),
                       sub_rect=pygame.Rect((0,0),(80,80)),
                       main_rect=pygame.Rect((0,0),(640,560)),
                       tclass=blocks.bgnd_block)
        pmap.show_grid = True
    map.cur_map = pmap
    intr = interface(pmap)
    
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
        pmap.draw(screen)
        intr.draw(screen)
        
        events = pygame.event.get()
        
        for event in events:
            if (event.type == KEYDOWN and event.key == K_p):
                ##time to return a pmap object, clean up things first though...
                del intr
                input.mouse.cur_sel = None
                
                ##done cleaning, return pmap
                return pmap
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
                map_pos = pmap.click_engine(event.pos)
                if map_pos !=(-1,-1):
                    tile_rel =  pmap.map[map_pos][0]._rel_click(pmap,event.pos,map_pos)
                else:
                    tile_rel = (-2,-2)
                logger.debug("m=%s t=%s r=%s"%(event.pos,map_pos,tile_rel))
                ##drop button
                if input.mouse.cur_sel and (map_pos != (-1,-1)):
                    
                    if input.mouse.cur_sel.able_drop(map_pos,pmap):
                        input.mouse.cur_sel.drop(map_pos,pmap)
                        ##dont forget to clean mouse...
                        input.mouse.cur_sel = None
                        
                    pmap.render()
                
                ##pick up button
                elif input.mouse.cur_sel is None and \
                     (map_pos != (-1,-1)) and \
                     pmap.map[map_pos][0].draggable and \
                     pmap.map[map_pos][0].check_drag_click(pmap,event.pos,map_pos):
                    ##we have no mouse item
                    ##map pos is good
                    ##button CAN be dragged...
                    ##click hits drag location on tile
                    input.mouse.cur_sel = pmap.map[map_pos][0].drag(pmap)
                    pmap.render()
                
                elif map_pos == (-1,-1):
                    ##we are off the map, lets check if the interface needs anything...
                    
                    ##try to make a button, remove whatever is __in__ the mouse right now
                    ##moved button ccreation to intrface, should have been its job from start
                    intr.click_engine(event.pos)
                    
                
        intr.event_engine(events,pmap)
        if input.mouse.cur_sel:
            input.mouse.cur_sel.draw(screen,input.mouse.cur_pos())
        
        
        pygame.display.flip()




if __name__ == '__main__':
    pygame.init()
    lib.common.debug(2)
    screen = pygame.display.set_mode((800, 600))
    #load map tiles...
    import tiles
    tiles.find_tiles()
    
    create_programming_gui(screen,None)