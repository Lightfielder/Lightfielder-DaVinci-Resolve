---
title: "Install Ops"
sidebar_label: "Install Ops"
sidebar_position: 1
description: "Install the Lightfielder Operators files, the Python runtime, and the Ops presets."
---

# Lightfielder Operators | Install Ops

## Overview

Ops is a [rust language](https://rust-lang.org/) based agentic interface to control and visualize distributed render tasks running on HPC systems. It is cross-platform compatible and works across Linux, Windows, and macOS. A Swift UI based iOS and VisionOS app acts as a thin client to interface with Ops when you are on the go.

The Ops development effort was bootstrapped using open-source LGPL licensed [Kartaverse](https://github.com/Kartaverse) technology.

## Installation Checklist:

- Install the Ops files
- Install [Python and the Python Modules](install-python.md)
- Import the [Ops presets](../usage/presets.md)

## Installation File Paths

For a single user configuration, the Ops resources are typically installed to:

	$HOME/Ops/

The temporary files are saved to:

	$HOME/Ops/Temp/

The Log files are saved to:

	$HOME/Ops/Logs/

The Ops based Python scripts are located at:

	$HOME/Ops/Scripts/

## Ops Paths

Ops uses the term Paths to represent the installation location used for resources like Lua/Python scripts, menus, and toolbars. The basic process for creating a custom Path entry in the Ops Preferences involves:

1. Open the "Ops \> Ops Settings…" menu.
2. Navigate to the "Paths" section on the left side of the settings dialog:

### Paths:

The Paths settings in "Ops" lets the software know where the files are installed on your hard disk. This makes Ops portable so it can be installed in a cross-platform compatible way.

(Linux)  
**From:** Ops:  
**TO:** /home/Me/Ops/  

(macOS)  
**From:** Ops:  
**To:** /Users/Me/Ops/  

(Windows)  
**From:** Ops:  
**To**: C:\\Users\\Me\\Ops\\  

### Ops Scripts Folders

Inside the "Scripts" folder there are sub-folders that allow you to control where a Python or Lua script shows up in the Ops UI. 

Scripting errors are shown in the Ops Console window which is accessed using the "Scripts \> Console" menu. The Console can also be shown using the "Shift \+ 0" hotkey.

### Paths Disaster Recovery

If you have a Path issue that causes problems with Ops, the Paths settings are stored in a JSON file format at the following location:

Relative Paths: 
	Ops:/Default/Ops.json

Rename the file to "Ops.json.bak" and that setting file will be skipped. A default "Ops \> Ops Settings" menu set of prefs will be generated on the next program launch.

Inside the Ops.json file, the Paths entries can be found in this section of the Lua Table based text file.

To help with troubleshooting, if you want to launch Ops on Linux from the terminal window you can run:

```bash
cd /opt/Ops/bin/
./ops
```
