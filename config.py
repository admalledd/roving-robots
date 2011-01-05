'''configuration/menu system

key components: 
    1:change_config(screen)
        exactly what it says
    
    2:keymap
        dictionary mapping strings to keys'''

import ConfigParser
import os
import logging
logger=logging.getLogger('config')

import pygame
from pygame.locals import *

import lib


keycfg=ConfigParser.ConfigParser()
keycfg.read(os.path.join(lib.common.curdir,'config.ini'))
keymap=keycfg._sections['keymap']

def change_config(screen):
    
    back_ground = screen.copy()
    
    
    clock = pygame.time.Clock()
    _fps=0
    while True:
        clock.tick(30)
        if int(clock.get_fps()) != _fps:
            _fps = int(clock.get_fps())
            
        #blit background FIRST! (it my just so happen to cover up your other stuff...)
        
        #draw background (img of robots/terrain)
        screen.blit(back_ground,(0,0))
        screen.fill((0, 25, 0,50))
        
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                print keymap
                #keymap['open_proggrammer']=K_p
                
            elif event.type == KEYDOWN and event.key == K_RETURN:
                print 'new keymap loaded'
                keycfg._sections['keymap']={
                                                '__name__':'keymap',#was part of the original dict...
                                                'open_programmer':K_p,
                                                'open_menu':K_ESCAPE,
                                                'goto_robot':K_g,
                                                'follow_robot':K_f,
                                                'map_up':K_UP,
                                                'map_down':K_DOWN,
                                                'map_left':K_LEFT,
                                                'map_right':K_RIGHT
                                                
                                           }
                
                keycfg.write(open(os.path.join(lib.common.curdir,'config.ini'),'w'))
                
    
        pygame.display.flip()
    
if __name__ == '__main__':
    
    pygame.init()
    lib.common.debug(2)
    screen = pygame.display.set_mode((800, 600),pygame.SRCALPHA)
    change_config(screen)