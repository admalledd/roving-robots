'''an attempt (however poorly) to recreate the game known as stormrunner from lego
into a python game.'''
import pygame
from pygame.locals import *
import sys

import map
import lib.common

import tiles

from mouse import mouse
import load_map
import vehicle

def main():
    #init stuff....
    pygame.init()
    lib.common.set_directory()
    screen = pygame.display.set_mode((800, 600))
    
    #load map tiles...
    tiles.find_tiles()
    
    #load map... (can be called again(?) to change to a new map...)
    load_map.load_map('test_map')
    
    v=vehicle.rcx()
    while True:
        pygame.time.wait(10)
        
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return None
            elif event.type == MOUSEBUTTONDOWN and event.button==1:
                mouse.click_engine(event.pos)
        ##map no longer is in charge of events...
        #map.map.events(events)
        map.map.draw(screen)
        
        v.events(events)
        v.draw(screen)
        
        pygame.display.flip()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        #eventually change to be based off the optparse module instead...
        if sys.argv[1].startswith('-v'):
            lib.common.debug=len(sys.argv[1][1:])
    if lib.common.debug>0:print 'debug level is:%s'%lib.common.debug
    main()