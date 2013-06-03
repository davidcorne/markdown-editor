; Markdown_Editor.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install Markdown_Editor.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "Markdown Editor"

; The file to write
OutFile "Binaries\setup.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\Markdown Editor"

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\Markdown_Editor" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "Markdown_Editor (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File "Binaries\EXE\MarkdownEditor.exe"
  File "Markdown Editor on the web.url"
  File /r /x *_Options.pickle "Resources"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\NSIS_Markdown_Editor "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Markdown_Editor" "DisplayName" "Markdown_Editor"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Markdown_Editor" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Markdown_Editor" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Markdown_Editor" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\Markdown Editor"
  CreateShortCut "$SMPROGRAMS\Markdown Editor\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\Markdown Editor\Markdown Editor.lnk" "$INSTDIR\MarkdownEditor.exe" "" "$INSTDIR\MarkdownEditor.exe" 0
  CreateShortCut "$SMPROGRAMS\Markdown Editor\Markdown Editor on the web.lnk" "$INSTDIR\Markdown Editor on the web.url" "" "$INSTDIR\Markdown Editor on the web.url" 0
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Desktop Shortcut"

  CreateShortCut "$DESKTOP\Markdown Editor.lnk" "$INSTDIR\MarkdownEditor.exe" "" "$INSTDIR\MarkdownEditor.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Markdown_Editor"
  DeleteRegKey HKLM SOFTWARE\NSIS_Markdown_Editor

  ; Remove files and uninstaller
  Delete $INSTDIR\MarkdownEditor.exe
  Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\Markdown Editor\*.*"
  Delete "$DESKTOP\Markdown Editor.lnk"

  ; Remove directories used
  RMDir "$SMPROGRAMS\Markdown Editor"
  RMDir "$INSTDIR"

SectionEnd
