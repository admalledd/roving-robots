import pygame
import os

import lib




if __name__ == '__main__':
    
    pygame.mixer.init()
    
    lib.common.set_directory()
    
    #screen = pygame.display.set_mode((800, 600))
    
    pre  = pygame.mixer.Sound(os.path.join(lib.common.curdir,'data', 'sounds', 'bg', 'electric_engine_start.ogg'))
    mid  = pygame.mixer.Sound(os.path.join(lib.common.curdir,'data', 'sounds', 'bg', 'electric_engine_loop.ogg'))
    post = pygame.mixer.Sound(os.path.join(lib.common.curdir,'data', 'sounds', 'bg', 'electric_engine_end.ogg'))
    
    chan = pygame.mixer.Channel(0)
    
    chan.play(pre)
    chan.queue(mid)
    #pygame.time.wait(10)
    while chan.get_queue():
        pygame.time.wait(10)
        print 'playing pre'
    
    chan.queue(post)
    #pygame.time.wait(10)
    while chan.get_queue():
        pygame.time.wait(10)
        print 'playing mid'
    
    #pygame.time.wait(10)
    while chan.get_busy():
        pygame.time.wait(10)
        print 'playing prost'
    
    
    