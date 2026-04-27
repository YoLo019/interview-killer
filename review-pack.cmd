@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "POWERSHELL_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"

if not exist "%POWERSHELL_EXE%" (
  echo PowerShell not found: "%POWERSHELL_EXE%"
  exit /b 1
)

"%POWERSHELL_EXE%" -ExecutionPolicy Bypass -File "%SCRIPT_DIR%review-pack.ps1" %*
exit /b %ERRORLEVEL%
