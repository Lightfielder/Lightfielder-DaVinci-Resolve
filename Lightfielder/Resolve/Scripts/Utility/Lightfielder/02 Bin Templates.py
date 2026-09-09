"""
Lightfielder 02 Bin Templates.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

A Resolve new-project automation script to quickly create Media page based Bin folders.

Script Usage:

1. Select the "Workspace > Script > Lightfielder > 02 Bin Templates" menu item. A "Bin Templates" window will appear.

2. Use the "Preset" menu to select a Resolve project folder layout. The "Bin Preview" tree view shows what the folder structure will look like.

3. Click the "Go" button to make the Resolve Project folder structures.

Create a New Preset:
1. You can create a new Bin preset from your current Media page Bin folder hierarchy by pressing the "+" button.

 This will snapshot the active Resolve bin folder structure and save it as a new preset.

2. A "Save Preset" dialog will appear that allows you to name the preset.

3. The preset is saved as a .json format document into the folder location:
$HOME/Lightfielder/Resolve/Scripts/Utility/Lightfielder/Presets/Bins/

If you want to delete a preset, simply remove the .json file from the presets folder.

The presets are saved as JSON formatted plain-text documents that can be viewed with a programmer's text editor. Each Bin folder path is entered on its own line and the path is wrapped inside a pair of quotes.


Todo:
Add back the options for on-disk folder creation in a separate section of the UI.

The "Show folders on Completion" checkbox allows you to see the newly created folder structure in Finder (macOS)/Explorer (Win)/Nautilus (Linux) folder browsing views.

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

startTimer = datetime.datetime.now()

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
	dlg.RecalcLayout()

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

def GenerateBinsWindow():
	presetsBasePath = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Bins/")

	def GetJSON(presetName):
		presetAbsPath = presetsBasePath + str(presetName) + ".json"
		#print("[Bin Preset] " + str(presetName))

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
				"bins": [
				]
			}

	def SetJSON(presetName, data):
		presetAbsPath = presetsBasePath + str(presetName) + ".json"
		#print("[Lightfielder][Bin Preset] " + str(presetName))

		# Export the JSON preset file
		try:
			with open(presetAbsPath, "w") as f:
				# Todo: Add a try element to catch JSON formatting errors in the presets
				# json.dump(data, f, ensure_ascii = True, indent = 4, sort_keys = True)
				json.dump(data, f, ensure_ascii = True, indent = "\t")
				print("[Lightfielder][Bin][Save Preset] " + str(presetName))
		except OSError as error:
			print("\t[Lightfielder][Exception][JSON Save Error]", error)

	def CreateDefaultJSON():
		# Make a default preset
		jsonData = {
			"version": 1.0,
			"bins":[
				"01_delivery/render_checks",
				"01_delivery/reviews",
				"02_timelines/old",
				"03_footage/reference",
				"03_footage/renders",
				"03_footage/source",
				"04_graphics/cmpd_grfx",
				"05_audio",
				"06_compounds",
				"07_projects_xml",
				"08_documents",
				"09_project_bu"
			]
		}

		SetJSON("Bin_Default", jsonData)


	# Create the intermediate directories on disk for the presets
	if not os.path.exists(presetsBasePath):
		try:
			# Make the dir
			os.makedirs(presetsBasePath)
			print("[Lightfielder][Bin][Make Directory]", presetsBasePath)

			# Make a default preset
			CreateDefaultJSON()
		except OSError as error:
			print("[Lightfielder][Exception][Bin][Make Directory Error]", error)

	# Should this window float above all other views
	windowFloat = app.GetData("Lightfielder.WindowStaysOnTop")
	if windowFloat is None:
		windowFloat = True

	ui = fu.UIManager
	disp = bmd.UIDispatcher(ui)

	dlg = disp.AddWindow({
		"WindowTitle": "Lightfielder",
		"WindowFlags": {"Window": True, "WindowStaysOnTopHint": windowFloat},
		"ID": "BinWin",
		"TargetID" : "BinWin",
		"Geometry": [10, 185, 482, 556],
		"MinimumSize": [482, 556],
		"Spacing": 0,
	},[
		ui.VGroup({"ID": "root", "Weight": 10.0,},[
			ui.VGroup({
				"Weight": 0.1,
				#"StyleSheet": "background-color: rgb(37, 37, 37);",
			},[
				ui.HGroup({
					"Weight": 0.5,
				},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "02 Bin Templates",
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
# 			ui.HGroup({"Weight": 0.0,},[
# 				ui.Label({"ID": "BaseLabel", "Text": "Project Base Folder", "Weight": 0.1}),
# 				ui.LineEdit({"ID": "FolderLineTxt", "Text": "", "PlaceholderText": "Please enter a folder path", "Weight": 0.9}),
# 				ui.Button({"ID": "BrowseButton", "Text": "Browse", "Geometry": [0, 0, 30, 50], "Weight": 0.1}),
# 			]),
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
			ui.VGroup({"ID": "root", "Weight": 10.0,},[
				ui.Label({"ID": "BinPreviewLabel", "Text": "Bin Preview", "Weight": 0.01,}),
				ui.Tree({
					"ID": "Tree",
					"Weight": 1.0,
					"SortingEnabled": True,
					"HeaderHidden": True,
					"Events": {
						"CurrentItemChanged": False,
						"ItemActivated": False,
						"ItemClicked": False,
						"ItemDoubleClicked": False,
					},
				}),
# 				ui.CheckBox({
# 					"ID": "ShowFoldersCheckbox",
# 					"Text": "Show folders on Completion",
# 					"Checked": True,
# 					"Weight": 0.01,
# 				}),
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
						"ID": "MainCloseButton",
						"Text": "Close",
						"Weight": 0.5,
					}),
					ui.Button({
						"ID": "GoButton",
						"Text": "Go",
						"Weight": 0.5,
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
		WindowPrefSave(dlg, "Lightfielder.BinWin.Geometry")

		# Save the pref
		PrefSave(dlg)
	dlg.On.BinWin.Hide = HideFunc

	# The window was closed
	def CloseFunc(ev):
		print("[Lightfielder][Window][Closed]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.BinWin.Geometry")

		# Save the pref
		PrefSave(dlg)

		# Reset the progress caption
		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.BinWin.Close = CloseFunc

	def MainCloseButtonFunc(ev):
		print("[Lightfielder][Window][Close Button]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.BinWin.Geometry")

		# Save the pref
		PrefSave(dlg)

		# Reset the progress caption
		# itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.MainCloseButton.Clicked = MainCloseButtonFunc

	def PrevScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Prev Item]")
		ProcessToolbarButton(ev, dlg, "Tool2", "Tool1")

		disp.ExitLoop()
	dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

	def NextScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Next Item]")
		ProcessToolbarButton(ev, dlg, "Tool2", "Tool3")

		disp.ExitLoop()
	dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

	# Add your GUI element based event functions here:

	def HelpButtonFunc(ev):
		ShowHelpTopic("Docs/Scripts_02_Bin_Templates.md")
	dlg.On.HelpButton.Clicked = HelpButtonFunc

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

	# Add a header row
	hdr = itm["Tree"].NewItem()
	hdr.Text[0] = "Paths"
	itm["Tree"].SetHeaderItem(hdr)

	# Number of columns in the Tree list
	itm["Tree"].ColumnCount = 1

	# Resize the Columns
	itm["Tree"].ColumnWidth[0] = 200

	# Change the sorting order of the tree
	itm["Tree"].SortByColumn(0, "AscendingOrder")

	# Select the default bin preset item
	itm["PresetCombo"].CurrentText = "Bin_Default"

	def ShowPresetButtonFunc(ev):
		ShowFolderFromFilepath(app.MapPath("Scripts:/Utility/Lightfielder/Presets/Bins/"))
	dlg.On.ShowPresetButton.Clicked = ShowPresetButtonFunc

	def PresetComboFunc(ev):
		RefreshTree()
	dlg.On.PresetCombo.CurrentIndexChanged = PresetComboFunc

	def AddPresetButtonFunc(ev):
		mediapool = GetMediaPool()
		rootFolder = mediapool.GetRootFolder()

		# Bin folders
		binFolderItems = []

		def GetSubFolder(parentFolder, path):
			for folder in parentFolder.GetSubFolderList():
				if path != "":
					updatedPath = str(path) + "/" + str(folder.GetName())
				else:
					updatedPath = str(folder.GetName())
				binFolderItems.append(updatedPath)
				# Scan Deeper
				GetSubFolder(folder, updatedPath)

		# Build the preset bin paths
		GetSubFolder(rootFolder, "")
		#print(binFolderItems)

		# Get the preset name
		presetString = str(SavePresetWindow())
		if presetString != "":
			jsonName = "Bin_" + str(presetString)
			print("[Lightfielder][Bin][Add Preset] " + str(jsonName))

			jsonData = {
				"version": 1,
				"bins": binFolderItems
			}

			# Export the JSON to disk
			SetJSON(jsonName, jsonData)

			# Add the new entry to the preset combo menu
			itm["PresetCombo"].AddItem(jsonName)
	dlg.On.AddPresetButton.Clicked = AddPresetButtonFunc

# 	def BrowseButtonFunc(ev):
# 		selectedPath = fu.RequestDir("", "", {
# 			"FReqS_Title": "Choose a base folder for the new project hiearchy."
# 		})
# 		if selectedPath:
# 			itm["FolderLineTxt"].Text = str(selectedPath)
# 	dlg.On.BrowseButton.Clicked = BrowseButtonFunc

	def GoButtonFunc(ev):
		startTimer = datetime.datetime.now()
		startTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")
		itm["ProgressLabel"].Text = "  Progress: Creating Bins"

		res = app.GetResolve()
		mediapool = GetMediaPool()
		rootFolder = mediapool.GetRootFolder()
		res.OpenPage("media")

		# Expand any PathMaps in the URLs
		#baseFolder = app.MapPath(itm["FolderLineTxt"].Text)
		binsList = ""

		print("[Lightfielder][Bin Templates][Go]")
		# Check if the base folder exists and is a directory
		#if os.path.isdir(baseFolder):
		if True:
			#print("\t[Lightfielder][Project Base Folder] \"" + str(baseFolder) + "\"")
			print("\t[Lightfielder][Preset] \"" + str(itm["PresetCombo"].CurrentText) + "\"")

			# Iterate through the uiTree items
			for i in range(int(itm["Tree"].TopLevelItemCount())):
				# Read the tree item
				treeItem = itm["Tree"].TopLevelItem(i)

				# Get the text for the tree item
				# Example: "01_delivery/render_checks"
				binItemPath = treeItem.Text[0]

# 				# Build the directory path for the tree item
# 				# Example: "/Users/vfx/Desktop/Bins/01_delivery/render_checks"
# 				# directoryPath = os.path.join(baseFolder, binItemPath)
# 				directoryPath = app.MapPath(baseFolder + "/" + binItemPath)
#
# 				# Create the intermediate directories on disk for the tree item
# 				if not os.path.exists(directoryPath):
# 					try:
# 						print("\t[Lightfielder][Bin][Make Directory]", directoryPath)
# 						os.makedirs(directoryPath)
# 					except OSError as error:
# 						print("\t[Lightfielder][Bin][Make Directory Error]", error)
# 				else:
# 					print("\t[Lightfielder][Bin][Directory Exists]", directoryPath)

				#print("\t\t[Item " + str(i) + "] \"" + str(directoryPath) + "\"")
				#print("\t\t[Item " + str(i) + "] \"" + str(binItemPath) + "\"")

				# Create the Media Pool Bins
				binSubFolders = binItemPath.split("/")
				parentFolder = rootFolder
				for f in binSubFolders:
					if (f != None) and (f != ""):
						parentFolder = GetFolder(parentFolder, f, mediapool)

			# Refresh the bins
			mediapool.RefreshFolders()

			# Switch back to the Media Pool root folder
			mediapool.SetCurrentFolder(rootFolder)

			# Refresh the bins
			mediapool.RefreshFolders()

			# Hide the window
			# disp.Hide()

			itm["ProgressLabel"].Text = "  Progress: Bins created using the \"" + str(itm["PresetCombo"].CurrentText) + "\" preset [Wallclock " + GetTimeElapsed(startTimer) + "]"

			# Play the sound effect
			# soundName = app.GetData("Lightfielder.SoundEffectsError")
			soundName = app.GetData("Lightfielder.SoundEffectsComplete")
			if soundName != None:
				SoundEffectSelect(soundName)

			# Task Completed
			# ErrorWindow("Completed", "The new bins have been created successfully using the \"" + str(itm["PresetCombo"].CurrentText) + "\" preset!")

			# Close the window
			# disp.ExitLoop()

# 			# Reveal folders on disk
# 			if itm["ShowFoldersCheckbox"].Checked:
# 				app.Execute('bmd.openfileexternal("Open", [[' + str(baseFolder) + '"]]')
# 		else:
# 			print("\t[Lightfielder][Project Base Folder] [Missing] \"" + str(baseFolder) + "\"")
# 			ErrorWindow("Error", "The \"Project Base Folder\" textfield is empty. This field is used to specify a working directory on disk where you want the new Resolve project hierarchy to be created. Please select a \"Project Base Folder\" and then press the Go button.")
		# disp.ExitLoop()
	dlg.On.GoButton.Clicked = GoButtonFunc

	def ConsoleButtonFunc(ev):
		if itm["ConsoleButton"].Checked == True:
			app.DoAction("Console_Show", {"Show": True})
		else:
			app.DoAction("Console_Show", {"Show": False})
	dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

	def RefreshTree():
		itm["Tree"].UpdatesEnabled = False
		itm["Tree"].SortingEnabled = False

		itm["Tree"].Clear()

		# Read the current preset ComboMenu entry
		presetName = itm["PresetCombo"].CurrentText
		if presetName != "":
			data = GetJSON(presetName)
			folders = data["bins"]
			#print(folders)
		else:
			folders = []

		# Build the tree
		GetTreeHiearchy(folders)

		itm["Tree"].UpdatesEnabled = True
		itm["Tree"].SortingEnabled = True

	def GetTreeHiearchy(list):
		for i in list:
			# Add a uiTree row
			itRow = itm["Tree"].NewItem()
			itPath = str(i)

			itRow.Text[0] = itPath
			itm["Tree"].AddTopLevelItem(itRow)

	def GetMediaPool():
		resolve = app.GetResolve()
		projectManager = resolve.GetProjectManager()
		project = projectManager.GetCurrentProject()
		mediapool = project.GetMediaPool()
		return mediapool

	def GetFolder(parentFolder, childFolder, mediaPool):
		for folder in parentFolder.GetSubFolderList():
			if folder.GetName() == childFolder:
				return folder
		else:
			return mediaPool.AddSubFolder(parentFolder, childFolder)

	# Add a close window hotkey event handler
	app.Execute(
	"""
	app:AddConfig('BinWin', {
		Target {
			ID = 'BinWin',
		},
		Hotkeys {
			Target = 'BinWin',
			Defaults = true,

			CONTROL_W = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
			CONTROL_F4 = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
			ESCAPE = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
		},
	})
	""")

	RefreshTree()

	# Load the window preferences
	WindowPrefLoad(dlg, "Lightfielder.BinWin.Geometry")

	# Toggle the Toolbar button to the pressed (on) state
	UnpressToolbarButton(dlg.ID, True)

	dlg.Show()
	disp.RunLoop()
	dlg.Hide()

	# Toggle the Toolbar button to the unpressed (off) state
	UnpressToolbarButton(dlg.ID, False)

	# Save the window preferences
	WindowPrefSave(dlg, "Lightfielder.BinWin.Geometry")

if __name__ == "__main__":
	GenerateBinsWindow()
	print("[Lightfielder][Done]")
