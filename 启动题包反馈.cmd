@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "POWERSHELL_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
set "SERVER_SCRIPT=%SCRIPT_DIR%scripts\review_server.py"

if not exist "%POWERSHELL_EXE%" (
  echo PowerShell not found: "%POWERSHELL_EXE%"
  exit /b 1
)

if not exist "%SERVER_SCRIPT%" (
  echo review_server.py not found: "%SERVER_SCRIPT%"
  exit /b 1
)

if not exist "%SCRIPT_DIR%.interview" mkdir "%SCRIPT_DIR%.interview"
if not exist "%SCRIPT_DIR%interview-packs" mkdir "%SCRIPT_DIR%interview-packs"

"%POWERSHELL_EXE%" -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='SilentlyContinue';" ^
  "$port=8765;" ^
  "$scriptPath='%SERVER_SCRIPT%';" ^
  "$listener=Get-NetTCPConnection -LocalPort $port -State Listen;" ^
  "if($listener){$listener | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force }};" ^
  "Start-Process python -ArgumentList @($scriptPath,'--port',$port,'--no-browser') -WindowStyle Hidden;" ^
  "Start-Sleep -Seconds 2;" ^
  "Start-Process 'http://127.0.0.1:8765/review-pack.html';"

exit /b %ERRORLEVEL%
