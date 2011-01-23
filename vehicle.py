import os
import logging
logger=logging.getLogger('vehicle')
import pygame
from pygame.locals import *


import lib.common 
from lib.decorators import *

import map
import programmer
import overlays

class rcx(object):

    def __init__(self):
        self.loc=(8,6)
        
        self.img = lib.common.load_img(os.path.join('rcx','test.bmp')).convert()
        self.img.set_colorkey((255,0,255))
        
        self.rect = self.img.get_rect()
        
        self._direction = 'n'
        
        self.items=[]
        
        #item on the arm  (disable arm when not equipped..?)
        self.arm=None
        
        self.ani_step = 0
        
        self.vmove='walkable' ##type of terrain i can move across
        
        ##removed code sample, merging pgrid.py into programmer.py
        self.code=None
        self.cur_cmd=None
        
    def draw(self,screen):
        self.rect.center = map.map.map[self.loc][1].center
        screen.blit(self.img,self.rect)
        
        #find direction end_pos:
        if self.direction == 'n':
            end_pos = self.rect.midtop
        if self.direction == 'e':
            end_pos = self.rect.midright
        if self.direction == 's':
            end_pos = self.rect.midbottom
        if self.direction == 'w':
            end_pos = self.rect.midleft
        pygame.draw.line(screen, (255,0,255), self.rect.center, end_pos, 3)
        
    def events(self,events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.turn('left')
                elif event.key == K_RIGHT:
                    self.turn('right')
                elif event.key == K_UP:
                    self.move_fwd()
                elif event.key == K_DOWN:
                    self.move_bck()
                elif event.key == K_SPACE:
                    if self.arm:
                        self.put_down()
                    else:
                        self.pick_up()
                elif event.key == K_RETURN:
                    self.run_cmd()
    def move_fwd(self):
        '''programming tool's job is to decide how often to run these things...'''
        if not self.front_sq() in map.map.overlays and self.vmove in map.map.map[self.front_sq()][0].vmove:
            if self.direction == 'w':
                self.loc=(self.loc[0]-1,self.loc[1])
            elif self.direction == 'e':
                self.loc=(self.loc[0]+1,self.loc[1])
            elif self.direction == 'n':
                self.loc=(self.loc[0],self.loc[1]-1)
            elif self.direction == 's':
                self.loc=(self.loc[0],self.loc[1]+1)
        else:
            self.play_sound('err')
            self.play_ani('move_err:%s'%self.direction)
    def move_bck(self):
        '''programming tool's job is to decide how often to run these things...'''
        if not self.back_sq() in map.map.overlays and self.vmove in map.map.map[self.back_sq()][0].vmove:
            if self.direction == 'e':
                self.loc=(self.loc[0]-1,self.loc[1])
            elif self.direction == 'w':
                self.loc=(self.loc[0]+1,self.loc[1])
            elif self.direction == 's':
                self.loc=(self.loc[0],self.loc[1]-1)
            elif self.direction == 'n':
                self.loc=(self.loc[0],self.loc[1]+1)
    
    @propget
    def direction(self):
        return self._direction
        
    @propset
    def direction(self, value):
        l=('left','l')
        r=('right','r')
        if self._direction == 'n':
            if value in l:
                self._direction = 'w'
                self.play_ani('turn:n->w')
            elif value in r:
                self._direction = 'e'
                self.play_ani('turn:n->e')
        elif self._direction == 'e':
            if value in l:
                self._direction = 'n'
                self.play_ani('turn:e->n')
            elif value in r:
                self._direction = 's'
                self.play_ani('turn:e->s')
        elif self._direction == 's':
            if value in l:
                self._direction = 'e'
                self.play_ani('turn:s->e')
            elif value in r:
                self._direction = 'w'
                self.play_ani('turn:s->w')

        elif self._direction == 'w':
            if value in l:
                self._direction = 's'
                self.play_ani('turn:w->s')
            elif value in r:
                self._direction = 'n'
                self.play_ani('turn:w->n')
        
    def turn(self,way):
        
        self.direction = way
        
    def front_sq(self):
        if self.direction == 'w':
            return (self.loc[0]-1,self.loc[1])
        elif self.direction == 'e':
            return (self.loc[0]+1,self.loc[1])
                
        elif self.direction == 'n':
            return (self.loc[0],self.loc[1]-1)
                
        elif self.direction == 's':
            return (self.loc[0],self.loc[1]+1)
                
    def back_sq(self):
        if self.direction == 'e':
            return (self.loc[0]-1,self.loc[1])
        elif self.direction == 'w':
            return (self.loc[0]+1,self.loc[1])
                
        elif self.direction == 's':
            return (self.loc[0],self.loc[1]-1)
                
        elif self.direction == 'n':
            return (self.loc[0],self.loc[1]+1)
    
    @propget
    def loc(self):
        return self._loc

    @propset
    def loc(self, value):
        self._loc=value[0],value[1]
        map.map.loc=value[0]-8,value[1]-6
    
    def pick_up(self):
    
        if not self.arm:
            if self.front_sq() in map.map.overlays and isinstance(map.map.overlays[self.front_sq()],overlays.item):
                self.arm = map.map.overlays[self.front_sq()]
                map.map.remove_overlay(self.front_sq())
                self.play_sound('pick_up_item')
                self.play_ani('pick_up:%s'%self.direction)
                map.map.render()
            else:
                self.play_sound('err')
                self.play_ani('pick_up_err:%s'%self.direction)
        else:
            self.play_sound('err')
            self.play_ani('pick_up_err:%s'%self.direction)
    
    def put_down(self):
    
        if self.arm:
            if not self.front_sq() in map.map.overlays:
                map.map.add_overlay(self.front_sq(), self.arm)
                self.arm = None
                self.play_sound('put_down_item')
                self.play_ani('put_down:%s'%self.direction)
                map.map.render()
            else:
                self.play_sound('err')
                self.play_ani('put_down_err:%s'%self.direction)
        else:
            self.play_sound('err')
            self.play_ani('put_down_err:%s'%self.direction)
                
    def store(self):
        if self.arm:
                self.items.append(self.arm)
                self.arm = None
                self.play_sound('store_item')
                self.play_ani('store:%s'%self.direction)
        else:
            self.play_sound('err')
            self.play_ani('store_err:%s'%self.direction)
    #TODO: retrieve    
    @disabled
    def play_ani(self,cmd):
        '''how  this works: changes the self.surf attribute for every frame of the animation
        
        ideas for implimentation:
            1: after current animation finishes, run next command... (if of correct type?)
            2: use pygame.time.clock() to keep same speeds of frame movement?'''
        if cmd == None:
            self.ani_step += 1
        
        else:
            if self.ani_step > 0:
                return #error... should not play animations at the same time...
            elif os.path.exists(os.path.join(lib.common.curdir,'rcx', 'ani' , cmd.split(':')[0])):
                pass
        file = os.path.join(lib.common.curdir,'rcx', 'ani' , cmd.split(':')[0] , ''.join((cmd.split(':')[1],'00.png')))
        print 'vehicle::%s'%file
        
        
    @disabled
    def play_sound(self,cmd):
        '''just use the pygame sound library to play misc sounds...'''
        pass
        
    def run_cmd(self):
        '''ask code object to run to next command
        note: returning to code after completion is _INTENDED_ to take two "runs"
              it was just by hapenstance that it uses two, one for the last bgnd block
              and one for main block.'''
        if not self.cur_cmd:
            if self.code:
                self.cur_cmd = self.code.map[programmer.MAIN_BLOCK][0]
            else:
                logger.warn('robot tried to run with no code!')
                self.play_sound('err')
                return
        logger.debug('cur_cmd:%s'%self.cur_cmd)
        self.cur_cmd.action(self)
        self.cur_cmd = self.cur_cmd.next(self)
        
        