"""
Lightfielder 01 Preferences.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Allows you to change Lightfielder settings for attributes like rig geometry. This makes it possible to work with volumetric footage from the different eras of the camera array design.

Script Usage:

1. Open Resolve.
-  Select the menu item: "Workspace > Scripts > Lightfielder > 01 Preferences" OR Select "Tool Bar" then click the "01" button.

2. Choose the settings you would like to use. The "Camera Array Geometry" ComboBox menu includes entries for:

- Planar Grid (A1-E5)
- Edge 3M (A1-E5)
- Polar (A100-Z997)

3. If the "Camera Array Geometry" Polar entry is selected, then a "JSON Source File" based filepath entry text field is displayed. Use the "JSON Source File" text field to select a .json formatted Technisync configuration file. The "Load Settings" button will refresh the "Number of Cameras" value using the latest data from the Technisync JSON file.

4. The "Number of Cameras" SpinBox control allows you to define how many cameras are present in the volumetric capture camera rig. This is typically a value from 50 to 55 that is related to the current "Camera Array Geometry" setting.

5. The "Media Format" ComboBox menu includes entries for:

- R3D
- Movie
- Image Sequence
- Still Frame

6. The Project and Sensor "Drop Frame Timecode (DF) checkboxes specifies if the frame rate is formatted as "24" vs "23.97" FPS. The "Sensor Frame Rate" control defines the frame rate present in the captured footage. The "Project Frame Rate" control defines the frame rate present in the Resolve project and editing timelines. The "Sensor Frame Rate" and "Project Frame Rate" ComboBox menus include entries for:

- 24 FPS
- 25 FPS
- 30 FPS
- 48 FPS
- 50 FPS
- 60 FPS
- 90 FPS
- 100 FPS
- 120 FPS
- Custom

7. Click the "Save" button to continue.

Note: The Active Toolbar presets is saved as a .json format document into the folder location:
$HOME/Lightfielder/Resolve/Scripts/Utility/Lightfielder/Presets/Toolbars/

If you want to delete a preset, simply remove the .json file from the presets folder.

The presets are saved as JSON formatted plain-text documents that can be viewed with a programmer's text editor. Each Bin folder path is entered on its own line and the path is wrapped inside a pair of quotes.

Note: The "Use Local Help" checkbox allows you to switch between displaying local on-disk help docs, and  the GitHub repo hosted help docs.

Note: The "Play user interface sound effects" checkbox allows the Lightfielder scripts to play sound effects when tasks are completed, or errors occur.

Note: There is a soft-limit on the Preference windows "Number of Cameras" SpinBox control maximum value that is set to 2048 views. This is applied mostly as a error-check to reduce accidental keyboard entry errors. If you wish to un-clamp that maximum input range for this setting, look in the Python script for the "ID": "NumberOfCamerasSpinner" entry and modify the "Maximum": 2048, number value.

"""

import subprocess
import re
from pprint import pprint
from collections import defaultdict
import os, json, datetime, math
import platform
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

startTimer = datetime.datetime.now()

defaultJSONToolbar = {
	"version": 1,
	"width": 11,
	"height": 2,
	"toolbar": {
		"tool1": {
			"icon": "fa-gear",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/01 Preferences.py",
			"id": "PrefsWin",
			"text": "01",
			"tooltip": "01 Preferences"
		},
		"tool2": {
			"icon": "fa-archive",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/02 Bin Templates.py",
			"id": "BinWin",
			"text": "02",
			"tooltip": "02 Bin Templates"
		},
		"tool3": {
			"icon": "fa-medkit",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/03 Shot Validator.py",
			"id": "ShotlogPreFlightWin",
			"text": "03",
			"tooltip": "03 Shot Pre-Flight"
		},
		"tool4": {
			"icon": "fa-list-alt",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/04 Import Footage.py",
			"id": "ImportFootageWin",
			"text": "04",
			"tooltip": "04 Import Footage"
		},
		"tool5": {
			"icon": "fa-tags",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/05 Metadata Sync.py",
			"id": "MetadataWin",
			"text": "05",
			"tooltip": "05 Metadata Sync"
		},
		"tool6": {
			"icon": "fa-qrcode",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/06 Still Frames Export.py",
			"id": "CalibrationWin",
			"text": "06",
			"tooltip": "06 Still Frames Export"
		},
		"tool7": {
			"icon": "fa-film",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/07 Create EDLs.py",
			"id": "CreateEDLWin",
			"text": "07",
			"tooltip": "07 Create EDLs"
		},
		"tool8": {
			"icon": "fa-cut",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/08 Batch Trim.py",
			"id": "TrimWin",
			"text": "08",
			"tooltip": "08 Batch Trim"
		},
		"tool09": {
			"icon": "fa-level-up",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/11 EDL Stack Swizzle.py",
			"id": "EDLStackSwizzleWin",
			"text": "09",
			"tooltip": "09 EDL Stack Swizzle"
		},
		"tool10": {
			"icon": "fa-fire",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/10 EDL Checker.py",
			"id": "EDLChecker",
			"text": "10",
			"tooltip": "10 EDL Checker"
		},
		"tool11": {
			"icon": "fa-triangle",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/11 Log Viewer.py",
			"id": "LogViewerWin",
			"text": "11",
			"tooltip": "11 Log Viewer"
		},
		"tool12": {
			"icon": "fa-check-circle",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/12 Video Track Solo.py",
			"id": "VideoTrackSoloWin",
			"text": "12",
			"tooltip": "12 Video Track Solo"
		},
		"tool13": {
			"icon": "fa-camera",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/13 Camera Contact Sheet.py",
			"id": "CCSWin",
			"text": "13",
			"tooltip": "13 Camera Contact Sheet"
		},
		"tool14": {
			"icon": "fa-eyedropper",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/14 Grade Automation.py",
			"id": "GradeAutomationWin",
			"text": "14",
			"tooltip": "14 Grade Automation"
		},
		"tool15": {
			"icon": "fa-paper-plane",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/15 EDL Export.py",
			"id": "EDLExportWin",
			"text": "15",
			"tooltip": "15 EDL Export"
		},
		"tool16": {
			"icon": "fa-puzzle-piece",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/16 Extensions.py",
			"id": "ExtensionsWin",
			"text": "16",
			"tooltip": "16 Extensions"
		},
		"tool17": {
			"icon": "fa-book",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/17 Jupyter Link.py",
			"id": "JupyterWin",
			"text": "17",
			"tooltip": "17 Jupyter Link"
		},
		"tool18": {
			"icon": "fa-folder-open",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/18 Open Lightfielder Folder.py",
			"id": "Docs",
			"text": "18",
			"tooltip": "18 Open Lightfielder Folder"
		},
		"tool19": {
			"icon": "fa-file-code-o",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/19 Edit Python Module.py",
			"id": "Docs",
			"text": "19",
			"tooltip": "19 Edit Python Module"
		},
		"tool20": {
			"icon": "fa-file-code-o",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/20 Console.py",
			"id": "fa-file-code-o",
			"text": "20",
			"tooltip": "20 Show Console"
		},
		"tool21": {
			"icon": "fa-code",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/21 Documentation.py",
			"id": "Docs",
			"text": "21",
			"tooltip": "21 Documentation"
		},
		"tool22": {
			"icon": "fa-info-circle",
			"script": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/22 About Lightfielder",
			"id": "AboutWin",
			"text": "22",
			"tooltip": "22 About Lightfielder"
		}
	}
}

def SavePresetWindow():
	ui = fu.UIManager
	preset_disp = bmd.UIDispatcher(ui)

	preset_dlg = preset_disp.AddWindow({
		"WindowTitle": "",
		"ID": "PresetWin",
		"TargetID" : "PresetWin",
		"Geometry": [0, 85, 430, 130],
		"MinimumSize": [0, 85, 430, 130],
		"FixedSize": [0, 85, 430, 130],
		"Spacing": 0,
	},[
		ui.VGroup({"ID": "root", "Weight": 10.0,},[
			ui.VGroup({
				"Weight": 0.1,
			},[
				ui.HGroup({},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "  Save Preset",
						"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
						"Weight": 0.01,
					}),
				]),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 3px; background-color: rgb(76, 154, 109); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
			]),
			ui.HGroup({"Weight": 0.0,},[
				ui.Label({"ID": "PresetLabel", "Text": "Preset Name:", "Weight": 0.1}),
				ui.LineEdit({"ID": "PresetTxt", "Text": "New_Preset", "PlaceholderText": "Please enter a preset name", "Weight": 0.9}),
			]),
			ui.HGroup({"Weight": 0.0,},[
				ui.Button({
					"ID": "CloseButton",
					"Text": "Close",
					"Weight": 0.01,
				}),
				ui.Button({
					"ID": "OKButton",
					"Text": "OK",
					"Weight": 0.01,
				}),
			]),
		]),
	])

	# Resize the window
	preset_dlg.RecalcLayout()

	preset_itm = preset_dlg.GetItems()

	def WindowPrefSave(winDlg, prefName):
		# Save the window position
		if winDlg != None:
			# print("[Lightfielder][Preferences] Saved")
			app.SetData(prefName, winDlg.Geometry)
			# print(app.GetData("Lightfielder"))

			# Write the preferences to disk
			app.SavePrefs()

	def WindowPrefLoad(winDlg, prefName):
		# Restore the window position
		if winDlg != None:
			# print("[Lightfielder][Preferences] Loaded")
			# print(app.GetData("Lightfielder"))
			pref = app.GetData(prefName)
			if pref != None:
				# print(pref)
				winDlg.Geometry = pref
				# Resize the window
				winDlg.RecalcLayout()

	# The window was hidden
	def HideFunc(ev):
		print("[Lightfielder][Window][Hidden]")

		# Save the window preferences
		WindowPrefSave(preset_disp, "Lightfielder.PresetWin.Geometry")
	preset_dlg.On.PresetWin.Hide = HideFunc

	# The window was closed
	def PresetWinFunc(ev):
		preset_disp.ExitLoop()
	preset_dlg.On.PresetWin.Close = PresetWinFunc

	# Add your GUI element based event functions here:

	def OKButtonFunc(ev):
		print("[Lightfielder][Window][OK Button]")
		preset_disp.ExitLoop()
	preset_dlg.On.OKButton.Clicked = OKButtonFunc

	def CloseButtonFunc(ev):
		print("[Lightfielder][Window][Close Button]")
		preset_itm["PresetTxt"].Text = ""
		preset_disp.ExitLoop()
	preset_dlg.On.CloseButton.Clicked = CloseButtonFunc

	# Load the window preferences
	WindowPrefLoad(preset_dlg, "Lightfielder.PresetWin.Geometry")

	preset_dlg.Show()
	preset_disp.RunLoop()
	preset_dlg.Hide()

	# Save the window preferences
	WindowPrefSave(preset_dlg, "Lightfielder.PresetWin.Geometry")

	# When the window is closed send back the preset name
	return str(preset_itm["PresetTxt"].Text)

def CreatePrefsWindow():
	presetsBasePath = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Toolbars/")

	def GetJSON(presetName):
		presetAbsPath = presetsBasePath + str(presetName) + ".json"
		print("[Toolbar Preset] " + str(presetName))

		# Import the JSON preset file
		try:
			with open(presetAbsPath, "r") as f:
				# Todo: Add a try element to catch JSON formatting errors in the presets when they are json.load() accessed.
				jsonStr = json.load(f)
				return jsonStr
		except OSError as error:
			print("\t[Lightfielder][Exception][JSON Get Error]", error)
			return defaultJSONToolbar

	def SetJSON(presetName, data):
		presetAbsPath = presetsBasePath + str(presetName) + ".json"
		print("[Lightfielder][Toolbar Preset] " + str(presetName))

		# Export the JSON preset file
		try:
			with open(presetAbsPath, "w") as f:
				# Todo: Add a try element to catch JSON formatting errors in the presets
				# json.dump(data, f, ensure_ascii = True, indent = 4, sort_keys = True)
				json.dump(data, f, ensure_ascii = True, indent = "\t")
				print("[Lightfielder][Toolbar][Save Preset] " + str(presetName))
		except OSError as error:
			print("\t[Lightfielder][Exception][JSON Save Error]", error)

	def CreateDefaultJSON():
		# Make a default preset
		jsonData = defaultJSONToolbar

		SetJSON("Toolbar_Default", jsonData)

	# Create the intermediate directories on disk for the presets
	if not os.path.exists(presetsBasePath):
		try:
			# Make the dir
			os.makedirs(presetsBasePath)
			print("[Lightfielder][Toolbar][Make Directory]", presetsBasePath)

			# Make a default preset
			CreateDefaultJSON()
		except OSError as error:
			print("[Lightfielder][Exception][Toolbar][Make Directory Error]", error)

	# Get the project name
	res = app.GetResolve()
	project = GetProject()
	if project is None:
		print("[Lightfielder][Project] No Resolve project is open at this time.")
		exit()
	else:
		projectName = project.GetName()

		# Should this window float above all other views
		windowFloat = app.GetData("Lightfielder.WindowStaysOnTop")
		if windowFloat is None:
			windowFloat = True

		# Create a new UI Manager window
		ui = fu.UIManager
		disp = bmd.UIDispatcher(ui)

		dlg = disp.AddWindow({
			"WindowTitle": "Lightfielder",
			"WindowFlags": {"Window": True, "WindowStaysOnTopHint": windowFloat},
			"ID": "PrefsWin",
			"TargetID" : "PrefsWin",
			"Geometry": [500, 50, 815, 665],
			"MinimumSize": [815, 665],
			"FixedSize": [815, 665],
			#"Spacing": 0,
			#"Margin": 5,
		},[
			ui.VGroup({
				"ID": "Content",
				"Weight": 1.0,
			},[
				ui.HGroup({
					"Weight": 0.01,
				},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "01 Preferences",
						"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
						"Margin": 0,
						"Spacing": 0,
						"Weight": 0.01,
					}),
					ui.HGap(20, 1),
					ui.Button({
						"ID": "HelpButton",
						"Flat": True,
						"ToolTip": GetTooltip("Read the docs", "Show the help topic on GitHub"),
						"MinimumSize": [64, 32],
						"Icon": ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Toolbar/fa-question-circle.png"}),
						"Weight": 0.01
					}),
				]),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 3px; background-color: rgb(76, 154, 109); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.TextEdit({
					"ID": "TipTxt",
					"Text": "Tip of the day: The \"Number of Cameras\" control modifies how many video tracks are created when timelines are built with a vertical track layout. 55 views will result in 55 video tracks being added as new multi-view EDLs and timelines are constructed.",
					"ReadOnly": True,
					"StyleSheet": "QTextEdit { border: 0px; }",
					"Weight": 1.0,
				}),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
						"Weight": 0.01,
				},[
					ui.Label({
						"ID": "CameraArrayGeometryLabel",
						"Text": "Camera Array Geometry",
						"Weight": 0.1,
						"MinimumSize": [145, 32],
					}),
					ui.ComboBox({
						"ID": "CameraArrayGeometryCombo",
						"Text": "Mode",
						"ToolTip": GetTooltip("Select a camera rig", "What era of volumetric camera rig design and R3D filename based view labelleing are we using?\nThe A1-E5 format was used from 2022-2024, and the polar layout was used from 2024-2026+."),
						"Weight": 1.0,
					}),
					ui.Button({
						"ID": "LoadSettingsButton",
						"Text": "Load Settings",
						"ToolTip": GetTooltip("Load the settings from the JSON","When the Polor camera array geometry is used, we can pull the preferences \ndirectly from the Technisync JSON configuration file."),
						"MinimumSize": [100, 32],
						"Weight": 0.1
					})
				]),
				ui.HGroup({
					"Weight": 0.01,
					"ID": "CameraGroup",
				},[
					ui.Button({
						"ID": "NumberOfCamerasButton",
						"Flat": True,
						"MinimumSize": [145, 32],
						"Text": GetTooltip("Number of Cameras","Number of Cameras"),
						"Weight": 0.01,
					}),
					ui.SpinBox({
						"ID": "NumberOfCamerasSpinner",
						"ToolTip": GetTooltip("How many cameras do you have?","How many cameras are present in the volumetric capture camera rig?"),
						"Minimum": 1,
						"Maximum": 2048,
						"Value": 50,
						"MinimumSize": [54, 32],
						"Weight": 1.0,
					})
				]),
				ui.HGroup({
					"Weight": 0.01,
					"ID": "JSONSourceGroup",
				},[
					ui.Button({
						"ID": "ShowJSONFilenameButton",
						"Flat": True,
						"MinimumSize": [145, 32],
						"Text": "JSON Source File",
						"ToolTip": GetTooltip("Show the JSON file","Clicking this text label will open the base folder where the JSON file is located in a desktop folder browsing window. This requires a file \npath to be entered in the text field. Shift-clicking the text label will open the file in a JSON viewer. Command-clicking will open the file \nin a text editor."),
						"Weight": 0.01,
					}),
					ui.LineEdit({
						"ID": "JSONCameraConfigFileLineTxt",
						"Text": "",
						"PlaceholderText": "Please enter an activeTechnisyncConfig.json filename",
						"ToolTip": GetTooltip("Enter the location of the JSON file","The Technisync JSON configuration file provides essential details \nfor each R3D camera like the camera angle name, frame rate, etc."),
						"Weight": 0.9
					}),
					ui.Button({
						"ID": "JSONBrowseFileButton",
						"Text": "Browse",
						"MinimumSize": [100, 32],
						"Weight": 0.1
					}),
				]),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
						"Weight": 0.01,
						"ID": "MediaFormatGroup",
				},[
					ui.Button({
						"ID": "MediaFormatButton",
						"Flat": True,
						"MinimumSize": [145, 32],
						"Text": "Media Format",
						"Weight": 0.01,
					}),
					ui.ComboBox({
						"ID": "MediaFormatCombo",
						"Text": "Media Format",
						"ToolTip": GetTooltip("Are you loading R3D RAW footage or something else?","What type of multi-view footage we are going to import?\nThe default option is RED Digital Cinema R3D RAW files."),
						"Weight": 1.0,
					}),
				]),
				ui.HGroup({
						"Weight": 0.01,
						"ID": "SensorFrameRateGroup",
				},[
					ui.Button({
						"ID": "SensorFrameRateButton",
						"Flat": True,
						"MinimumSize": [145, 32],
						"Text": "Sensor Frame Rate",
						"Weight": 0.01,
					}),
					ui.ComboBox({
						"ID": "SensorFrameRateCombo",
						"Text": "Sensor Frame Rate",
						"ToolTip": GetTooltip("The source footage frame rate.","The frame rate used when the source footage was captured to a R3D file or movie."),
						"Weight": 1.0,
					}),
					ui.SpinBox({
						"ID": "SensorFrameRateCustomSpinner",
						"ToolTip": GetTooltip("Enter a custom frame rate","When the \"Sensor Frame Rate\" menu item is set to \"Custom\" you have the option to manually enter a frame rate."),
						"Minimum": 1,
						"Maximum": 2048,
						"Value": 24,
						"MinimumSize": [54, 32],
						"Weight": 0.1,
					}),
					ui.Label({
						"ID": "SensorFrameRateCustomLabel",
						"Text": "FPS",
						"Weight": 0.1,
					}),
					ui.CheckBox({
						"ID": "SensorDropFrameTimecodeCheckbox",
						"Text": "Drop Frame Timecode (DF)",
						"ToolTip": GetTooltip("Was drop-frame timecode used?","Should the timecode and frame rate be formatted as an integer based (non-drop frame value) \nlike \"24\", or as a floating-point (drop-frame value) like \"23.97\" FPS?"),
						"Checked": False,
					}),
				]),
				ui.HGroup({
						"Weight": 0.01,
						"ID": "ProjectFrameRateGroup",
				},[
					ui.Button({
						"ID": "ProjectFrameRateButton",
						"Flat": True,
						"MinimumSize": [145, 32],
						"Text": "Project Frame Rate",
						"Weight": 0.01,
					}),
					ui.ComboBox({
						"ID": "ProjectFrameRateCombo",
						"Text": "Project Frame Rate",
						"ToolTip": GetTooltip("What frame rate is used for Resolve projects and timelines","The frame rate used for the Resolve project and editing timelines."),
						"Weight": 1.0,
					}),
					ui.SpinBox({
						"ID": "ProjectFrameRateCustomSpinner",
						"ToolTip": GetTooltip("Enter a custom frame rate","When the \"Project Frame Rate\" menu item is set to \"Custom\" you have the option to manually enter a frame rate."),
						"Minimum": 1,
						"Maximum": 2048,
						"Value": 24,
						"MinimumSize": [54, 32],
						"Weight": 0.1,
					}),
					ui.Label({
						"ID": "ProjectFrameRateCustomLabel",
						"Text": "FPS",
						"Weight": 0.1,
					}),
					ui.CheckBox({
						"ID": "ProjectDropFrameTimecodeCheckbox",
						"Text": "Drop Frame Timecode (DF)",
						"ToolTip": GetTooltip("Was drop-frame timecode used?","Should the timecode and frame rate be formatted as an integer based (non-drop frame value) \nlike \"24\", or as a floating-point (drop-frame value) like \"23.97\" FPS?"),
						"Checked": False,
					}),
				]),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
						"Weight": 0.01,
						"ID": "HelpGroup1",
				},[
					ui.CheckBox({
						"ID": "AutoloadToolbarOnLaunchCheckbox",
						"Text": "Autoload Toolbar on Launch",
						"ToolTip": GetTooltip("Do you want to see the toolbar when Resolve starts up?","When this option is enabled it tells the Lightfielder Toolbar to \nopen up automatically when DaVinci Resolve Studio starts."),
						"Checked": False,
					}),
					ui.CheckBox({
						"ID": "WindowStaysOnTopCheckbox",
						"Text": "Script Window Stays On Top",
						"ToolTip": GetTooltip("(WIP) Should the Lightfielder scripts always float ontop?", "(WIP) When this option is enabled the Lightfielder script user interface \nwindows will always float ontop of all other programs and windows."),
						"Checked": True,
					}),
					ui.CheckBox({
						"ID": "RTFMTooltipsCheckbox",
						"Text": "RTFM Tooltips",
						"ToolTip": GetTooltip("Do you want long tooltips or short tooltips?", "When this option is enabled the tooltips will provide more detailed help information \nthat will save you a visit to the documentation for tool usage information."),
						"Checked": True,
					}),
					ui.CheckBox({
						"ID": "UseLocalHelpCheckbox",
						"Text": "Use Local Help Docs",
						"ToolTip": GetTooltip("Use the documentation on my hard disk.", "When this option is enabled the help is shown using local HTML files that are displayed in your web browser.\nIf the option is disabled then the help is shown using reference content hosted on the project's GitHub repo."),
						"Checked": False,
					}),
					ui.CheckBox({
						"ID": "FuzzyR3DDateMatchingCheckbox",
						"Text": "Fuzzy R3D Date Matching",
						"ToolTip": GetTooltip("(WIP) Do you have date problems to fix with your footage?", "(WIP) When this option is enabled the Shotlog CSV date field will be considered \na match with the R3D filename date value if they are within 1 day +/-."),
						"Checked": False,
					}),
				]),
				ui.HGroup({
					"Weight": 0.01,
					"ID": "HelpGroupSoundEffects1",
				},[
					ui.CheckBox({
						"ID": "PlayUserInterfacesSoundEffectsCheckbox",
						"Text": "Play user interface sound effects",
						"ToolTip": GetTooltip("Play sound effects when things happen.", "(WIP) When this option is enabled the Lightfielder scripts will play \nsound effects when tasks are completed, or errors occur."),
						"Checked": True,
					}),
					ui.Label({
						"ID": "SoundEffectsVolumeLabel",
						"Text": "Volume",
						"ToolTip": GetTooltip("Change the volume of the sound effects.", "Adjust the playback volume of the user interface sound effects."),
						"Weight": 0.1,
					}),
					# Add a button icon for a low volume speaker
					ui.Slider({
						"ID": "SoundEffectsVolumeSlider",
						"ToolTip": GetTooltip("Change the volume of the sound effects.", "Adjust the playback volume of the user interface sound effects."),
						"Value": 5,
						"Minimum": 0,
						"Maximum": 11,
						"StepBy": 0.1,
						"SingleStep": 0.1,
					}),
					ui.Label({
						"ID": "SoundEffectsVolumeNumberLabel",
						"Text": "🔉",
						"ToolTip": GetTooltip("The volume goes from 0 to 11", "The playback volume as a number from 0 to 11."),
						"Weight": 0.1,
					}),
					# Add a button icon for a high volume speaker
				]),
				ui.HGroup({
						"Weight": 0.01,
						"ID": "HelpGroupSoundEffects2",
				},[
					ui.Button({
						"ID": "SoundEffectsErrorButton",
						"Flat": True,
						"Text": "Event: On Error Sound",
						"ToolTip": GetTooltip("Preview the \"On Error\" sound effect", "Listen to a preview of the sound effect that plays when Lightfielder reports an error occured."),
						"Weight": 0.01,
					}),
					ui.ComboBox({
						"ID": "SoundEffectsErrorCombo",
						"ToolTip": GetTooltip("What error sound effect should I used?", "Choose the sound effect that plays when Lightfielder reports an error occurred."),
						"Weight": 1.0,
					}),
					ui.Button({
						"ID": "SoundEffectsCompleteButton",
						"Flat": True,
						"Text": "Event: Task Complete Sound",
						"ToolTip": GetTooltip("Preview the \"Task Complete\" sound effect", "Listen to a preview of the sound effect that plays when Lightfielder reports a task completed."),
						"Weight": 0.01,
					}),
					ui.ComboBox({
						"ID": "SoundEffectsCompleteCombo",
						"ToolTip": GetTooltip("What task completed sound effect should I used?", "Choose the sound effect that plays when Lightfielder reports a task completed."),
						"Weight": 1.0,
					}),
				]),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
					"Weight": 0.01,
					"ID": "ToolbarPresetGroup",
				},[
					ui.Button({
						"ID": "ShowToolbarPresetButton",
						"Flat": True,
						"MinimumSize": [170, 26],
						"Text": "Toolbar Preset",
						"ToolTip": "Clicking this text label will open the base folder where the Toolbar Preset file \nis located in a desktop folder browsing window.",
						"Weight": 0.01,
					}),
					ui.ComboBox({
						"ID": "ToolbarCombo",
						"ToolTip": GetTooltip("Select a Toolbar preset","The Toolbar window is now fully customizable using \na JSON preset format."),
						"MinimumSize": [150, 26],
						"Weight": 2.0,
					}),
					ui.Button({"ID": "AddPresetButton", "Text": "+", "MinimumSize": [32, 24], "Weight": 0.1}),
					ui.Button({
						"ID": "ToolbarSettingsButton",
						"Text": "Toolbar Settings",
						#"MinimumSize": [120, 32],
						"Weight": 1.0,
					}),
				]),
				ui.HGroup({
					"Weight": 0.01,
					"ID": "ToolbarGeometryGroup",
				},[
					# ui.HGap(20, 1),
					ui.Button({
						"ID": "ToolbarLayoutButton",
						"Flat": True,
						"MinimumSize": [170, 26],
						"Text": "Toolbar Grid Layout",
						"ToolTip": "Reset the Toolbar window layout to the default values.",
						"Weight": 0.1,
					}),
					ui.SpinBox({
						"ID": "WindowLayoutHorizontalSpinner",
						"ToolTip": GetTooltip("Horizontal Buttons","How many buttons wide is the Toolbar window?"),
						"Minimum": 1,
						"Maximum": 64,
						"Value": 11,
						"MinimumSize": [40, 26],
						"Weight": 0.1,
					}),
					ui.Label({
						"ID": "WideLayoutLabel",
						"Text": "Wide by",
						"Weight": 0.1,
					}),
					ui.SpinBox({
						"ID": "WindowLayoutVerticalSpinner",
						"ToolTip": GetTooltip("Vertical Buttons","How many buttons tall is the Toolbar window?"),
						"Minimum": 1,
						"Maximum": 64,
						"Value": 2,
						"MinimumSize": [40, 26],
						"Weight": 0.1,
					}),
					ui.Label({
						"ID": "ButtonsLabel",
						"Text": "Tall",
						"Weight": 0.1,
					}),
					ui.HGap(1, 1),
				]),
				ui.HGroup({
					"Weight": 0.1
				},[
					ui.Label({
						"ID": "ProgressLabel",
						"Text": "  Progress: Awaiting User Input",
						"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
						"Margin": 0,
						"Spacing": 0,
						"Weight": 0.01,
						"MinimumSize": [355, 24],
					}),
					ui.Button({
						"ID": "ConsoleButton",
						"Text": "  Console",
						"Margin": 0,
						"Spacing": 0,
						"Weight": 0.01,
						"MaximumSize": [86, 24],
						"IconSize": [16, 16],
						"Checkable": True,
						"Icon": ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Toolbar/fa-code.png"}),
					}),
				]),
				ui.HGroup({
					"Weight": 0.01,
				},[
					ui.Button({
						"ID": "CloseButton",
						"Text": "Close",
						"Weight": 0.5,
					}),
					ui.Button({
						"ID": "SaveButton",
						"Text": "Save",
						"MinimumSize": [120, 32],
						"Weight": 0.5
					}),
					ui.Button({
						"ID": "PrevScriptButton",
						"Text": "<",
						"ToolTip": GetTooltip("Show the previous script.", "Open the previous script from the Lightfielder Toolbar"),
						"MinimumSize": [32, 32],
						"Weight": 0.01
					}),
					ui.Button({
						"ID": "NextScriptButton",
						"Text": ">",
						"ToolTip": GetTooltip("Show the next script.", "Open the next script from the Lightfielder Toolbar"),
						"MinimumSize": [32, 32],
						"Weight": 0.01
					}),
				]),
			]),
		])

		itm = dlg.GetItems()

		# Camera Array Geometry
		itm["CameraArrayGeometryCombo"].AddItem("Planar Grid (A1-E5)")
		itm["CameraArrayGeometryCombo"].AddItem("Wedge 3M (A1-E5)")
		itm["CameraArrayGeometryCombo"].AddItem("Polar (A110-Z977)")

		# Media Format
		itm["MediaFormatCombo"].AddItem("R3D")
		itm["MediaFormatCombo"].AddItem("Movie")
		itm["MediaFormatCombo"].AddItem("Image Sequence")
		itm["MediaFormatCombo"].AddItem("Still Frame")

		# Frame Rate
		itm["SensorFrameRateCombo"].AddItem("24 FPS")
		itm["SensorFrameRateCombo"].AddItem("25 FPS")
		itm["SensorFrameRateCombo"].AddItem("30 FPS")
		itm["SensorFrameRateCombo"].AddItem("48 FPS")
		itm["SensorFrameRateCombo"].AddItem("50 FPS")
		itm["SensorFrameRateCombo"].AddItem("60 FPS")
		itm["SensorFrameRateCombo"].AddItem("90 FPS")
		itm["SensorFrameRateCombo"].AddItem("100 FPS")
		itm["SensorFrameRateCombo"].AddItem("120 FPS")
		itm["SensorFrameRateCombo"].AddItem("Custom")

		itm["ProjectFrameRateCombo"].AddItem("24 FPS")
		itm["ProjectFrameRateCombo"].AddItem("25 FPS")
		itm["ProjectFrameRateCombo"].AddItem("30 FPS")
		itm["ProjectFrameRateCombo"].AddItem("48 FPS")
		itm["ProjectFrameRateCombo"].AddItem("50 FPS")
		itm["ProjectFrameRateCombo"].AddItem("60 FPS")
		itm["ProjectFrameRateCombo"].AddItem("90 FPS")
		itm["ProjectFrameRateCombo"].AddItem("100 FPS")
		itm["ProjectFrameRateCombo"].AddItem("120 FPS")
		itm["ProjectFrameRateCombo"].AddItem("Custom")

		# User interface sounds
		itm["SoundEffectsErrorCombo"].AddItem("None")
		itm["SoundEffectsErrorCombo"].AddItem("Steam Train Whistle Sound")
		itm["SoundEffectsErrorCombo"].AddItem("Trumpet Sound")
		itm["SoundEffectsErrorCombo"].AddItem("Braam Sound")
		itm["SoundEffectsCompleteCombo"].AddItem("None")
		itm["SoundEffectsCompleteCombo"].AddItem("Steam Train Whistle Sound")
		itm["SoundEffectsCompleteCombo"].AddItem("Trumpet Sound")
		itm["SoundEffectsCompleteCombo"].AddItem("Braam Sound")

		def PrefSave(winDlg):
			# Save the prefs
			if winDlg != None:
				# print("[Lightfielder][Preferences] Saved")
				app.SetData("Lightfielder.JSONCameraConfigFile", itm["JSONCameraConfigFileLineTxt"].Text)
				app.SetData("Lightfielder.ArrayGeometry", itm["CameraArrayGeometryCombo"].CurrentIndex)
				app.SetData("Lightfielder.NumberOfCameras", itm["NumberOfCamerasSpinner"].Value)
				app.SetData("Lightfielder.MediaFormat", itm["MediaFormatCombo"].CurrentText)
				app.SetData("Lightfielder.SensorFrameRateCustom", itm["SensorFrameRateCustomSpinner"].Value)
				app.SetData("Lightfielder.SensorDropFrameTimecode", itm["SensorDropFrameTimecodeCheckbox"].Checked)
				app.SetData("Lightfielder.ProjectFrameRateCustom", itm["ProjectFrameRateCustomSpinner"].Value)
				app.SetData("Lightfielder.ProjectDropFrameTimecode", itm["ProjectDropFrameTimecodeCheckbox"].Checked)

				app.SetData("Lightfielder.Toolbar", itm["ToolbarCombo"].CurrentText)
				app.SetData("Lightfielder.WindowLayoutHorizontal", itm["WindowLayoutHorizontalSpinner"].Value)
				app.SetData("Lightfielder.WindowLayoutVertical", itm["WindowLayoutVerticalSpinner"].Value)

				app.SetData("Lightfielder.AutoloadToolbarOnLaunch", itm["AutoloadToolbarOnLaunchCheckbox"].Checked)
				app.SetData("Lightfielder.UseLocalHelp", itm["UseLocalHelpCheckbox"].Checked)
				app.SetData("Lightfielder.RTFMTooltips", itm["RTFMTooltipsCheckbox"].Checked)
				app.SetData("Lightfielder.FuzzyR3DDateMatching", itm["FuzzyR3DDateMatchingCheckbox"].Checked)
				app.SetData("Lightfielder.WindowStaysOnTop", itm["WindowStaysOnTopCheckbox"].Checked)
				app.SetData("Lightfielder.PlayUserInterfacesSoundEffects", itm["PlayUserInterfacesSoundEffectsCheckbox"].Checked)
				app.SetData("Lightfielder.SoundEffectsVolume", itm["SoundEffectsVolumeSlider"].Value)
				app.SetData("Lightfielder.SoundEffectsError", itm["SoundEffectsErrorCombo"].CurrentText)
				app.SetData("Lightfielder.SoundEffectsComplete", itm["SoundEffectsCompleteCombo"].CurrentText)

				# FPS Lookups
				app.SetData("Lightfielder.ProjectFrameRate", itm["ProjectFrameRateCombo"].CurrentText)
				app.SetData("Lightfielder.SensorFrameRate", itm["SensorFrameRateCombo"].CurrentText)
				# print(app.GetData("Lightfielder"))

		def PrefLoad(winDlg):
			# Restore the prefs
			if winDlg != None:
				# print("[Lightfielder][Preferences] Loaded")
				# print(app.GetData("Lightfielder.CSVFile"))
				# CSV File
				pref = app.GetData("Lightfielder.JSONCameraConfigFile")
				if pref != None:
					# print(pref)
					itm["JSONCameraConfigFileLineTxt"].Text = pref
				pref = app.GetData("Lightfielder.ArrayGeometry")
				if pref != None:
					# print(pref)
					itm["CameraArrayGeometryCombo"].CurrentIndex = pref
				pref = app.GetData("Lightfielder.NumberOfCameras")
				if pref != None:
					# print(pref)
					itm["NumberOfCamerasSpinner"].Value = pref
				pref = app.GetData("Lightfielder.MediaFormat")
				if pref != None:
					# print(pref)
					itm["MediaFormatCombo"].CurrentText = pref
				pref = app.GetData("Lightfielder.SensorFrameRate")
				if pref != None:
					# print(pref)
					itm["SensorFrameRateCombo"].CurrentText = pref
				pref = app.GetData("Lightfielder.SensorFrameRateCustom")
				if pref != None:
					# print(pref)
					itm["SensorFrameRateCustomSpinner"].Value = pref
				pref = app.GetData("Lightfielder.SensorDropFrameTimecode")
				if pref != None:
					# print(pref)
					itm["SensorDropFrameTimecodeCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.ProjectFrameRate")
				if pref != None:
					# print(pref)
					itm["ProjectFrameRateCombo"].CurrentText = pref
				pref = app.GetData("Lightfielder.ProjectFrameRateCustom")
				if pref != None:
					# print(pref)
					itm["ProjectFrameRateCustomSpinner"].Value = pref
				pref = app.GetData("Lightfielder.ProjectDropFrameTimecode")
				if pref != None:
					# print(pref)
					itm["ProjectDropFrameTimecodeCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.Toolbar")
				if pref != None:
					# print(pref)
					itm["ToolbarCombo"].CurrentText = pref
				pref = app.GetData("Lightfielder.WindowLayoutHorizontal")
				if pref != None:
					# print(pref)
					itm["WindowLayoutHorizontalSpinner"].Value = pref
				pref = app.GetData("Lightfielder.WindowLayoutVertical")
				if pref != None:
					# print(pref)
					itm["WindowLayoutVerticalSpinner"].Value = pref
				pref = app.GetData("Lightfielder.AutoloadToolbarOnLaunch")
				if pref != None:
					# print(pref)
					itm["AutoloadToolbarOnLaunchCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.UseLocalHelp")
				if pref != None:
					# print(pref)
					itm["UseLocalHelpCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.RTFMTooltips")
				if pref != None:
					# print(pref)
					itm["RTFMTooltipsCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.FuzzyR3DDateMatching")
				if pref != None:
					# print(pref)
					itm["FuzzyR3DDateMatchingCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.WindowStaysOnTop")
				if pref != None:
					# print(pref)
					itm["WindowStaysOnTopCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.PlayUserInterfacesSoundEffects")
				if pref != None:
					# print(pref)
					itm["PlayUserInterfacesSoundEffectsCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.SoundEffectsVolume")
				if pref != None:
					# print(pref)
					itm["SoundEffectsVolumeSlider"].Value = pref
				pref = app.GetData("Lightfielder.SoundEffectsError")
				if pref != None:
					# print(pref)
					itm["SoundEffectsErrorCombo"].CurrentText = pref
				pref = app.GetData("Lightfielder.SoundEffectsComplete")
				if pref != None:
					# print(pref)
					itm["SoundEffectsCompleteCombo"].CurrentText = pref

		def WindowPrefSave(winDlg, prefName):
			# Save the window position
			if winDlg != None:
				# print("[Lightfielder]][Preferences] Saved")
				app.SetData(prefName, winDlg.Geometry)
				# print(app.GetData("Lightfielder"))

				# Write the preferences to disk
				app.SavePrefs()

		def WindowPrefLoad(winDlg, prefName):
			# Restore the window position
			if winDlg != None:
				# print("[Lightfielder][Preferences] Loaded")
				# print(app.GetData("Lightfielder"))
				pref = app.GetData(prefName)
				if pref != None:
					# print(pref)
					winDlg.Geometry = pref
					# Resize the window
					winDlg.RecalcLayout()

		# The window was hidden
		def HideFunc(ev):
			print("[Lightfielder][Window][Hidden]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.PrefsWin.Geometry")

			# Save the pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
		dlg.On.PrefsWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.PrefsWin.Geometry")

			# Save the pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.PrefsWin.Close = CloseFunc

		def CloseButtonFunc(ev):
			print("[Lightfielder][Window][Close Button]")
			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)
			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.PrefsWin.Geometry")

			# Save the pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.CloseButton.Clicked = CloseButtonFunc

		def SaveButtonFunc(ev):
			# startTimer = datetime.datetime.now()
			# startTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")
			print("[Lightfielder][Preferences][Save Button]")

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.PrefsWin.Geometry")

			# Save the pref
			PrefSave(dlg)

			# itm["ProgressLabel"].Text = "  Progress: Saved Preferences [Wallclock " + GetTimeElapsed(startTimer) + "]"

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
		dlg.On.SaveButton.Clicked = SaveButtonFunc

		# Add your GUI element based event functions here:

		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_01_Preferences.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		# Click on the filename text label to open the filename in an external editor, or open the containing folder in the operating system's folder browsing view
		def ShowJSONFilenameButtonFunc(ev):
			buttonModifier = ev["modifiers"]["ShiftModifier"]
			buttonModifierControl = ev["modifiers"]["ControlModifier"]

			if buttonModifier == True:
				# shift was held down so open the OS default program for this filetype
				 ShowInDefaultProgram(itm["JSONCameraConfigFileLineTxt"].Text)
				 itm["ProgressLabel"].Text = "  Progress: Open the Technisync JSON file"
			elif buttonModifierControl == True:
				# Command/Control was held down so open the programmer's text editor
				ExternalEditor(itm["JSONCameraConfigFileLineTxt"].Text)
				itm["ProgressLabel"].Text = "  Progress: Edit the Technisync JSON file"
			else:
				# Label was clicked on with no modifier keys so open the containing folder in the operating system's folder browsing view
				ShowFolderFromFilepath(itm["JSONCameraConfigFileLineTxt"].Text)
				itm["ProgressLabel"].Text = "  Progress: Show Technisync JSON file containing folder"
		dlg.On.ShowJSONFilenameButton.Clicked = ShowJSONFilenameButtonFunc

		# Show a file browsing dialog to select the JSON file
		def JSONBrowseFileButtonFunc(ev):
			selectedPath = fu.RequestFile()
			if selectedPath:
				jsonCameraConfigFile = str(app.MapPath(selectedPath))
				itm["JSONCameraConfigFileLineTxt"].Text = jsonCameraConfigFile

				# Pull the Number of Camerascount from the Technisync JSON file
				if os.path.isfile(jsonCameraConfigFile):
					if selectedPath.endswith(".json") and not selectedPath.startswith("."):
						viewCount = GetJSONConfigViews(jsonCameraConfigFile, "views")
						itm['NumberOfCamerasSpinner'].Value = int(viewCount)
						itm["ProgressLabel"].Text = "  Progress: Loaded JSON File: \"" + str(os.path.basename(selectedPath)) + "\""
					else:
						print("[Lightfielder][Preferences] This file lacks the .json file extension.")
						itm["ProgressLabel"].Text = "  Progress: This file lacks the .json file extension. Select a JSON file."
				else:
					print("[Lightfielder][Preferences] A JSON File does not exist at this filepath.")
					itm["ProgressLabel"].Text = "  Progress: A JSON File does not exist at this filepath. Select a JSON file."
			# Save the prefs
			PrefSave(dlg)
		dlg.On.JSONBrowseFileButton.Clicked = JSONBrowseFileButtonFunc

		# Only show the "JSON Source File" input fields if a polar camera array is used
		def CameraArrayGeometryComboFunc(ev):
			cameraArrayGeometry = itm["CameraArrayGeometryCombo"].CurrentIndex
			if cameraArrayGeometry == 0 or cameraArrayGeometry == 1:
				itm["ShowJSONFilenameButton"].Visible = False
				itm["JSONCameraConfigFileLineTxt"].Visible = False
				itm["JSONBrowseFileButton"].Visible = False
				itm["JSONSourceGroup"].Visible = False
				# itm["LoadSettingsButton"].Visible = False
			else:
				itm["ShowJSONFilenameButton"].Visible = True
				itm["JSONCameraConfigFileLineTxt"].Visible = True
				itm["JSONBrowseFileButton"].Visible = True
				itm["JSONSourceGroup"].Visible = True
				# itm["LoadSettingsButton"].Visible = True
			dlg:RecalcLayout()
			# itm["ProgressLabel"].Text = "  Progress: Updated \"Camera Array Geometry\" to \"" + str(itm["CameraArrayGeometryCombo"].CurrentText) + "\""
		dlg.On.CameraArrayGeometryCombo.CurrentIndexChanged = CameraArrayGeometryComboFunc

		# Only show the "Custom Frame Rate" input fields when required
		def SensorFrameRateComboFunc(ev):
			custom = itm["SensorFrameRateCombo"].CurrentText
			# print(custom)
			if custom == "Custom":
				itm["SensorFrameRateCustomSpinner"].Visible = True
				itm["SensorFrameRateCustomLabel"].Visible = True
				itm["ProgressLabel"].Text = "  Progress: Displaying Sensor \"Custom\" FPS Controls"
			else:
				itm["SensorFrameRateCustomSpinner"].Visible = False
				itm["SensorFrameRateCustomLabel"].Visible = False
			dlg:RecalcLayout()
		dlg.On.SensorFrameRateCombo.CurrentIndexChanged = SensorFrameRateComboFunc

		# Only show the "Custom Frame Rate" input fields when required
		def ProjectFrameRateComboFunc(ev):
			custom = itm["ProjectFrameRateCombo"].CurrentText
			# print(custom)
			if custom == "Custom":
				itm["ProjectFrameRateCustomSpinner"].Visible = True
				itm["ProjectFrameRateCustomLabel"].Visible = True
				itm["ProgressLabel"].Text = "  Progress: Displaying Project \"Custom\" FPS Controls"
			else:
				itm["ProjectFrameRateCustomSpinner"].Visible = False
				itm["ProjectFrameRateCustomLabel"].Visible = False
			dlg:RecalcLayout()
		dlg.On.ProjectFrameRateCombo.CurrentIndexChanged = ProjectFrameRateComboFunc

		# How many cameras are in the camera rig?
		def NumberOfCamerasSpinnerFunc(ev):
			viewNum = itm['NumberOfCamerasSpinner'].Value
		dlg.On.NumberOfCamerasSpinner.ValueChanged = NumberOfCamerasSpinnerFunc

		def MediaFormatButtonFunc(ev):
			print("[Lightfielder][Preferences] Reset Media Format to R3D")
			itm['MediaFormatCombo'].CurrentText = "R3D"
			itm["ProgressLabel"].Text = "  Progress: Reset \"Media Format\" to R3D"
		dlg.On.MediaFormatButton.Clicked = MediaFormatButtonFunc

		def MediaFormatComboFunc(ev):
			print("[Lightfielder][Preferences] Updated \"Media Format\" to " + str(itm["MediaFormatCombo"].CurrentText))
			PrefSave(dlg)

			# Write the preferences to disk
			app.SavePrefs()

			# itm["ProgressLabel"].Text = "  Progress: Updated \"Media Format\" to " + str(itm["MediaFormatCombo"].CurrentText)
		dlg.On.MediaFormatCombo.CurrentIndexChanged = MediaFormatComboFunc

		def NumberOfCamerasButtonFunc(ev):
			print("[Lightfielder][Preferences] Reset Number of Cameras Count")
			cameraArrayGeometry = itm["CameraArrayGeometryCombo"].CurrentIndex

			if cameraArrayGeometry == 0:
				# Planar Grid (A1-E5)
				itm['NumberOfCamerasSpinner'].Value = 50
			elif cameraArrayGeometry == 1:
				# Wedge 3M (A1-E5)
				itm['NumberOfCamerasSpinner'].Value = 50
			elif cameraArrayGeometry == 2:
				# Polar (A110-Z977)
				itm['NumberOfCamerasSpinner'].Value = 55
			else:
				itm['NumberOfCamerasSpinner'].Value = 55

			itm["ProgressLabel"].Text = "  Progress: Reset \"Number of Cameras\" Count to " + str(itm['NumberOfCamerasSpinner'].Value)
		dlg.On.NumberOfCamerasButton.Clicked = NumberOfCamerasButtonFunc

		def SensorFrameRateButtonFunc(ev):
			print("[Lightfielder][Preferences] Update Sensor Frame Rate")
			cameraArrayGeometry = itm["CameraArrayGeometryCombo"].CurrentIndex

			if cameraArrayGeometry == 0:
				# Planar Grid (A1-E5)
				itm['SensorFrameRateCombo'].CurrentText = "30 FPS"
			elif cameraArrayGeometry == 1:
				# Wedge 3M (A1-E5)
				itm['SensorFrameRateCombo'].CurrentText = "30 FPS"
			elif cameraArrayGeometry == 2:
				# Polar (A110-Z977)
				# Pull the info from the Technisync JSON file
				jsonCameraConfigFile = str(app.MapPath(itm["JSONCameraConfigFileLineTxt"].Text))
				if os.path.isfile(jsonCameraConfigFile):
					# Sensor Frame Rate
					sensorfps = GetJSONConfigViews(jsonCameraConfigFile, "sensorfps")
					# print(fps)
					if sensorfps == "24 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "24 FPS"
					elif sensorfps == "25 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "25 FPS"
					elif sensorfps == "30 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "30 FPS"
					elif sensorfps == "48 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "48 FPS"
					elif sensorfps == "50 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "50 FPS"
					elif sensorfps == "60 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "60 FPS"
					elif sensorfps == "90 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "90 FPS"
					elif sensorfps == "100 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "100 FPS"
					elif sensorfps == "120 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "120 FPS"
					else:
						# Fallback FPS rate
						itm['SensorFrameRateCombo'].CurrentText = "Custom"
						
					itm["ProgressLabel"].Text = "  Progress: Updated \"Sensor Frame Rate\" to " + str(itm['SensorFrameRateCombo'].CurrentText)
				else:
					print("[Lightfielder][Preferences] A JSON File does not exist at this filepath.")
					itm["ProgressLabel"].Text = "  Progress: A JSON File does not exist at this filepath"
		dlg.On.SensorFrameRateButton.Clicked = SensorFrameRateButtonFunc

		def ProjectFrameRateButtonFunc(ev):
			print("[Lightfielder][Preferences] Update Project Frame Rate")
			cameraArrayGeometry = itm["CameraArrayGeometryCombo"].CurrentIndex

			if cameraArrayGeometry == 0:
				# Planar Grid (A1-E5)
				itm['ProjectFrameRateCombo'].CurrentText = "30 FPS"
			elif cameraArrayGeometry == 1:
				# Wedge 3M (A1-E5)
				itm['ProjectFrameRateCombo'].CurrentText = "30 FPS"
			elif cameraArrayGeometry == 2:
				# Polar (A110-Z977)
				# Pull the info from the Technisync JSON file
				jsonCameraConfigFile = str(app.MapPath(itm["JSONCameraConfigFileLineTxt"].Text))
				if os.path.isfile(jsonCameraConfigFile):
					# project Frame Rate
					projectfps = GetJSONConfigViews(jsonCameraConfigFile, "projectfps")
					# print(fps)
					if projectfps == "24 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "24 FPS"
					elif projectfps == "25 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "25 FPS"
					elif projectfps == "30 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "30 FPS"
					elif projectfps == "48 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "48 FPS"
					elif projectfps == "50 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "50 FPS"
					elif projectfps == "60 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "60 FPS"
					elif projectfps == "90 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "90 FPS"
					elif projectfps == "100 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "100 FPS"
					elif projectfps == "120 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "120 FPS"
					else:
						# Fallback Sensor FPS rate
						itm['ProjectFrameRateCombo'].CurrentText = "Custom"
					
					itm["ProgressLabel"].Text = "  Progress: Updated \"Project Frame Rate\" to " + str(itm['ProjectFrameRateCombo'].CurrentText)
				else:
					print("[Lightfielder][Preferences] A JSON File does not exist at this filepath.")
					itm["ProgressLabel"].Text = "  Progress: A JSON File does not exist at this filepath"
		dlg.On.ProjectFrameRateButton.Clicked = ProjectFrameRateButtonFunc

		def LoadSettingsButtonFunc(ev):
			startTimer = datetime.datetime.now()
			startTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")

			print("[Lightfielder][Preferences] Load Settings")
			cameraArrayGeometry = itm["CameraArrayGeometryCombo"].CurrentIndex

			if cameraArrayGeometry == 0:
				# Planar Grid (A1-E5)
				itm['NumberOfCamerasSpinner'].Value = 50
				itm['MediaFormatCombo'].CurrentText = "R3D"
				itm['SensorFrameRateCombo'].CurrentText = "30 FPS"
				itm['ProjectFrameRateCombo'].CurrentText = "30 FPS"
				itm["SensorFrameRateCustomSpinner"].Value = 30
				itm["ProjectFrameRateCustomSpinner"].Value = 30

				itm["ProgressLabel"].Text = "  Progress: Loading Settings for a \"" + str(itm["CameraArrayGeometryCombo"].CurrentText) + "\" camera array to use the defaults"
			elif cameraArrayGeometry == 1:
				# Wedge 3M (A1-E5)
				itm['NumberOfCamerasSpinner'].Value = 50
				itm['MediaFormatCombo'].CurrentText = "R3D"
				itm['SensorFrameRateCombo'].CurrentText = "30 FPS"
				itm['ProjectFrameRateCombo'].CurrentText = "30 FPS"
				itm["SensorFrameRateCustomSpinner"].Value = 30
				itm["ProjectFrameRateCustomSpinner"].Value = 30
				
				itm["ProgressLabel"].Text = "  Progress: Loading Settings for a \"" + str(itm["CameraArrayGeometryCombo"].CurrentText) + "\" camera array to use the defaults"
			elif cameraArrayGeometry == 2:
				# Polar (A110-Z977)
				# Pull the info from the Technisync JSON file
				jsonCameraConfigFile = str(app.MapPath(itm["JSONCameraConfigFileLineTxt"].Text))
				if os.path.isfile(jsonCameraConfigFile):
					viewCount = GetJSONConfigViews(jsonCameraConfigFile, "views")
					# print(viewCount)
					itm['NumberOfCamerasSpinner'].Value = int(viewCount)
					itm['MediaFormatCombo'].CurrentText = "R3D"
					# Sensor Frame Rate
					sensorfps = GetJSONConfigViews(jsonCameraConfigFile, "sensorfps")
					# print(fps)
					if sensorfps == "24 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "24 FPS"
					elif sensorfps == "25 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "25 FPS"
					elif sensorfps == "30 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "30 FPS"
					elif sensorfps == "48 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "48 FPS"
					elif sensorfps == "50 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "50 FPS"
					elif sensorfps == "60 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "60 FPS"
					elif sensorfps == "90 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "90 FPS"
					elif sensorfps == "100 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "100 FPS"
					elif sensorfps == "120 FPS":
						itm['SensorFrameRateCombo'].CurrentText = "120 FPS"
					else:
						# Fallback FPS rate
						itm['SensorFrameRateCombo'].CurrentText = "Custom"
						itm["SensorFrameRateCustomSpinner"].Value = fps
					# Project Frame Rate
					projectfps = GetJSONConfigViews(jsonCameraConfigFile, "projectfps")
					# print(fps)
					if projectfps == "24 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "24 FPS"
					elif projectfps == "25 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "25 FPS"
					elif projectfps == "30 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "30 FPS"
					elif projectfps == "48 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "48 FPS"
					elif projectfps == "50 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "50 FPS"
					elif projectfps == "60 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "60 FPS"
					elif projectfps == "90 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "90 FPS"
					elif projectfps == "100 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "100 FPS"
					elif projectfps == "120 FPS":
						itm['ProjectFrameRateCombo'].CurrentText = "120 FPS"
					else:
						# Fallback FPS rate
						itm['ProjectFrameRateCombo'].CurrentText = "Custom"
						itm["ProjectFrameRateCustomSpinner"].Value = fps
					
					itm["ProgressLabel"].Text = "  Progress: Loaded Settings for a \"" + str(itm["CameraArrayGeometryCombo"].CurrentText) + "\" camera array to use JSON sourced data"
				else:
					print("[Lightfielder][Preferences] A JSON File does not exist at this filepath.")
					itm["ProgressLabel"].Text = "  Progress: A JSON File does not exist at this filepath"
			else:
				itm['NumberOfCamerasSpinner'].Value = 55
				itm['MediaFormatCombo'].CurrentText = "R3D"
				itm['SensorFrameRateCombo'].CurrentText = "60 FPS"
				itm['ProjectFrameRateCombo'].CurrentText = "60 FPS"
				itm["SensorFrameRateCustomSpinner"].Value = 60
				itm["ProjectFrameRateCustomSpinner"].Value = 60
				itm["ProgressLabel"].Text = "  Progress: Loading Settings for \"" + str(itm["CameraArrayGeometryCombo"].CurrentText) + "\" to use the defaults"
		dlg.On.LoadSettingsButton.Clicked = LoadSettingsButtonFunc

		def AutoloadToolbarOnLaunchCheckboxFunc(ev):
			print("[Lightfielder][Preferences] Autoload Toolbar On Launch Updated: " + str(itm["AutoloadToolbarOnLaunchCheckbox"].Checked))
			itm["ProgressLabel"].Text = "  Progress: Updated \"Autoload Toolbar On Launch\" to " + str(itm["AutoloadToolbarOnLaunchCheckbox"].Checked)
		dlg.On.AutoloadToolbarOnLaunchCheckbox.Clicked = AutoloadToolbarOnLaunchCheckboxFunc

		def RTFMTooltipsCheckboxFunc(ev):
			print("[Lightfielder][Preferences] RTFM Tooltips Updated: " + str(itm["RTFMTooltipsCheckbox"].Checked))
			PrefSave(dlg)

			# Write the preferences to disk
			app.SavePrefs()
			
			itm["ProgressLabel"].Text = "  Progress: Updated \"RTFM Tooltips\" to " + str(itm["RTFMTooltipsCheckbox"].Checked)
		dlg.On.RTFMTooltipsCheckbox.Clicked = RTFMTooltipsCheckboxFunc

		def UseLocalHelpCheckboxFunc(ev):
			print("[Lightfielder][Preferences] Use Local Help Setting Updated")
			PrefSave(dlg)

			# Write the preferences to disk
			app.SavePrefs()

			itm["ProgressLabel"].Text = "  Progress: Updated \"Use Local Help\""
		dlg.On.UseLocalHelpCheckbox.Clicked = UseLocalHelpCheckboxFunc

		def FuzzyR3DDateMatchingCheckboxFunc(ev):
			print("[Lightfielder][Preferences] Updated \"Fuzzy R3D Date Matching\"")
			PrefSave(dlg)

			# Write the preferences to disk
			app.SavePrefs()

			itm["ProgressLabel"].Text = "  Progress: Updated \"Fuzzy R3D Date Matching\""
		dlg.On.FuzzyR3DDateMatchingCheckbox.Clicked = FuzzyR3DDateMatchingCheckboxFunc
		
		def WindowStaysOnTopCheckboxFunc(ev):
			print("[Lightfielder][Preferences] Script Window Stays On Top Updated to " + str(itm["WindowStaysOnTopCheckbox"].Checked))
			PrefSave(dlg)
			
			# Write the preferences to disk
			app.SavePrefs()

			# Should this window float above all other views -- "WindowStaysOnTopHint
			# print("[Window Attrs]", dlg.WindowFlags)
			# dlg.WindowFlags["WindowStaysOnTopHint"]= itm["WindowStaysOnTopCheckbox"].Checked

			itm["ProgressLabel"].Text = "  Progress: Updated \"Script Window Stays On Top\" to " + str(itm["WindowStaysOnTopCheckbox"].Checked)
		dlg.On.WindowStaysOnTopCheckbox.Clicked = WindowStaysOnTopCheckboxFunc

		def PlayUserInterfacesSoundEffectsCheckboxFunc(ev):
			print("[Lightfielder][Preferences] Play User Interface Sound Effects Checkbox: " + str(itm["PlayUserInterfacesSoundEffectsCheckbox"].Checked))
			if itm["PlayUserInterfacesSoundEffectsCheckbox"].Checked == False:
				# Sound is OFF
				itm["SoundEffectsVolumeLabel"].Visible = False
				itm["SoundEffectsVolumeSlider"].Visible = False
				itm["SoundEffectsVolumeNumberLabel"].Visible = False
				itm["HelpGroupSoundEffects2"].Visible = False
				itm["SoundEffectsErrorButton"].Visible = False
				itm["SoundEffectsErrorCombo"].Visible = False
				itm["SoundEffectsCompleteButton"].Visible = False
				itm["SoundEffectsCompleteCombo"].Visible = False
			else:
				# Sound is ON
				itm["SoundEffectsVolumeLabel"].Visible = True
				itm["SoundEffectsVolumeSlider"].Visible = True
				itm["SoundEffectsVolumeNumberLabel"].Visible = True
				itm["HelpGroupSoundEffects2"].Visible = True
				itm["SoundEffectsErrorButton"].Visible = True
				itm["SoundEffectsErrorCombo"].Visible = True
				itm["SoundEffectsCompleteButton"].Visible = True
				itm["SoundEffectsCompleteCombo"].Visible = True

			itm["ProgressLabel"].Text = "  Progress: Updated \"Play User Interface Sound Effects\" to " + str(itm["PlayUserInterfacesSoundEffectsCheckbox"].Checked)
		dlg.On.PlayUserInterfacesSoundEffectsCheckbox.Clicked = PlayUserInterfacesSoundEffectsCheckboxFunc

		def SoundEffectsVolumeSliderFunc(ev):
			print("[Lightfielder][Preferences] User Interface Sound Effects Volume: " + str(ev['Value']))

			volumestatus = ""
			# volumestatus = "(" + str(ev['Value']) + ")"
			if ev['Value'] == 0:
				# Muted Volume
				volumestatus += "🔇"
				itm["SoundEffectsVolumeNumberLabel"].ToolTip = "Muted"
			elif ev['Value'] <= 3:
				# Low Volume
				volumestatus += "🔈"
				itm["SoundEffectsVolumeNumberLabel"].ToolTip = "Low Volume"
			elif ev['Value'] >= 11:
				# Spinal Tap Volume 11
				volumestatus += "🎸"
				itm["SoundEffectsVolumeNumberLabel"].ToolTip = "Spinal Tap Volume - It goes all the way to 11!"
			elif ev['Value'] >= 7:
				# High Volume
				volumestatus += "🔊"
				itm["SoundEffectsVolumeNumberLabel"].ToolTip = "High Volume"
			else:
				# Medium Volume
				volumestatus += "🔉"
				itm["SoundEffectsVolumeNumberLabel"].ToolTip = "Medium Volume"
			itm["SoundEffectsVolumeNumberLabel"].Text = volumestatus
			# itm["ProgressLabel"].Text = "  Progress: Updated \"Sound Effects Volume\" to "  + str(ev['Value']) + " - " + str(itm["SoundEffectsVolumeNumberLabel"].ToolTip)
			# itm["ProgressLabel"].Text = "  Progress: Updated \"Sound Effects Volume\" to "  + str(ev['Value'])

			# Save the pref
			PrefSave(dlg)
		dlg.On.SoundEffectsVolumeSlider.ValueChanged = SoundEffectsVolumeSliderFunc

		def SoundEffectsErrorComboFunc(ev):
			print("[Lightfielder][Preferences][Event][On Error Sound] " + str(itm["SoundEffectsErrorCombo"].CurrentText))
			# itm["ProgressLabel"].Text = "  Progress: Updated Event \"On Error Sound\" to \"" + str(itm["SoundEffectsErrorCombo"].CurrentText) + "\""
		dlg.On.SoundEffectsErrorCombo.CurrentIndexChanged = SoundEffectsErrorComboFunc

		def SoundEffectsCompleteComboFunc(ev):
			print("[Lightfielder][Preferences][Event][Task Complete Sound] " + str(itm["SoundEffectsCompleteCombo"].CurrentText))
			# itm["ProgressLabel"].Text = "  Progress: Updated Event \"Task Complete Sound\" to \"" + str(itm["SoundEffectsErrorCombo"].CurrentText) + "\""
		dlg.On.SoundEffectsCompleteCombo.CurrentIndexChanged = SoundEffectsCompleteComboFunc

		def SoundEffectsErrorButtonFunc(ev):
			soundName = itm["SoundEffectsErrorCombo"].CurrentText

			print("[Lightfielder][Preferences][Sound Preview][Event] On Error [Sound] " + str(soundName))
			SoundEffectSelect(soundName)
		dlg.On.SoundEffectsErrorButton.Clicked = SoundEffectsErrorButtonFunc

		def SoundEffectsCompleteButtonFunc(ev):
			soundName = itm["SoundEffectsCompleteCombo"].CurrentText

			print("[Lightfielder][Preferences][Sound Preview][Event] Task Complete [Sound] " + str(soundName))
			SoundEffectSelect(soundName)
		dlg.On.SoundEffectsCompleteButton.Clicked = SoundEffectsCompleteButtonFunc

		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool1", "Tool22")

			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool1", "Tool2")

			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		# Click on the Active Toolbar Preset label to open the JSON preset in an external editor, or open the containing folder in the operating system's folder browsing view
		def ShowToolbarPresetButtonFunc(ev):
			buttonModifier = ev["modifiers"]["ShiftModifier"]
			buttonModifierControl = ev["modifiers"]["ControlModifier"]
			jsonFilename = str(presetsBasePath) + str(itm["ToolbarCombo"].CurrentText) + str(".json")

			if buttonModifier == True:
				# shift was held down so open the OS default program for this filetype
				 ShowInDefaultProgram(jsonFilename)
				 itm["ProgressLabel"].Text = "  Progress: Open the \"Toolbar Preset\" JSON file \"" + str(itm["ToolbarCombo"].CurrentText)+ str(".json") + "\""
			elif buttonModifierControl == True:
				# Command/Control was held down so open the programmer's text editor
				ExternalEditor(jsonFilename)
				itm["ProgressLabel"].Text = "  Progress: Edit the \"Toolbar Preset\" JSON file \"" + str(itm["ToolbarCombo"].CurrentText)+ str(".json") + "\""
			else:
				# Label was clicked on with no modifier keys so open the containing folder in the operating system's folder browsing view
				ShowFolderFromFilepath(app.MapPath(presetsBasePath))
				itm["ProgressLabel"].Text = "  Progress: Show the \"Toolbar Preset\" file containing folder"
		dlg.On.ShowToolbarPresetButton.Clicked = ShowToolbarPresetButtonFunc

		def ToolbarSettingsButtonFunc(ev):
			print("[Lightfielder][Toolbar Settings][Button]")
		dlg.On.ToolbarSettingsButton.Clicked = ToolbarSettingsButtonFunc

		def ToolbarComboFunc(ev):
			jsonFilename = str(presetsBasePath) + str(itm["ToolbarCombo"].CurrentText) + str(".json")
			print("[Lightfielder][Toolbar Preset][Refresh] " + str(itm["ToolbarCombo"].CurrentText) + str(".json"))
			
			# Import the JSON preset file
			try:
				with open(jsonFilename, "r") as f:
					# Todo: Add a try element to catch JSON formatting errors in the presets when they are json.load() accessed.
					data = json.load(f)
					# print(data)
					w = data["width"]
					h = data["height"]
					itm["WindowLayoutHorizontalSpinner"].Value = w
					itm["WindowLayoutVerticalSpinner"].Value = h
			except OSError as error:
				print("\t[Lightfielder][Exception][JSON Get Error]", error)
				itm["WindowLayoutHorizontalSpinner"].Value = 10
				itm["WindowLayoutVerticalSpinner"].Value = 2
			
			# itm["ProgressLabel"].Text = "  Progress: Updated Toolbar Preset to \"" + str(itm["ToolbarCombo"].CurrentText) + "\""
		dlg.On.ToolbarCombo.CurrentIndexChanged = ToolbarComboFunc

		def ToolbarLayoutButtonFunc(ev):
			jsonFilename = str(presetsBasePath) + str(itm["ToolbarCombo"].CurrentText) + str(".json")
			print("[Lightfielder][[Toolbar Preset]][Reset the Window Layout] Using: " + str(itm["ToolbarCombo"].CurrentText))
			itm["ProgressLabel"].Text = "  Progress: Reset the Toolbar window layout to \"" + str(itm["ToolbarCombo"].CurrentText) + "\""

			# Import the JSON preset file
			try:
				with open(jsonFilename, "r") as f:
					# Todo: Add a try element to catch JSON formatting errors in the presets when they are json.load() accessed.
					data = json.load(f)
					print(data)
					w = data["width"]
					h = data["height"]
					itm["WindowLayoutHorizontalSpinner"].Value = w
					itm["WindowLayoutVerticalSpinner"].Value = h
			except OSError as error:
				print("\t[Lightfielder][Exception][JSON Get Error]", error)
				itm["WindowLayoutHorizontalSpinner"].Value = 10
				itm["WindowLayoutVerticalSpinner"].Value = 2
		dlg.On.ToolbarLayoutButton.Clicked = ToolbarLayoutButtonFunc

		# Add the items to the Presets ComboBox menu
		if len(os.listdir(presetsBasePath)) == 0:
			# Make a default preset
			CreateDefaultJSON()
		for file in sorted(os.listdir(presetsBasePath)):
			if file.endswith(".json") and not file.startswith("."):
				#presetFile = file.rstrip(".json")
				presetFile = file.replace(".json", "")
				itm["ToolbarCombo"].AddItem(presetFile)
				# print(presetFile)

		# Select the default bin preset item
		itm["ToolbarCombo"].CurrentText = "Toolbar_Default"

		# def ToolbarComboFunc(ev):
		# dlg.On.ToolbarCombo.CurrentIndexChanged = ToolbarComboFunc

		def AddPresetButtonFunc(ev):
			# Toolbar folders
			toolbarItems = {}
			for i in range(1, 21):
				num_str = f"{i:02d}"
				toolbarItems[f"Tool{i}"] = {
					"Icon": "fa-file-code-o",
					"ScriptFile": f"",
					"TargetID": "",
					"Text": num_str,
					"Tooltip": f"{num_str}",
				}
			# print(toolbarItems)

			# Get the preset name
			presetString = str(SavePresetWindow())
			if presetString != "":
				jsonName = "Toolbar_" + str(presetString)
				print("[Lightfielder][Toolbar][Add Preset] " + str(jsonName))

				jsonData = {
					"version": 1,
					"width": int(itm["WindowLayoutHorizontalSpinner"].Value),
					"height": int(itm["WindowLayoutVerticalSpinner"].Value),
					"Toolbar": toolbarItems
				}

				# Export the JSON to disk
				SetJSON(jsonName, jsonData)

				# Add the new entry to the preset combo menu
				itm["ToolbarCombo"].AddItem(jsonName)

				print("[Lightfielder][Edit] Lightfielder Python Module")
				# This feature requires the "xdg-open" package to be installed on Linux.
				ExternalEditor(str("Scripts:/Utility/Lightfielder/Presets/Toolbars/") + str(jsonName) + str(".json"))
		dlg.On.AddPresetButton.Clicked = AddPresetButtonFunc

		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.PrefsWin.Geometry")

		# Load the prefs
		PrefLoad(dlg)

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('PrefsWin', {
			Target {
				ID = 'PrefsWin',
			},
			Hotkeys {
				Target = 'PrefsWin',
				Defaults = true,

				CONTROL_W = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
				CONTROL_F4 = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
				ESCAPE = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
			},
		})
		""")

		dlg.Show()
		disp.RunLoop()
		dlg.Hide()

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.PrefsWin.Geometry")

		# Save the prefs
		PrefSave(dlg)

if __name__ == "__main__":
	CreatePrefsWindow()
