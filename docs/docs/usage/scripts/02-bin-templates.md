---
title: "02 Bin Templates"
sidebar_label: "02 Bin Templates"
sidebar_position: 3
description: "Create Media page based bin folder structures from pre-made templates."
---

# Lightfielder | Scripts

## 02 Bin Templates

Quickly create Media page based Bin folders using pre-made templates.

![Bin Templates](../../images/script_02_Bin_Templates.png)

Tip: The help "?" button at the top right of the window can be used to quickly show this help topic.

### Script Usage

1. Select the "Workspace > Script > Lightfielder > 02 Bin Template" menu item. A "Bin Template" window will appear • OR Select Tool Bar then click "02" button.

2. Use the "Preset" menu to select a Resolve project folder layout. The "Bin Preview" tree view shows what the folder structure will look like.

3. Click the "Go" button to make the Resolve Project folder structures.

### Create a New Preset:

1. You can create a new Bin preset from your current Media page Bin folder hierarchy by pressing the "+" button.

	This will snapshot the active Resolve bin folder structure and save it as a new preset.

2. A "Save Preset" dialog appears that allows you to name the preset.

3. The preset is saved as a .json format document into the folder location:

> `$HOME/Lightfielder/Resolve/Scripts/Utility/Lightfielder/Presets/Bins/`

If you want to delete a preset, simply remove the .json file from the presets folder.

The presets are saved as JSON formatted plain-text documents that can be viewed with a programmer's text editor. Each Bin folder path is entered on its own line and the path is wrapped inside a pair of quotes.

### On-Disk Folder Operations

#### Import External Folders Button

Selects an on-disk project folder hierarchy and imports that (empty) folder structure into the Resolve Media page bins. No files are imported during this process.

#### Create External Folders

Export the current Resolve Media page bin folders. This hierarchy will be re-created as an on-disk folder structure.

### Custom 3DGS Bin Preset

The "Bin_Splat_Postshot" preset is optimized for Gaussian Splatting workflows. It allows you to better manage your multi-view footage in Resolve, along with your [Postshot](https://www.jawset.com/) trained 3DGS output.

![Postshot Bin Templates](../../images/bin_splat_postshot.png)

