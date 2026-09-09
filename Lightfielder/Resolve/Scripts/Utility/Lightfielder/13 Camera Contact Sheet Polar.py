"""
Lightfielder 13 Camera Contact Sheet Polar.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Control the visibility of the CCS (Camera Contact Sheet) views. This window acts as a camera array layout preview window which helps you understand the relationship between the physical camera names and the clip layout in the timeline.

Array Preset Location:
$HOME/Lightfielder/Resolve/Scripts/Utility/Lightfielder/Presets/Array/

Toggling camera views On/Off in this window functions like a multitrack version of the stack solo script.

Script Usage:

1. Open a Resolve Edit page based timeline. Select the "Workspace > Script > Lightfielder > 13 Camera Contact Sheet Polar" menu item. A "Camera Contact Sheet" window will appear.

2. Use the "Preset" menu to select from a list of pre-saved camera layouts.

When you customize the CCS view by toggling On/Off individual cameras, the Preset entry will change to the state labelled "Active Layout".

If you would like to enable a quick preset that has zero cameras selected choose the "Array_Default" entry.

The initial Preset list includes the following entries listed below.

Array_Center_Box
Array_Boxes
Array_Center_Star
Array_Center_Target
Array_Center
Array_Checkerboard_A
Array_Checkerboard_B
Array_Column_A
Array_Column_B
Array_Default
Array_Edge_4
Array_Edge_9_Center_Star
Array_Edge_9
Array_Everything_Off
Array_Everything_On
Array_Row_A
Array_Row_B
Array_VistaView_3
Array_VistaView_5

3. If you are on the Edit, Color, or Deliver page, using the CCS window presets will auto-toggle the available clips. This allows you to quickly modify which views are rendered to disk on the Deliver page. You can also target color grading to specific views on the color page via the CCS window.

Create a New Preset:
1. You can create a new Camera Contact Sheet preset by pressing the "+" button.

2. A "Save Preset" dialog will appear that allows you to name the preset.

3. The preset is saved as a .json document in the folder location:
$HOME/Lightfielder/Resolve/Scripts/Utility/Lightfielder/Presets/Array/

If you want to delete a preset, simply remove the .json file from the presets folder.

The presets are saved as JSON formatted plain-text documents. For a preset, each of the active camera array buttons that are pressed down in the CCS window, has an entry listed in the JSON file on its own line that is wrapped inside a pair of quotes. The array entries can range between "AA - "JE" for a 50 view rig.

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

	# The window was closed
	def PresetWinFunc(ev):
		preset_disp.ExitLoop()
	preset_dlg.On.PresetWin.Close = PresetWinFunc

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

def CreateArrayWindow():
	presetsBasePath = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Array/")

	def GetJSON(presetName):
		presetAbsPath = presetsBasePath + str(presetName) + ".json"
		#print("[Array Preset] " + str(presetName))

		# Import the JSON preset file
		try:
			with open(presetAbsPath, "r") as f:
				# Todo: Add a try element to catch JSON formatting errors in the presets when they are json.load() accessed.
				jsonStr = json.load(f)
				return jsonStr
		except OSError as error:
			print("\t[Lightfielder][Exception][JSON Get Error]", error)
			return {
				"version": 1,
				"array": [
				]
			}

	def SetJSON(presetName, data):
		presetAbsPath = presetsBasePath + str(presetName) + ".json"
		#print("[Array Preset] " + str(presetName))

		# Export the JSON preset file
		try:
			with open(presetAbsPath, "w") as f:
				# Todo: Add a try element to catch JSON formatting errors in the presets
				# json.dump(data, f, ensure_ascii = True, indent = 4, sort_keys = True)
				json.dump(data, f, ensure_ascii = True, indent = "\t")
				print("[Lightfielder][Array][Save Preset] " + str(presetName))
		except OSError as error:
			print("\t[Lightfielder][Exception][JSON Save Error]", error)

	def CreateDefaultJSON():
		# Make a default preset
		jsonData = {
			"version": 1.0,
			"array":[
			]
		}

		SetJSON("Array_Default", jsonData)

	# Create the intermediate directories on disk for the presets
	if not os.path.exists(presetsBasePath):
		try:
			# Make the dir
			os.makedirs(presetsBasePath)
			print("[Lightfielder][Array][Make Directory]", presetsBasePath)

			# Make a default preset
			CreateDefaultJSON()
		except OSError as error:
			print("[Lightfielder][Array][Make Directory Error]", error)

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
		"ID": "CCSWin",
		"TargetID" : "CCSWin",
		"Geometry": [100, 110, 640, 750],
		"MinimumSize": [640, 750],
		"FixedSize": [640, 750],
		"Spacing": 0,
		"Margin": 0,
	},[
		ui.VGroup({},[
			# Add your GUI elements here:
			ui.VGroup({
				"Weight": 0.1,
				"StyleSheet": "background-color: rgb(37, 37, 37);",
			},[
				ui.HGroup({
					"Weight": 0.5,
				},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "  13 Camera Contact Sheet",
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
			]),
			ui.HGroup({"ID": "row", "Weight": 0.01,},[
				ui.Label({"ID": "PresetLabel", "Text": "Preset", "Weight": 0.01,}),
				ui.ComboBox({
					"ID": "PresetCombo",
					"Text": "Preset",
					"Weight": 1.0,
				}),
				ui.Button({"ID": "AddPresetButton", "Text": "+", "MinimumSize": [32, 32], "Weight": 0.1}),
			]),
			ui.HGroup({
				"ID": "PolarGrid",
				"Spacing": 0,
				"Weight": 0.2,
			},[
				ui.Button({
					'ID': 'PolarButton',
					'Flat': True,
					'IconSize': [640, 620],
					'MinimumSize': [640, 620],
					'Flat': True,
					'Icon': ui.Icon({'File': 'Scripts:/Utility/Lightfielder/Icons/Polar/polar_chart.png'}),
				}),
			]),
			ui.VGroup({
				"Weight": 0.1
			},[
# 				ui.Label({
# 					"ID": "DividerLabel",
# 					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
# 					"Spacing": 0,
# 					"Margin": 0,
# 					"Weight": 0.01,
# 				}),
# 				ui.HGroup({
# 					"Weight": 0.1
# 				},[
# 					ui.Label({
# 						"ID": "ProgressLabel",
# 						"Text": "  Progress: Awaiting User Input",
# 						"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
# 						"Margin": 0,
# 						"Spacing": 0,
# 						"Weight": 0.01,
# 						"MinimumSize": [355, 24],
# 					}),
# 					ui.Button({
# 						"ID": "ConsoleButton",
# 						"Text": "  Console",
# 						"Margin": 0,
# 						"Spacing": 0,
# 						"Weight": 0.01,
# 						"MaximumSize": [86, 24],
# 						"IconSize": [16, 16],
# 						"Checkable": True,
# 						"Icon": ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Toolbar/fa-code.png"}),
# 					}),
# 				]),
				ui.HGroup({
					"Weight": 0.01
				},[
					ui.Button({
						"ID": "MainCloseButton",
						"Text": "Close",
						"Weight": 0.5,
					}),
					ui.HGap(20, 1),
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

	itm["PresetCombo"].AddItem("Active Layout")

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
	def WinCloseFunc(ev):
		disp.ExitLoop()
	dlg.On.CCSWin.Close = WinCloseFunc

	def MainCloseButtonFunc(ev):
		print("[Lightfielder][Window][Close Button]")

		# Reset the progress caption
		# itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.MainCloseButton.Clicked = MainCloseButtonFunc
	
	def ConsoleButtonFunc(ev):
		if itm["ConsoleButton"].Checked == True:
			app.DoAction("Console_Show", {"Show": True})
		else:
			app.DoAction("Console_Show", {"Show": False})
	dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

	def PrevScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Prev Item]")
		ProcessToolbarButton(ev, dlg, "Tool13", "Tool12")

		disp.ExitLoop()
	dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

	def NextScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Next Item]")
		ProcessToolbarButton(ev, dlg, "Tool13", "Tool14")

		disp.ExitLoop()
	dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

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

	def AddPresetButtonFunc(ev):
		# Get the preset name
		presetString = str(SavePresetWindow())
		if presetString != "":
			jsonName = "Array_" + str(presetString)
			print("[Lightfielder][Array][Add Preset] " + str(jsonName))

			arrayItems = Cameras()

			jsonData = {
				"version": 1,
				"array": arrayItems
			}

			# Export the JSON to disk
			SetJSON(jsonName, jsonData)

			# Add the new entry to the preset combo menu
			itm["PresetCombo"].AddItem(jsonName)
	dlg.On.AddPresetButton.Clicked = AddPresetButtonFunc

# 	def PresetComboFunc(ev):
# 		# Read the current Resolve page
# 		page = resolve.GetCurrentPage()
# 		# Part 1 - Butterfly to the edit page and back to apply the track soloing
# 		if (itm["PresetCombo"].CurrentText != "Active Layout") and ((page ==  "color") or (page ==  "deliver")):
# 			resolve.OpenPage("edit")
# 
# 		# Read the current preset ComboMenu entry
# 		presetName = itm["PresetCombo"].CurrentText
# 		if presetName == "Active Layout":
# 			# This is the current layout from the edit page video tracks
# 			camItems = GetCameras()
# 		elif presetName != "":
# 			# The preset is defining the layout
# 			data = GetJSON(presetName)
# 			camActiveItems = data["array"]
# 			camItems = GetCameras()
# # 			for c in camItems:
# # 				if itm[c].Checked != False:
# # 					itm[c].Checked = False
# # 			for c in camActiveItems:
# # 				if itm[c].Checked != True:
# # 					itm[c].Checked = True
# 		else:
# 			# Nothing is active
# 			camActiveItems = []
# 
# 		# Update the video track state
# 		UpdateActiveLayout()
# 
# 		# Part 2 - Butterfly to the edit page and back to apply the track soloing
# 		if (page ==  "color") or (page ==  "deliver"):
# 			resolve.OpenPage(page)
# 	dlg.On.PresetCombo.CurrentIndexChanged = PresetComboFunc

	def Cameras():
		camActiveItems = []
		camItems = GetCameras()

# 		for c in camItems:
# 			if itm[c].Checked == True:
# 				camActiveItems.append(c)

		return camActiveItems

	def ToogleTrackFunc(state, name, viewNum):
		# Button Unbounce
		print("[Lightfielder][CCS] [View] " + str(name) + " [Num] " + str(viewNum) + " [State] " + str(state))

# 	def LoadCurrentLayoutOnFirstRun():
# 		print("[Lightfielder][CCS] Load Current Layout")
# 		# Get the project name
# 		project = GetProject()
# 		if project is None:
# 			ErrorWindow("Camera Contact Sheet", "Please open a Resolve project before running this script")
# 			exit()
# 		else:
# 			projectName = project.GetName()
# 			projectSetting = project.GetSetting()
# 
# 			# Get the timeline object
# 			timeline = GetTimeline()
# 			if timeline is None:
# 				ErrorWindow("Camera Contact Sheet", "Please open a Resolve timeline before running this script")
# 				exit()
# 			else:
# 				# Get the timeline name
# 				timelineName = timeline.GetName()
# 				#print("[Timeline Name] " + str(timelineName))
# 
# 				# Get the timeline settings
# 				timelineSetting = timeline.GetSetting()
# 
# 				# Get the track count
# 				timelineVideoTrackCount = timeline.GetTrackCount("video")
# 
# 				presetName = itm["PresetCombo"].CurrentText
# 				if presetName == "Active Layout":
# 					for i in range(1,int(timelineVideoTrackCount) + 1):
# 						camName = GetCameraNumber(i)
# # 						itm[camName].Checked = timeline.GetIsTrackEnabled("video", i)

# 	def UpdateActiveLayout():
# 		print("[Lightfielder][CCS] Layout Refresh")
# 		# Get the project name
# 		project = GetProject()
# 		if project is None:
# 			ErrorWindow("Camera Contact Sheet", "Please open a Resolve project before running this script")
# 			exit()
# 		else:
# 			projectName = project.GetName()
# 			projectSetting = project.GetSetting()
# 
# 			# Get the timeline object
# 			timeline = GetTimeline()
# 			if timeline is None:
# 				ErrorWindow("Camera Contact Sheet", "Please open a Resolve timeline before running this script")
# 				exit()
# 			else:
# 				# Get the timeline name
# 				timelineName = timeline.GetName()
# 				#print("[Timeline Name] " + str(timelineName))
# 
# 				# Get the timeline settings
# 				timelineSetting = timeline.GetSetting()
# 
# 				# Get the track count
# 				timelineVideoTrackCount = timeline.GetTrackCount("video")
# 
# 				for i in range(1,int(timelineVideoTrackCount) + 1):
# 					camName = GetCameraNumber(i)
# 					camState = None
# # 					camState = itm[camName].Checked
# 					#print(i)
# 					if camName != None:
# 						if camState == True:
# 							if timeline.GetIsTrackEnabled("video", i) == False:
# 								timeline.SetTrackEnable("video", i, True)
# 						else:
# 							if timeline.GetIsTrackEnabled("video", i) == True:
# 								timeline.SetTrackEnable("video", i, False)
# 						#print("[CCS] [View] " + str(camName) + " [Button State] " + str(camState) + " [Video Track] " + str(i) + " [Track State] " + str(timeline.GetIsTrackEnabled("video", i)))

	# Add your GUI element based event functions here:

	def HelpButtonFunc(ev):
		ShowHelpTopic("Docs/Scripts_13_Camera_Contact_Sheet.md")
	dlg.On.HelpButton.Clicked = HelpButtonFunc

	# Row A
# 	def CCSFunc(ev):
# 		# Read the current Resolve page
# 		page = resolve.GetCurrentPage()
# 		# Part 1 - Butterfly to the edit page and back to apply the track soloing
# 		if (page ==  "color") or (page ==  "deliver"):
# 			resolve.OpenPage("edit")
# 
# 		# A button was pressed so switch the preset ComboBox menu to "Active Layout"
# 		itm["PresetCombo"].CurrentText = "Active Layout"
# 
# 		camName = ev["who"]
# 		camNum = GetCameraName(camName)
# 		camState = ev["On"]
# 
# 		#print("[Camera View]" + str(camName))
# 		#print(ev)
# 
# 		ToogleTrackFunc(camState, camName, camNum)
# 
# 		# Update the video track state
# 		UpdateActiveLayout()
# 
# 		# Part 2 - Butterfly to the edit page and back to apply the track soloing
# 		if (page ==  "color") or (page ==  "deliver"):
# 			resolve.OpenPage(page)

# 
# 	# RowA
# 	dlg.On.AA.Clicked = CCSFunc
# 	dlg.On.BA.Clicked = CCSFunc
# 	dlg.On.CA.Clicked = CCSFunc
# 	dlg.On.DA.Clicked = CCSFunc
# 	dlg.On.EA.Clicked = CCSFunc
# 	dlg.On.FA.Clicked = CCSFunc
# 	dlg.On.GA.Clicked = CCSFunc
# 	dlg.On.HA.Clicked = CCSFunc
# 	dlg.On.IA.Clicked = CCSFunc
# 	dlg.On.JA.Clicked = CCSFunc
# 
# 	# RowB
# 	dlg.On.AB.Clicked = CCSFunc
# 	dlg.On.BB.Clicked = CCSFunc
# 	dlg.On.CB.Clicked = CCSFunc
# 	dlg.On.DB.Clicked = CCSFunc
# 	dlg.On.EB.Clicked = CCSFunc
# 	dlg.On.FB.Clicked = CCSFunc
# 	dlg.On.GB.Clicked = CCSFunc
# 	dlg.On.HB.Clicked = CCSFunc
# 	dlg.On.IB.Clicked = CCSFunc
# 	dlg.On.JB.Clicked = CCSFunc
# 
# 	# RowC
# 	dlg.On.AC.Clicked = CCSFunc
# 	dlg.On.BC.Clicked = CCSFunc
# 	dlg.On.CC.Clicked = CCSFunc
# 	dlg.On.DC.Clicked = CCSFunc
# 	dlg.On.EC.Clicked = CCSFunc
# 	dlg.On.FC.Clicked = CCSFunc
# 	dlg.On.GC.Clicked = CCSFunc
# 	dlg.On.HC.Clicked = CCSFunc
# 	dlg.On.IC.Clicked = CCSFunc
# 	dlg.On.JC.Clicked = CCSFunc
# 
# 	# RowD
# 	dlg.On.AD.Clicked = CCSFunc
# 	dlg.On.BD.Clicked = CCSFunc
# 	dlg.On.CD.Clicked = CCSFunc
# 	dlg.On.DD.Clicked = CCSFunc
# 	dlg.On.ED.Clicked = CCSFunc
# 	dlg.On.FD.Clicked = CCSFunc
# 	dlg.On.GD.Clicked = CCSFunc
# 	dlg.On.HD.Clicked = CCSFunc
# 	dlg.On.ID.Clicked = CCSFunc
# 	dlg.On.JD.Clicked = CCSFunc
# 
# 	# RowE
# 	dlg.On.AE.Clicked = CCSFunc
# 	dlg.On.BE.Clicked = CCSFunc
# 	dlg.On.CE.Clicked = CCSFunc
# 	dlg.On.DE.Clicked = CCSFunc
# 	dlg.On.EE.Clicked = CCSFunc
# 	dlg.On.FE.Clicked = CCSFunc
# 	dlg.On.GE.Clicked = CCSFunc
# 	dlg.On.HE.Clicked = CCSFunc
# 	dlg.On.IE.Clicked = CCSFunc
# 	dlg.On.JE.Clicked = CCSFunc

	itm["PresetCombo"].CurrentText = "Active Layout"
# 	LoadCurrentLayoutOnFirstRun()

	# Load the window preferences
	WindowPrefLoad(dlg, "Lightfielder.CCSWin.Geometry")

	# Toggle the Toolbar button to the pressed (on) state
	UnpressToolbarButton(dlg.ID, True)

	# Add a close window hotkey event handler
	app.Execute(
	"""
	app:AddConfig('CCSWin', {
		Target {
			ID = CCSWin',
		},
		Hotkeys {
			Target = 'CCSWin',
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
	WindowPrefSave(dlg, "Lightfielder.CCSWin.Geometry")

if __name__ == "__main__":
	if GetProject() and GetTimeline():
		CreateArrayWindow()
	else:
		print("[Lightfielder] Please open a Resolve project and timeline before running this script.")
		ErrorWindow("Lightfielder", "Please open a Resolve project and timeline before running this script.")
	print("[Lightfielder][Done]")
