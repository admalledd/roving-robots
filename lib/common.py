#from pygame.locals import *
import os
import pygame

import lib.decorators

curdir=''
debug=0
def set_directory(datadir='data'):
    """change the active directory for our use in the presentation
    tries three drifrent ways of finding the data files
        1:::see if the current directory has a directory {data}
        2:::check if directory up one has {data}
        3:::if none of these worked, find the location of this file and use it."""
    global curdir
    print "current path    ::",  os.getcwd()
    #check if current directory has a foldier with the same name as the dadadir variable...
    if os.path.exists(os.path.normpath(os.path.realpath(os.path.join(os.getcwd(),datadir)))):
        print 'current path works'
        curdir = os.getcwd()
        return
    #check one dir up from current...
    elif os.path.exists(os.path.normpath(os.path.realpath(os.path.join(os.getcwd(),'..',datadir)))):
        curdir = os.path.normpath(os.path.realpath(os.path.join(os.getcwd(),'..')))
        print "changing path to::" , curdir
        #os.chdir(curdir)
    #we have a problem... try loading from where this file is (hopefully...)
    else:
        print 'could not find data folder manualy, trying dynamicly...'
        import inspect
        class DummyClass: pass
        curdir = os.path.dirname(os.path.abspath(inspect.getsourcefile(DummyClass)))
        if os.path.exists(os.path.normpath(os.path.realpath(os.path.join(curdir,'..',datadir)))):
            curdir = os.path.normpath(os.path.realpath(os.path.join(curdir,'..')))
        else:
            print 'ERROR!! could not find main directory!'
            raise SystemExit
        print 'changing path to::' , curdir
        #os.chdir(curdir)

@lib.decorators.memoized
def load_img(name):
    """ Load image and return image object"""
    fullname = os.path.join(curdir,'data','img',name)
    try:
        image = pygame.image.load(fullname)
        #convert the img to have transparencies...
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image