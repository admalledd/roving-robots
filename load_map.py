'''tile layout:::
folder_xxxx.gif
where xxxx is the direction and layout of the image.
axxx == top right
xaxx == bottom right
xxax == bottom left
xxxa == top left'''
import os
import logging
logger=logging.getLogger('load_map')
import pygame

import tiles
import lib
import map
import items

import ConfigParser

def load_map(map_name):
    #open/convert map:
    data=open(os.path.join(lib.common.curdir,'data','maps',map_name+'.map'),'r').read().split('\n')
    
    
    map_size=len(data[0]),len(data)-1
    logger.info("map size:(%s , %s)"%(len(data),len(data[0])))
    
    #get a random tiles size...
    sub_rect= tiles.tile().surf.get_rect()
    
    #change this to change displayed map size.
    main_rect=pygame.Rect((0,0),(800,600))
    
    map.map = map.MAP(map_size,sub_rect,main_rect)
    
    
    #open and read map configuration
    map.cfg = ConfigParser.ConfigParser()
    map.cfg.read(os.path.join(lib.common.curdir,'data','maps',map_name+'.ini'))
    
    #set walkable tiles... (any and all other configs accesable through map.cfg)
    tiles.walkable=map.cfg.get('main','walkable').split('|')
    
    #get tile types (.=wwww @=bbbb e=(energry,%(.)))
    tile_names = dict(map.cfg.items('tiles'))
    #check for special tiles (energy, metal...) and convert...
    for key,value in tile_names.items():
        if value.count('|') > 0:
            tile_names[key] = tuple(value.split('|'))
    
    
    #set tiles!
    for i in range(0,len(data[0])):
        for j in range(0,len(data)-1):
            if data[j][i] in tile_names:
                #normal tile
                if type(tile_names[data[j][i]]) == str:
                    map.map.map[(i,j)][0].set_tile(tile_names[data[j][i]])
                #item carrying tile
                else:
                    map.map.map[(i,j)][0].set_tile(tile_names[data[j][i]][0])
                    #create item...
                    map.map.map[(i,j)][0].item =  eval('items.'+tile_names[data[j][i]][1])
            #we dont have the tile data... set as error tile...
            else:
                    
                map.map.map[(i,j)][0].set_tile('uuuu')