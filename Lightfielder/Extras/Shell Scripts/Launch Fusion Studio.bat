@ECHO OFF
REM Run the script as a minimized window
if /i not "%~1"=="__minimized" (
    start "" /min "%~f0" __minimized
    exit /b
)

@title Launch Fusion Studio in a DIY Virtual Environment
setlocal EnableDelayedExpansion

REM Override all of the OFX folders that Fusion will look inside of, when Fusion Render Node and Fusion Studio start up
REM This will hide any OFX plugins installed in the program files "common files" folder to avoid the evil OFX plugins from crashing this Fusion session.
REM You have the option to change these values per Fusion host version if needed
@set "FUSION_OFX_PLUGIN_PATH=C:\Reactor\DeployOpenFX"
@set "OFX_PLUGIN_PATH=C:\Reactor\DeployOpenFX"

REM Define where Fusion preferences should be stored. You have the option to change these values per Fusion host version if needed
@set "FUSION16_PROFILE_DIR=C:\Reactor\Fusion\Profiles\Default\"
@set "FUSION17_PROFILE_DIR=C:\Reactor\Fusion\Profiles\Default\"
@set "FUSION19_PROFILE_DIR=C:\Reactor\Fusion\Profiles\Default\"
@set "FUSION20_PROFILE_DIR=C:\Reactor\Fusion\Profiles\Default\"
@set "FUSION21_PROFILE_DIR=C:\Reactor\Fusion\Profiles\Default\"

REM Turning on the log enabler item by default.
@set "FUSION_Log=true"

REM Define where Fusion stores its log files at launch
@set "FUSION_Log_DIR=C:\Reactor\Fusion\Logs"

REM ---------------------------------
REM Display the environment variables

echo Active Environment Variables
echo FUSION PROFILE DIR
echo %FUSION20_PROFILE_DIR%
echo.
echo FUSION_OFX_PLUGIN_PATH
echo %FUSION_OFX_PLUGIN_PATH%
echo.
echo OFX_PLUGIN_PATH
echo %OFX_PLUGIN_PATH%
echo.
echo FUSION_Log File Status
echo %FUSION_Log%
echo.
echo FUSION_Log_DIR
echo %FUSION_Log_DIR%
echo.
echo FUSION Log Files
echo %FUSION_Log_DIR%\FusionStudio_Log.txt
echo %FUSION_Log_DIR%\FusionRenderNode_Log.txt
echo.

REM ---------------------------------
REM Create the intermediate folders

if defined OFX_PLUGIN_PATH (
    if not exist "%OFX_PLUGIN_PATH%\." mkdir "%OFX_PLUGIN_PATH%"
)

if defined FUSION_Log_DIR (
    if not exist "%FUSION_Log_DIR%\." mkdir "%FUSION_Log_DIR%"
)

REM ---------------------------------
REM Launch the required programs

REM echo Startup my Render Node just on this computer
start "" "C:\Program Files\Blackmagic Design\Fusion Render Node 21\FusionRenderNode.exe" -verbose -quiet -log "%FUSION_Log_DIR%\FusionRenderNode_Log.txt" -cleanlog

REM Sleep for a few seconds for the Fusion render Node can finish loading and collapse to the windows tray
echo Delaying next task for 2 seconds
timeout /T 2

REM Fusion Studio
echo Start Fusion Studio GUI
"C:\Program Files\Blackmagic Design\Fusion 21\Fusion.exe" -verbose -quiet -log "%FUSION_Log_DIR%\FusionStudio_Log.txt" -cleanlog
echo.

REM Quit Fusion Render Node on demand
echo The Fusion Studio GUI session was quit
echo.

tasklist /fi "imagename eq FusionRenderNode.exe" 2>NUL | find /i "FusionRenderNode.exe" >NUL
if "%errorlevel%"=="0" (
    echo Stopping Fusion Render Node...
    taskkill /f /im "FusionRenderNode.exe"
    echo.

    echo Waiting 5 seconds for Fusion Render Node shutdown completion
    echo.
    timeout /t 5 /nobreak > nul
) else (
    echo Fusion Render Node is not currently running
    echo.
)

REM Print the log files to the display
echo Displaying Log files
powershell -NoProfile -Command "& { Get-Content -LiteralPath '%FUSION_Log_DIR%\FusionRenderNode_Log.txt' }"
echo.
powershell -NoProfile -Command "& { Get-Content -LiteralPath '%FUSION_Log_DIR%\FusionStudio_Log.txt' }"
echo.

REM Wait until Fusion quits before closing this command prompt window
REM Ask the user to press a key before this view will disappear
echo Fusion Exit Procedure Completed
pause

