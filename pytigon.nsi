Unicode true

!include "MUI2.nsh"

Name "Pytigon"
OutFile ".\install\pytigon.exe"
InstallDir "$LOCALAPPDATA\pytigon"
InstallDirRegKey HKCU "Software\pytigon" ""
RequestExecutionLevel user

InstType "$(full)" 
InstType "$(only_server)" 
InstType "$(no_python_runtime)"

!define MUI_ABORTWARNING
!define MUI_LANGDLL_ALLLANGUAGES

;--------------------------------
;Pages
  !insertmacro MUI_PAGE_LICENSE "LICENSE"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
;--------------------------------
;Languages
  !insertmacro MUI_LANGUAGE "English"
  !insertmacro MUI_LANGUAGE "Polish"

;--------------------------------
;Installer Sections

Section "pytigon - server"

  SectionIn 1 2 3
  
  SetOutPath $INSTDIR\ext_lib
  File /r  /x __pycache__ /x *.pyc /x *.pyo ext_lib\*.*
  SetOutPath $INSTDIR\ext_prg
  File /r  /x __pycache__ /x *.pyc /x *.pyo ext_prg\*.*
  SetOutPath $INSTDIR\schlib
  File /r  /x __pycache__ /x *.pyc /x *.pyo schlib\*.*
  SetOutPath $INSTDIR\schserw
  File /r  /x __pycache__ /x *.pyc /x *.pyo schserw\*.*
  SetOutPath $INSTDIR\static
  File /r static\*.*
  SetOutPath $INSTDIR\static_src
  File /r static_src\*.*
  SetOutPath $INSTDIR\templates
  File /r templates\*.html
  SetOutPath $INSTDIR\templates_src
  File /r templates_src\*.ihtml
  SetOutPath $INSTDIR
  File LICENSE
  
  ;Store installation folder
  WriteRegStr HKCU "Software\pytigon" "" $INSTDIR

  ReadRegStr $R0 HKCU "Software\Classes\.ptig" ""
  StrCmp $R0 "Software\Classes\Pytigon" 0 +2
    DeleteRegKey HKCU "Software\Classes\Pytigon"

  WriteRegStr HKCU "Software\Classes\.ptig" "" "Pytigon.0"
  WriteRegStr HKCU "Software\Classes\Pytigon.0" "" "Pytigon file"
  WriteRegStr HKCU "Software\Classes\Pytigon.0\DefaultIcon" "" "$INSTDIR\pytigon.exe,0"
  ReadRegStr $R0 HKCU "Software\Classes\Pytigon.0\shell\open\command" ""
  ${If} $R0 == ""
    WriteRegStr HKCU "Software\Classes\Pytigon.0\shell" "" "open"
    WriteRegStr HKCU "Software\Classes\Pytigon.0\shell\open\command" "" '$INSTDIR\pytigon.exe "%1"'
  ${EndIf}


  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd


Section "pytigon - client"

  SectionIn 1 3
  SetOutPath $INSTDIR\schcli
  File /r  /x __pycache__ /x *.pyc /x *.pyo schcli\*.*
  SetOutPath $INSTDIR\schappdata
  File /r  /x __pycache__ /x *.pyc /x *.pyo schappdata\*.*
  ;SetOutPath $INSTDIR\app_pack\_schmsg
  ;File /r  /x __pycache__ /x *.pyc /x *.pyo app_pack\_schmsg\*.*
  SetOutPath $INSTDIR\app_pack\_schtasks
  File /r  /x __pycache__ /x *.pyc /x *.pyo app_pack\_schtasks\*.*
  SetOutPath $INSTDIR\app_pack\_schtools
  File /r  /x __pycache__ /x *.pyc /x *.pyo app_pack\_schtools\*.*
  SetOutPath $INSTDIR\app_pack\_schwiki
  File /r  /x __pycache__ /x *.pyc /x *.pyo app_pack\_schwiki\*.*
  SetOutPath $INSTDIR\app_pack\schdevtools
  File /r  /x __pycache__ /x *.pyc /x *.pyo app_pack\schdevtools\*.*
  SetOutPath $PROFILE\.pytigon
  File /r install\.pytigon\*.*

  SetOutPath $INSTDIR
  File pytigon.py
  File pytigon.ini
  File pytigon_task.py
  File wsgi.py
  File asgi.py
  File pytigon.exe
  File pytigon_cmd.exe
  File pytigon_splash.jpeg
  File pytigon.png
  File pytigon.ico
  File manage.py

  WriteRegStr HKCU "Software\pytigon" "" $INSTDIR
  WriteRegDWORD HKCU "SOFTWARE\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BROWSER_EMULATION" "python.exe" 0x2AF9

SectionEnd


Section "python runtime"
  SectionIn 1
  SetOutPath $INSTDIR\python
  File /r /x *.pyo /x __pycache__  python\*.*
SectionEnd



Section "vcredist"
  SectionIn 1
  SetOutPath "$TEMP"
  File ".\install\vcredist_x86.exe"
  ExecWait '"$TEMP\vcredist_x86.exe" /passive /norestart'
  Delete "$TEMP\vcredist_x86.exe"
SectionEnd


;--------------------------------
;Uninstaller Section

Section "Uninstall"
  Delete "$INSTDIR\Uninstall.exe"

  RMDir /r /REBOOTOK $INSTDIR
  
  DeleteRegKey /ifempty HKCU "Software\pytigon"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString full ${LANG_ENGLISH} "Full"
  LangString full ${LANG_POLISH} "Wszystko"
  LangString no_python_runtime ${LANG_ENGLISH} "No python runtime"
  LangString no_python_runtime ${LANG_POLISH} "Bez oprogramowanie python"
  LangString only_server ${LANG_ENGLISH} "Only server"
  LangString only_server ${LANG_POLISH} "Tylko serwer"
