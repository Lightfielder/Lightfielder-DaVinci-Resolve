"""
Lightfielder 14 Grade Automation.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

The Grade Automation view allows you to apply CDL/DRX/LUT grades to the multi-view clips in a timeline.

Script Usage:
1. Open a Resolve Edit page based timeline. Select the menu item: "Workspace > Scripts > Lightfielder > 14 Grade Automation".

2. Apply a combination of CDL, DRX, and LUT grades to your footage. When applying a CDL Grade, clicking the Offset/Slope/Power labels will reset the values. Clicking on individual "R", "G", or "B" channel labels will reset those specific channel values.

3. If you want to apply view-dependent grading changes, the "CCS" Camera Contact Sheet script can be used to target the specific camera views that will have grading operations applied to the clips.

4. Press the individual "Apply Grade" buttons in the user interface to see the results of your changes.


Create a New Preset:
1. You can create a new grading preset by pressing the "+" button. This will snapshot the active settings from the window and save it as a new preset.

2. A "Save Preset" dialog will appear that allows you to name the preset.

3. The preset is saved as a .json format document into the folder location:
$HOME/Lightfielder/Resolve/Scripts/Utility/Lightfielder/Presets/Grade/

If you want to delete a preset, simply remove the .json file from the presets folder.

The presets are saved as JSON formatted plain-text documents that can be viewed with a programmer's text editor. Each grade preset is entered on its own line. Number values are entered directly, while values like file paths are wrapped in double quotes.

"""

from pprint import pprint
from collections import defaultdict
import json, os
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

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
				#"StyleSheet": "background-color: rgb(37, 37, 37);",
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
			ui.VGap(10),
			ui.HGroup({"Weight": 0.0,},[
				ui.Button({
					"ID": "CloseButton",
					"Text": "Cancel",
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

	preset_itm = preset_dlg.GetItems()

	def PrefSave(winDlg):
		# Save the prefs
		if winDlg != None:
			print("[Lightfielder][Preferences] Saved")
			#print(app.GetData("Lightfielder"))

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


def CreateGradeWindow():
	presetsBasePath = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Grade/")

	def GetJSON(presetName):
		presetAbsPath = presetsBasePath + str(presetName) + ".json"
		#print("[Grade Preset] " + str(presetName))

		# Import the JSON preset file
		try:
			with open(presetAbsPath, "r") as f:
				# Todo: Add a try element to catch JSON formatting errors in the presets when they are json.load() accessed.
				jsonStr = json.load(f)
				return jsonStr
		except OSError as error:
			print("\t[Lightfielder][JSON Get Error]", error)
			return {
				"version": 1,
				"grade": [
				]
			}

	def SetJSON(presetName, data):
		presetAbsPath = presetsBasePath + str(presetName) + ".json"
		#print("[Grade Preset] " + str(presetName))

		# Export the JSON preset file
		try:
			with open(presetAbsPath, "w") as f:
				# Todo: Add a try element to catch JSON formatting errors in the presets
				# json.dump(data, f, ensure_ascii = True, indent = 4, sort_keys = True)
				json.dump(data, f, ensure_ascii = True, indent = "\t")
				print("[Lightfielder][Grade][Save Preset] " + str(presetName))
		except OSError as error:
			print("\t[Lightfielder][Exception][JSON Save Error]", error)
			ErrorWindow("Grade", "JSON Save Error" + str(error))

	def CreateDefaultJSON():
		# Make a default preset
		#jsonData = {
		#	"version": 1.0,
		#	"grade":[
		#	]
		#}

		jsonData = {
			"version": 1,
			"grade": {
				"cdl": {
					"node": 1,
					"power": {
						"R": 1.0,
						"G": 1.0,
						"B": 1.0
					},
					"slope": {
						"R": 1.0,
						"G": 1.0,
						"B": 1.0
					},
					"offset": {
						"R": 0.0,
						"G": 0.0,
						"B": 0.0
					},
					"saturation": 1.0
				},
				"drx": {
					"file": ""
				},
				"lut": {
					"node": 1,
					"file": ""
				}
			}
		}

		SetJSON("Grade_Default", jsonData)

	# Create the intermediate directories on disk for the presets
	if not os.path.exists(presetsBasePath):
		try:
			# Make the dir
			os.makedirs(presetsBasePath)
			print("[Lightfielder][Grade][Make Directory]", presetsBasePath)

			# Make a default preset
			CreateDefaultJSON()
		except OSError as error:
			print("[Lightfielder][Grade][Make Directory Error]", error)
			ErrorWindow("Grade", "Make Directory Error" + str(error))

	# Get the project name
	project = GetProject()
	if project is None:
		print("[Lightfielder] No Resolve project is open at this time.")
		ErrorWindow("Lightfielder", "No Resolve project is open at this time.")
	else:
		projectName = project.GetName()
		projectSetting = project.GetSetting()

		# Get the timeline object
		timeline = GetTimeline()
		if timeline is None:
			print("[Lightfielder][Grade][Please open a Resolve timeline before running this script")
			ErrorWindow("Grade", "Please open a Resolve timeline before running this script")
		else:
			# Get the timeline name
			timelineName = timeline.GetName()
			#print("[Timeline Name] " + str(timelineName))

			# Get the timeline settings
			timelineSetting = timeline.GetSetting()

			# Get the track count
			timelineVideoTrackCount = timeline.GetTrackCount("video") + 1

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
				"ID": "GradeAutomationWin",
				"TargetID" : "GradeAutomationWin",
				"Geometry": [500, 50, 375, 780],
				"MinimumSize": [375, 780],
				"FixedSize": [375, 780],
				#"Spacing": 0,
				#"Margin": 5,
			},[
				ui.VGroup({
					"ID": "Content",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 1.0,
				},[
					ui.HGroup({
						"Weight": 0.5,
					},[
						ui.Label({
							"ID": "ViewLabel",
							"Text": "14 Grade Automation",
							"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
							"Margin": 0,
							"Spacing": 0,
							"Weight": 0.01,
						}),
						ui.HGap(20, 1),
						ui.Button({
							"ID": "HelpButton",
							"Flat": True,
							"ToolTip": "Show the help topic on GitHub",
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
					ui.HGroup({"ID": "row", "Weight": 0.01,},[
						ui.Button({
							"ID": "ShowPresetButton",
							"Flat": True,
							"MinimumSize": [45, 32],
							"Text": "Preset",
							"ToolTip": "Clicking this text label will open the base folder where the Preset file \nis located in a desktop folder browsing window.",
							"Weight": 0.01,
						}),
						ui.ComboBox({
							"ID": "PresetCombo",
							"Text": "Preset",
							"Weight": 1.0,
						}),
						ui.Button({"ID": "AddPresetButton", "Text": "+", "MinimumSize": [32, 32], "Weight": 0.1}),
					]),
					ui.VGroup({
						"Weight": 0.1,
						"ID": "ColorTab",
					},[
						ui.VGroup({
							"Weight": 0.1,
						},[
							ui.HGroup({},[
								ui.Label({
									"ID": "ViewLabel",
									"Text": "  CDL Grade All Clips",
									"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
									"Margin": 0,
									"Spacing": 0,
									"Weight": 0.01,
								}),
							]),
							ui.Label({
								"ID": "DividerLabel",
								"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
								"Spacing": 0,
								"Margin": 0,
								"Weight": 0.01,
							}),
						]),
						ui.HGroup({
							"Weight": 1.0,
						},[
							ui.Label({"ID": "NodeIndexLabel", "Text": "Node Index", "Weight": 0.1, "MinimumSize": [80, 32],}),
							ui.SpinBox({
								"ID": "CDLNodeIndexSpinner",
								"Minimum": 1,
								"Maximum": 99999,
								"Value": 1.0,
								"MinimumSize": [54, 32],
								"Weight": 1.0,
							}),
						]),
						ui.HGroup({
							"Weight": 1.0,
						},[
							ui.VGroup({
								"Weight": 1.0,
							},[
								ui.Button({
									"ID": "OffsetButton",
									"Flat": True,
									"MinimumSize": [60, 32],
									"Text": "Offset",
									"Weight": 0.01,
								}),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "OffsetRButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "R",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "OffsetRSpinner",
										"Minimum": -10,
										"Maximum": 10,
										"Value": 0.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "OffsetGButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "G",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "OffsetGSpinner",
										"Minimum": -10,
										"Maximum": 10,
										"Value": 0.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "OffsetBButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "B",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "OffsetBSpinner",
										"Minimum": -10,
										"Maximum": 10,
										"Value": 0.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
							]),
							ui.VGroup({
								"Weight": 1.0,
							},[
								ui.Button({
									"ID": "SlopeButton",
									"Flat": True,
									"MinimumSize": [60, 32],
									"Text": "Slope",
									"Weight": 0.01,
								}),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "SlopeRButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "R",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "SlopeRSpinner",
										"Minimum": 0,
										"Maximum": 10,
										"Value": 1.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "SlopeGButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "G",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "SlopeGSpinner",
										"Minimum": 0,
										"Maximum": 10,
										"Value": 1.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "SlopeBButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "B",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "SlopeBSpinner",
										"Minimum": 0,
										"Maximum": 10,
										"Value": 1.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
							]),
							#ui.VGap(),
							ui.VGroup({
								"Weight": 1.0,
							},[
								ui.Button({
									"ID": "PowerButton",
									"Flat": True,
									"MinimumSize": [16, 32],
									"Text": "Power",
									"Weight": 0.01,
								}),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "PowerRButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "R",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "PowerRSpinner",
										"Minimum": 0,
										"Maximum": 10,
										"Value": 1.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "PowerGButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "G",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "PowerGSpinner",
										"Minimum": 0,
										"Maximum": 10,
										"Value": 1.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
								ui.HGroup({
									"Weight": 1.0,
								},[
									ui.Button({
										"ID": "PowerBButton",
										"Flat": True,
										"MinimumSize": [16, 32],
										"Text": "B",
										"Weight": 0.01,
									}),
									ui.DoubleSpinBox({
										"ID": "PowerBSpinner",
										"Minimum": 0,
										"Maximum": 10,
										"Value": 1.0,
										"SingleStep": 0.1,
										"MinimumSize": [54, 32],
										"Weight": 1.0,
									}),
								]),
							]),
						]),
						ui.HGroup({
							"Weight": 1.0,
						},[
							ui.Button({
									"ID": "SaturationButton",
									"Flat": True,
									"MinimumSize": [80, 32],
									"Text": "Saturation",
									"Weight": 0.01,
								}),
							ui.DoubleSpinBox({
								"ID": "SaturationSpinner",
								"Minimum": 0,
								"Maximum": 10,
								"Value": 1.0,
								"SingleStep": 0.1,
								"MinimumSize": [54, 32],
								"Weight": 1.0,
							}),
						]),
						#ui.VGap(),
						ui.HGroup({"Weight": 0.1},[
							ui.Button({"ID": "ResetCDLGradeButton", "Text": "Reset", "Geometry": [0, 0, 30, 50], "Weight": 0.1}),
							ui.HGap(20, 1),
							ui.Button({"ID": "ApplyCDLGradeButton", "Text": "Apply Grade", "Geometry": [0, 0, 30, 50], "Weight": 0.1}),
						]),
						ui.VGroup({
							"Weight": 0.1,
						},[
							ui.HGroup({},[
								ui.Label({
									"ID": "ViewLabel",
									"Text": "  DRX Grade All Clips",
									"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
									"Weight": 0.01,
								}),
							]),
							ui.Label({
								"ID": "DividerLabel",
								"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
								"Spacing": 0,
								"Margin": 0,
								"Weight": 0.01,
							}),
						]),
						ui.HGroup({
							"Weight": 1.0,
						},[
							ui.Label({"ID": "GradeModeLabel", "Text": "Grade Mode", "Weight": 0.1, "MinimumSize": [80, 32],}),
							ui.ComboBox({"ID": "GradeModeCombo", "Text": "Grade Mode", "Weight": 0.9}),
						]),
						ui.HGroup({
							"Weight": 1.0,
						},[
							ui.Button({
								"ID": "ShowGradeModeButton",
								"Flat": True,
								"MinimumSize": [80, 32],
								"Text": "Filename",
								"Weight": 0.01,
							}),
							ui.LineEdit({"ID": "DRXFileLineTxt", "Text": "", "PlaceholderText": "Please enter a .drx filepath.", "Weight": 0.9}),
							ui.Button({"ID": "BrowseDRXButton", "Text": "Browse", "Geometry": [0, 0, 30, 50], "Weight": 0.1}),
						]),
						ui.HGroup({"Weight": 0.1},[
							ui.HGap(20, 1),
							ui.Button({"ID": "ApplyDRXGradeButton", "Text": "Apply Grade", "Geometry": [0, 0, 30, 50], "Weight": 0.1}),
						]),
						ui.VGroup({
							"Weight": 0.1,
						},[
							ui.HGroup({},[
								ui.Label({
									"ID": "ViewLabel",
									"Text": "  LUT Grade All Clips",
									"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
									"Weight": 0.01,
								}),
							]),
							ui.Label({
								"ID": "DividerLabel",
								"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
								"Spacing": 0,
								"Margin": 0,
								"Weight": 0.01,
							}),
						]),
						ui.HGroup({
							"Weight": 0.1,
						},[
							ui.Label({"ID": "NodeIndexLabel", "Text": "Node Index", "Weight": 0.1, "MinimumSize": [80, 32],}),
							ui.SpinBox({
								"ID": "LUTNodeIndexSpinner",
								"Minimum": 1,
								"Maximum": 99999,
								"Value": 1.0,
								"MinimumSize": [54, 32],
								"Weight": 1.0,
							}),
						]),
						ui.HGroup({
							"Weight": 1.0,
						},[
							ui.Button({
								"ID": "ShowLUTFileButton",
								"Flat": True,
								"MinimumSize": [80, 32],
								"Text": "Filename",
								"Weight": 0.01,
							}),
							ui.LineEdit({"ID": "LUTFileLineTxt", "Text": "", "PlaceholderText": "Please enter a LUT filepath.", "Weight": 0.9}),
							ui.Button({"ID": "BrowseLUTButton", "Text": "Browse", "Geometry": [0, 0, 30, 50], "Weight": 0.1}),
						]),
						ui.HGroup({
							"Weight": 0.1
						},[
							ui.HGap(20, 1),
							ui.Button({
								"ID": "ApplyLUTGradeButton",
								"Text": "Apply Grade",
								"Weight": 0.5
							}),
						]),
						ui.VGroup({
							"Weight": 0.1
						},[
							ui.Label({
								"ID": "DividerLabel",
								"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
								"Spacing": 0,
								"Margin": 0,
								"Weight": 0.01,
							}),
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
						]),
						ui.HGroup({
							"Weight": 0.1
						},[
							ui.Button({
								"ID": "CloseButton",
								"Text": "Close",
								"Weight": 0.5
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
								"ToolTip": "Open the previous script from the Lightfielder Toolbar",
								"MinimumSize": [32, 32],
								"Weight": 0.01
							}),
							ui.Button({
								"ID": "NextScriptButton",
								"Text": ">",
								"ToolTip": "Open the next script from the Lightfielder Toolbar",
								"MinimumSize": [32, 32],
								"Weight": 0.01
							}),
						]),
					]),
				]),
			])

			itm = dlg.GetItems()

			itm["PresetCombo"].AddItem("Active Grade")

			# Add the items to the Presets ComboBox menu
			if len(os.listdir(presetsBasePath)) == 0:
				# Make a default preset
				CreateDefaultJSON()
			for file in sorted(os.listdir(presetsBasePath)):
				if file.endswith(".json") and not file.startswith("."):
					#presetFile = file.rstrip(".json")
					presetFile = file.replace(".json", "")
					itm["PresetCombo"].AddItem(presetFile)
					# print(presetFile)

			# Grade Mode ComboBox
			itm["GradeModeCombo"].AddItem("No keyframes")
			itm["GradeModeCombo"].AddItem("Source Timecode aligned")
			itm["GradeModeCombo"].AddItem("Start Frames aligned")

			# Resize the window
			dlg.RecalcLayout()
		
			def PrefSave(winDlg):
				# Save the prefs
				if winDlg != None:
					print("[Lightfielder][Preferences] Saved")
					#print(app.GetData("Lightfielder"))
		
			def PrefLoad(winDlg):
				# Restore the prefs
				if winDlg != None:
					print("[Lightfielder][Preferences] Loaded")
					# print(app.GetData("Lightfielder"))

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
	
				# Toggle the Toolbar button to the unpressed (off) state
				UnpressToolbarButton(dlg.ID, False)

				# Save the window preferences
				WindowPrefSave(dlg, "Lightfielder.GradeAutomationWin.Geometry")
			dlg.On.GradeAutomationWin.Hide = HideFunc

			# The window was closed
			def CloseFunc(ev):
				print("[Lightfielder][Window][Closed]")

				# Toggle the Toolbar button to the unpressed (off) state
				UnpressToolbarButton(dlg.ID, False)

				# Save the window preferences
				WindowPrefSave(dlg, "Lightfielder.GradeAutomationWin.Geometry")

				# Reset the progress caption
				itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

				disp.ExitLoop()
			dlg.On.GradeAutomationWin.Close = CloseFunc

			def CloseButtonFunc(ev):
				print("[Lightfielder][Window][Close Button]")
		
				# Toggle the Toolbar button to the unpressed (off) state
				UnpressToolbarButton(dlg.ID, False)

				# Save the window preferences
				WindowPrefSave(dlg, "Lightfielder.GradeAutomationWin.Geometry")

				# Reset the progress caption
				itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

				disp.ExitLoop()
			dlg.On.CloseButton.Clicked = CloseButtonFunc

			def SaveButtonFunc(ev):
				print("[Lightfielder][Preferences][Save Button]")
	
				# Save the window preferences
				WindowPrefSave(dlg, "Lightfielder.PrefsWin.Geometry")
	
				# Save the pref
				PrefSave(dlg)

				# Reset the progress caption
				itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
			dlg.On.SaveButton.Clicked = SaveButtonFunc

			def AddPresetButtonFunc(ev):
				# Get the preset name
				presetString = str(SavePresetWindow())
				if presetString != "":
					jsonName = "Grade_" + str(presetString)
					print("[Lightfielder][Grade][Add Preset] " + str(jsonName))

					grdeItems = GradeSettings()

					jsonData = {
						"version": 1,
						"grade": grdeItems
					}

					# Export the JSON to disk
					SetJSON(jsonName, jsonData)

					# Add the new entry to the preset combo menu
					itm["PresetCombo"].AddItem(jsonName)
			dlg.On.AddPresetButton.Clicked = AddPresetButtonFunc

			def GradeSettings():
				gradeDict = {}
				gradeDict["cdl"] = {}
				gradeDict["cdl"]["node"] = itm["CDLNodeIndexSpinner"].Value

				gradeDict["cdl"]["power"] =  {}
				gradeDict["cdl"]["power"]["R"] = itm["PowerRSpinner"].Value
				gradeDict["cdl"]["power"]["G"] = itm["PowerGSpinner"].Value
				gradeDict["cdl"]["power"]["B"] = itm["PowerBSpinner"].Value

				gradeDict["cdl"]["slope"] =  {}
				gradeDict["cdl"]["slope"]["R"] = itm["SlopeRSpinner"].Value
				gradeDict["cdl"]["slope"]["G"] = itm["SlopeGSpinner"].Value
				gradeDict["cdl"]["slope"]["B"] = itm["SlopeBSpinner"].Value

				gradeDict["cdl"]["offset"] = {}
				gradeDict["cdl"]["offset"]["R"] = itm["OffsetRSpinner"].Value
				gradeDict["cdl"]["offset"]["G"] = itm["OffsetGSpinner"].Value
				gradeDict["cdl"]["offset"]["B"] = itm["OffsetBSpinner"].Value

				gradeDict["cdl"]["saturation"] = itm["SaturationSpinner"].Value

				gradeDict["drx"] = {}
				gradeDict["drx"]["file"] = itm["DRXFileLineTxt"].Text

				gradeDict["lut"] = {}
				gradeDict["lut"]["node"] = itm["LUTNodeIndexSpinner"].Value
				gradeDict["lut"]["file"] = itm["LUTFileLineTxt"].Text

				return gradeDict

			def PresetComboFunc(ev):
				# Read the current preset ComboMenu entry
				presetName = itm["PresetCombo"].CurrentText
				if (presetName != "") and (presetName != "Active Grade"):
					# The preset is defining the layout
					data = GetJSON(presetName)
					gradeItems = data["grade"]
					#print(gradeItems)
					if "cdl" in gradeItems:
						if "node" in gradeItems["cdl"]:
							itm["CDLNodeIndexSpinner"].Value = gradeItems["cdl"]["node"]
						if "power" in gradeItems["cdl"]:
							if gradeItems["cdl"]["power"]:
								itm["PowerRSpinner"].Value = gradeItems["cdl"]["power"]["R"]
								itm["PowerGSpinner"].Value = gradeItems["cdl"]["power"]["G"]
								itm["PowerBSpinner"].Value = gradeItems["cdl"]["power"]["B"]
						if "slope" in gradeItems["cdl"]:
							if gradeItems["cdl"]["slope"]:
								itm["SlopeRSpinner"].Value = gradeItems["cdl"]["slope"]["R"]
								itm["SlopeGSpinner"].Value = gradeItems["cdl"]["slope"]["G"]
								itm["SlopeBSpinner"].Value = gradeItems["cdl"]["slope"]["B"]
						if "offset" in gradeItems["cdl"]:
							if gradeItems["cdl"]["offset"]:
								itm["OffsetRSpinner"].Value = gradeItems["cdl"]["offset"]["R"]
								itm["OffsetGSpinner"].Value = gradeItems["cdl"]["offset"]["G"]
								itm["OffsetBSpinner"].Value = gradeItems["cdl"]["offset"]["B"]
						if "saturation" in gradeItems["cdl"]:
							itm["SaturationSpinner"].Value = gradeItems["cdl"]["saturation"]
					if "drx" in gradeItems:
						if "file" in gradeItems["drx"]:
							itm["DRXFileLineTxt"].Text = gradeItems["drx"]["file"]
					if "lut" in gradeItems:
						if "node" in gradeItems["lut"]:
							itm["LUTNodeIndexSpinner"].Value = gradeItems["lut"]["node"]
						if "file" in gradeItems["lut"]:
							itm["LUTFileLineTxt"].Text = gradeItems["lut"]["file"]
			dlg.On.PresetCombo.CurrentIndexChanged = PresetComboFunc

			# =====================================================
			# Top Navbar
			def NavigationButtonFunc(ev):
				itm["ColorButton"].Checked = False
				itm["EditButton"].Checked = False
			dlg.On.NavigationButton.Clicked = NavigationButtonFunc

			def EditButtonFunc(ev):
				itm["ColorButton"].Checked = False
				itm["NavigationButton"].Checked = False
			dlg.On.EditButton.Clicked = EditButtonFunc

			def ColorButtonFunc(ev):
				itm["NavigationButton"].Checked = False
				itm["EditButton"].Checked = False
			dlg.On.ColorButton.Clicked = ColorButtonFunc

			def ToolbarCollapseButtonFunc(ev):
				# Collapse
				if itm["ToolbarCollapseButton"].Text == "˄":
					itm["ToolbarCollapseButton"].Text = "˅"

					itm["ColorButton"].Checked = False
					itm["NavigationButton"].Checked = False
					itm["EditButton"].Checked = False
				else:
					itm["ToolbarCollapseButton"].Text = "˄"
			dlg.On.ToolbarCollapseButton.Clicked = ToolbarCollapseButtonFunc


			# =====================================================
			# CDL Grade All Clips
			def ApplyCDLGradeButtonFunc(ev):
				# UI Values
				nodeIndexStr = str(itm["CDLNodeIndexSpinner"].Value)

				powerR = round(itm["PowerRSpinner"].Value, 3)
				powerG = round(itm["PowerGSpinner"].Value, 3)
				powerB = round(itm["PowerBSpinner"].Value, 3)
				powerStr = str(powerR) + " " + str(powerG) + " " + str(powerB)

				slopeR = round(itm["SlopeRSpinner"].Value, 3)
				slopeG = round(itm["SlopeGSpinner"].Value, 3)
				slopeB = round(itm["SlopeBSpinner"].Value, 3)
				slopeStr = str(slopeR) + " " + str(slopeG) + " " + str(slopeB)

				offsetR = round(itm["OffsetRSpinner"].Value, 3)
				offsetG = round(itm["OffsetGSpinner"].Value, 3)
				offsetB = round(itm["OffsetBSpinner"].Value, 3)
				offsetStr = str(offsetR) + " " + str(offsetG) + " " + str(offsetB)

				satStr = str(round(itm["SaturationSpinner"].Value, 3))
				print("[Lightfielder][Apply CDL Grade] [NodeIndex] \"" + nodeIndexStr + "\" [Slope] \"" + slopeStr + "\" [Offset] \"" + offsetStr + "\" [Power] \"" + powerStr + "\" [Saturation] \"" + satStr + "\"")
				itm["ProgressLabel"].Text = "  Progress: Apply CDL Grade"
				#itm["ProgressLabel"].Text = "  Progress: Apply CDL Grade using [NodeIndex] \"" + nodeIndexStr + "\" [Slope] \"" + slopeStr + "\" [Offset] \"" + offsetStr + "\" [Power] \"" + powerStr + "\" [Saturation] \"" + satStr + "\""

				# Get the timeline object
				timeline = GetTimeline()

				# Get the timeline name
				timelineName = timeline.GetName()
				#print("[Timeline Name] " + str(timelineName))

				# Get the timeline settings
				timelineSetting = timeline.GetSetting()

				# Get the track count
				timelineVideoTrackCount = timeline.GetTrackCount("video")

				# Get the track structure
				for i in range(int(timelineVideoTrackCount + 1)):
					if timeline.GetIsTrackEnabled("video", i) == True:
						# Get the clips in the track
						clips = timeline.GetItemListInTrack("video", i)
						for clip in clips:
							result = clip.SetCDL({"NodeIndex" : nodeIndexStr, "Slope" : slopeStr, "Offset" : offsetStr, "Power" : powerStr, "Saturation" : satStr})
			dlg.On.ApplyCDLGradeButton.Clicked = ApplyCDLGradeButtonFunc

			def SpinBoxFunc(ev):
				itm["PresetCombo"].CurrentText = "Active Grade"

			dlg.On.LUTNodeIndexSpinner.EditingFinished = SpinBoxFunc
			dlg.On.CDLNodeIndexSpinner.EditingFinished = SpinBoxFunc
			dlg.On.OffsetRSpinner.EditingFinished = SpinBoxFunc
			dlg.On.OffsetGSpinner.EditingFinished = SpinBoxFunc
			dlg.On.OffsetBSpinner.EditingFinished = SpinBoxFunc
			dlg.On.PowerRSpinner.EditingFinished = SpinBoxFunc
			dlg.On.PowerGSpinner.EditingFinished = SpinBoxFunc
			dlg.On.PowerBSpinner.EditingFinished = SpinBoxFunc
			dlg.On.SlopeRSpinner.EditingFinished = SpinBoxFunc
			dlg.On.SlopeGSpinner.EditingFinished = SpinBoxFunc
			dlg.On.SlopeBSpinner.EditingFinished = SpinBoxFunc

# 			dlg.On.LUTNodeIndexSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.CDLNodeIndexSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.OffsetRSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.OffsetGSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.OffsetBSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.PowerRSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.PowerGSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.PowerBSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.SlopeRSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.SlopeGSpinner.ValueChanged = SpinBoxFunc
# 			dlg.On.SlopeBSpinner.ValueChanged = SpinBoxFunc

			# Reset channels
			# Offset
			def OffsetButtonFunc(ev):
				itm["OffsetRSpinner"].Value = 0.0
				itm["OffsetGSpinner"].Value = 0.0
				itm["OffsetBSpinner"].Value = 0.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.OffsetButton.Clicked = OffsetButtonFunc

			def OffsetRButtonFunc(ev):
				itm["OffsetRSpinner"].Value = 0.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.OffsetRButton.Clicked = OffsetRButtonFunc

			def OffsetGButtonFunc(ev):
				itm["OffsetGSpinner"].Value = 0.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.OffsetGButton.Clicked = OffsetGButtonFunc

			def OffsetBButtonFunc(ev):
				itm["OffsetBSpinner"].Value = 0.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.OffsetBButton.Clicked = OffsetBButtonFunc

			# Power
			def PowerButtonFunc(ev):
				itm["PowerRSpinner"].Value = 1.0
				itm["PowerGSpinner"].Value = 1.0
				itm["PowerBSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.PowerButton.Clicked = PowerButtonFunc

			def PowerRButtonFunc(ev):
				itm["PowerRSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.PowerRButton.Clicked = PowerRButtonFunc

			def PowerGButtonFunc(ev):
				itm["PowerGSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.PowerGButton.Clicked = PowerGButtonFunc

			def PowerBButtonFunc(ev):
				itm["PowerBSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.PowerBButton.Clicked = PowerBButtonFunc

			# Slope
			def SlopeButtonFunc(ev):
				itm["SlopeRSpinner"].Value = 1.0
				itm["SlopeGSpinner"].Value = 1.0
				itm["SlopeBSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.SlopeButton.Clicked = SlopeButtonFunc

			def SlopeRButtonFunc(ev):
				itm["SlopeRSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.SlopeRButton.Clicked = SlopeRButtonFunc

			def SlopeGButtonFunc(ev):
				itm["SlopeGSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.SlopeGButton.Clicked = SlopeGButtonFunc

			def SlopeBButtonFunc(ev):
				itm["SlopeBSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.SlopeBButton.Clicked = SlopeBButtonFunc

			# Saturation
			def SaturationButtonFunc(ev):
				itm["SaturationSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.SaturationButton.Clicked = SaturationButtonFunc

			# Reset CDL
			def ResetCDLGradeButtonFunc(ev):
				itm["CDLNodeIndexSpinner"].Value = 1

				itm["PowerRSpinner"].Value = 1.0
				itm["PowerGSpinner"].Value = 1.0
				itm["PowerBSpinner"].Value = 1.0

				itm["SlopeRSpinner"].Value = 1.0
				itm["SlopeGSpinner"].Value = 1.0
				itm["SlopeBSpinner"].Value = 1.0

				itm["OffsetRSpinner"].Value = 0.0
				itm["OffsetGSpinner"].Value = 0.0
				itm["OffsetBSpinner"].Value = 0.0

				itm["SaturationSpinner"].Value = 1.0

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.ResetCDLGradeButton.Clicked = ResetCDLGradeButtonFunc

			def CDLCollapseButtonFunc(ev):
				# Collapse
				if itm["CDLCollapseButton"].Text == "˄":
					itm["CDLCollapseButton"].Text = "˅"
				else:
					itm["CDLCollapseButton"].Text = "˄"
			dlg.On.CDLCollapseButton.Clicked = CDLCollapseButtonFunc

			# =====================================================
			# DRX Grade All Clips
			def ApplyDRXGradeButtonButtonFunc(ev):
				# UI Values
				gradeMode = int(itm["GradeModeCombo"].CurrentIndex)
				filepath = str(app.MapPath(itm["DRXFileLineTxt"].Text or ""))
				print("[Lightfielder][Apply DRX Grade] [File] \"" + filepath + "\" [Grade Mode] " + str(gradeMode))
				itm["ProgressLabel"].Text = "  Progress: Apply DRX Grade using \"" + filepath + "\" [Grade Mode] " + str(gradeMode)

				# Get the timeline object
				timeline = GetTimeline()

				# Get the timeline name
				timelineName = timeline.GetName()
				# print("[Timeline Name] " + str(timelineName))

				# Get the timeline settings
				timelineSetting = timeline.GetSetting()

				# Get the track count
				timelineVideoTrackCount = timeline.GetTrackCount("video")
				# print("[Video Tracks] ", timelineVideoTrackCount)

				# Get the track structure
				for i in range(int(timelineVideoTrackCount + 1)):
					# print("[Track] ", i)
					if timeline.GetIsTrackEnabled("video", i) == True:
						# Get the clips in the track
						clips = timeline.GetItemListInTrack("video", i)
						for clip in clips:
							# print(dir(clip))
							# print(dir(clip.GetNodeGraph()))
							graph = clip.GetNodeGraph()
							if graph != None:
								result = graph.ApplyGradeFromDRX(filepath, gradeMode)
								# print("\t[Color Page Graph][ApplyGradeFromDRX] ", result, " [File] ", filepath)
							#else:
								# print("\t[Color Page Graph] is empty")
			dlg.On.ApplyDRXGradeButton.Clicked = ApplyDRXGradeButtonButtonFunc

			def DRXCollapseButtonFunc(ev):
				# Collapse
				if itm["DRXCollapseButton"].Text == "˄":
					itm["DRXCollapseButton"].Text = "˅"
				else:
					itm["DRXCollapseButton"].Text = "˄"
			dlg.On.DRXCollapseButton.Clicked = DRXCollapseButtonFunc

			def BrowseDRXButtonFunc(ev):
				selectedPath = fu.RequestFile()
				if selectedPath:
					itm["DRXFileLineTxt"].Text = str(selectedPath)

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.BrowseDRXButton.Clicked = BrowseDRXButtonFunc

			def ShowGradeModeButtonFunc(ev):
				ShowFolderFromFilepath(itm["DRXFileLineTxt"].Text)
			dlg.On.ShowGradeModeButton.Clicked = ShowGradeModeButtonFunc

			def ShowLUTFileButtonFunc(ev):
				ShowFolderFromFilepath(itm["LUTFileLineTxt"].Text)
			dlg.On.ShowLUTFileButton.Clicked = ShowLUTFileButtonFunc

			# =====================================================
			# LUT Grade All Clips
			def ApplyLUTGradeButtonFunc(ev):

				# UI Values
				nodeIndex = int(itm["LUTNodeIndexSpinner"].Value)
				filepath = str(app.MapPath(itm["LUTFileLineTxt"].Text or ""))

				print("[Lightfielder][Apply LUT Grade] [File] \"" + filepath + "\" [Node Index] " + str(nodeIndex))
				itm["ProgressLabel"].Text = "  Progress: Apply LUT Grade using \"" + filepath + "\" [Node Index] " + str(nodeIndex)

				# Get the timeline object
				timeline = GetTimeline()

				# Get the timeline name
				timelineName = timeline.GetName()
				#print("[Timeline Name] " + str(timelineName))

				# Get the timeline settings
				timelineSetting = timeline.GetSetting()

				# Get the track count
				timelineVideoTrackCount = timeline.GetTrackCount("video")

				# Get the track structure
				for i in range(int(timelineVideoTrackCount + 1)):
					if timeline.GetIsTrackEnabled("video", i) == True:
						# Get the clips in the track
						clips = timeline.GetItemListInTrack("video", i)
						for clip in clips:
							result = clip.SetLUT(nodeIndex, filepath)
			dlg.On.ApplyLUTGradeButton.Clicked = ApplyLUTGradeButtonFunc

			def LUTCollapseButtonFunc(ev):
				# Collapse
				if itm["LUTCollapseButton"].Text == "˄":
					itm["LUTCollapseButton"].Text = "˅"
				else:
					itm["LUTCollapseButton"].Text = "˄"
			dlg.On.LUTCollapseButton.Clicked = LUTCollapseButtonFunc

			def BrowseLUTButtonFunc(ev):
				selectedPath = fu.RequestFile()
				if selectedPath:
					itm["LUTFileLineTxt"].Text = str(selectedPath)

				itm["PresetCombo"].CurrentText = "Active Grade"
			dlg.On.BrowseLUTButton.Clicked = BrowseLUTButtonFunc

			# Add your GUI element based event functions here:

			def HelpButtonFunc(ev):
				ShowHelpTopic("Docs/Scripts_14_Grade_Automation.md")
			dlg.On.HelpButton.Clicked = HelpButtonFunc

			def ShowPresetButtonFunc(ev):
				ShowFolderFromFilepath(app.MapPath("Scripts:/Utility/Lightfielder/Presets/Grade/"))
			dlg.On.ShowPresetButton.Clicked = ShowPresetButtonFunc

			def ConsoleButtonFunc(ev):
				if itm["ConsoleButton"].Checked == True:
					app.DoAction("Console_Show", {"Show": True})
				else:
					app.DoAction("Console_Show", {"Show": False})
			dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

			def PrevScriptButtonFunc(ev):
				print("[Lightfielder][Toolbar][Show Prev Item]")
				ProcessToolbarButton(ev, dlg, "Tool14", "Tool13")
	
				disp.ExitLoop()
			dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc
	
			def NextScriptButtonFunc(ev):
				print("[Lightfielder][Toolbar][Show Next Item]")
				ProcessToolbarButton(ev, dlg, "Tool14", "Tool15")
	
				disp.ExitLoop()
			dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

			# Load the window preferences
			WindowPrefLoad(dlg, "Lightfielder.GradeAutomationWin.Geometry")

			# Toggle the Toolbar button to the pressed (on) state
			UnpressToolbarButton(dlg.ID, True)

			# Add a close window hotkey event handler
			app.Execute(
			"""
			app:AddConfig('GradeAutomationWin', {
				Target {
					ID = 'GradeAutomationWin',
				},
				Hotkeys {
					Target = 'GradeAutomationWin',
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
			WindowPrefSave(dlg, "Lightfielder.GradeAutomationWin.Geometry")

if __name__ == "__main__":
	if GetProject() and GetTimeline():
		CreateGradeWindow()
	else:
		print("[Lightfielder] Please open a Resolve project and timeline before running this script.")
		ErrorWindow("Lightfielder", "Please open a Resolve project and timeline before running this script.")
	print("[Lightfielder][Done]")
