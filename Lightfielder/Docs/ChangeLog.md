# Lightfielder | ChangeLog

## 2026-09-09

- When the camera array geometry preference is set to the "A1-E" modes the traditional Camera Contact Sheet "Rect" (rectangular) window is shown that fully works as expected. When the camera array geometry is set to the  "Polar mode the (WIP) Camera Contact Sheet Polar window is shown.
	- The CCS Polar window has had its operational code commented out, early this morning, so displaying the window does not toggle off the active timeline video tracks.
- Updated the "Jupyter Link" script's initial window height to solve a button visibility issue at the bottom row of the windows.

## 2026-09-08

- Started validating Lightfielder compatibility with Resolve Studio v21.1.

## 2026-09-04

- Added a new `Reset Lightfielder Fusion.prefs Entries.py` script to the "Workspace > Scripts > Lightfielder > Developer" menu. It quickly resets the location of the Lightfielder script windows and their settings by zeroing out the Lightfielder entries in the Fusion.prefs file.
- Added more information to the [Extensions](Scripts_16_Extensions.md) documentation topic, and placeholder python scripts for each of the anticipated filetypes.
- Updated the [Jupyter Link](Scripts_17_Jupyter_Link.md) script, and the included Jupyter Notebook example file to support Python v3.6 - 3.15+ by switching to the importlib Python module. This solves an issue where the Resolve API's previously recommended Python "imp" module usage that was depreciated at Python v3.11.
	- The initial Jupyter Link notebook preset is located on disk at: "`Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Presets/Jupyter/Jupyter for Resolve Studio.ipynb`"

## 2026-09-03

- Started packaging up additional learning content and example projects that can be downloaded with permissive Creative Commons license terms
- Updated the "`17 Jupyter Link.py`" script so it pulls the filepaths from the active Python location via the lightfielder.py python module provided function `path = GetPythonBinFilepath("jupyter-notebook")`
	- Example result: `/Library/Frameworks/Python.framework/Versions/3.10/bin/jupyter-notebook`

## 2026-09-02

- Updated the per-OS based Python module dialog in the lightfielder.py script
- Solved an "off by one" error in the "Camera Contact Sheet" script. It impacted the targeting of the final video track.
- Import Footage script
	- Added the code to support the "Add Media To Sources Folder" checkbox feature
	- Added the code to support the "Use Current Folder Hierarchy" checkbox feature
- Working on improvements to Lightfielder on Windows compatibility.
	- Updated the Powershell code that is called by the lightfielder.py script. This reduces the distracting flickering Powershell/Command Prompt window from appearing when CLI tasks are run.
	- Added the "`Lightfielder:\Extras\Shell Scripts\Restart DaVinci Resolve.bat`" script that helps accelerate new feature testing. Resolve can be relaunched to quickly to test changes from a fresh user session.

## 2026-09-01

- The "About Lightfielder" dialog, and the "Toolbar" window now pull their version number info from the Lightfielder python module's "`LFGetVersion(label)` function
- The [Metadata Sync](Scripts_05_Metadata_Sync.md) script has a new "Rig Section as Clip Color" checkbox control
	- The "Rig Section as Clip Color" checkbox allows you to colorize the clips as they appear in the Media Pool and the Editing timeline. The actual parameter is stored on the Media Pool clip. Then when the timeline is created later on the clip color is inherited by the footage at timeline levelm too. 
	- This process works by applying the first letter from the camera rig "A1-EJ" or "A110-Z997" style angle parameter as the index number for cycling through DaVinci Resolve's "clip color" palette. The end result is that each region of the camera array rig sections like "A - Z" get a unique color for their block of cameras.
	- This approach for rig section visualization rapidly speeds up how fast you can eye-ball check for missing views in a timeline as the colors help to "batch together" the groups of views by their specific hue / color swatch.

## 2026-08-31

- Added a "22 About Lightfielder.py" script
- Renamed the Jupyter Notebook script to "17 Jupyter Link.py". This required shifting the toolbar numbering to accomodate the change.
- Added next and previous toolbar item "<" and ">" script navigation buttons to the bottom of the Lightfielder script windows for the Camera Contact Sheet windows and the About Lightfielder window.
	- The Toolbar window uses the "Camera Array Geometry" preference to select if the Camera Contact Sheet Rect vs Polar view should be displayed. Further work needs to be done to complete the Polar view.
- Added Window "FixedSize" attributes to the Toolbar, EDL Stack Swizzle, Video Track Solo, EDL Export, and Camera Contact Sheet scripts. This helps to restore the views to their base size automatically
- Corrected an off-by-one error on the EDL Checker script's "Disabled Tracks" value
- Updated the "lightfielder.py" Python module's "`ExternalEditor()`" function to improve Rocky Linux support. Removed the "xdg-open" dependency for the subprocess task.
- Updated the "lightfielder.py" Python module to add the utility functions "`SoundEffectSelect()`" and "`SoundEffect()`". They implement the code to support the "User interface sound effects" feature in the Preference window.
- Added the code to support the Preference script's "Media Format" menu item. The allows a wider range of file formats, and camera system content to be processed by Lightfielder. This feature was validated with R3D files, videos, and images.
	- "Movie" support includes: Quicktime MOV, MP4, and MKV
	- "Image Sequence" and "Still Frame" image support includes: PNG, JPEG, EXR, DPX, TIFF

## 2026-08-30

- Added a "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Open/" sub-menu. I created and/or moved the following files into this folder:
	- Open BMD Support Center Webpage.py
	- Open Fusion.prefs File.py
	- Open PathMap Settings.py
	- Open ScriptLib File.py
	- Open Toolbar File.py
	- Show DCTL Folder.py
	- Show Extensions Folder.py
	- Show OpenFX Plugins Folder.py
	- Show Temp Folder.py

## 2026-08-29

- The "Fuzzy R3D Date Matching" checkbox works correctly to allow camera array footage with incorrect date data in the R3D filename to be processed without any modifications needed in the "Shotlog.csv" file, or the on-disk R3D clip filenames.
	- With the more flexible date code handlign support, Lightfielder is now able to process 54/55 camera array view based R3D video content, including the correct 60 FPS "Project Frame Rate" and "Sensor Frame Rate" parameters being imported from the Technisync JSON file on the Preferences page with the help of the "Load Settings" button.
- Renamed the "Shotlog Validator" script to "Shotlog Pre-Flight".
- The "CSV Source File" Browse button in the following scripts were updated so the "Shot Type" checkboxes are automatically enabled for the exact shot types present in the CSV file.
	- Import Footage
	- Metadata Sync
	- Still Frames Export
	- Create EDLs
- Added an initial "21 Jupyter Link.py" script to Lightfielder. This script improves support for Jupyter Notebook based Python scripting of the Resolve session for generating COLMAP style lens calibrations and more.
- Added next and previous toolbar item "<" and ">" script navigation buttons to the bottom of the Lightfielder script windows for the EDL Stack Swizzle, Video Track Solo, and EDL Export windows.

## 2026-08-28

- Markdown documentation screenshots updated for script user interfaces
- Toolbar script
	- Improved JSON based Lightfielder Preset system. Updated version tags, and refined the Toolbar Preset JSON syntax. The user-editable Toolbar items revamp is still an ongoing work-in-progress.
- Preferences Script
	- Added a "Script Window Stays On Top" checkbox. When this option is enabled the Lightfielder script user interface windows will always float ontop of all other programs and windows.
	- Added Progress messages to the window. This reduces the usage of modal dialogs by docking the results details into the window itself.
- Bin Templates Script
	- Added Progress messages to the window. This reduces the usage of modal dialogs by docking the results details into the window itself.
- Video Track Solo Script
	- Updated script to automatically track the active editing timeline each time a control is pressed.
	- Added Progress messages to the window. This reduces the usage of modal dialogs by docking the results details into the window itself.
- EDL Stack Swizzle script
	- Updated script to automatically track the active editing timeline each time a control is pressed.
	- Added Progress messages to the window. This reduces the usage of modal dialogs by docking the results details into the window itself.

## 2026-08-27

- Work begins on solving the Resolve v20-21 issues around timecode sync and "Start TC"/"End TC" usage when creating new EDL timelines. This will take several days to finally wrap up as it is a background R&D task.

## 2026-08-26

- Added a new Lightfielder Toolbar preset system that uses JSON to define the content dynamically. It is configured in the [01 Preferences](Scripts_01_Preferences.md) script window. 
	- The custom Toolbar presets are stored in: `Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Presets/Toolbars/`
- Added next and previous toolbar item "<" and ">" script navigation buttons to the bottom of the Lightfielder script windows for the Shotlog Validator, Batch Trim, EDL Checker, Log Viewer, and Extensions windows.
- The Log Viewer script's Log File menu now shows the relative folder path for the log items. This includes the active Resolve project name and the base part of the log filename. This supports a far smaller minimum the Log Viewer window width.

## 2026-08-24

- Updated the Camera Array Geometry "Polar (A110-R977)" menu entry to support "Polar (A110-Z977)" usage. This allows a far wider range of camera positions and views to be accessed in the JSON config file.
	- For the current volcap production needs of today, 55 camera angles can be source directly from a Technisync JSON file. This includes the new "Z" section cameras like "Z349", Z399", "Z419", "Z459", and "Z579".
	- This capability was validated using Lightfielder v26.8 RC5  with DaVinci Resolve Studio v21.0.4 on macOS Tahoe running on a Mac Studio M2 Ultra system. This validation process was done with the sample test footage that was filmed on February 23, 2026 . 
- Updated the [01 Preferences](Scripts_01_Preferences.md) script and the "lightfielder.py" Python module to better handle a wide range of frame rates from R3D media and other video content.
- Updated more ToolTip tags to support the RTFM Tooltips ON/Off preferences
- Updated `print()` command logging details in all scripts to add more event details
- Reformatted Python script code and updated the comments

## 2026-08-23

- Added next and previous toolbar item "<" and ">" script navigation buttons to the bottom of the Lightfielder script windows. These buttons display the previous or next script from the Lightfielder Toolbar. This makes the Lightfielder #01 to #07 scripts feel like they are part of a guided "Wizard" dialog driven process that has linear progression forward at each step.
- Updated the Batch Trim window layout and re-ordered its position in the Toolbar button list, relative to the EDL Swizzle toolbar button.
- [01 Preferences](Scripts_01_Preferences.md) script has "Sensor Frame Rate" and "Project Frame Rate" based "Custom" menu item that supports the manual entry of frame rate values using a SpinBox control.
- Clicking on a script's "Footage Folder", or "Output Folder" text label opens the folder in a desktop folder browsing window.
- When a new CSV document is selected using the "Browse" button next to the "CSV Source File" control, the active items in the tree view are selected automatically.
- Clicking on a script's "JSON Source File", "CSV Source File", or "HTML Log File" text label opens the containing folder in a desktop folder browsing window.
	- If you hold down the Shift modifier key when clicking on the "JSON Source File", or "CSV Source File", or "HTML Log File" text label, the file will be opened using the operating systems default program assigned to handle .json, .csv, or .html files. 
		- For .csv files this might be Apple Numbers (macOS), Excel (Windows/macOS), or Libre Office (Linux).
		- For .json files this might be VS Code (Windows/Linux/macOS), XCode (macOS), BBEdit (macOS), NotePad++(Windows), Gedit (Linux), Xed (Linux), or some other program you prefer.
		- For .html files this might be Chrome (Windows/Linux/macOS), Firefox (Windows/Linux/macOS), Safari (macOS), or Edge (Windows), or some other program you prefer.
	- If you hold down the Command (macOS) or Control (Windows/Linux) modifier key when clicking on the "JSON Source File", "CSV Source File", or "HTML Log File"  text label, the file will be opened using the default programmer's text editor that is defined in the Fusion page settings window's section for the script editor.
- Added a new "Workspaces > Scripts > Lightfielder > Development > Edit Toolbar File.py" menu script. It allows you to edit the "00 Toolbar.py" file using the script editor defined in Fusion's preferences.
- Added a new "Scripts:/Lightfielder.scriptlib" script that runs automatically when DaVinci Resolve starts a new editing session, or a Fusion page composite is created.
	-  The ScriptLib approach provides deeper access to Resolve's internal action/event system hooks that can be used down the road with the new Lightfielder extension system. This allows Lightfielder to auto-configure itself when a new volumetric editing session is lauched.
	- This scriptlib file makes it possible to process the Lightfielder [01 Preferences](Scripts_01_Preferences.md) script's "Autoload Toolbar on Launch" checkbox preference so the Lightfielder [00 Toolbar](Scripts_00_Toolbar.md) window will automatically load when DaVinci Resolve Studio is started and a project file is loaded. If there is an issue with this setting that makes it hard to start Resolve for any reason, the solution is to clear the "`Profiles:/Default/Fusion.prefs`" file which will turn this option off by default.

	- Added a new "Workspaces > Scripts > Lightfielder > Development > Edit ScriptLib File.py" menu script. It allows you to edit the "Scripts:/Lightfielder.scriptlib" file using the script editor defined in Fusion's preferences.

## 2026-08-21

- [01 Preferences](Scripts_01_Preferences.md) Script
	- The "Play user interface sound effects" checkbox allows the Lightfielder scripts to play sound effects when tasks are completed, or errors occur. There is a volume control, and you can specify if a sound effect should be played when python script events like "On Error" or "Task Completed" occur. You have the choice of selecting either "None", "Steam Train Whistle Sound", "Trumpet Sound", or "Braam Sound".

- [02 Bin Templates](Scripts_02_Bin_Templates.md) Script
	- Updated the window type to make it a floating dialog that always stays above other windows
	- Added support for clicking on the "Presets" text label, and the presets folder will be displayed in a desktop file browsing window. This makes it easy to manually adjust the contents of the presets shown. Also added this clickable presets feature to the "09 Camera Contact Sheet", and "11 Grade Automation" scripts.

- [03 Import Footage](Scripts_03_Import_Footage.md) Script
	- Added a "Console" button. This makes it a single click action to check if there were any issues/errors with the processing tasks.
	- Added a "Fuzzy R3D Date Matching" checkbox. It allows the Shotlog CSV date field to be considered a match with the R3D filename date if they are within 1 day +/-. Previously this control only existed on in the "01 Preferences" script.
	- Added a "Add Media To Sources Folder" checkbox. When this option is enabled the imported media is placed in the Media bin "03-footages/source/" folder without a "ID_####" subfolder.

- [04 Metadata Sync](Scripts_04_Metadata_Sync.md) Script
	- Added a "Console" button. This makes it a single click action to check if there were any issues/errors with the processing tasks.
	- Added a "Fuzzy R3D Date Matching" checkbox. It allows the Shotlog CSV date field to be considered a match with the R3D filename date if they are within 1 day +/-. Previously this control only existed on in the "01 Preferences" script.
	- Added a "Use Current Folder Hierarchy" checkbox control. When this option is enabled the metadata syncing process will be limited to the current folder in the media pool and any sub-folders.

- [05 Still Frames Export](Scripts_05_Still_Frames_Export.md) Script
	- Added a "Console" button. This makes it a single click action to check if there were any issues/errors with the processing tasks.

- [06 Create EDLs](Scripts_06_Create_EDLs.md) Script
	- Added a "Console" button. This makes it a single click action to check if there were any issues/errors with the processing tasks.
	- Added a "Create One Timeline" checkbox. This feature combines all the shots, for all shot types, into a single EDL timeline.
	- Added a "Fuzzy R3D Date Matching" checkbox. It allows the Shotlog CSV date field to be considered a match with the R3D filename date if they are within 1 day +/-. Previously this control only existed on in the "01 Preferences" script.

- [07 EDL Stack Swizzle](Scripts_07_EDL_Stack_Swizzle.md) Script
	- Added a "Assign Angle to Track Name" checkbox. It renames the video tracks from "V1 to V55" over to directly using the camera array geometry based camera angle name like "A1 to E5" or "A110 to Z977" as the actual track name. This makes it a heck of a lot easier on the Edit page to know what angle you are looking at when individual video tracks are soloed, or the CCS is used to enable and disable tracks.
	- Added a "Remove Empty Tracks" checkbox. When a Vertical Stack is created, this option will compact the video tracks in the timeline by removing any track that is missing its camera views. If you had an array with 55 cameras, and 10 of the cameras were not set to record, you would receive a swizzled timeline created with only 45 video tracks and no empty video tracks.

- Added a new "Workspaces > Scripts > Lightfielder > Development > Edit Fusion.prefs File.py" menu script. It allows you to modify the raw preferences for the Fusion PathMap values and the Lightfielder settings using an external text editor. This makes it possible to clear out the prior settings if one needs to track down issues related to multi-monitor window layouts or other gremlins.
- Updated the Technisync JSON debugging scripts. Renamed them to "Read Technisync Config JSON.py" and "Read Technisync Shotlog JSON.py" The JSON debugging scripts are found in the "Workspaces > Scripts > Lightfielder > Development >" menu system. They list information about the camera array and view labelling.
- Updated the UI Manager window creation code in the Python scripts to add a QT window creation "TargetID" attribute. This helps support the closing of the floating windows with the "Control + W", "Control + F4", and "Escape" keyboard hotkeys. This works in Resolve pages like the Fusion page that allow user defined hotkeys entries to be created for a window in Python... BMD's scripting API is not consistent across all pages.

## 2026-08-20 Afternoon

- Updated the "[01 Preferences](Scripts_01_Preferences.md)" script
	- Renamed the "Camera Array Views" control to "Number of Cameras"
	- The "Media Frame Rate" control is now named "Sensor Frame Rate"
	- The "Project Frame Rate" control is able to pull its value from the Technisync JSON file. This setting should match the Resolve Project and Timeline frame rate for most use cases.
	- The "RTFM Tooltips" checkbox provides more detailed help information that will save you a visit to the documentation for tool usage information. When the "RTFM Tooltips" checkbox is unchecked you will see very short tooltip messages that are concise.
	- The "Fuzzy R3D Date Matching" checkbox allows the Shotlog CSV date field to be considered a match with the R3D filename date if they are within 1 day +/-.

## 2026-08-20 Morning

- Improved Windows 11 support for the Lightfielder Python Module including the "ExternalEditor()" function and the way the Resolve object is accessed using `app.GetResolve()`
	-  The `ExternalEditor()` function that validated if a programmer's text editor was defined in the Fusion page settings before opening a python script needed to be revised again on macOS, after going through a round of Rocky Linux and Windows testing. The code was changed from using the Python `os.isfile()` function over to `os.exists()` since macOS `.app` files (macOS Application Packages) like a text editor program would have, are seen by Python as a folder, not a single file. This meant macOS text editor apps were being falsely detected as not existing on disk, which triggered error handling code to be printed to the Cnnsole window.
- "[02 Bin Template](Scripts_02_Bin_Templates.md)" script update. When the bin folders are created, the script completes the task by switching the Media pool focus back to the root level "Master" bin folder. Previously when the script finished the active folder in the Media pool was set to the last folder created by the saved preset which felt quite random, haphazard, and inconsistent.
- [Toolbar](Toolbar.md) Updates
	- The button items (16, 18, and 19) that open external resources like webpage URLs, script editors, or folder browsing windows are now set to act as momentary buttons that do not hold a persistent pressed state. This means you don't have to click them again to un-set the pressed state at a later time.
	- When the "Workspaces > Scripts > Lightfielder >" menu is used to open a script, the toolbar button pressed state is updated so it tracks the window visibility of the externally launched scripts.
	- When a Lightfielder script window is closed using either the window's "X" close box or the "Close" button the corresponding Toolbar button is unpressed/released as well. This keeps the Toolbar buttons updated so they stay in sync with the individual script window visibility states.
	- When the Toolbar window "X" close box is clicked, if the shift modifier key is held down at the same moment, the extra floating palette windows are force-closed at the same time, too. This makes it a quick task to de-clutter your workspace if you need to focus on something else.
- Import Footage and Metadata Sync Script Updates
	- Clicking on the "Camera Array Geometry" text label will open the "[01 Preferences](Scripts_01_Preferences.md)" window. This allows you to quickly adjust the camera rig settings.

## 2026-08-19

- Started adding tooltip captions to the script's user interface controls
- The [Toolbar](Toolbar.md) has been updated. Holding down the Command (macOS) or Control (Win/Linux) key when clicking on a toolbar item will edit that Python script. Resolve Studio will then open the toolbar button's .py script file up in an external programmer's text editor of your choice.
- Updated the "[01 Preferences](Scripts_01_Preferences.md)" script
	- A new "Use Local Help" checkbox allows you to switch between displaying local on-disk help docs, and  the GitHub repo hosted help docs 
	- The "Camera Array Views" SpinBox control has the maximum value limit raised to 2028 views. If you really need more than 2048 video tracks, this value can be raised higher using a tip on the Preferences documentation page.
- Updated the "`Scripts:/Utility/Lightfielder/Development/Timeline.py`" file to make the window consistently float above other views. Added Lightfielder python module support, and improved the preference handling for the camera array views value.
- Updated the python scripts titlebar code

## 2026-08-17

- Added "Wallclock" progress message details to the various scripts that take longer than ~10 seconds to run. This reports the hours, minutes, and seconds level of detail for the long running tasks using text at the bottom of the script window
- Updated the [Edit Python Module](Scripts_19_Edit_Python_Module.md) documentation topic to include example edit script file paths for macOS, Linux, and Windows

## 2026-08-16

- Lightfielder "[01 Preferences](Scripts_01_Preferences.md)" script code updated
	- The "Load Settings" button will refresh the "Camera Array Views" and "Media Frame Rate" values using the entries in the technisync JSON file.
	- The "Camera Array Views" SpinBox control allows you to define how many cameras are present in the volumetric capture camera rig. This is typically a value from 50 to 55 that is related to the current "Camera Array Geometry" setting. You can raise this value far higher than that if your technisync JSON has camera entries for the extra views.
	- The "Media Format" ComboBox menu includes entries for R3D, Movie, Image Sequence, and Still Frame. At this moment the R3D mode is what we are using.
	- The "Drop Frame Timecode (DF) checkbox specifies if the frame rate is formatted as "24" vs "23.97" FPS.
	- The "Media Frame Rate" control defines the frame rate present in the captured footage. This is typically a value like 30 FPS or 60 FPS.
- [Toolbar](Toolbar.md) layout update
- [Metadata Tags](Metadata_Tags.md) documentation topic update. Included a revised image that shows the current tag ordering used in Resolve v21
- [Unit Tests](Unit_Tests.md) examples update for "R3D Template for 55 Camera Array A110-Z579" example. Created a "slim" technisync JSON to allow easier validation testing while the code is being updated for this new camera rig spec.

## 2026-08-14

- Updated the heading title text on the scripts to add "?" (help topic) button to the far right of this row of text. The help button makes it easy to access to the GitHub markdown formatted docs for each scripted tool.

## 2026-08-12

- Adding support for a new "[Extensions](Scripts_17_Extensions.md)" toolbar item. Extensions (WIP) allow 3rd party Python based plugins to extend the Lightfielder ecosystem.

## 2026-08-05

- Validated the scripts work in DaVinci Resolve Studio v21.0.4
- Updated the Known Issues document
- Updated the Punchlist document
- Expanded the Toolbar window to be twice as high so it supports a two-row layout of toolbar buttons. This adds slots for a future lineup of 16 more tools in the Toolbar. New script buttons include:
	- [Open Lightfielder Folder](Scripts_18_Open_Lightfielder_Folder.md)
	- [Edit Python Module](Scripts_19_Edit_Python_Module.md)
	- [Shotlog Validator](Scripts_20_Shotlog_Validator.md)
- Lightfielder "01 Preferences" script code updated
	- The "Camera Array Geometry" control in the Lightfielder scripts will automatically show the "JSON Source File" attribute when Polar camera arrays are used. This reduces confusion when Grid and Wedge arrays are selected in the Preferences, Import Footage, and Metadata Sync scripts.
- Added a new "Bin_VFX" preset to the "02 Bin Templates" script. It is as short as possible and only adds the minimum folders needed to start being productive with Lightfielder in a visual effects capacity.

## 2026-08-01

- Lightfielder for Resolve v26.08 Update. Tested DaVinci Resolve Studio v21.0.3 compatibility.
- Added a workflow guide [PBR-GS Physically Based Rendering of Gaussian Splats](Workflow_Guides/Physically_Based_Rendering_of_Gaussian_Splats.md) that discusses temporal stability and PBR relighting data storage concepts in 4DGS/3DGS based gaussian splat .ply files.
- Added a "[Known Issues](Known_Issues.md)" documentation topic. This is separate from the official PunchList content which is task aligned for planning new features and changes.
- Updated the [Unit Tests](Unit_Tests.md) to include a synthetic 55 camera rig "A110-Z579" layout RED file naming example

## 2026-06-29

- Validated the scripts work in DaVinci Resolve Studio v21.0.1
- Added a [Volumetric Color Decision Lists](Workflow_Guides/Volumetric_Color_Decision_Lists.md) guide

## 2026-06-03

- Validated the scripts work in the DaVinci Resolve Studio v21 golden master release

## 2026-05-28

- Validated the scripts work in DaVinci Resolve Studio v21 Public Beta 4

## 2026-05-19

- Added a [Lightfielder HDR Image Based Rendering](Workflow_Guides/Lightfielder_HDR_Image_Based_Rendering.md) workflow guide

## 2026-05-15

- Validated the scripts work in DaVinci Resolve Studio v21 Public Beta 3
- Metadata documentation topic updated with additional screenshots

## 2026-05-02

- Docs update. Revised README.md table of contents layout.

## 2026-05-01

- Updated toolbar version number label to match current month
- Validated the scripts work in DaVinci Resolve Studio v21 Public Beta 2

## 2026-04-27

- In-house toolset renamed to "Lightfielder for DaVinci Resolve".
