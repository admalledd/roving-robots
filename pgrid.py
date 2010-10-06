
import map
import tiles


class button(object):
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


def test():
    pmap = map.MAP(r_c=(160,121),
                   sub_rect=pygame.Rect((0,0),(50,50)),
                   main_rect=pygame.Rect((0,0),(475,475)),
                   tclass=tile)
    























if __name__ == '__main__':
    test()