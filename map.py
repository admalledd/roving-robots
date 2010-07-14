import pygame
from pygame.locals import *
import lib.common 
import lib

from tiles import tile
from lib.decorators import propget, propset, propdel


class MAP(object):
    '''self.map={(x,y):(tile,rect,border color}
    third data point is left in as the possibility remains
    that i might want to use it for some random tile data...
    
    possibly creature/objects on said tile?'''
    def __init__(self,r_c=(160,121),sub_rect=pygame.Rect((0,0),(50,50)),main_rect=pygame.Rect((0,0),(475,475))):
        if lib.common.debug > 0:
            self.font = pygame.font.Font(None, 18)
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
                #print color
                self.map[(x,y)]=[tile(),tmp,color]
        self.surf=pygame.Surface((self.main_rect.width,self.main_rect.height))
        
        self.loc=(0,0)
    def render(self,screen):
        '''iterate through every tile and move it and draw the contents'''
        screen.fill((0,0,0))
        for x in range(self.main_rect.width/self.sub_rect.width):
            for y in range(self.main_rect.height/self.sub_rect.height):
                try:
                    #set current grid x and y locations
                    xx=self.loc[0]+x
                    yy=self.loc[1]+y
                    #move the rectangle
                    tmp_r=self.map[(xx,yy)][1]
                    tmp_r.topleft=((self.main_rect.left +(x*self.sub_rect.width  )),
                                   (self.main_rect.top  +(y*self.sub_rect.height )))
                    if self.main_rect.contains(tmp_r):
                        #if the rect fits, draw it, else dont
                        self.map[(xx,yy)][0].draw(screen,tmp_r)
                        #screen.blit(self.map[(xx,yy)][0].surf,tmp_r)#render tile to map screen...
                        
                        ##enable to draw rect outlines
                        if self.show_grid:
                            pygame.draw.rect(screen, self.map[(xx,yy)][2], tmp_r, 1)
                        if lib.common.debug > 0:
                            #render tile number text...
                            text = self.font.render(str((xx,yy)),True,(0,0,255)).convert_alpha()
                            screen.blit(text,tmp_r)
                except KeyError:
                    pass#key that doesnt exist? how and why?
                    #keys that go out of the map is what happens when we have a blank tile in the viewport...
                    if lib.common.debug >2:
                        print x,y
                        print xx,yy
        if lib.common.debug > 0:
            screen.blit(self.font.render(str((xx,yy)),True,(0,0,255)).convert_alpha(),(0,24))
            screen.blit(self.font.render(str(self.loc)
                        ,True,(0,0,255)).convert_alpha(),(0,12))
        
        #draw rect around main map area... disabled until i need it for the multi interface...
        #pygame.draw.rect(screen, (0,255,255), self.main_rect, 1)
        
    def draw(self,screen):
        '''fast draw function.
        i use a surface buffer for the "real" draw function
        and re-blit it here.'''
        screen.blit(self.surf,self.main_rect)
    
    def click_engine(self,pos):
        '''return what tile was clicked. (tile pos only?)'''
        
        if self.main_rect.collidepoint(pos):
            for x in range(self.map_size[0]-1):
                for y in range(self.map_size[1]-1):
                    try:
                        #set current grid x and y locations
                        xx=self.loc[0]+x
                        yy=self.loc[1]+y
                        if self.map[(xx,yy)][1].collidepoint(pos):
                            if lib.common.debug > 1:
                                print "%s,%s clicked"%(xx,yy)
                            return (xx,yy)
                            
                    except KeyError:
                        pass
        return (-1,-1)
    @propget
    def loc(self):
        '''this is perhaps one of my favorite little python hidden secrets:
            object attribute decorators... whenever i "get" the variable
            "self.loc" this function runs'''
        return self._loc

    @propset
    def loc(self, value):
        '''but, when i "set" self.loc, this function runs! even more, this 
        way, when i move the map, (changing the top left number self.loc)
        i re-render it!!
        
        now, if only there was a way to get pydev to understand this...'''
        self._loc=value
        self.render(self.surf)
