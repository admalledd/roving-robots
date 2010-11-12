from distutils.core import setup
import py2exe 
#from glob import glob
import lib.common

#data_files=[(glob(lib.common.curdir+'\\data\\*.*'))]
setup(
        #data_files=data_files,
        console=['main.py'],
        options={
                "py2exe":{
                        'bundle_files': 3,
                        "optimize": 0,
                        'excludes':["Tkconstants","Tkinter","tcl",'email','ssl','xml','numpy','_ssl'],
                        'dll_excludes':['w9xpopen.exe'],
                        'compressed':True
                }
        }
)
