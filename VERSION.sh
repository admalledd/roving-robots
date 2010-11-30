#!/bin/bash

git rev-list HEAD | sort > config.git-hash
MAJOR="0"
MINOR="0"
RELEASE="1"
LOCALVER=`wc -l config.git-hash | awk '{print $1}'`

if [ $LOCALVER \> 1 ] ; then
    VER=`git rev-list master | sort | join config.git-hash - | wc -l | awk '{print $1}'`
    if [ $VER != $LOCALVER ] ; then
        VER="$VER+$(($LOCALVER-$VER))"
    fi
    if git status | grep -q "modified:" ; then
        VER="${VER}M"
    fi
    VER="$VER $(git rev-list HEAD -n 1 | cut -c 1-7)"
    echo "__build__= \" r$VER\""
    echo "__build__= \" r$VER\"">version.py
else
    echo "__build__= \"\""
    echo "__build__= \"\"">version.py
    VER="x"
fi
rm -f config.git-hash

#verstion numbering: major.minor.release.build
echo "__version__ = \"$MAJOR.$MINOR.$RELEASE.$VER\""
echo "__version__ = \"$MAJOR.$MINOR.$RELEASE.$VER\"">>version.py