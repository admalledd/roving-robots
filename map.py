import logging
logger = logging.getLogger('map')

import pygame
from pygame.locals import *
import lib.common 
import lib

from tiles import tile

#these are global objects created by load_map.py or programmer.create_programming_gui() respectivly
map=None
cur_map=None


##        .==.        .==.          
##       //`^\\      //^`\\         
##      // ^ ^\(\__/)/^ ^^\\        
##     //^ ^^ ^/6  6\ ^^ ^ \\       
##    //^ ^^ ^/( .. )\^ ^ ^ \\      
##   // ^^ ^/\| v""v |/\^ ^ ^\\     
##  // ^^/\/ /  `~~`  \ \/\^ ^\\    
##  -----------------------------
### HERE BE DRAGONS

class MAP(object):
    '''self.map={(x,y):(tile,rect,border color}
    third data point is left in as the possibility remains
    that i might want to use it for some random tile data...
    
    possibly creature/objects on said tile?'''
    def __init__(self,r_c=(160,121),sub_rect=pygame.Rect((0,0),(50,50)),main_rect=pygame.Rect((0,0),(475,475)),tclass=tile):
        if lib.common.debug() > 0:
            import os
            self.font = lib.common.font
        self.map_size=r_c
        self.sub_rect=sub_rect
        self.main_rect=main_rect
        self.show_grid = False
        self.map={}
        
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                tmp=pygame.Rect(self.sub_rect.topleft,self.sub_rect.size)
                tmp.topleft=((self.sub_rect.width*x)+self.main_rect.left,(self.sub_rect.height*y)+self.main_rect.top)
                color = (255,255,0)
                #set map items::: tile class, rect, and grid color
                self.map[(x,y)]=[tclass(),tmp,color]
        self.surf=pygame.Surface((self.main_rect.width,self.main_rect.height),pygame.SRCALPHA)
        
        ##set location _AND_ render! (remember @propset)
        self.loc=(0,0)
        
        ##overlay mechanism:::
        ##  dict of {map_loc:overlay_object}
        ##  an overlay object is something that:::
        ##      1:has a obj.draw(screen) function  (and it does draw to screen! no buffers!)
        ##      2:has a obj.ticktime variable, showing how often to update (see add_overlay to know the numbers allowed)
        ##      3:has a obj.update(ms) function, taking time since last update (if needed)
        ##  
        ##  note: your object will run only at most once a frame (game trys to run at 30 fps)
        ##  
        self.overlays={'times':[]}
        self.timer=pygame.time.Clock()
        self._ticktime=0##last run timer tick (eg 500)
        self._tickcount=0##current/last time from reset
    def add_overlay(self,loc,obj):
        
        ##first, check if this is a new ticktime:
        if obj.ticktime not in self.overlays['times']:
            self.overlays['times'].append(obj.ticktime)
            self.overlays['times'].sort()    
            ##if we dont have it in times, we must also not have it in self.overlays[obj.ticktime]
            self.overlays[obj.ticktime]=[]
        
        ##simple test for now, maybe have it just silently ignore the error? what should i do? i will wait untill i develop more
        if loc in self.overlays:
            print 'what? overlay exists!'
            return
        else:
            self.overlays[obj.ticktime].append(loc)
        ##finaly, add location/object pairing
        self.overlays[loc]=obj
        
    def remove_overlay(self,loc):
        
        ##remove object as soon as possible
        tmp = self.overlays[loc]
        del self.overlays[loc]
        self.overlays[tmp.ticktime].remove(loc)
        ##is this the last of overlays at a specific time tick?
        if len(self.overlays[tmp.ticktime]) == 0:
            self.overlays['times'].remove(tmp.ticktime)
            self.overlays['times'].sort()    
        del tmp
    def update_overlays(self,screen):
        '''if overlay time ticker doesnt pan out, we /can/ just iterate through self.overlays.iteritems()-->obj.ticktime
        
        note, should we also draw the overlays here? for now we will, for it is mighty convieniant placement
        
        for draw code, we pass:
            1: screen
            2: loc
            3: map[loc][1].center
            4: actual time from time tick (eg, we cant hit 500 ms exactly)
            5: map (self here)
        '''
        
        
        ##calculate timetick first...
        self._tickcount +=self.timer.tick()
        if self._tickcount > self._ticktime:
            curtimes=[]
            for time in self.overlays['times']:
                if time < self._tickcount:
                    curtimes.append(time)
                    for loc in self.overlays[time]:
                        self.overlays[loc].update(screen,loc,self.map[loc][1].center,self._tickcount,self)
            if len(curtimes) != 0:
                self._ticktime = curtimes[-1]
                
        if self._tickcount > 60000:
            #here we call all 59+ second objects and reset the counter
            self._tickcount = 0
            self._ticktime = 0
            for time in self.overlays['times']:
                if time >= 59000:
                    for loc in self.overlays[time]:
                        self.overlays[loc].update(screen,loc,self.map[loc][1].center,self._tickcount,self)
                        
    def render(self):
        '''iterate through every tile and move it and draw the contents'''
        logger.debug('rendering map::(%s,%s)'%(self.loc))
        self.surf.fill((0,0,0))
        for x in range(self.main_rect.width/self.sub_rect.width):
            for y in range(self.main_rect.height/self.sub_rect.height):
                try:
                    #set current grid x and y locations
                    xx=self.loc[0]+x
                    yy=self.loc[1]+y
                    #move the rectangle
                    tmp_r=self.map[(xx,yy)][1]
                    tmp_r.topleft=(x*self.sub_rect.width,
                                   y*self.sub_rect.height )
                    #create copy to move and check against...
                    r_check = pygame.Rect(tmp_r)
                    
                    r_check.topleft=((self.main_rect.left +(x*self.sub_rect.width  )),
                                   (self.main_rect.top  +(y*self.sub_rect.height )))
                    if self.main_rect.contains(r_check):
                        #if the rect fits, draw it, else dont
                        self.map[(xx,yy)][0].draw(self.surf,tmp_r)
                        #self.surf.blit(self.map[(xx,yy)][0].surf,tmp_r)#render tile to map self.surf...
                        
                        ##enable to draw rect outlines
                        if self.show_grid:
                            pygame.draw.rect(self.surf, self.map[(xx,yy)][2], tmp_r, 1)
                        if lib.common.debug() > 0:
                            #render tile number text...
                            text = self.font.render(str((xx,yy)),True,(0,0,255)).convert_alpha()
                            self.surf.blit(text,tmp_r)
                except KeyError:
                    pass#key that doesnt exist? how and why?
                    #keys that go out of the map is what happens when we have a blank tile in the viewport...
                    if (xx >= 0 and yy >= 0):
                        if lib.common.debug() >2:
                            logger.debug('map location temp:%s,%s'%(x,y))
                            logger.debug('missing tile     :%s,%s'%(xx,yy))
        if lib.common.debug() > 0:
            self.surf.blit(self.font.render(str((xx,yy)),True,(0,0,255)).convert_alpha(),(0,24))
            self.surf.blit(self.font.render(str(self.loc)
                        ,True,(0,0,255)).convert_alpha(),(0,12))
        if lib.common.debug() > 1:
            #draw rect around main map area... disabled until i need it for the multi interface...
            pygame.draw.rect(self.surf, (0,255,255), self.main_rect, 1)
        
    def draw(self,screen):
        '''fast draw function.
        i use a surface buffer for the "real" draw function
        and re-blit it here.
        
        TODO:: known bug: if main_rect.topleft != (0,0) the position of the blocks falls apart'''
        screen.blit(self.surf,self.main_rect)
    
    def click_engine(self,pos):
        '''return what tile was clicked. (tile pos only?)'''
        if self.main_rect.collidepoint(pos):
            #fix pos for how far away from tl of screen we are...
            #must be done thanks to psudo surface
            pos=(pos[0]-self.main_rect.left,pos[1]-self.main_rect.top)
            for x in range(self.map_size[0]):
                for y in range(self.map_size[1]):
                    try:
                        #set current grid x and y locations
                        xx=self.loc[0]+(x)
                        yy=self.loc[1]+(y)
                        if self.map[(xx,yy)][1].collidepoint(pos):
                            logger.debug("%s,%s clicked"%(xx,yy))
                            return (xx,yy)
                            
                    except KeyError:
                        pass
        return (-1,-1)
    
    @lib.decorators.propget
    def loc(self):
        '''this is perhaps one of my favorite little python hidden secrets:
        object attribute decorators... whenever i "get" the variable
        "self.loc" this function runs'''
        return self._loc
    @lib.decorators.propset
    def loc(self, value):
        '''but, when i "set" self.loc, this function runs! even more, this 
        way, when i move the map, (changing the top left number self.loc)
        i re-render it!!
        
        now, if only there was a way to get pydev to understand this...'''
        self._loc=value
        self.render()
    def tile_gen(self):
        '''a generator using <yeild> to help with iterating over _every_ tile'''
        for x in range(self.map_size[0]-1):
            for y in range(self.map_size[1]-1):
                yield self.map[(x,y)],(x,y)


