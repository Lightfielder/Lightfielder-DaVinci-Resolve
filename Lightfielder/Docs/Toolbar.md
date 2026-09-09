# Lightfielder | Toolbar Scripts

## Overview

Lightfielder ships with a custom toolbar. The scripts are numbered in linear order to help make it quick to access individual tools.

![Toolbar](images/toolbar.png)

The Davinci Resolve Studio based Lightfielder workflow automation scripts are accessed using the "Workspace \> Scripts \> Lightfielder \> Toolbar" menu item.

![Workspace Menu](images/menu_workspace_lightfielder_toolbar.png)

The scripts present in this menu area include:

- [00 Toolbar](Scripts_00_Toolbar.md)
- [01 Preferences](Scripts_01_Preferences.md)
- [02 Bin Templates](Scripts_02_Bin_Templates.md)
- [03 Shotlog Pre-Flight](Scripts_03_Shotlog_PreFlight.md)
- [04 Import Footage](Scripts_04_Import_Footage.md)
- [05 Metadata Sync](Scripts_05_Metadata_Sync.md)
- [06 Still Frames Export](Scripts_06_Still_Frames_Export.md)
- [07 Create EDLs](Scripts_07_Create_EDLs.md)
- [08 Batch Trim](Scripts_08_Batch_Trim.md)
- [09 EDL Stack Swizzle](Scripts_11_EDL_Stack_Swizzle.md)
- [10 EDL Checker](Scripts_09_EDL_Checker.md)
- [11 Log Viewer](Scripts_10_Log_Viewer.md)
- [12 Video Track Solo](Scripts_12_Video_Track_Solo.md)
- [13 Camera Contact Sheet](Scripts_13_Camera_Contact_Sheet.md)
- [14 Grade Automation](Scripts_14_Grade_Automation.md)
- [15 EDL Export](Scripts_15_EDL_Export.md)
- [16 Extensions](Scripts_16_Extensions.md)
- [17 Edit Jupyter Link](Scripts_17_Jupyter_Link.md)
- [18 Open Lightfielder Folder](Scripts_18_Open_Lightfielder_Folder.md)
- [19 Show Console](Scripts_19_Show_Console.md)
- [20 Documentation](Scripts_20_Documentation.md)
- [21 Edit Python Module](Scripts_21_Edit_Python_Module.md)
- [22 About Lightfielder](Scripts_22_About_Lightfielder.md)

**Tip:** Hold down the shift key when clicking on a toolbar item to force-reload the script. This is handy if you have edited the script and want to refresh the view to show the changes.

**Tip:** Hold down the Command (macOS) or Control (Win/Linux) key when clicking on a toolbar item to edit that Python script. This works if you have a script editor program defined in the Fusion page settings.

If you do not have a script editor defined, then Resolve will switch to the Fusion page, and display the Fusion settings window to allow you to customize the script editor preference.

![Documentation](images/resolve-fusion-settings-script-editor.png)

A typical value for the Script editor filepath would be something like `/Applications/BBEdit.app` on macOS. On Linux workstations a Script editor filepath might be set to `/usr/bin/xed` or `/usr/bin/gedit`. On Windows you might choose to use a Script editor filepath that points to a copy of VS Code or Notepad++.

This feature requires the "xdg-open" package to be installed on Linux.
