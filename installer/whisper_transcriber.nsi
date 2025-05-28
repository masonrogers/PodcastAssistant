; Placeholder NSIS script for Whisper Transcriber
; Customize settings, icons, and signing as needed

!include "MUI2.nsh"

Name "Whisper Transcriber"
OutFile "WhisperTranscriberSetup.exe"
InstallDir "$PROGRAMFILES\WhisperTranscriber"

Section "MainSection" SEC01
    ; TODO: add files
SectionEnd

Section -Post
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd
