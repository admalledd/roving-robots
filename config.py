'''configuration/menu system
note::: 
    make sure that all key short cuts have mapped GUI interface
key components: 
    1:change_config(screen)
        exactly what it says
    
    2:keymap
        dictionary mapping strings to keys'''

import os
import logging
logger=logging.getLogger('config')

import pygame
from pygame.locals import *

import lib




keycfg=lib.configobj.ConfigObj(os.path.join(lib.common.curdir,'config.ini'))
keymap=keycfg['keymap']

def change_config(screen):
    
    back_ground = screen.copy()
    back_ground.blit(lib.common.load_img('gui','menu','background.png'),(80,60))
    
    #text to render and draw...
    info=lib.common.txt_box_render('''welcome to the configuration menu!\npress enter to return keyconfig to defaults\npress esc to return to game''',
                                  pygame.Rect((80,60),(320,240)),
                                  (255,255,255)
                                  )
    
    
    
    clock = pygame.time.Clock()
    _fps=0
    while True:
        clock.tick(30)
        if int(clock.get_fps()) != _fps:
            _fps = int(clock.get_fps())
            
        #blit background FIRST! (it my just so happen to cover up your other stuff...)
        
        #draw background (img of robots/terrain)
        screen.blit(back_ground,(0,0))
        
        
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                print keymap
                keymap['open_programmer']=K_p
                
            elif event.type == KEYDOWN and event.key == K_RETURN:
                logger.info('default keymap loaded')
                keycfg['keymap']['open_programmer'] =K_p                keycfg['keymap']['open_config']     =K_c                keycfg['keymap']['open_menu']       =K_ESCAPE                keycfg['keymap']['open_factory']    =K_t                keycfg['keymap']['goto_robot']      =K_g                keycfg['keymap']['goto_base']       =K_b                keycfg['keymap']['follow_robot']    =K_f                keycfg['keymap']['map_up']          =K_UP                keycfg['keymap']['map_down']        =K_DOWN                keycfg['keymap']['map_left']        =K_LEFT                keycfg['keymap']['map_right']       =K_RIGHT                keycfg['keymap']['program_run']     =K_r                keycfg['keymap']['program_stop']    =K_x
                
                keycfg.write()
                
        for line,rect in info:
            screen.blit(line,rect)
        pygame.display.flip()
    
if __name__ == '__main__':
    
    pygame.init()
    lib.common.debug(2)
    screen = pygame.display.set_mode((800, 600),pygame.SRCALPHA)
    change_config(screen)