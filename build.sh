#!/bin/sh
# Written by: DGC

set -e

mkdir -p Binaries
mkdir -p Binaries/EXE

# expand aliases
shopt -s expand_aliases
if [ -f ~/my_profile.ksh ]
then
  . ~/my_profile.ksh
fi

pyinstaller -F -w --icon=Resources/Images/icon.ico MarkdownEditor.py

echo ""

if [ -f dist/MarkdownEditor.exe ]
then
  mv -vf dist/MarkdownEditor.exe Binaries/EXE/
fi

# remove the temporary build files
rm -rf build/
rm -rf dist/
rm -f logdict*

echo ""

# now make the installer, first test if devenv is a command
if hash devenv 2>/dev/null
then
  (
    \cd Installer &&
    echo "Making windows installer" &&
    devenv Installer.sln /Project Installer.vdproj /Rebuild Release
  )
else
  echo "Devenv is not a command, skipping windows installer."
fi

echo ""
echo "Zipping windows installer"

(
  \cd Binaries &&
  zip -r MarkdownEditorWindows.zip MarkdownEditorWindows &&
  rm -rf MarkdownEditorWindows
)

echo ""
echo "Done"
