#!/bin/sh
# Written by: DGC

# should be run from project directory i.e markdown-editor

set -e

mkdir -p Downloads
mkdir -p Downloads/EXE

# expand aliases
shopt -s expand_aliases
if [ -f ~/my_profile.ksh ]
then
  . ~/my_profile.ksh
fi

pyinstaller -F -w --icon=Resources/Images/icon.ico MarkdownEditor.py
rm -f MarkdownEditor.spec

echo ""

if [ -f dist/MarkdownEditor.exe ]
then
  mv -vf dist/MarkdownEditor.exe Downloads/EXE/
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
makensis installer.nsi
rm -f "Markdown Editor on the web.url"

echo ""
echo "Done"
