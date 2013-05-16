#!/bin/sh
# Written by: DGC

# expand aliases
shopt -s expand_aliases
if [ -f ~/my_profile.ksh ]
then
  . ~/my_profile.ksh
fi

pyinstaller -F -w MarkdownEditor.py

# now make the installer, first test if devenv is a command
if hash devenv 2>/dev/null
then
  cd Installer
  devenv Installer.sln /Project Installer.vdproj /Rebuild Release
  else
  echo "no devenv"
fi