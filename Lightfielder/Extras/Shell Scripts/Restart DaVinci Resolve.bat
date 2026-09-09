@echo off
title Restart DaVinci Resolve

tasklist /fi "imagename eq Resolve.exe" 2>NUL | find /i "Resolve.exe" >NUL
if "%errorlevel%"=="0" (
    echo Stopping DaVinci Resolve...
    taskkill /f /im "Resolve.exe"

    echo Waiting 5 seconds...
    timeout /t 5 /nobreak > nul
) else (
    echo DaVinci Resolve is not currently running
)

echo Launching DaVinci Resolve...
start "" "%ProgramFiles%\Blackmagic Design\DaVinci Resolve\Resolve.exe"

exit
