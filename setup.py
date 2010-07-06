from distutils.core import setup
import py2exe 
#from glob import glob
import lib.common

lib.common.set_directory()
#data_files=[(glob(lib.common.curdir+'\\data\\*.*'))]
setup(
        #data_files=data_files,
        console=['main.py'],
        options={
                "py2exe":{
                        'bundle_files': 2,
                        "optimize": 0,
                        'excludes':['tcl','email','Tkinter','ssl','xml','numpy','_ssl']
                }
        }
)