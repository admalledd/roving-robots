#!/bin/sh

if [ -d "/cygdrive/f/prog/python" ]; then
    #cygwin
    #my flash drive
    export pywin="/cygdrive/f/prog/python/"
    $pywin/python.exe setup.py
#C:\prog\PortablePython_1.1_py2.6.1\App
elif [ -d "/cygdrive/c/prog/PortablePython_1.1_py2.6.1/App" ]; then
    #VM machine's python...
    echo "vm interior build"
    export pywin="/cygdrive/c/prog/PortablePython_1.1_py2.6.1/App"
    $pywin/python.exe setup.py
elif [ -d "/c/python" ]; then
    #mingw32 (laptop)
    export pywin="/c/python/"
    $pywin/python.exe setup.py
elif [ -d "/cygdrive/c/prog/python" ]; then
    #my laptops' cygwin
    export pywin="/cygdrive/c/prog/python/"
    $pywin/python.exe setup.py
elif [ -d "/home/admalledd/.PlayOnLinux/" ];then
    #actually running on linux, try to connect to virtual box cygwin sshd, and run build there...
    #some one needs to update this section to handle other computers besides MY build computers
    echo "building via virtual box"
    ssh Owner@192.168.56.101 'cd /home/Owner/roving-robots && /home/Owner/roving-robots/build.sh'
    exit 0;
fi

