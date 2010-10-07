
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

class block(object):
    def __init__(self,img,lable,num=None):
        '''example init:::
        block(os.path.join(~~~~~),pygame.font.render(~~~~~),1)'''
        self.img = lib.common.load_img(img)
        self.lable = lable
        if num is not None:
            self.num = num
        pass
    def link_up(self):
        pass
    def link_down(self):
        pass
    def link_left(self):
        pass
    def link_right(self):
        pass
    
    #properties--> block locations
    def dblock(self):
        pass
    
    def ublock(self):
        pass
    def lblock(self):
        pass
    def rblock(self):
        pass
        
    #action stuff
    def action(self,robot):
        pass
        
    def drag(self):
        '''cleans up object for a 'drop' '''
        pass
    def drop(self,pos):
        '''find any problems with the drop and cancle it if needed...'''
        pass
    def save(self):
        '''return a string which will allow recreation of this block (type,lable,num,pos,binding)'''
        pass
    def load(self,s):
        '''places block and recreates block based on "s" '''
        pass
def test():
    pmap = map.MAP(r_c=(160,121),
                   sub_rect=pygame.Rect((0,0),(50,50)),
                   main_rect=pygame.Rect((0,0),(475,475)),
                   tclass=tile)
    























if __name__ == '__main__':
    test()