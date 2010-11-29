# py2exe setup program
from distutils.core import setup
import py2exe
import sys
import os
import glob, shutil
import pygame
sys.argv.append("py2exe")
 
VERSION = '0.0.9'
AUTHOR_NAME = 'Eric Driggers'
AUTHOR_EMAIL = 'admalledd@gmail.com'
##dont have website yet. :(
#AUTHOR_URL = "http://www.urlofyourgamesite.com/"
PRODUCT_NAME = "Roving Robots"
SCRIPT_MAIN = 'main.py'
VERSIONSTRING = PRODUCT_NAME + " ALPHA " + VERSION
ICONFILE = 'logo.ico'
 
# Remove the build tree on exit automatically
REMOVE_BUILD_ON_EXIT = True
PYGAMEDIR = os.path.split(pygame.base.__file__)[0]
 
SDL_DLLS = glob.glob(os.path.join(PYGAMEDIR,'*.dll'))
 
if os.path.exists('dist/'): shutil.rmtree('dist/')


##files to load/copy to distrobution
extra_files = [ ("",[ICONFILE,'logo.png','README','HISTORY']),
                    #map files
                   (os.path.join('data','maps')                         ,glob.glob(os.path.join('data','maps','*.ini'))),
                   (os.path.join('data','maps')                         ,glob.glob(os.path.join('data','maps','*.map'))),
                   
                   #images, GUI first ignore source files (.xfc extra)
                   (os.path.join('data','img','gui','programmer')       ,glob.glob(os.path.join('data','img','gui','programmer','*.png'))),
                   (os.path.join('data','img','items')                  ,glob.glob(os.path.join('data','img','items','*.png'))),
                   (os.path.join('data','img','rcx')                    ,glob.glob(os.path.join('data','img','rcx','*.bmp'))),
                   (os.path.join('data','img','rcx')                    ,glob.glob(os.path.join('data','img','rcx','*.png'))),#hows this work for non-existant files?
                   (os.path.join('data','img','tiles')                  ,glob.glob(os.path.join('data','img','tiles','*.gif'))),#to be converted to .png's later
                   
                   #fonts, and other text-rendering resources
                   (os.path.join('data',"fonts")                        ,glob.glob(os.path.join('data','fonts','*.ttf'))),
                   
                   #sounds/music
                   (os.path.join('data','sounds','bg')                  ,glob.glob(os.path.join('data','sounds','bg','*.ogg'))),
                   (os.path.join('data','sounds','bg')                  ,glob.glob(os.path.join('data','sounds','bg','*.wav')))
                   
                   
                   #story is not included right now, needs much more work in game, and writing wise...
                   #(os.path.join('data','story')                  ,glob.glob(os.path.join('data','story','*.*')))
              ]
 
# List of all modules to automatically exclude from distribution build
# This gets rid of extra modules that aren't necessary for proper functioning of app
# You should only put things in this list if you know exactly what you DON'T need
# This has the benefit of drastically reducing the size of your dist
 
MODULE_EXCLUDES =[
'email',
'AppKit',
'Foundation',
'bdb',
'difflib',
'tcl',
'Tkinter',
'Tkconstants',
'curses',
'distutils',
'setuptools',
'urllib',
'urllib2',
'urlparse',
'BaseHTTPServer',
'_LWPCookieJar',
'_MozillaCookieJar',
'ftplib',
'gopherlib',
'_ssl',
'htmllib',
'httplib',
'mimetools',
'mimetypes',
'rfc822',
'tty',
'webbrowser',
'socket',
'hashlib',
'base64',
'compiler',
'pydoc']
 
INCLUDE_STUFF = ['encodings',"encodings.latin_1",]
 
setup(console=[
             {'script': SCRIPT_MAIN,
               'other_resources': [(u"VERSIONTAG",1,VERSIONSTRING)],
               'icon_resources': [(1,ICONFILE)]}],
         options = {"py2exe": {
                             "optimize": 2,
                             #"includes": INCLUDE_STUFF,
                             "compressed": 1,
                             #"ascii": 1,
                             "bundle_files": 2,
                             "ignores": ['tcl','AppKit','Numeric','Foundation'],
                             "excludes": MODULE_EXCLUDES
                             }
                   },
          name = PRODUCT_NAME,
          version = VERSION,
          data_files = extra_files,
          zipfile = None,
          author = AUTHOR_NAME,
          author_email = AUTHOR_EMAIL
          ##no website yet. :(
          #url = AUTHOR_URL
     )
 
## Create the /save folder for inclusion with the installer
#shutil.copytree('save','dist/save')
 
if os.path.exists('dist/tcl'): shutil.rmtree('dist/tcl') 
 
# Remove the build tree
if REMOVE_BUILD_ON_EXIT:
     shutil.rmtree('build/')
 
if os.path.exists('dist/tcl84.dll'): os.unlink('dist/tcl84.dll')
if os.path.exists('dist/tk84.dll'): os.unlink('dist/tk84.dll')
 
for f in SDL_DLLS:
    fname = os.path.basename(f)
    try:
        shutil.copyfile(f,os.path.join('dist',fname))
        print 'copied SDL DLL "%s"'%f
    except: pass
    
print 'creating debug/run files'
open(os.path.join('dist','run.bat'),'w').write('''main.exe\r\npause\r\n''')
open(os.path.join('dist','debug.bat'),'w').write('''main.exe -vvvvv \r\npause\r\n''')