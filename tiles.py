import os
import pygame
import lib
import random
tile_cache=None
prog_cache=None
walkable=tuple()
class tile(object):
    def __init__(self,type=None):
        if type==None:
            #get a random tile from the cache
            #to be depreciated...
            self.set_tile()
        self.walkable=False
        
        self.item = None
    def set_tile(self,type=None):
        if type is not None and len(type) < 4:
            raise Exception('tile type MUST be a four-charichtar length string!')
        self.type=type
        if type=='rand':
            #get a random tile from the cache
            self.surf=tile_cache.get(tile_cache.cache.keys()[int(random.random()*len(tile_cache.cache.keys()))])
        else:
            try:
                self.surf = tile_cache.get(type)
            except:
                self.surf = tile_cache.get('uuuu')
        if type == None:
            self.walkable = False
        elif type in  walkable:
            self.walkable = True
        else:
            self.walkable = False
            
    def draw(self,screen,rect):
        screen.blit(self.surf,rect)
        if self.item:
            self.item.draw(screen,rect)
    @lib.decorators.propget
    def walkable(self):
        if self.item:
            return False
        else:
            return self._walkable
    @lib.decorators.propset
    def walkable(self, value):
        self._walkable=value

class Tile_Cache(object):
    def __init__(self,path):
        '''tile layout:::
        folder_xxxx.gif
        where xxxx is the direction and layout of the image.
        axxx == top right
        xaxx == bottom right
        xxax == bottom left
        xxxa == top left'''
        self.cache={}
        
        for dir, dirs, files in os.walk(path):
            for f in files:#we only need to look at the files for this...
                if f.endswith('.gif') or f.endswith('.png'):#check for img's only...
                    #see if similarly tagged img is in the cache...
                    imgname=f.split('.')[0].split('_')[1]
                    if imgname in self.cache:
                        self.cache[imgname].append(lib.common.load_img(dir,f))
                    else:
                        self.cache[imgname]= [lib.common.load_img(dir,f)]
                        
        if lib.common.debug() >2:
            import pprint
            f_ = open('random-tile-name-file.txt','w')
            pprint.pprint(self.cache,f_)
            f_.close()
        self.cache['uuuu']=pygame.Surface((50, 50))
        self.cache['uuuu'].fill((255,0,255))
    def get(self,key):
        if type(self.cache[key]) in (tuple,list):
            return random.choice(self.cache[key])
        else: return self.cache[key]
def find_tiles():
    global tile_cache
    tile_cache=Tile_Cache(os.path.join(lib.common.curdir,'data','img','tiles'))
    #global prog_cache
    #prog_cache=Tile_Cache(os.path.join(lib.common.curdir,'data','img','gui','programmer'))
    
def set_tile(loc,type):
        map.map[loc][0].set_tile(type)
        