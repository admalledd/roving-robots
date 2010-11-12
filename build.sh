#!/bin/sh
echo "removing previous builds..."
./clean.sh
rm -r dist/
echo "cleaning done, BUILD!"

if [ -d "/cygdrive/c/prog/python" ]; then
    #cygwin (VM box cygwin windows xp sp2)
    #or my laptops' cygwin
    export pywin="/cygdrive/c/prog/python/"
    $pywin/python.exe setup.py py2exe
elif [ -d "/cygdrive/f/prog/python" ]; then
    #cygwin (VM box cygwin windows xp sp2)
    export pywin="/cygdrive/f/prog/python/"
    $pywin/python.exe setup.py py2exe
elif [ -d "/c/python" ]; then
    #mingw32 (laptop)
    export pywin="/c/python/"
    $pywin/python.exe setup.py py2exe
elif [ -d "/home/admalledd/.PlayOnLinux/" ];then
    #actually running on linux, try to connect to virtual box cygwin sshd, and run build there...
    #some one needs to update this section to handle other computers besides MY build computers
    echo "building via virtual box"
    ssh Owner@192.168.56.101 'cd /home/Owner/roving-robots && /home/Owner/roving-robots/build.sh'
    exit 0;
fi


echo "build done, copying required dll's"
cp $pywin/Lib/site-packages/pygame/*.dll ./dist/
echo "copy done, creating test code..."
echo "main.exe" > dist/run.bat
echo "pause" >> dist/run.bat

echo "main.exe -vvvv" > dist/debug.bat
echo "pause" >> dist/debug.bat

echo "done, done done... now cleaning extras..."
./clean.sh