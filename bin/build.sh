#!/bin/sh
# Written by: DGC

# should be run from project directory i.e markdown-editor

set -e

if [ ! -d markdown-editor-downloads ]
then
  echo "No markdown-editor-downloads directory, can get it using

hg clone https://davidcorne@bitbucket.org/davidcorne/markdown-editor-downloads
"
  exit
fi

# expand aliases
shopt -s expand_aliases
if [ -f ~/my_profile.ksh ]
then
  . ~/my_profile.ksh
fi

pyinstaller -w --icon=Resources/Images/icon.ico Main.py
rm -f Main.spec

echo ""

if [ -f dist/Main/Main.exe ]
then
  mkdir -p markdown-editor-downloads/EXE/
  cp -rv dist/Main/* markdown-editor-downloads/EXE/
  mv -fv markdown-editor-downloads/EXE/Main.exe markdown-editor-downloads/EXE/mde.exe
  cp tpl/* markdown-editor-downloads/EXE/
  cp -r Resources markdown-editor-downloads/EXE/
else
  echo "No executable made"
  exit
fi

# remove the temporary build files
rm -rf build/
rm -rf dist/
rm -f logdict*

echo ""

echo "[InternetShortcut]
URL=https://bitbucket.org/davidcorne/markdown-editor
" > "Markdown Editor on the web.url"

echo "Making windows installer" 
makensis bin/installer.nsi
rm -f "Markdown Editor on the web.url"

echo ""
echo "Done"
