#!/bin/sh
echo "removing previous builds..."
./clean.sh
echo "cleaning done, BUILD!"
python setup.py py2exe

echo "build done, creating test code..."
echo main.exe >> dist/test.bat
echo pause >> dist/test.bat

@pause