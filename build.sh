#!/bin/sh
echo "removing previous builds..."
./clean.sh
rm -r dist/
echo "cleaning done, BUILD!"
python setup.py py2exe

echo "build done, copying required dll's"
cp /c/python/Lib/site-packages/pygame/SDL_ttf.dll ./dist/
cp /c/python/Lib/site-packages/pygame/libogg-0.dll ./dist/
echo "copy done, creating test code..."
echo "main.exe" > dist/run.bat
echo "pause" >> dist/run.bat

echo "main.exe -vvvv" > dist/debug.bat
echo "pause" >> dist/debug.bat

echo "done, done done... now cleaning extras..."
./clean.sh