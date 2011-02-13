'''an attempt (however poorly) to recreate the game known as stormrunner from lego
into a python game.

TODO:::
ask pypy if it can help with @propget speeds??
remake map_overlay concept
'''
import sys
import logging
logger = logging.getLogger('main')
import pygame
from pygame.locals import *


import config

import map
import lib.common

import tiles

import input
import load_map
import vehicle
import programmer


def main(options):
    pygame.init()
    screen = pygame.display.set_mode((800, 600),pygame.SRCALPHA)
    #load map tiles...
    tiles.find_tiles()
    #load map... (can be called again(?) to change to a new map...)
    load_map.load_map('test_map')
    
    
    v=vehicle.rcx()
    clock=pygame.time.Clock()
    
    while True:
        clock.tick(30)
        
        
        
        
        events = pygame.event.get()
        
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                return None
            elif event.type == MOUSEBUTTONDOWN and event.button==1:
                logger.info(map.map.click_engine(event.pos))
            
            elif event.type == KEYDOWN:
                if event.key == config.keymap['open_menu']:
                    ##to be changed later to actually open a main menu like thingy with save and stuff...
                    config.change_config(screen)
            
                elif event.key == config.keymap['open_programmer']:
                    ##warning:: blocking code
                    v.code = programmer.create_programming_gui(screen,v.code)
        ##we clear the screen after events because anything that can occur in the events should be 'blocking'
        ##meaning that they actualy run thier own loop for a bit
        screen.fill((0, 0, 0))
        
        map.map.draw(screen)
        map.map.update_overlays(screen)
        
        v.events(events)
        v.draw(screen)
        
        pygame.display.flip()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print 'i really need to add those command line options huh?'
        lib.common.debug(int(sys.argv[1]))
    lib.common.debug(2)
    main(None)
    
