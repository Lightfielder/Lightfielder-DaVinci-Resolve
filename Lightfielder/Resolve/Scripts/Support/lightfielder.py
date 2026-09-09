"""
Lightfielder Python Module 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Lightfielder Script Usage Tip:
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	print(sys.path)
	from lightfielder import *

"""

import datetime
import json
import os
import platform
import re
import sys
import csv

# Grab app/bmd/fu scope from the script that calls the lightfielder module import
import __main__
app = getattr(__main__, "app", None)
bmd = getattr(__main__, "bmd", None)
fu = getattr(__main__, "fu", None)

def LFGetVersion(label):
	# Provide the Lightfielder version number when requested
	# return str(label) + "26.09"
	return str(label) + "26.09.09"

def execfile(filepath, globals = None, locals = None):
	try:
		app.RunScript(filepath)
	except SystemExit:
		print("[Lightfielder][Exception] A Python \"System Exit\" exception was called")

# Run a shell command
def Command(path):
	# Trim the filepath down to the parent folder
	dir = os.path.dirname(path)

	# Make the output filepath
	dest = dir + os.sep

	# Build the launching command
	cmd = ""
	args = []

	if sys.platform == "win32":
		cmd = "start"
		args = [cmd, "", dest]
		#cmd = "explorer"
		#args = [cmd, dest]
	elif sys.platform == "darwin":
		cmd = "open"
		args = [cmd, dest]
	elif sys.platform == "linux" or sys.platform == "linux2":
		cmd = "xdg-open"
		args = [cmd, dest]

	print("\t[Lightfielder][Open Containing Folder] " + str(args))

	# Run Open
	import subprocess
	# subprocess.call(args)
	subprocess.Popen(args)

# Edit a script in the default text editor
def ExternalEditor(path):
	editorPath = app.MapPath(app.GetPrefs('Global.Script.EditorPath'))
	if editorPath == "":
		print('[Script] The "Editor Path" is empty. Please choose a text editor in the Fusion Preferences "Global and Default Settings > Script > Editor Path" section.\n')
		res = app.GetResolve()
		page = res.GetCurrentPage()
		if page is not None and page != "fusion":
			res.OpenPage("fusion")
			fu.ShowPrefs("PrefsScript")
	elif not os.path.exists(editorPath):
		print('[Script] The "Editor Path" is not a valid location as the program does not exist. Please choose a text editor in the Fusion Preferences "Global and Default Settings > Script > Editor Path" section.\n')
		res = app.GetResolve()
		page = res.GetCurrentPage()
		if page is not None and page != "fusion":
			res.OpenPage("fusion")
			fu.ShowPrefs("PrefsScript")
	else:
		dest = app.MapPath(path)

		# Build the launching command
		cmd = ""
		args = []

		if sys.platform == "win32":
			cmd = "start"
			args = [editorPath, dest]
			# args = [cmd, "", editorPath, dest]
			#cmd = "explorer"
			#args = [cmd, dest]
		elif sys.platform == "darwin":
			cmd = "open"
			args = [cmd, "-a", editorPath, dest]
		elif sys.platform == "linux" or sys.platform == "linux2":
			args = [editorPath, dest]
			# cmd = "xdg-open"
			# args = [cmd, editorPath, dest]

		print("\t[Lightfielder][Edit Script Using] " + str(args))

		# Run Open
		import subprocess
		# subprocess.call(args)
		subprocess.Popen(args)

# Choose a sound effect from a ComboMenu item name
# Example: SoundEffectSelect("Steam Train Whistle Sound")
# Example: SoundEffectSelect("Trumpet Sound")
# Example: SoundEffectSelect("Braam Sound")
def SoundEffectSelect(soundName):
	soundBasePath = "Lightfielder:/Resolve/Sounds/"

	# Lookup the .wav file to play
	if soundName == "Steam Train Whistle Sound":
		SoundEffect(soundBasePath + str("steam-train-whistle.wav"))
	elif soundName == "Trumpet Sound":
		SoundEffect(soundBasePath + str("trumpet-fanfare.wav"))
	elif soundName == "Braam Sound":
		SoundEffect(soundBasePath + str("cinematic-musical-sting-braam.wav"))

# Play a sound effect:
# Example: SoundEffect("Lightfielder:/Resolve/Sounds/trumpet-fanfare.wav")
def SoundEffect(path):
	audioFilePath = app.MapPath(path)

	# Build the launching command
	cmd = ""
	args = []

	# Check if the sound volume is muted
	playSound = app.GetData("Lightfielder.PlayUserInterfacesSoundEffects")
	volume = app.GetData("Lightfielder.SoundEffectsVolume")
	if playSound != None and playSound == True and volume != None and volume >= 1:
		# Check if we actually have the .wav sound file on disk
		if os.path.exists(audioFilePath):
			if sys.platform == "win32":
				cmd = f"(New-Object System.Media.SoundPlayer '{audioFilePath}').PlaySync();"
				args = ["powershell", "-c", cmd]
			elif sys.platform == "darwin":
				cmd = "afplay"
				args = [cmd, audioFilePath]
			elif sys.platform == "linux" or sys.platform == "linux2":
				cmd = "xdg-open"
				args = [cmd, audioFilePath]
		
			# Run Open
			import subprocess
			print(f"\t[Lightfielder][Sound Effect Using] {args}")
			
			if sys.platform == "win32":
				# Suppress the command prompt window
				startupinfo = subprocess.STARTUPINFO()
				startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
				subprocess.Popen(args, startupinfo=startupinfo)
			else:
				subprocess.Popen(args)
		else:
			print("\t[Lightfielder][Sound Effect][Audio File Missing]" + str(audioFilePath))
	else:
		print("\t[Lightfielder][Sound Effect][Volume] Playback is muted with a volume of 0")

# Find the Toolbar tool items
def GetTools():
	return [
		"Tool1",
		"Tool2",
		"Tool3",
		"Tool4",
		"Tool5",
		"Tool6",
		"Tool7",
		"Tool8",
		"Tool9",
		"Tool10",
		"Tool11",
		"Tool12",
		"Tool13",
		"Tool14",
		"Tool15",
		"Tool16",
		"Tool17",
		"Tool18",
		"Tool19",
		"Tool20",
		"Tool21",
		"Tool22"
	]

# Get the toolbar script filepath by the tool ID
def GetToolScript(tool):
	# Lightfielder Scripts Utility Folder
	baseFolderPathMap = "Lightfielder:/Resolve/Scripts/Utility/Lightfielder"

	scriptDict = {}

	cameraArrayGeometry = app.GetData("Lightfielder.ArrayGeometry")
	if cameraArrayGeometry == 0 or cameraArrayGeometry == 1:
		# A1-E5 Array Style
		scriptDict = {
			"Tool1": f"{baseFolderPathMap}/01 Preferences.py",
			"Tool2": f"{baseFolderPathMap}/02 Bin Templates.py",
			"Tool3": f"{baseFolderPathMap}/03 Shotlog Pre-Flight.py",
			"Tool4": f"{baseFolderPathMap}/04 Import Footage.py",
			"Tool5": f"{baseFolderPathMap}/05 Metadata Sync.py",
			"Tool6": f"{baseFolderPathMap}/06 Still Frames Export.py",
			"Tool7": f"{baseFolderPathMap}/07 Create EDLs.py",
			"Tool8": f"{baseFolderPathMap}/08 Batch Trim.py",
			"Tool9": f"{baseFolderPathMap}/09 EDL Stack Swizzle.py",
			"Tool10": f"{baseFolderPathMap}/10 EDL Checker.py",
			"Tool11": f"{baseFolderPathMap}/11 Log Viewer.py",
			"Tool12": f"{baseFolderPathMap}/12 Video Track Solo.py",
			"Tool13": f"{baseFolderPathMap}/13 Camera Contact Sheet Rect.py",
			"Tool14": f"{baseFolderPathMap}/14 Grade Automation.py",
			"Tool15": f"{baseFolderPathMap}/15 EDL Export.py",
			"Tool16": f"{baseFolderPathMap}/16 Extensions.py",
			"Tool17": f"{baseFolderPathMap}/17 Jupyter Link.py",
			"Tool18": f"{baseFolderPathMap}/18 Open Lightfielder Folder.py",
			"Tool19": f"{baseFolderPathMap}/19 Edit Python Module.py",
			"Tool20": f"{baseFolderPathMap}/20 Show Console.py",
			"Tool21": f"{baseFolderPathMap}/21 Documentation.py",
			"Tool22": f"{baseFolderPathMap}/22 About Lightfielder.py"
		}
	else:
		# Polar Array Style
		scriptDict = {
			"Tool1": f"{baseFolderPathMap}/01 Preferences.py",
			"Tool2": f"{baseFolderPathMap}/02 Bin Templates.py",
			"Tool3": f"{baseFolderPathMap}/03 Shotlog Pre-Flight.py",
			"Tool4": f"{baseFolderPathMap}/04 Import Footage.py",
			"Tool5": f"{baseFolderPathMap}/05 Metadata Sync.py",
			"Tool6": f"{baseFolderPathMap}/06 Still Frames Export.py",
			"Tool7": f"{baseFolderPathMap}/07 Create EDLs.py",
			"Tool8": f"{baseFolderPathMap}/08 Batch Trim.py",
			"Tool9": f"{baseFolderPathMap}/09 EDL Stack Swizzle.py",
			"Tool10": f"{baseFolderPathMap}/10 EDL Checker.py",
			"Tool11": f"{baseFolderPathMap}/11 Log Viewer.py",
			"Tool12": f"{baseFolderPathMap}/12 Video Track Solo.py",
			"Tool13": f"{baseFolderPathMap}/13 Camera Contact Sheet Polar.py",
			"Tool14": f"{baseFolderPathMap}/14 Grade Automation.py",
			"Tool15": f"{baseFolderPathMap}/15 EDL Export.py",
			"Tool16": f"{baseFolderPathMap}/16 Extensions.py",
			"Tool17": f"{baseFolderPathMap}/17 Jupyter Link.py",
			"Tool18": f"{baseFolderPathMap}/18 Open Lightfielder Folder.py",
			"Tool19": f"{baseFolderPathMap}/19 Edit Python Module.py",
			"Tool20": f"{baseFolderPathMap}/20 Show Console.py",
			"Tool21": f"{baseFolderPathMap}/21 Documentation.py",
			"Tool22": f"{baseFolderPathMap}/22 About Lightfielder.py"
		}

	return scriptDict[tool]

# Find a Toolbar item's icon filename
def GetIconFromToolNum(tool):
	if tool == "Tool1":
		return "fa-gear.png"
	elif tool == "Tool2":
		return "fa-archive.png"
	elif tool == "Tool3":
		return "fa-medkit.png"
	elif tool == "Tool4":
		return "fa-list-alt.png"
	elif tool == "Tool5":
		return "fa-tags.png"
	elif tool == "Tool6":
		return "fa-qrcode.png"
	elif tool == "Tool7":
		return "fa-film.png"
	elif tool == "Tool8":
		return "fa-cut.png"
	elif tool == "Tool9":
		return "fa-level-up.png"
	elif tool == "Tool10":
		return "fa-fire.png"
	elif tool == "Tool11":
		return "fa-triangle.png"
	elif tool == "Tool12":
		return "fa-check-circle.png"
	elif tool == "Tool13":
		return "fa-camera.png"
	elif tool == "Tool14":
		return "fa-eyedropper.png"
	elif tool == "Tool15":
		return "fa-paper-plane.png"
	elif tool == "Tool16":
		return "fa-puzzle-piece.png"
	elif tool == "Tool17":
		return "fa-book.png"
	elif tool == "Tool18":
		return "fa-folder-open.png"
	elif tool == "Tool19":
		return "fa-file-code-o.png"
	elif tool == "Tool20":
		return "fa-code.png"
	elif tool == "Tool21":
		return "fa-question-circle.png"
	elif tool == "Tool22":
		return "fa-info-circle.png"
	else:
		return "fa-gear.png"

# Find a Toolbar item's nice name
def GetWindowTitleFromToolNum(tool):
	if tool == "Tool1":
		return "01 Preferences"
	elif tool == "Tool2":
		return "02 Bin Templates"
	elif tool == "Tool3":
		return "03 Shotlog Pre-Flight"
	elif tool == "Tool4":
		return "04 Import Footage"
	elif tool == "Tool5":
		return "05 Metadata Sync"
	elif tool == "Tool6":
		return "06 Still Frames Export"
	elif tool == "Tool7":
		return "07 Create EDLs"
	elif tool == "Tool8":
		return "08 Batch Trim"
	elif tool == "Tool9":
		return "09 EDL Stack Swizzle"
	elif tool == "Tool10":
		return "10 EDL Checker"
	elif tool == "Tool11":
		return "11 Log Viewer"
	elif tool == "Tool12":
		return "12 Video Track Solo"
	elif tool == "Tool13":
		return "13 Camera Contact Sheet"
	elif tool == "Tool14":
		return "14 Grade Automation"
	elif tool == "Tool15":
		return "15 EDL Export"
	elif tool == "Tool16":
		return "16 Extensions"
	elif tool == "Tool17":
		return "17 Jupyter Link"
	elif tool == "Tool18":
		return "18 Open Lightfielder Folder"
	elif tool == "Tool19":
		return "19 Edit Python Module"
	elif tool == "Tool20":
		return "20 Show Console"
	elif tool == "Tool21":
		return "21 Documentation"
	elif tool == "Tool22":
		return "22 About Lightfielder"
	else:
		return "Docs"

# Find a Toolbar item's window
def GetWindowIDFromToolNum(tool):
	if tool == "Tool1":
		return "PrefsWin"
	elif tool == "Tool2":
		return "BinWin"
	elif tool == "Tool3":
		return "ShotlogPreFlightWin"
	elif tool == "Tool4":
		return "ImportFootageWin"
	elif tool == "Tool5":
		return "MetadataWin"
	elif tool == "Tool6":
		return "CalibrationWin"
	elif tool == "Tool7":
		return "CreateEDLWin"
	elif tool == "Tool8":
		return "TrimWin"
	elif tool == "Tool9":
		return "EDLStackSwizzleWin"
	elif tool == "Tool10":
		return "EDLChecker"
	elif tool == "Tool11":
		return "LogViewerWin"
	elif tool == "Tool12":
		return "VideoTrackSoloWin"
	elif tool == "Tool13":
		return "CCSWin"
	elif tool == "Tool14":
		return "GradeAutomationWin"
	elif tool == "Tool15":
		return "EDLExportWin"
	elif tool == "Tool16":
		return "ExtensionsWin"
	elif tool == "Tool17":
		return "JupyterWin"
	elif tool == "Tool18":
		return "Docs"
	elif tool == "Tool19":
		return "Docs"
	elif tool == "Tool20":
		return "Console"
	elif tool == "Tool21":
		return "Docs"
	elif tool == "Tool22":
		return "AboutWin"
	else:
		return "Docs"

# Find a Toolbar item' from the Window ID
def GetToolNumFromWindowID(windowID):
	if windowID == "PrefsWin":
		return "Tool1"
	elif windowID == "BinWin":
		return "Tool2"
	elif windowID == "ShotlogPreFlightWin":
		return "Tool3"
	elif windowID == "ImportFootageWin":
		return "Tool4"
	elif windowID == "MetadataWin":
		return "Tool5"
	elif windowID == "CalibrationWin":
		return "Tool6"
	elif windowID == "CreateEDLWin":
		return "Tool7"
	elif windowID == "TrimWin":
		return "Tool8"
	elif windowID == "EDLStackSwizzleWin":
		return "Tool9"
	elif windowID == "EDLChecker":
		return "Tool10"
	elif windowID == "LogViewerWin":
		return "Tool11"
	elif windowID == "VideoTrackSoloWin":
		return "Tool12"
	elif windowID == "CCSWin":
		return "Tool13"
	elif windowID == "GradeAutomationWin":
		return "Tool14"
	elif windowID == "EDLExportWin":
		return "Tool15"
	elif windowID == "ExtensionsWin":
		return "Tool16"
	elif windowID == "JupyterWin":
		return "Tool17"
	elif windowID == "Docs":
		return "Tool18"
	elif windowID == "Docs":
		return "Tool19"
	elif windowID == "Console":
		return "Tool20"
	elif windowID == "Docs":
		return "Tool21"
	elif windowID == "AboutWin":
		return "Tool22"
	else:
		return "Docs"

# Toggle Toolbar button state
# Example: UnpressToolbarButton(dlg.ID, False)
# Example: UnpressToolbarButton("PrefsWin", False)
def UnpressToolbarButton(tool, boolState):
	if tool is not None and tool != "":
		# Target the toolbar window
		winItm = GetWindow("ToolbarWin")
		# Check if the Toolbar window was loaded before inside this session
		if winItm is not None:
			# Get the toolbar item name
			toolbarItm = winItm.GetItems()
			if toolbarItm is not None:
				# print(toolbarItm)
				# Turn that into the item ID to check/uncheck
				t = GetToolNumFromWindowID(tool)
				if t is not None:
					toolbarItm[t].Checked = boolState

# Should short tooltips or long tooltip messages be used?
# Example: "ToolTip": GetTooltip("The toolbar will show up when Resolve launches",  "(WIP) When this option is enabled the Lightfielder Toolbar \nwill automatically load when DaVinci Resolve Studio is started.)
def GetTooltip(short, long):
	#  Read the setting on the "01 Preferences" script. Fallback is to use the short tip.
	rtfm = app.GetData("Lightfielder.RTFMTooltips")
	if rtfm == True:
		return long

	return short

# Find a Toolbar item's window
def GetWindow(tool):
	if tool is not None and tool != "":
		ui = fu.UIManager
		return ui.FindWindow(tool)
	else:
		return None
		
# Find a Toolbar item's window geometry as a dict
def GetWindowGeometry(tool):
	if tool is not None and tool != "":
		ui = fu.UIManager
		winDlg = ui.FindWindow(tool)
		if winDlg is not None and winDlg.Geometry is not None:
			data = winDlg.Geometry
			# return winDlg.Geometry
			return f"[XY] {data[1]} x {data[2]} px [Width/Height] {data[3]} x {data[4]} px"
	return ""

# Handle the Toolbar item switching when the < or > buttons are pressed
# Example: buttonName = "Tool1"
# Example: ProcessToolbarButton(ev, dlg, currentButtonName, buttonName):
def ProcessToolbarButton(ev, toolbarItm, currentButtonName, buttonName):
	toolbarDlg = GetWindow("ToolbarWin")
	toolbarItm = toolbarDlg.GetItems()

	# Modifier keys like Shift, Alt/Option, and Control/Command
	buttonModifier = ev["modifiers"]["ShiftModifier"]
	buttonModifierControl = ev["modifiers"]["ControlModifier"]
	buttonModifierAlt = ev["modifiers"]["AltModifier"]

	# Look up the script name
	selectedScript = app.MapPath(GetToolScript(buttonName))

	# The caller script's window name
	currentWinName = GetWindowIDFromToolNum(currentButtonName)
	currentWinItm = GetWindow(currentWinName)
	currentWinTitle = GetWindowTitleFromToolNum(currentButtonName)

	# Run the Python script if the window is not already open
	winName = GetWindowIDFromToolNum(buttonName)
	winItm = GetWindow(winName)
	winTitle = GetWindowTitleFromToolNum(buttonName)

	# Button Status Info
	# print("[Lightfielder][Toolbar][Show][Window Name] " + str(winTitle) + " [Button Checked State] " + str(toolbarItm[buttonName].Checked) + " [Script] " + str(selectedScript))

	# Sync the Window position prefs
	# Current Window
	currentPrefName = str("Lightfielder.") + str(currentWinName) + str(".Geometry")
	currentWinGeoPref = app.GetData(currentPrefName)
	if currentWinGeoPref is not None:
		# print("[Lightfielder][Preference][Current Window Pref] " + str(currentPrefName) + "\t[Geo] " + str(currentWinGeoPref) + "\t[Geo Datatype] " + str(type(currentWinGeoPref)))

		# New window
		prefName = ("Lightfielder." )+ str(winName) + (".Geometry")
		winGeoPref = app.GetData(prefName)
		if winGeoPref is not None:
			# print("[Lightfielder][Preference][New Window Pref] " + str(prefName) + "\t[Geo] " + str(winGeoPref) + "\t[Geo Datatype] " + str(type(winGeoPref)))

			if buttonModifierAlt == True:
				# alt modifier key used with previous or next button navigation

				# Snap the windows to the left or right edge of each other as they are displayed
				# Window Y position
				winGeoYDifference = currentWinGeoPref[2.0] - winGeoPref[2.0]
				# print("[Lightfielder][Window Difference Math][Y]", winGeoYDifference, "[Data Type]", type(winGeoYDifference))

				# Window X position
				winGeoXDifference = currentWinGeoPref[1.0] - winGeoPref[1.0]
				# print("[Lightfielder][Window Difference Math][X]", winGeoYDifference, "[Data Type]", type(winGeoYDifference))

				# Window Height
				winGeoHeightDifference = currentWinGeoPref[4.0] - winGeoPref[4.0]

				# Window Widths
				winGeoWidthDifference = currentWinGeoPref[3.0] - winGeoPref[3.0]

				# Window Y Offset
				winGeoYOffset = winGeoYDifference + winGeoHeightDifference

				# Window X Offset = Stack the windows to the left/right of each other on the page flips
				# keep the variable in scope with an initial value assigned
				winGeoXOffset = 0

				# Trim the tool ID like "Tool1" or "Tool2" down to the numbers on the end like "1" or "2". 
				# Then compute if this is a previous or next toolbar direction cycle
				currentNum = int(currentButtonName.split("Tool")[1])
				buttonNum = int(buttonName.split("Tool")[1])
				if currentNum > buttonNum:
					# Previous Toolbar item = Shift Left
					print("[Lightfielder][Window Modifier Key][Alt] Stack to the Left")
					winGeoXOffset = winGeoXDifference - winGeoWidthDifference
				elif currentNum < buttonNum:
					# Next Toolbar item = Shift Right
					print("[Lightfielder][Window Modifier Key][Alt] Stack to the Right")
					winGeoXOffset = winGeoXDifference + winGeoWidthDifference
				# else:
					# Same Toolbar item = Stays the same

				# updatedWinGeoPref = currentWinGeoPref
				updatedWinGeoPref = [currentWinGeoPref[1.0] + winGeoXOffset, currentWinGeoPref[2.0] + winGeoYOffset, currentWinGeoPref[3.0], currentWinGeoPref[4.0]]

				# print("[Lightfielder][Window Difference Math][Y]", winGeoYDifference, "[Height]", winGeoHeightDifference, "[Width]", winGeoHeightDifference, "[Y Offset]", winGeoYOffset, "[Src Geo]", currentWinGeoPref, "[Updated Geo]", updatedWinGeoPref, "[Data Type]", type(updatedWinGeoPref))
			else:
				# Not modifier keys used with previous or next button navigation
				# Window Y position
				winGeoYDifference = currentWinGeoPref[2.0] - winGeoPref[2.0]
				# print("[Lightfielder][Window Difference Math][Y]", winGeoYDifference, "[Data Type]", type(winGeoYDifference))

				# Window X position
				winGeoXDifference = 0
				# print("[Lightfielder][Window Difference Math][X]", winGeoYDifference, "[Data Type]", type(winGeoYDifference))

				# Window Heights
				winGeoHeightDifference = currentWinGeoPref[4.0] - winGeoPref[4.0]

				# Window Widths
				winGeoWidthDifference = 0

				# Window Y Offset
				winGeoYOffset = winGeoYDifference + winGeoHeightDifference

				# WindowX Offset
				winGeoXOffset = 0

				# updatedWinGeoPref = currentWinGeoPref
				updatedWinGeoPref = [currentWinGeoPref[1.0] + winGeoXOffset, currentWinGeoPref[2.0] + winGeoYOffset, currentWinGeoPref[3.0], currentWinGeoPref[4.0]]

				# print("[Lightfielder][Window Difference Math][Y]", winGeoYDifference, "[Height]", winGeoHeightDifference, "[Width]", winGeoHeightDifference, "[Y Offset]", winGeoYOffset, "[Src Geo]", currentWinGeoPref, "[Updated Geo]", updatedWinGeoPref, "[Data Type]", type(updatedWinGeoPref))

# 			x, y, width, height = winGeoPref[0], winGeoPref[1], winGeoPref[2], winGeoPref[3]
# 			geometry = [prev_x, prev_y, width, height]

			# If the next window (Y + Height) is higher up on the view than the previous window (Y + Height) then adjust their placement
			# Offset the new window height so the lower edge stays aligned between page flipping
			# Math: (Y - Previous Y) + (Height - Previous Height)
			# currentWinGeoPref[1] = (winGeoPref[1] - currentWinGeoPref[1]) + (winGeoPref[3] - currentWinGeoPref[3])
			# print("[Lightfielder][Geo Offset] ",  currentWinGeoPref, " vs ", winGeoPref)

			# New window updated window location prefs
			app.SetData(prefName, updatedWinGeoPref)
			# app.SetData(prefName, currentWinGeoPref)

			# Write the preferences to disk
			print("[Lightfielder][Preferences] Save")
			app.SavePrefs()

			# Recall the value to see if it was saved OK
			savedPref = app.GetData(prefName)
			# app.SetData(prefName, geometry)

			# print("[Lightfielder][Preference] [Geo Updated] " + str(prefName) + " [Geo] " + str(savedPref) + " [Geo Datatype] " + str(type(savedPref)))
		else:
			print("[Lightfielder][Preference] " + str(winTitle) + " is missing")
	else:
		print("[Lightfielder][Preference] " + str(currentWinTitle) + " is missing")

	# Toggle the Toolbar window states
	if toolbarItm[buttonName].Checked == False:
		# The button was just checked so show the window or run the script
		# print("[Lightfielder][Toolbar][Checked State][False]")
		if winItm == None or winItm == "":
			if buttonModifierControl == True:
				# Hold down the control key when clicking on a toolbar item to edit the script in a programmer's text editor
				# This feature requires the "xdg-open" package to be installed on Linux.
				print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Edit this Window] " + str(winName) + " [Script Edit] " + str(selectedScript))
				ExternalEditor(selectedScript)
			else:
				print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Run the Script] " + str(selectedScript))
				execfile(selectedScript)
		elif winItm != None:
			if buttonModifierAlt == True:
				print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Stack Window] " + str(winName))
				winItm.Show()
				winItm.Raise()
				winItm.ActivateWindow()
			elif buttonModifier == False and buttonModifierControl == False:
				print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Show Window] " + str(winName))
				winItm.Show()
				winItm.Raise()
				winItm.ActivateWindow()
			elif buttonModifierControl == True:
				# Hold down the control key when clicking on a toolbar item to edit the script in a programmer's text editor
				# This feature requires the "xdg-open" package to be installed on Linux.

				print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Edit this Window] " + str(winName) + " [Script Edit] " + str(selectedScript))
				ExternalEditor(selectedScript)

				print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Show Window] " + str(winName))
				winItm.Show()
				winItm.Raise()
				winItm.ActivateWindow()
			else:
				# Hold down the shift key when clicking on a toolbar item to force-reload the script
				print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Reload Window] " + str(winName) + " [Script] " + str(selectedScript))
				winItm.Close()
				execfile(selectedScript)
		else:
			print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [NOP]")

		# The new window is now open. We can move it into place
		# The geometry is stored using integer position and size values like "[X, Y, Width, Height]"
		#if winItm is not None and currentWinItm is not None:
		#	winItm.Geometry = winGeoPref
		#	# winItm.Geometry = currentWinItm.Geometry
		#elif toolbarItm[buttonName].Checked == True:
		if toolbarItm[buttonName].Checked == True:
			print("[Lightfielder][Toolbar][Button][Checked State][True]")
			# If the button is unchecked then hide the window if the window is open
			if winItm != None:
				if buttonModifierAlt == True:
					print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Stack Window] " + str(winName))
				elif buttonModifier == False and buttonModifierControl == False:
					print("[Lightfielder][Toolbar][Button]" + str(buttonName) + "] [Hide Window] " + str(winName))
					winItm.Hide()
				elif buttonModifierControl == True:
					# Hold down the control key when clicking on a toolbar item to edit the script in a programmer's text editor
					# This feature requires the "xdg-open" package to be installed on Linux.
					print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Edit this Window] " + str(winName) + " [Script Edit] " + str(selectedScript))
					ExternalEditor(selectedScript)
				else:
					# If the button is unchecked hold down the shift key to force-close the window if the window is open
					print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Close Window] " + str(winName))
					winItm.Close()
	else:
		# Error handling fallback stats
		print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [NOP] Don't do anything at all")

# Display the 01 Preferences window
# Example: ShowPrefsWindow(True)
def ShowPrefsWindow(boolState):
	winItm = GetWindow("PrefsWin")
	if winItm == None or winItm == "":
		# Look up the script name
		selectedScript = app.MapPath("Lightfielder:/Resolve/Scripts/Utility/Lightfielder/01 Preferences.py")
		print("[Lightfielder][Run the Script] " + str(selectedScript))
		execfile(selectedScript)

# Check the operating system
# Example: currentOS = GetPlatform()
def GetPlatform():
	import platform
	currentOS = ""
	if platform.system() == "Windows":
		currentOS = "Windows"
	elif platform.system() == "win32":
		currentOS = "Windows"
	elif platform.system()== "Darwin":
		currentOS = "Mac"
	elif platform.system() == "Linux":
		currentOS = "Linux"
	elif platform.system() == "Linux2":
		currentOS = "Linux"
	else:
		currentOS = "Linux"
	# print("Running on " + currentOS + "\n")
	return currentOS

def ShowFolderFromFilepath(filename):
	if filename != "":
		folderAbs = app.MapPath(os.path.dirname(filename))
		print("[Lightfielder][Show Output Folder] ", folderAbs)
		# Create the folder
		if not os.path.exists(folderAbs):
			os.makedirs(folderAbs)
			print("[Lightfielder][Make Directory] ", folderAbs)
		app.Execute('bmd.openfileexternal("Open", [[' + str(folderAbs) + ']])')
	else:
		print("[Lightfielder][Show Output Folder] The text field is empty.")

def ShowFolder(folder):
	if folder != "":
		folderAbs = app.MapPath(folder)
		print("[Lightfielder][Show Output Folder] ", folderAbs)
		# Create the folder
		if not os.path.exists(folderAbs):
			os.makedirs(folderAbs)
			print("[Lightfielder][Make Directory] ", folderAbs)
		app.Execute('bmd.openfileexternal("Open", [[' + str(folderAbs) + ']])')
	else:
		print("[Lightfielder][Show Output Folder] The text field is empty.")

def ShowHelpTopic(docsTopic):
	# docsTopic = "/Docs/Scripts_10_Batch_Trim.md"

	# Is the preferences window "Use Local Help" checkbox enabled?
	useLocalHelp = app.GetData("Lightfielder.UseLocalHelp")

	if useLocalHelp is None or useLocalHelp == False:
		# Use online GitHub repo hosted help docs
		# None or False

		# This is the Lightfielder beta help content link:
		weblink = "https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve/blob/main/Lightfielder/" + str(docsTopic)

		print("[Lightfielder][Showing Help Topic] " + str(weblink))
		ShowWebpage(weblink)
	else:
		# Use the local help docs
		docsfile = str(app.MapPath("Lightfielder:/" + str(docsTopic)))
		print("[Lightfielder][Showing Local Help Topic] " + str(docsfile))
		ShowWebpage(docsfile)

def ShowInDefaultProgram(filename):
	currentOS = GetPlatform()
	viewerPath = ""
	args = ""
	launchCommand = ""
	if currentOS == "Mac":
		args = "--args"
		launchCommand = ["open"]
		launchCommand.append(filename)

		print("[Launching Command]\n")
		print(launchCommand)
		import subprocess
		subprocess.Popen(launchCommand)
	elif currentOS == "Windows":
		# Open the folder in Explorer (Win), Finder (macOS), and xdg-open (Linux)
		os.startfile(filename)
	elif currentOS == "Linux":
		launchCommand = ["xdg-open"]
		launchCommand.append(filename)

		print("[Launching Command]\n")
		print(launchCommand)
		import subprocess
		subprocess.Popen(launchCommand)

def ShowWebpage(filename):
	currentOS = GetPlatform()
	viewerPath = ""
	args = ""
	launchCommand = ""
	if currentOS == "Mac":
		args = "--args"
		launchCommand = ["open"]
		launchCommand.append(filename)

		print("[Launching Command]\n")
		print(launchCommand)
		import subprocess
		subprocess.Popen(launchCommand)
	elif currentOS == "Windows":
		# Open the folder in Explorer (Win), Finder (macOS), and xdg-open (Linux)
		os.startfile(filename)
	elif currentOS == "Linux":
		launchCommand = ["xdg-open"]
		launchCommand.append(filename)

		print("[Launching Command]\n")
		print(launchCommand)
		import subprocess
		subprocess.Popen(launchCommand)

def GetProject():
	# Get the current Resolve timeline
	res = app.GetResolve()
	projectManager = res.GetProjectManager()
	project = projectManager.GetCurrentProject()
	if project is None:
		print("[Lightfielder] No Resolve project is open at this time.")
		ErrorWindow("Lightfielder", "No Resolve project is open at this time.")
		exit()
	else:
		return project

def GetTimeline():
	project = GetProject()
	timeline = project.GetCurrentTimeline()

	if not timeline:
		if project.GetTimelineCount() > 0:
			timeline = project.GetTimelineByIndex(1)
			project.SetCurrentTimeline(timeline)

	return timeline

def GetMediaPool():
	resolve = app.GetResolve()
	projectManager = resolve.GetProjectManager()
	project = projectManager.GetCurrentProject()
	mediapool = project.GetMediaPool()
	return mediapool

def GetFolder(parentFolder, childFolder, mediapool):
	if parentFolder != None:
		for folder in parentFolder.GetSubFolderList():
			if folder.GetName() == childFolder:
				return folder
		else:
			return mediapool.AddSubFolder(parentFolder, childFolder)
	else:
		return None

#
# # Bin folders
# binFolderItems = []
# def GetSubFolder(parentFolder, path):
# 	for folder in parentFolder.GetSubFolderList():
# 		if path != "":
# 			updatedPath = str(path) + "/" + str(folder.GetName())
# 		else:
# 			updatedPath = str(folder.GetName())
# 		binFolderItems.append(updatedPath)
# 		# Scan Deeper
# 		GetSubFolder(folder, updatedPath)


# def GetSubFolder(parentFolder, path):
# 	for folder in parentFolder.GetSubFolderList():
# 		if path != "":
# 			updatedPath = str(path) + "/" + str(folder.GetName())
# 		else:
# 			updatedPath = str(folder.GetName())
# 		FilepathItems.append(updatedPath)
# 		FolderItems.append(folder)
#
# 		# Scan Deeper
# 		GetSubFolder(folder, updatedPath)

def GetRenderJob(project, jobId):
	jobList = project.GetRenderJobList()
	for jobDetail in jobList:
		if jobDetail["JobId"] == jobId:
			return jobDetail
	return ""

def GetHTMLFiles(dirPath):
	# Was originally called "GetFiles(dirPath)"
	matches = []
	for root, dirnames, filenames in os.walk(app.MapPath(dirPath)):
		for file in filenames:
			# The double parenthesis are used in the endswith() function to make the file types into a tupple like list
			if file.endswith(('.html', '.HTML')) and not file.startswith("."):
				matches.append(os.path.join(root, file))

	# Sort the filenames alphabetically in descending order
	matches.sort()

	return matches

def GetPyFiles(dirPath):
	# Was originally called "GetFiles(dirPath)"
	matches = []
	for root, dirnames, filenames in os.walk(app.MapPath(dirPath)):
		for file in filenames:
			# The double parenthesis are used in the endswith() function to make the file types into a tupple like list
			if file.endswith('.py') and not file.startswith("."):
				matches.append(os.path.join(root, file))

	# Sort the filenames alphabetically in descending order
	matches.sort()

	return matches

def GetPythonBinFilepath(program):
	# path = GetPythonBinFilepath("jupyter-notebook")
	# print(sys.version)
	# print(sys.prefix)

	# Probe the active Python version to create Jupyter filepath like:
	# /Library/Frameworks/Python.framework/Versions/3.10/bin/jupyter-notebook
	return os.path.join(sys.prefix, "bin", program)

def GetMediaFiles(dirPath):
	# Note: The double parenthesis are used in the endswith() function to make the file types into a tupple like list
	
	# Check what type of footage to import
	mediaFormat = app.GetData("Lightfielder.MediaFormat") or "R3D"

	matches = []
	for root, dirnames, filenames in os.walk(app.MapPath(dirPath)):
		for file in filenames:
			if not file.startswith("."):
				if mediaFormat == "R3D" and file.endswith(('.R3D', '.r3d')):
					# Red Digital Cinema R3D RAW
					matches.append(os.path.join(root, file))
				elif mediaFormat == "Movie" and file.endswith(('.MOV', '.mov', '.MP4', '.mp4', '.MKV', '.mkv')):
					# Quicktime, MP4, MKV video
					matches.append(os.path.join(root, file))
				elif (mediaFormat == "Image Sequence" or mediaFormat == "Still Frame") and file.endswith(('.PNG', '.png', '.JPEG', '.jpeg', '.JPG', '.jpg', '.EXR', '.exr', '.DPX', '.dpx', '.TIF', '.TIFF', '.tif', '.tiff')):
					# PNG, JPEG, EXR, DPX, TIFF,
					matches.append(os.path.join(root, file))
				else:
					# Fallback: Unknown media format from the preferences
					# Red Digital Cinema R3D RAW
					if file.endswith(('.R3D', '.r3d')):
						matches.append(os.path.join(root, file))

	# Sort the filenames alphabetically in descending order
	matches.sort()

	return matches

def SplitMediaFilename(clipName, cameraArrayGeometry):
	# Todo: For image sequences we will have to handle more than 3 digits of frame numbers

	# Check what type of footage to import
	mediaFormat = app.GetData("Lightfielder.MediaFormat") or "R3D"

	# AA-JE
	viewCol = ""
	viewRow = ""
	# 001-999
	clipID = ""
	dateID = ""

	viewColNum = ""

	# .r3d sub-clip items
	subClip = 0

	pattern = ""
	# Regular expressions matching pattern for a RED filename like "F001_D050_0309BX_001.R3D"
	# The revised RED filename appears to have an extra trailing month/day field digit "01286" vs the earlier "0309".
	# (?P<extra>[0-9]*)                     # Extra 0-9 (This is new and optional)
	# (?P<month>[0-9][0-9])                 # Month 01-12
	# (?P<day>[0-9][0-9])                   # Day 01-31

	# Sub-cliping sequence naming example:
	# A001_A004_1003RH_008.R3D
	# A001_A004_1003RH_001.R3D
	# A001_A004_1003RH_004.R3D
	# A001_A004_1003RH_006.R3D
	# A001_A004_1003RH_003.R3D
	# A001_A004_1003RH_005.R3D
	# A001_A004_1003RH_002.R3D
	# A001_A004_1003RH_007.R3D

	if (cameraArrayGeometry == 0 or cameraArrayGeometry == 1) or cameraArrayGeometry == None:
		# Rectangular Example: A001_A004_1003RH_001.R3D
		pattern = r"""
^                                     # Start of line
(?P<col>[A-Z])                        # Array Col A-J
([0-9][0-9][0-9])                     # Number 001-999
([_])                                 # Underscore separator
(?P<row>[A-Z])                        # Array Row A-E
(?P<id>[0-9][0-9][0-9])               # Number 001-999 (Clip ID)
([_])                                 # Underscore separator
(?P<date>[0-9][0-9][0-9][0-9])        # Month 01-12 Day 01-31
([A-Z0-9][A-Z0-9])                    # Letters + Numbers AA-99
([_])                                 # Underscore separator
(?P<subclip>[0-9][0-9][0-9][0-9]?[0-9]?[0-9]?) # Subclip Item Number 001-999 or 0001-9999 or 00001-99999 or 000001-999999
([.][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]?) # File Extension
$                                     # End of line
"""

		# Process a regular expression based named group
		# print("\t\t[Lightfielder][R3D RegEx] "      + str(clipName))
		pat = re.compile(pattern, re.VERBOSE)
		mat = pat.match(clipName)
		result = None
		if mat != None or mat == "":
			m = mat.groupdict()
			if m != None:
				# print("\t\t[Lightfielder][Media Pattern] "    + str(pattern))
				# print("\t\t\t[Lightfielder][Media Match] " + str(m))
				# print(m)
				if m:
					if "subclip" in m:
						subClip = int(float(m["subclip"]))
						if "id" in m:
							clipID = int(float(m["id"]))
							#clipID = m["id"]
						if "col" in m:
							viewCol = m["col"]
						if "row" in m:
							viewRow = m["row"]
						if "date" in m:
							dateID = m["date"]

						# After passing the regex operation return the values
						if mediaFormat == "R3D" and clipName.endswith(('.R3D', '.r3d')):
							# Red Digital Cinema R3D RAW
							return dateID, clipID, viewCol, viewRow, subClip
						elif mediaFormat == "Movie" and clipName.endswith(('.MOV', '.mov', '.MP4', '.mp4', '.MKV', '.mkv')):
							# Quicktime MOV, MP4, MKV video
							return dateID, clipID, viewCol, viewRow, subClip
						elif (mediaFormat == "Image Sequence" or mediaFormat == "Still Frame") and clipName.endswith(('.PNG', '.png', '.JPEG', '.jpeg', '.JPG', '.jpg', '.EXR', '.exr', '.DPX', '.dpx', '.TIF', '.TIFF', '.tif', '.tiff')):
							# PNG, JPEG, EXR, DPX, TIFF
							return dateID, clipID, viewCol, viewRow, subClip
		else:
			print("\t\t\t[Lightfielder][Media Match Error] Line 1050 - Empty Pattern. Check the shotlog CSV formatting and media filenames for changes.")
	elif cameraArrayGeometry == 2:
		# Polar Example: A150_A001_1030BH_001.R3D
		pattern = r"""
^                                     # Start of line
(?P<col>[A-Z])                        # Array Col A-R,
(?P<colnum>[0-9][0-9][0-9])           # Vertical Row Number 1-5, Rig Section Sub-divison 1-7, Vertical Row Sub-divison 1-7
([_])                                 # Underscore separator
(?P<row>[A-Z])                        # Array Row A-E
(?P<id>[0-9][0-9][0-9])               # Number 001-999 (Clip ID)
([_])                                 # Underscore separator
(?P<date>[0-9][0-9][0-9][0-9])        # Month 01-12 Day 01-31
([A-Z0-9][A-Z0-9])                    # Letters + Numbers AA-99
([_])                                 # Underscore separator
(?P<subclip>[0-9][0-9][0-9][0-9]?[0-9]?[0-9]?) # Subclip Item Number 001-999 or 0001-9999 or 00001-99999 or 000001-999999
([.][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]?) # File Extension
$                                     # End of line
"""

		# Process a regular expression based named group
		# print("\t\t[Lightfielder][R3D RegEx] "      + str(clipName))
		pat = re.compile(pattern, re.VERBOSE)
		mat = pat.match(clipName)
		result = None
		if mat != None or mat == "":
			m = mat.groupdict()
			if m != None:
				# print("\t\t[Lightfielder][Media Pattern] "    + str(pattern))
				# print("\t\t\t[Lightfielder][Media Match] " + str(m))
				# print(m)

				if m:
					if "subclip" in m:
						subClip = int(float(m["subclip"]))
						if "id" in m:
							clipID = int(float(m["id"]))
							#clipID = m["id"]
						if "col" in m:
							viewCol = m["col"]
						if "colnum" in m:
							viewColNum = m["colnum"]
						if "row" in m:
							viewRow = m["row"]
						if "date" in m:
							dateID = m["date"]
						if viewCol != None and viewColNum != None:
							# Append the view
							viewCol += str(viewColNum)
						# After passing the regex operation return the values
						if mediaFormat == "R3D" and clipName.endswith(('.R3D', '.r3d')):
							# Red Digital Cinema R3D RAW
							return dateID, clipID, viewCol, viewRow, subClip
						elif mediaFormat == "Movie" and clipName.endswith(('.MOV', '.mov', '.MP4', '.mp4', '.MKV', '.mkv')):
							# Quicktime MOV, MP4, MKV video
							return dateID, clipID, viewCol, viewRow, subClip
						elif (mediaFormat == "Image Sequence" or mediaFormat == "Still Frame") and clipName.endswith(('.PNG', '.png', '.JPEG', '.jpeg', '.JPG', '.jpg', '.EXR', '.exr', '.DPX', '.dpx', '.TIF', '.TIFF', '.tif', '.tiff')):
							# PNG, JPEG, EXR, DPX, TIFF
							return dateID, clipID, viewCol, viewRow, subClip
		else:
			print("\t\t\t[Lightfielder][Media Match Error]Line 1109 - Empty Pattern. Check the shotlog CSV formatting and media filenames for changes.")

	# These values should be empty strings
	return dateID, clipID, viewCol, viewRow, subClip

def GetClips():
	project = GetProject()
	mediapool = project.GetMediaPool()

	# Get the timeline object
	timeline = GetTimeline()

	# Get the track count
	timelineVideoTrackCount = timeline.GetTrackCount("video")

	# Store the current timeline clips
	clipDict = []

	# Get the track structure
	for i in range(1, int(timelineVideoTrackCount) + 1):
		# Check if the video track is enabled
		if timeline.GetIsTrackEnabled("video", i) == True:
			# Get the clips in the track
			clips = timeline.GetItemListInTrack("video", i)
			for clip in clips:
				cProp = clip.GetProperty()

				mpItem = clip.GetMediaPoolItem()
				mpProp = mpItem.GetClipProperty()
				mpID = mpItem.GetMediaId()

				mpStartTC = str(mpItem.GetClipProperty("Start TC"))
				mpEndTC = str(mpItem.GetClipProperty("End TC"))
				mpDuration = mpItem.GetClipProperty("Duration")
				mpFile = str(mpItem.GetClipProperty("File Path"))

				clipDuration = float(clip.GetDuration())
				clipStart = float(clip.GetStart())
				clipEnd = float(clip.GetEnd())
				clipName = str(clip.GetName())

				dateID, clipID, clipViewCol, clipViewRow, subClip = SplitMediaFilename(clipName)
				# The angle holds a CCS view name like AA-JE
				angle = str(clipViewCol) + str(clipViewRow)

				clipDict.append({
					"SourceFilename": mpFile,
					"ClipName": clipName,
					"Angle": angle,
					"ClipID": clipID,
					"StartFrame": clipStart,
					"EndFrame": clipEnd,
					"Duration": clipDuration,
					"TrackIndex": i})

	return clipDict

def FindVideoClips(folder):
	clipItems = []

	if folder != None:
		clips = folder.GetClips()
		for key in clips:
			clip = clips[key]
			if (clip.GetClipProperty("Type") == "Video") or (clip.GetClipProperty("Type") == "Video + Audio"):
				clipItems.append(clip)

	return clipItems

def FindVideoClipPath(folder, filepath):
	clipItems = []
	fileItems = []

	if folder != None:
		clips = folder.GetClips()
		for key in clips:
			clip = clips[key]
			if (clip.GetClipProperty("Type") == "Video") or (clip.GetClipProperty("Type") == "Video + Audio"):
				mpFile = str(clip.GetClipProperty("File Path"))
				#clipItems.append(clip)
				#fileItems.append(mpFile)
				if app.MapPath(mpFile) == app.MapPath(filepath):
					return mpFile, clip

	return None, None

def FindTimelineClips(folder):
	timelineItems = []

	if folder != None:
		clips = folder.GetClips()
		for key in clips:
			clip = clips[key]
			if (clip.GetClipProperty("Type") == "Timeline"):
				timelineItems.append(clip)

	return timelineItems

def FindTimelineByName(folder, name):
	timelines = FindTimelineClips(folder)

	if folder != None:
		if (name != None) and (name != ""):
			for timeline in timelines:
				if (timeline != None) and (timeline.GetName() == name):
					return timeline

	return None

def FindTimelineBin():
	return FindRootLevelBin("timelines")

def FindTimelineStillFramesBin():
	project = GetProject()
	mediapool = project.GetMediaPool()

	timelinesBinName, timelinesBin = FindTimelineBin()
	folder = GetFolder(timelinesBin, "still_frames", mediapool)
	if folder != None:
		binName = folder.GetName()
		return binName, folder

	return None, None

def FindTimelineShotTypeBin(BinName):
	project = GetProject()
	mediapool = project.GetMediaPool()

	timelinesBinName, timelinesBin = FindTimelineBin()
	folder = GetFolder(timelinesBin, BinName, mediapool)
	if folder != None:
		binName = folder.GetName()
		return binName, folder

	return None, None

def FindRootLevelBin(folderName):
	project = GetProject()
	mediapool = project.GetMediaPool()
	rootFolder = mediapool.GetRootFolder()

	if len(rootFolder.GetSubFolderList()) == 0:
		print("[Lightfielder] There are zero bins in this project! You might want to run the \"Bin Templates\" script to set up the initial bin hierarchy so you have a \"" + str(folderName) + "\" bin.")
		ErrorWindow("Error", "There are zero bins in this project! You might want to run the \"Bin Templates\" script to set up the initial bin hierarchy so you have a \"" + str(folderName) + "\" bin.")
		return None, None

	# Bin folders
	for folder in rootFolder.GetSubFolderList():
		if folder != None:
			# Current bin item
			binName = folder.GetName()

			# Regular expressions matching pattern for a "02_footage" like bin name
			pattern = r"""
	^                                     # Start of line
	(?P<order>[0-9][0-9])                 # Number prefix [00-99]
	([_\-])                               # Underscore or hyphen separator
	(?P<name>.*)                          # Any Characters (Bin Name)
	$                                     # End of line
	"""
			# Process a regular expression based named group
			pat = re.compile(pattern, re.VERBOSE)
			mat = pat.match(binName)
			result = None
			if mat:
				m = mat.groupdict()
				#print(m)
				if m:
					if "name" in m:
						if str(m["name"]) == folderName:
							return binName, folder

	return None, None

def FindFootageBin():
	return FindRootLevelBin("footage")

def ResetPreferences():
	# Reset the Lightfielder preferences stored in the Fusion.prefs file.
	print("[Lightfielder][Preferences] Resetting to the default values")
	app.SetData("Lightfielder", None)

def GetMaxNumberOfCameras():
	# defaults to 50 views in the array
	maxCameras = 50

	# defaults to A1-EJ Array geometry
	cameraArrayGeometry = 0

	# Get the camera array type
	pref = app.GetData("Lightfielder.ArrayGeometry")
	if pref != None:
		cameraArrayGeometry = int(pref)
	else:
		# No preference was set
		print("[Lightfielder][Preferences] No initial camera array geometry was defined. Falling back to a default value of A1-EJ.")
		app.SetData("Lightfielder.ArrayGeometry", 0)

	# Get the number of cameras views in the array
	pref = app.GetData("Lightfielder.NumberOfCameras")
	if pref != None:
		maxCameras = int(pref)
	else:
		# No preference was set
		if cameraArrayGeometry == 0 or cameraArrayGeometry == 1:
			# Planar Grid and Wedge Array
			print("[Lightfielder][Preferences] No initial number of cameras was defined. Falling back to a default value of 50 camera views.")
			app.SetData("Lightfielder.NumberOfCameras", 50)
		else:
			# Polar Array
			print("[Lightfielder][Preferences] No initial number of cameras was defined. Falling back to a default value of 55 camera views.")
			app.SetData("Lightfielder.NumberOfCameras", 55)

	return maxCameras

def GetSensorFrameRate():
	# Read the frame rate from the preferences
	# Return a non-drop frame frame rate as an integer value
	fps = 60

	custom = app.GetData("Lightfielder.SensorFrameRateCustom")
	fps = app.GetData("Lightfielder.SensorFrameRate")
	if fps != None:
		if fps == "24 FPS":
			fps = 24
		elif fps == "25 FPS":
			fps = 25
		elif fps == "30 FPS":
			fps = 30
		elif fps == "48 FPS":
			ifps = 48
		elif fps == "50 FPS":
			fps = 50
		elif fps == "60 FPS":
			fps = 60
		elif fps == "90 FPS":
			fps = 90
		elif fps == "100 FPS":
			fps = 100
		elif fps == "120 FPS":
			fps = 120
		elif fps == "Custom":
			if custom != None:
				# Read the custom frame rate value
				fps = custom
			else:
				fps = 60
			print("[Lightfielder][Fallback][Sensor Frame Rate] Used a default value of 60 FPS")
		else:
			# Todo: Custom Fallback Rate
			fps = 60
			print("[Lightfielder][Fallback][Sensor Frame Rate] Used a default value of 60 FPS")
	else:
		# No preference was set
		print("[Lightfielder][Fallback][Sensor Frame Rate] Used a default value of 60 FPS")
		app.SetData("Lightfielder.SensorFrameRate", 60)

	app.SetData("Lightfielder.SensorFrameRate", fps)
	return fps


def GetProjectFrameRate():
	# Read the frame rate from the preferences
	# Return a non-drop frame frame rate as an integer value
	fps = 60

	custom = app.GetData("Lightfielder.ProjectFrameRateCustom")
	fps = app.GetData("Lightfielder.ProjectFrameRate")
	if fps != None:
		if fps == "24 FPS":
			fps = 24
		elif fps == "25 FPS":
			fps = 25
		elif fps == "30 FPS":
			fps = 30
		elif fps == "48 FPS":
			ifps = 48
		elif fps == "50 FPS":
			fps = 50
		elif fps == "60 FPS":
			fps = 60
		elif fps == "90 FPS":
			fps = 90
		elif fps == "100 FPS":
			fps = 100
		elif fps == "120 FPS":
			fps = 120
		elif fps == "Custom":
			if custom != None:
				# Read the custom frame rate value
				fps = custom
			else:
				fps = 60
			print("[Lightfielder][Fallback][Project Frame Rate] Used a default value of 60 FPS")
		else:
			# Todo: Custom Fallback Rate
			fps = 60
			print("[Lightfielder][Fallback][Project Frame Rate] Used a default value of 60 FPS")
	else:
		# No preference was set
		print("[Lightfielder][Fallback][Project Frame Rate] Used a default value of 60 FPS")
		app.SetData("Lightfielder.ProjectFrameRate", 60)

	app.SetData("Lightfielder.ProjectFrameRate", fps)
	return fps

def GetColorByIndex(idx):
	color = ""

	# Rotate through the available 16 color range
	# index = (idx - 1) % 16 + 1

	# Ping-pong rotate through the available 16 color range
	x = (idx - 1) % 30
	if x < 16:
		index = x + 1
	else:
		index = 31 - x

	if index == 1:
		color = "Orange"
	elif index == 2:
		color = "Apricot"
	elif index == 3:
		color = "Yellow"
	elif index == 4:
		color = "Lime"
	elif index == 5:
		color = "Olive"
	elif index == 6:
		color = "Green"
	elif index == 7:
		color = "Teal"
	elif index == 8:
		color = "Navy"
	elif index == 9:
		color = "Blue"
	elif index == 10:
		color = "Purple"
	elif index == 11:
		color = "Violet"
	elif index == 12:
		color = "Pink"
	elif index == 13:
		color = "Tan"
	elif index == 14:
		color = "Beige"
	elif index == 15:
		color = "Brown"
	elif index == 16:
		color = "Chocolate"
	
	return GetColor(color), color

def GetColor(color):
	# Get the color
	Black = {
		"R": 0.0,
		"G": 0.0,
		"B": 0.0,
		"A": 1.00,
	}
	White = {
		"R": 1.0,
		"G": 1.0,
		"B": 1.0,
		"A": 1.00,
	}
	Orange = {
		"R": 0.916,
		"G": 0.422,
		"B": 0.113,
		"A": 1.00,
	}
	Apricot = {
		"R": 0.998,
		"G": 0.654,
		"B": 0.254,
		"A": 1.00,
	}
	Yellow = {
		"R": 0.834,
		"G": 0.676,
		"B": 0.196,
		"A": 1.00,
	}
	Lime = {
		"R": 0.639,
		"G": 0.778,
		"B": 0.183,
		"A": 1.00,
	}
	Olive = {
		"R": 0.391,
		"G": 0.602,
		"B": 0.174,
		"A": 1.00,
	}
	Green = {
		"R": 0.286,
		"G": 0.563,
		"B": 0.402,
		"A": 1.00,
	}
	Teal = {
		"R": 0.084,
		"G": 0.599,
		"B": 0.598,
		"A": 1.00,
	}
	Navy = {
		"R": 0.000,
		"G": 0.323,
		"B": 0.465,
		"A": 1.00,
	}
	Blue = {
		"R": 0.260,
		"G": 0.464,
		"B": 0.625,
		"A": 1.00,
	}
	Purple = {
		"R": 0.593,
		"G": 0.445,
		"B": 0.623,
		"A": 1.00,
	}
	Violet = {
		"R": 0.806,
		"G": 0.328,
		"B": 0.551,
		"A": 1.00,
	}
	Pink = {
		"R": 0.784,
		"G": 0.478,
		"B": 0.618,
		"A": 1.00,
	}
	Tan = {
		"R": 0.727,
		"G": 0.686,
		"B": 0.597,
		"A": 1.00,
	}
	Beige = {
		"R": 0.768,
		"G": 0.626,
		"B": 0.495,
		"A": 1.00,
	}
	Brown = {
		"R": 0.599,
		"G": 0.397,
		"B": 0.080,
		"A": 1.00,
	}
	Chocolate = {
		"R": 0.547,
		"G": 0.350,
		"B": 0.256,
		"A": 1.00,
	}

	if color == "White":
		return White
	elif color == "Black":
		return Black
	elif color == "Orange":
		return Orange
	elif color == "Apricot":
		return Apricot
	elif color == "Yellow":
		return Yellow
	elif color == "Lime":
		return Lime
	elif color == "Olive":
		return Olive
	elif color == "Green":
		return Green
	elif color == "Teal":
		return Teal
	elif color == "Navy":
		return Navy
	elif color == "Blue":
		return Blue
	elif color == "Purple":
		return Purple
	elif color == "Violet":
		return Violet
	elif color == "Pink":
		return Pink
	elif color == "Tan":
		return Tan
	elif color == "Beige":
		return Beige
	elif color == "Brown":
		return Brown
	elif color == "Chocolate":
		return Chocolate

def GetCameraNumber(number):
	if number == 1:
		return "AA"
	elif number == 6:
		return "BA"
	elif number == 11:
		return "CA"
	elif number == 16:
		return "DA"
	elif number == 21:
		return "EA"
	elif number == 26:
		return "FA"
	elif number == 31:
		return "GA"
	elif number == 36:
		return "HA"
	elif number == 41:
		return "IA"
	elif number == 46:
		return "JA"
	elif number == 2:
		return "AB"
	elif number == 7:
		return "BB"
	elif number == 12:
		return "CB"
	elif number == 17:
		return "DB"
	elif number == 22:
		return "EB"
	elif number == 27:
		return "FB"
	elif number == 32:
		return "GB"
	elif number == 37:
		return "HB"
	elif number == 42:
		return "IB"
	elif number == 47:
		return "JB"
	elif number == 3:
		return "AC"
	elif number == 8:
		return "BC"
	elif number == 13:
		return "CC"
	elif number == 18:
		return "DC"
	elif number == 23:
		return "EC"
	elif number == 28:
		return "FC"
	elif number == 33:
		return "GC"
	elif number == 38:
		return "HC"
	elif number == 43:
		return "IC"
	elif number == 48:
		return "JC"
	elif number == 4:
		return "AD"
	elif number == 9:
		return "BD"
	elif number == 14:
		return "CD"
	elif number == 19:
		return "DD"
	elif number == 24:
		return "ED"
	elif number == 29:
		return "FD"
	elif number == 34:
		return "GD"
	elif number == 39:
		return "HD"
	elif number == 44:
		return "ID"
	elif number == 49:
		return "JD"
	elif number == 5:
		return "AE"
	elif number == 10:
		return "BE"
	elif number == 15:
		return "CE"
	elif number == 20:
		return "DE"
	elif number == 25:
		return "EE"
	elif number == 30:
		return "FE"
	elif number == 35:
		return "GE"
	elif number == 40:
		return "HE"
	elif number == 45:
		return "IE"
	elif number == 50:
		return "JE"
	else:
		return None

def GetCameraName(name):
	camDict = {
		"AA": 1,
		"BA": 6,
		"CA": 11,
		"DA": 16,
		"EA": 21,
		"FA": 26,
		"GA": 31,
		"HA": 36,
		"IA": 41,
		"JA": 46,
		"AB": 2,
		"BB": 7,
		"CB": 12,
		"DB": 17,
		"EB": 22,
		"FB": 27,
		"GB": 32,
		"HB": 37,
		"IB": 42,
		"JB": 47,
		"AC": 3,
		"BC": 8,
		"CC": 13,
		"DC": 18,
		"EC": 23,
		"FC": 28,
		"GC": 33,
		"HC": 38,
		"IC": 43,
		"JC": 48,
		"AD": 4,
		"BD": 9,
		"CD": 14,
		"DD": 19,
		"ED": 24,
		"FD": 29,
		"GD": 34,
		"HD": 39,
		"ID": 44,
		"JD": 49,
		"AE": 5,
		"BE": 10,
		"CE": 15,
		"DE": 20,
		"EE": 25,
		"FE": 30,
		"GE": 35,
		"HE": 40,
		"IE": 45,
		"JE": 50,
	}
	return camDict[name]

def GetCameras():
	return [
		"AA",
		"BA",
		"CA",
		"DA",
		"EA",
		"FA",
		"GA",
		"HA",
		"IA",
		"JA",
		"AB",
		"BB",
		"CB",
		"DB",
		"EB",
		"FB",
		"GB",
		"HB",
		"IB",
		"JB",
		"AC",
		"BC",
		"CC",
		"DC",
		"EC",
		"FC",
		"GC",
		"HC",
		"IC",
		"JC",
		"AD",
		"BD",
		"CD",
		"DD",
		"ED",
		"FD",
		"GD",
		"HD",
		"ID",
		"JD",
		"AE",
		"BE",
		"CE",
		"DE",
		"EE",
		"FE",
		"GE",
		"HE",
		"IE",
		"JE",
	]


def GetJSONConfigViews(jsonFile, displayMode):
	# Reads the camera array JSON file and returns a list of camera view position strings like "A220"
	# Note: displayMode = "dump" does a JSON log dump
	# Note: displayMode = "sensorfps" returns the JSON sensor frame rate
	# Note: displayMode = "projectfps" returns the JSON project frame rate
	# Note: displayMode = "views" returns how many cameras exist
	# Note: displayMode = "records" parses the JSON for camera array values
	cameraItems = []

	# Open the JSON log file and read it line by line
	print("[Lightfielder][JSON Config Views] [File] " + str(jsonFile) + " [Mode] " + str(displayMode))
	try:
		with open(jsonFile, "r") as f:
			j = json.load(f)
			# Format the data for terminal output
			if displayMode == "dump":
				# Add indentations to the json data to make it easier to read
				print(json.dumps(j, ensure_ascii = True, indent = "\t"))
			elif displayMode == "sensorfps":
				# Display a short summary of the info
				if "required_configuration" in j:
					config = len(j["required_configuration"])
					# print("\t[config] " + str(config))
					if config != None:
						try:
							for c in j["required_configuration"]:
								if "SENSOR_FRAME_RATE" in c:
									fps = j["required_configuration"]["SENSOR_FRAME_RATE"]["str"]
									# print(fps)
									return fps
						except StopIteration:
							pass
			elif displayMode == "projectfps":
				# Display a short summary of the info
				if "required_configuration" in j:
					config = len(j["required_configuration"])
					# print("\t[config] " + str(config))
					if config != None:
						try:
							for c in j["required_configuration"]:
								if "PROJECT_FRAME_RATE" in c:
									fps = j["required_configuration"]["PROJECT_FRAME_RATE"]["str"]
									# print(fps)
									return fps
						except StopIteration:
							pass
			elif displayMode == "views":
				# return the number of camera views as an integer number
				if "controlBoxes" in j:
					controllerCount = len(j["controlBoxes"])
					# print("\t[Controllers] " + str(controllerCount))
					if controllerCount != None:
						for c in j["controlBoxes"]:
							if "ports" in c:
								portCount = len(c["ports"])
								# print("\t\t[Ports] ", portCount)
								for p in c["ports"]:
									try:
										## A1 - J5
										cameras = str(c["cameras"][p-1])

										# AA - DE
										cameraAlias = str(c["cameraAlias"][p-1])

										# 0, 210 - 650
										cameraPosition = str(c["cameraPosition"][p-1]).zfill(3)

										# Reposition Letters A220B
										cameraLabel = str(cameraAlias[:-1]) + str(cameraPosition)
										if cameras != None and cameras != "--":
											#cameraItems.append([cameras, cameraAlias, cameraPosition])
											#cameraItems.append([cameraLabel])
											cameraItems.append(cameraLabel)
									except StopIteration:
										pass
				cameraItems.sort()
				return len(cameraItems)
			elif displayMode == "records":
				# Display a short summary of the info
				if "controlBoxes" in j:
					controllerCount = len(j["controlBoxes"])
					# print("\t[Controllers] " + str(controllerCount))
					if controllerCount != None:
						for c in j["controlBoxes"]:
							if "ports" in c:
								portCount = len(c["ports"])
								# print("\t\t[Ports] ", portCount)
								for p in c["ports"]:
									try:
										## A1 - J5
										cameras = str(c["cameras"][p-1])

										# AA - DE
										cameraAlias = str(c["cameraAlias"][p-1])

										# 0, 210 - 650
										cameraPosition = str(c["cameraPosition"][p-1]).zfill(3)

										# Reposition Letters A220B
										cameraLabel = str(cameraAlias[:-1]) + str(cameraPosition)
										if cameras != None and cameras != "--":
											#cameraItems.append([cameras, cameraAlias, cameraPosition])
											#cameraItems.append([cameraLabel])
											cameraItems.append(cameraLabel)
									except StopIteration:
										pass
			cameraItems.sort()
			#print("[Cameras]", len(cameraItems))
			#if cameraItems != None:
			#	for c in cameraItems:
			#		print("\t", c)
	except OSError as error:
		print("\tLightfielder][Exception][JSON Get Error]", error)

	return cameraItems

def GetMissingViews(cID, clips, cameraArrayGeometry, cameraJSONConfigViews):
	camViewItems = []
	camNumItems = []
	missingCamNumItems = []
	missingCamViewItems = []
	result = []

	# Get the number of cameras views in the array
	maxCameras = GetMaxNumberOfCameras()

	if cameraArrayGeometry == 0 or cameraArrayGeometry == 1:
		# Planar Grid and Wedge array
		if clips != None:
			for clip in clips:
				mpFile = str(clip.GetClipProperty("File Path"))
				clipFileName = os.path.basename(app.MapPath(mpFile))
				dateID, clipID, clipViewCol, clipViewRow, subClip = SplitMediaFilename(clipFileName, cameraArrayGeometry)
				if (clipID != None) and (cID != None):
					if int(clipID) == int(cID):
						# The angle holds a CCS view name like AA-JE
						angle = str(clipViewCol) + str(clipViewRow)
						camViewItems.append(angle)

			# Translate the camera view letters (AA-JE) into camera view numbers (1-50)
			for camNam in camViewItems:
				camNumItems.append(GetCameraName(camNam))

			# Check what camera views are missing from the clip ID based set of R3D files
			result = set(range(1, maxCameras + 1)).difference(set(camNumItems))
			missingCamNumItems = list(result)

			# Sort the camera view numbers in descending order
			missingCamNumItems.sort()

			# Translate the missing view numbers back into view letters
			for camNum in missingCamNumItems:
				missingCamViewItems.append(GetCameraNumber(camNum))
		else:
			result = set(range(1, maxCameras + 1))
			missingCamNumItems = list(result)
	else:
		# Polar array
		if clips != None:
			for clip in clips:
				mpFile = str(clip.GetClipProperty("File Path"))
				clipFileName = os.path.basename(app.MapPath(mpFile))
				dateID, clipID, clipViewCol, clipViewRow, subClip = SplitMediaFilename(clipFileName, cameraArrayGeometry)
				if (clipID != None) and (cID != None):
					if int(clipID) == int(cID):
						# The angle holds a CCS view name like A220
						angle = str(clipViewCol)
						camViewItems.append(angle)
			# print("[camViewItems]")
			# print(camViewItems)
			# print("[cameraJSONConfigViews]")
			# print(cameraJSONConfigViews)

			result = set(cameraJSONConfigViews).difference(camViewItems)
			#print("[Cam View List Difference Result]", result)
			missingCamViewItems = list(result)
		else:
			result = set(range(1, maxCameras + 1))
			missingCamNumItems = list(result)

# 	print("[camViewItems]")
# 	print(camViewItems)
#
# 	print("[cameraJSONConfigViews]")
# 	print(cameraJSONConfigViews)
#
# 	print("[missingCamNumItems]")
# 	print(missingCamNumItems)

	return missingCamViewItems

def GetJSON(file):
	# Import the JSON file
	try:
		with open(file, "r") as f:
			# Todo: Add a try element to catch JSON formatting errors in the file when they are json.load() accessed.
			jsonStr = json.load(f)
			return jsonStr
	except OSError as error:
		print("\t[Lightfielder][Exception][JSON Get Error]", error)
		return

def GetTempFolder():
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))

	# Example: Lightfielder:/Temp/Projects/Project_1/
	#tempDirRel = "$(HOME)/Desktop/Projects/" + str(projectNameNoSpaces) + "/"
	#tempDirRel = "Temp:/Lightfielder/Projects/" + str(projectNameNoSpaces) + "/"
	tempDirRel = "Lightfielder:/Temp/Projects/" + str(projectNameNoSpaces) + "/"
	tempDirAbs = app.MapPath(tempDirRel)

	# Create the temporary folder
	if not os.path.exists(tempDirAbs):
		os.makedirs(tempDirAbs)
		print("[Lightfielder][Make Directory] ", tempDirAbs)

	return tempDirAbs

def GetTimeElapsed(startTime):
	elapsedTime = datetime.datetime.now() - startTime
	totalSeconds = elapsedTime.total_seconds()

	minutes, seconds = divmod(totalSeconds, 60)
	hours, minutes = divmod(minutes, 60)
	secInt = int(seconds)
	milliseconds = elapsedTime.microseconds // 1000

	if hours > 0:
		return f"{int(hours)}h {int(minutes)}m {secInt}s"
	if minutes > 0:
		return f"{int(minutes)}m {secInt}s"

	return f"{secInt}.{milliseconds:03d}s"

def TimecodeParse(text, lockTimecode):
	# +/-HH.MM.SS.FF
	# +/-HH:MM:SS:FF
	separators = int(text.count(".")) + (text.count(":"))
	timecodePattern = ""
	if separators == 0:
		timecodePattern = r"""
^                                           # Start of line
(?P<offset>[+\-])?
(?P<frame>[0-9]|[0-2][0-9])?                # Frames as [00-29]
$                                           # End of line
"""
	elif separators == 1:
		timecodePattern = r"""
^                                           # Start of line
(?P<offset>[+\-])?
(?P<sec>[0-9]|[0-5][0-9]?)?(:|\.)           # Seconds as [00-59]
(?P<frame>[0-9]|[0-2][0-9])?                # Frames as [00-29]
$                                           # End of line
"""
	elif separators == 2:
		timecodePattern = r"""
^                                           # Start of line
(?P<offset>[+\-])?
(?P<min>[0-9]|[0-5][0-9]?)?(:|\.)           # Minutes as [00-59]
(?P<sec>[0-9]|[0-5][0-9]?)?(:|\.)           # Seconds as [00-59]
(?P<frame>[0-9]|[0-2][0-9])?                # Frames as [00-29]
$                                           # End of line
"""
	elif separators == 3:
		timecodePattern = ""

		if lockTimecode == True:
			# Clamp timecode range at 24 hours
			timecodePattern = r"""
^                                           # Start of line
(?P<offset>[+\-])?
(?P<hour>[0-9]|[0-1][0-9]|[2][0-3])?(:|\.)  # Hours as [00-23]
(?P<min>[0-9]|[0-5][0-9]?)?(:|\.)           # Minutes as [00-59]
(?P<sec>[0-9]|[0-5][0-9]?)?(:|\.)           # Seconds as [00-59]
(?P<frame>[0-9]|[0-2][0-9])?                # Frames as [00-29]
$                                           # End of line
"""
		else:
			# Unclamped timecode range
			timecodePattern = r"""
^                                           # Start of line
(?P<offset>[+\-])?
(?P<hour>[0-9][0-9][0-9]|[0-9][0-9])?(:|\.) # Hours as [00-99] or [000-999]
(?P<min>[0-9]|[0-5][0-9]?)?(:|\.)           # Minutes as [00-59]
(?P<sec>[0-9]|[0-5][0-9]?)?(:|\.)           # Seconds as [00-59]
(?P<frame>[0-9]|[0-2][0-9])?                # Frames as [00-29]
$                                           # End of line
"""

	#print("\t[Lightfielder][Separators] " + str(separators))
	#print("\t[Lightfielder][Pattern] " + str(timecodePattern))

	# Process a regular expression based named group
	pat = re.compile(timecodePattern, re.VERBOSE)
	mat = pat.match(text)
	result = None
	if mat:
		#print("\n[Lightfielder][Timecode] " + str(text))
		result = mat.groupdict()
	#else:
	#	print("\t[Lightfielder][Invalid Timecode] " + str(text))
	return result

def FormatTimecode(text, lockTimecode):
	m = TimecodeParse(text, lockTimecode)

	# +/-HH:MM:SS:FF
	offset = "+"
	hour = 0
	minute = 0
	second = 0
	frame = 0

	valid = False

	if m:
		valid = True
		if 'offset' in m:
			offset = m['offset'] or "+"
		if 'hour' in m:
			hour = m['hour'] or 0
		if 'min' in m:
			minute = m['min'] or 0
		if 'sec' in m:
			second = m['sec'] or 0
		if 'frame' in m:
			frame = m['frame'] or 0
	# Display the formatted output
	result = ""
	#result += str(offset)
	result += str(int(hour)).zfill(2) + ":"
	result += str(int(minute)).zfill(2) + ":"
	result += str(int(second)).zfill(2) + ":"
	result += str(int(frame)).zfill(2)

	#print(result)
	return result, offset, valid

def CreateFootageShotIdBin(shotid, folder):
	mediapool = GetMediaPool()
	footageShotIdBin = None

	# Was the "Add Media To Sources Folder" preference enabled?
	sourcesFolder = app.GetData("Lightfielder.AddMediaToSourcesFolder")
	if sourcesFolder != None and sourcesFolder == True:
		# The footage should be added directly to the 03_footage folder. (Skip creating the <Shot ID> subfolder.)
		# return folder
		return GetFolder(folder, "source", mediapool)

	# Create the "03_footage/<Shot ID>/" bin
	return GetFolder(folder, shotid, mediapool)

def MatchClipToShot(mFile, cItems, cameraArrayGeometry):
	# Should the footage matching ignore the date field in the R3D filename?
	ignoreDate = app.GetData("Lightfielder.FuzzyR3DDateMatching")
	if ignoreDate is None:
		ignoreDate = False
	
	# Parse the R3D "J001_E050_0309BX_001" name for the clip ID and the CCS View
	clipFileName = os.path.basename(mFile)

	# Debug exit point:
	# print(clipFileName, mFile)
	# return "", "", "", "", "", ""

	dateID, clipID, clipViewCol, clipViewRow, subClip = SplitMediaFilename(clipFileName, cameraArrayGeometry)

	# Debug exit point:
	# print(dateID, clipID, clipViewCol, clipViewRow, subClip)
	# return "", "", "", "", "", ""

	angle = ""

	if cameraArrayGeometry == 0 or cameraArrayGeometry == 1:
		# Planar Grid or Wedge
		# The angle holds a CCS view name like AA-JE
		angle = str(clipViewCol) + str(clipViewRow)
	else:
		# Polar
		# The angle holds a CCS view name like A520
		angle = str(clipViewCol)

	# Match the clip ID from the R3D file with the shotlog clip heading.
	shotID = None
	desc = None
	for row in cItems:
		#print(row)
		cID = int(float(row[0]))
		sID = row[1]
		dID = row[2]
		desc = row[3]
		if ignoreDate == True and clipID == cID:
			# Ignore the date field in the R3D filename
			shotID = sID
			# To validate: Shove the date value from the CSV Date field into the R3D provided filename info
			dateID = dID
			break
		elif clipID == cID and dateID == dID:
			# Include the date field in the matching parameters
			shotID = sID
			break
	# print("\t[Lightfielder][File] " + str(clipFileName) + " [R3D Subclip] " + str(subClip) + " [Clip ID] " + str(clipID) + " [Shot ID] " + str(shotID) + " [Date ID] " + str(dateID) + " [Col] " + str(clipViewCol) + " [Row] " + str(clipViewRow) + " [Angle] " + str(angle))
	return shotID, clipID, dateID, angle, desc, subClip

def GetClipIDCount(cID, clips, cameraArrayGeometry):
	countIDs = 0
	for clip in clips:
		mpFile = str(clip.GetClipProperty("File Path"))
		clipFileName = os.path.basename(app.MapPath(mpFile))
		dateID, clipID, clipViewCol, clipViewRow, subClip = SplitMediaFilename(clipFileName, cameraArrayGeometry)
		# print(int(clipID), int(cID), mpFile)
		if int(clipID) == int(cID):
			countIDs += 1

	return countIDs

def IntersectFootageRanges(clipItems):
	# This function expects a list with sub-lists of frame ranges [[1,2,3],[2,3,4],[3,4,5]]

	try:
		result = set.intersection(*map(set, clipItems))
		start = min(result)
		end = max(result)
		duration = end - start
		return start, end, duration
	except:
		print("[Lightfielder][Error] Comparing invalid timecode ranges!")
		return 0, 0, 0


def ValidateClipRangesOTIO(timeline, inPoint, outPoint, lockTimecode):
	clips = ""
	inTime, inOffset, inValid = FormatTimecode(inPoint, lockTimecode)
	outTime, outOffset, outValid = FormatTimecode(outPoint, lockTimecode)

	# Timeline Frame rate
	fps = timeline.duration().rate

# 	# Track the shortest handle range available across the clips
# 	minHandleStart = None
# 	minHandleEnd = None

	# Scan the OTIO Timeline footage for frame ranges
	vRangeItems = []
	sRangeItems = []
	aRangeItems = []
	for each_seq in timeline.tracks:
		for each_item in each_seq:
			if isinstance(each_item, otio.schema.Clip):
				# Clip frame ranges
				availableStartFrame = otio.opentime.to_frames(each_item.available_range().start_time)
				availableEndFrame = otio.opentime.to_frames(each_item.available_range().end_time_exclusive())

				sourceStartFrame = otio.opentime.to_frames(each_item.source_range.start_time)
				sourceEndFrame = otio.opentime.to_frames(each_item.source_range.end_time_exclusive())

				visibleStartFrame = otio.opentime.to_frames(each_item.visible_range().start_time)
				visibleEndFrame = otio.opentime.to_frames(each_item.visible_range().end_time_exclusive())

				aRangeItems.append(list(range(availableStartFrame, availableEndFrame)))
				sRangeItems.append(list(range(sourceStartFrame, sourceEndFrame)))
				vRangeItems.append(list(range(visibleStartFrame, visibleEndFrame)))

	# Calculate the overlapping first and last frames from the footage
	vStartFrame, vEndFrame, vDuration = IntersectFootageRanges(vRangeItems)
	aStartFrame, aEndFrame, aDuration = IntersectFootageRanges(aRangeItems)
	sStartFrame, sEndFrame, sDuration = IntersectFootageRanges(sRangeItems)

	clips += "[Visible][Range] " + str(vStartFrame) + "-" + str(vEndFrame) + " [Duration] " + str(vDuration) + "<br>\n"
	clips += "[Source][Range] " + str(sStartFrame) + "-" + str(sEndFrame) + " [Duration] " + str(sDuration) + "<br>\n"
	clips += "[Available][Range] " + str(aStartFrame) + "-" + str(aEndFrame) + " [Duration] " + str(aDuration) + "<br>\n"

	#clips += "[Clip] " + str(name) + " [Range] " + str(otStart) + "-" + str(otEnd) + " [Duration] " + str(otDuration) + "<br>\n"

	return clips


def ValidateClipRangesNative(timeline, inPoint, outPoint, lockTimecode, flipRangesMode):
	results = ""
	errorCount = 0

	inTime, inOffset, inValid = FormatTimecode(inPoint, lockTimecode)
	outTime, outOffset, outValid = FormatTimecode(outPoint, lockTimecode)

	# Timeline frame rate
	fps = GetProjectFrameRate()
	# fps = GetSensorFrameRate()
	# fps = 60
	# fps = 30
	# fps = 29.97
	# fps = 24

	# Get the track count
	timelineVideoTrackCount = timeline.GetTrackCount("video")

	# Frame range used by the batch trim request
	moveStartFrame = 0
	moveEndFrame = 0
	if inOffset == "+":
		moveStartFrame -= otio.opentime.to_frames(otio.opentime.from_timecode(inTime, fps))
	else:
		moveStartFrame += otio.opentime.to_frames(otio.opentime.from_timecode(inTime, fps))

# 	if inOffset == "+":
# 		moveStartFrame += otio.opentime.to_frames(otio.opentime.from_timecode(inTime, fps))
# 	else:
# 		moveStartFrame -= otio.opentime.to_frames(otio.opentime.from_timecode(inTime, fps))

	if outOffset == "+":
		moveEndFrame += otio.opentime.to_frames(otio.opentime.from_timecode(outTime, fps))
	else:
		moveEndFrame -= otio.opentime.to_frames(otio.opentime.from_timecode(outTime, fps))

	# Store the current timeline clips
	clipItems = []

	# Build a list of the frame ranges for media
	sRangeItems = []

	# Get the track structure
	for i in range(1, int(timelineVideoTrackCount) + 1):
		# Get the clips in the track
		clips = timeline.GetItemListInTrack("video", i)
		for clip in clips:
			cProp = clip.GetProperty()

			mpItem = clip.GetMediaPoolItem()
			mpProp = mpItem.GetClipProperty()
			mpID = mpItem.GetMediaId()

			mpStartTC = str(mpItem.GetClipProperty("Start TC"))
			mpEndTC = str(mpItem.GetClipProperty("End TC"))
			mpDuration = mpItem.GetClipProperty("Duration")

			clipDuration = float(clip.GetDuration())
			clipStart = float(clip.GetStart())
			clipEnd = float(clip.GetEnd())
			clipName = str(clip.GetName())

			# Convert to timecode to frames
			sourceStartFrame = otio.opentime.to_frames(otio.opentime.from_timecode(mpStartTC, fps))
			sourceEndFrame = otio.opentime.to_frames(otio.opentime.from_timecode(mpEndTC, fps))

			# Timeline footage range
			leftOffset = clip.GetLeftOffset()
			rightOffset = clip.GetRightOffset() - 1

			# Post-trim footage range
			postTrimStartFrame = leftOffset + moveStartFrame
			postTrimEndFrame = rightOffset + moveEndFrame

			# Swap the start and end handle values if their positions are inverted
			#if (flipRangesMode == True) and (postTrimStartFrame > postTrimEndFrame):
			#	postTrimStartFrame, postTrimEndFrame = postTrimEndFrame, postTrimStartFrame

			postTrimDuration = postTrimEndFrame - postTrimStartFrame

			# Available clip handles
			missingStartFrames = sourceStartFrame - postTrimStartFrame
			missingEndFrames = sourceEndFrame - postTrimEndFrame

			# Add insufficient duration clips to a list
# 			if (missingStartFrames < 0) or (missingEndFrames < 0) or (postTrimDuration < 0):
# 				errorCount += 1
			if (postTrimStartFrame < 0) or (postTrimEndFrame < 0) or (postTrimDuration < 0):
				errorCount += 1

				results += "<tr><td>" + str(clipName) + "</td><td>V" + str(i) + "</td><td>"
				#if (missingStartFrames < 0):
				#results += str(missingStartFrames) + " " + str(sourceStartFrame) + " "
				#results += str(postTrimStartFrame)
				#results += str(otio.opentime.to_timecode(otio.opentime.from_frames(abs(missingStartFrames), fps)))
				results += str(otio.opentime.to_timecode(otio.opentime.from_frames(abs(postTrimStartFrame), fps)))

				results += "</td><td>"
				#if (missingEndFrames < 0):
				#results += str(missingEndFrames) + " " + str(sourceEndFrame) + " "
				#results += str(postTrimEndFrame)
				#results += str(otio.opentime.to_timecode(otio.opentime.from_frames(abs(missingEndFrames), fps)))
				results += str(otio.opentime.to_timecode(otio.opentime.from_frames(abs(postTrimEndFrame), fps)))

				results += "</td>"
				results += "<td>" + str(postTrimDuration) + "</td></tr>\n"

			print("[Lightfielder][Frame Handles] [In]", missingStartFrames, " [Out] " , missingEndFrames)

	#Debug TEMP
	#errorCount = 999
	return results, errorCount

def TimelineImport(file, name):
	project = GetProject()
	mediapool = project.GetMediaPool()
	currentFolder = mediapool.GetCurrentFolder()

	RelinkFolderItems = []
	RelinkFolderItems.append(currentFolder)

	importSourceClips = False
	timelineNameFromFilename = True

	# Use the current folder to help relink content
	#sourceClipsFolders = mediapool.GetCurrentFolder()

	# EDL File name
	filepath = file

	# EDL file extension ".edl" or ".otio"
	newTimelineBaseName, newTimelineExt = os.path.splitext(filepath)

	# set the timeline name from the filename
	newTimelineName = name
	#newTimelineName = os.path.basename(newTimelineBaseName)

	print("[Lightfielder][Timeline][Import File] \"" + filepath + "\" [Timeline Name] " + str(newTimelineName) +  " [Automatically import source clips] " + str(importSourceClips))

	mediapool.ImportTimelineFromFile(filepath, {
		"timelineName": newTimelineName,
		"importSourceClips": importSourceClips,
		"sourceClipsFolders": RelinkFolderItems
	})

	# Import the timeline as is
	#mediapool.ImportTimelineFromFile(filepath, {})

	# Import the timeline
	#mediapool.ImportTimelineFromFile(filepath, {
	#	#"timelineName": newTimelineName,
	#	"importSourceClips": importSourceClips,
	#	"sourceClipsPath": sourceClipsItems
	#})

def TimelineExport():
	res = app.GetResolve()

	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))

	projectSetting = project.GetSetting()

	# Get the timeline object
	timeline = GetTimeline()

	# Get the timeline name
	timelineName = timeline.GetName()
	timelineNameNoSpaces = str(timelineName.replace(" ", "_"))
	#print("[Lightfielder][Timeline Name] " + str(timelineName))

	mp = project.GetMediaPool()
	folder = mp.GetCurrentFolder()

	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")

	timelineExt = "otio"
	# Example: Timeline_1_2023-May-08_16.48.52.580631.otio
	tempTimeline = str(timelineNameNoSpaces) + "_" + str(timeStamp) + "." + str(timelineExt)

	# Example: Lightfielder:/Temp/Projects/Project_1/
	tempDirAbs = GetTempFolder()

	# Example: Lightfielder:/Temp/Projects/Project_1/Timeline_1_2023-May-08_16.48.52.580631.otio
	tempPathRel = tempDirAbs + tempTimeline
	tempPathAbs = app.MapPath(tempPathRel)

	result = timeline.Export(tempPathAbs, res.EXPORT_OTIO)
	if result:
		print("[Lightfielder][Timeline][Export] {0} ".format(tempPathAbs))
	else:
		print("[Lightfielder][Timeline][Export Failed] {0}".format(tempPathAbs))
		tempPathAbs = None
	return tempPathAbs, timelineName

def TimelineRename(name, layout):
	# Trim the old timeline layout suffix

	pattern = r"""
(?P<name>.*)         # Any Characters (Timeline Name)
\s                   # Whitespace - Tab or Space
(?P<counter>\d+)     # One or more numbers
\s?                  # Optional Whitespace - Tab or Space
$                    # End of line
"""

	# Postfix removal
	name = name.replace("VStack", "")
	name = name.replace("HStack", "")

	# Double space removal
	name = name.replace("  ", " ")

	counter = 1
	timelineName = name

	# Process a regular expression based named group
	pat = re.compile(pattern, re.VERBOSE)
	mat = pat.match(timelineName)
	result = None
	if mat:
		m = mat.groupdict()
		#print(m)
		if m:
			if 'name' in m:
				timelineName = str(m["name"])
			if 'counter' in m:
				# Increment the timeline number
				counter = int(m["counter"]) + 1

	# Double space removal
	timelineName = timelineName.replace("  ", " ")

	if layout == 0:
		# Create an OTIO VSTACK Timeline
		timelineName += " " + str(counter) + " VStack"
	else:
		# Create an OTIO HSTACK Timeline
		timelineName += " " + str(counter) + " HStack"

	# Double space removal
	timelineName = timelineName.replace("  ", " ")

	return timelineName


def TimelineRenameTrim(name):
	# Trim the old timeline layout suffix

	pattern = r"""
(?P<name>.*)         # Any Characters (Timeline Name)
\s                   # Whitespace - Tab or Space
(?P<counter>\d+)     # One or more numbers
\s?                  # Optional Whitespace - Tab or Space
$                    # End of line
"""

	# Postfix removal
	name = name.replace("Trim", "")

	# Double space removal
	name = name.replace("  ", " ")

	counter = 1
	timelineName = name

	# Process a regular expression based named group
	pat = re.compile(pattern, re.VERBOSE)
	mat = pat.match(timelineName)
	result = None
	if mat:
		m = mat.groupdict()
		#print(m)
		if m:
			if 'name' in m:
				timelineName = str(m["name"])
			if 'counter' in m:
				# Increment the timeline number
				counter = int(m["counter"]) + 1

	# Double space removal
	timelineName = timelineName.replace("  ", " ")

	# Create an OTIO VSTACK Timeline
	timelineName += " " + str(counter) + " Trim"

	# Double space removal
	timelineName = timelineName.replace("  ", " ")

	return timelineName

def ReadTimeline(file):
	# fps = GetProjectFrameRate()
	# fps = GetSensorFrameRate()
	# fps = 60
	# fps = 30
	# fps = 29.97
	# fps = 24
	# timeline = otio.adapters.read_from_file(file, rate = fps, ignore_timecode_mismatch = True)
	timeline = otio.adapters.read_from_file(file)

	#print("[Lightfielder][Timeline]")
	#print(timeline)

	#print("[Lightfielder][Name]")
	#print(timeline.name)

	#print("[Lightfielder][Tracks]")
	#print(timeline.tracks)

	return timeline


def ReadTimelineClips(timeline):
	print("[Lightfielder][Timeline][Name] ", timeline.name)
	for each_seq in timeline.tracks:
		for each_item in each_seq:
			if isinstance(each_item, otio.schema.Clip):
				# A001_A055_1116A5_001.R3D
				name = each_item.name
				trackName = each_seq.name

				# AA - JE
				#reel = ""
				#if ("cmx_3600" in each_item.metadata) and ("reel" in each_item.metadata["cmx_3600"]):
				#	reel = each_item.metadata["cmx_3600"]["reel"]
				print("[Lightfielder][Read Clip] [Kind] " + str(each_seq.kind) + "\t[" + str(trackName) + "] " + str(name))

				#print(each_item)
				#print(each_item.name, each_item.metadata)
				#print(each_item.media_reference)

def ModifyTimelineNative(timelineOld, name, inPoint, outPoint, lockTimecode, clipColorMode, flipRangesMode):
	# frame rate
	fps = GetProjectFrameRate()
	# fps = GetSensorFrameRate()
	# fps = 60
	# fps = 30
	# fps = 29.97
	# fps = 24

	#print("[Lightfielder][Clips]")
	clipNames = ""
	report = ""

	res = app.GetResolve()
	project = GetProject()
	mediapool = project.GetMediaPool()

	# Get the timeline object
	timeline = GetTimeline()

	# Get the timeline name
	timelineName = timeline.GetName()

	# Get the number of cameras views in the array
	maxCameras = GetMaxNumberOfCameras()

	# Get the track count
	if timeline is not None:
		timelineVideoTrackCount = timeline.GetTrackCount("video")
		if timelineVideoTrackCount <= maxCameras:
			trackGoal = maxCameras - timelineVideoTrackCount
			# Add the required video tracks
			for x in range(trackGoal):
				timeline.AddTrack("video")
		timelineAudioTrackCount = timeline.GetTrackCount("audio")
		if timelineAudioTrackCount <= maxCameras:
			trackGoal = maxCameras - timelineAudioTrackCount
			# Add the required audio tracks
			for x in range(trackGoal):
				timeline.AddTrack("audio")

	# Get the track count
	timelineVideoTrackCount = timeline.GetTrackCount("video")

	inTime, inOffset, inValid = FormatTimecode(inPoint, lockTimecode)
	outTime, outOffset, outValid = FormatTimecode(outPoint, lockTimecode)

	# Frame range used by the batch trim request
	moveStartFrame = 0
	moveEndFrame = 0
	if inOffset == "+":
		moveStartFrame += otio.opentime.to_frames(otio.opentime.from_timecode(inTime, fps))
	else:
		moveStartFrame -= otio.opentime.to_frames(otio.opentime.from_timecode(inTime, fps))

	if outOffset == "+":
		moveEndFrame += otio.opentime.to_frames(otio.opentime.from_timecode(outTime, fps))
	else:
		moveEndFrame -= otio.opentime.to_frames(otio.opentime.from_timecode(outTime, fps))

	print("[Lightfielder][Move Start Frame] " + str(moveStartFrame) + " [Move Start Frame] " + str(moveEndFrame))

	# Store the current timeline clips
	clipItems = []

	# Build a list of the frame ranges for media
	sRangeItems = []

	# Get the track structure
	for i in range(1, int(timelineVideoTrackCount) + 1):
		# Get the clips in the track
		clips = timeline.GetItemListInTrack("video", i)
		for clip in clips:
			cProp = clip.GetProperty()

			mpItem = clip.GetMediaPoolItem()
			mpProp = mpItem.GetClipProperty()
			mpID = mpItem.GetMediaId()

			mpStartTC = str(mpItem.GetClipProperty("Start TC"))
			mpEndTC = str(mpItem.GetClipProperty("End TC"))
			mpDuration = mpItem.GetClipProperty("Duration")

			clipDuration = float(clip.GetDuration())
			clipStart = float(clip.GetStart())
			clipEnd = float(clip.GetEnd())
			clipColor = str(clip.GetClipColor())

			# Convert to timecode to frames
			sourceStartFrame = otio.opentime.to_frames(otio.opentime.from_timecode(mpStartTC, fps))
			sourceEndFrame = otio.opentime.to_frames(otio.opentime.from_timecode(mpEndTC, fps))

			leftOffset = clip.GetLeftOffset()
			rightOffset = clip.GetRightOffset() - 1

			#print(cProp)
			#print(clip.GetLeftOffset(),clip.GetRightOffset())
			#print("[Lightfielder][Clip]", clipStart, clipEnd, " [MP] ", sourceStartFrame, sourceEndFrame, " [Handles] " , clip.GetLeftOffset(),clip.GetRightOffset())

			clipItems.append([mpItem, i, leftOffset, rightOffset, sourceStartFrame, sourceEndFrame, clipColor])
			sRangeItems.append(list(range(sourceStartFrame, sourceEndFrame)))

	# Create the new timeline
	#newTimelineName = timelineName
	newTimelineName = timelineName + " Trim"
	newTimeline = mediapool.CreateEmptyTimeline(newTimelineName)
	trackIndex = 1

	timelineStartTimecode = "01:00:00:00"
	timelineStartFrames = otio.opentime.to_frames(otio.opentime.from_timecode(timelineStartTimecode, fps))

	# Check if the footage has a valid start frame - end frame range
	#print(sRangeItems)
	#if len(sRangeItems) > 0:
	#	# Timecode Sync
	#	tStartFrame, tEndFrame, tDuration = IntersectFootageRanges(sRangeItems)
	#else:
	#	report += "[Sync Issue] No Overlapping Frames<br>\n"

	c = 0
	prevTrackIndex = -1
	trackRecordFrame = timelineStartFrames
	for clip in clipItems:
		c += 1

		mpClip = clip[0]
		trackIndex = clip[1]

		# Edit Page Source Range
		sStartFrame = clip[2]
		sEndFrame = clip[3]
		sDuration = sEndFrame - sStartFrame

		# Original Duration Range
		pStartFrame = clip[4]
		pEndFrame = clip[5]
		pDuration = pEndFrame - pStartFrame
		pClipColor = clip[6]
		#print("[Lightfielder][Clip Color] " + str(pClipColor))

		if prevTrackIndex != trackIndex:
			# Reset a new video track at the recordFrame starting position in the timeline
			trackRecordFrame = timelineStartFrames

			postTrimStartFrame = sStartFrame + moveStartFrame
			postTrimEndFrame = sEndFrame + moveEndFrame

			# Swap the start and end handle values if their positions are inverted
			#if (flipRangesMode == True) and (postTrimStartFrame > postTrimEndFrame):
			#	postTrimStartFrame, postTrimEndFrame = postTrimEndFrame, postTrimStartFrame

			mpFootage = {
				"mediaPoolItem" : mpClip,
				"startFrame": postTrimStartFrame,
				"endFrame" : postTrimEndFrame,
				"recordFrame" : trackRecordFrame,
				"trackIndex" : trackIndex
			}
			# Add the clip to the timeline
			timelineItem = mediapool.AppendToTimeline([mpFootage])
			#print("[Lightfielder][Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

			# Add the clip color
			if timelineItem[0] != None and clipColorMode == True:
				timelineItem[0].SetClipColor(pClipColor)
		else:
			mpFootage = {
				"mediaPoolItem" : mpClip,
				"startFrame": postTrimStartFrame,
				"endFrame" : postTrimStartFrame,
				"trackIndex" : trackIndex
			}
			# Add the clip to the timeline
			timelineItem = mediapool.AppendToTimeline([mpFootage])
			#print("[Lightfielder][Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

			# Add the clip color
			if timelineItem[0] != None and clipColorMode == True:
				timelineItem[0].SetClipColor(pClipColor)

		#trackRecordFrame += sDuration
		prevTrackIndex = clip[1]

	return newTimeline, clipNames

def ModifyTimelineOTIO(timelineOld, name, inPoint, outPoint, lockTimecode):
	timelineNew = otio.schema.Timeline(name = name, global_start_time = timelineOld.global_start_time)

	inTime, inOffset, inValid = FormatTimecode(inPoint, lockTimecode)
	outTime, outOffset, outValid = FormatTimecode(outPoint, lockTimecode)

	# Timeline Frame rate
	fps = timelineOld.duration().rate

	#print("[Timeline Name]")
	#print(timelineNew.name)

	#print("[Clips]")
	clipNames = ""

	# Scan the old timeline
	v = 0
	a = 0
	for each_seq in timelineOld.tracks:
		# Create the tracks
		if each_seq.kind == "Video":
			v += 1
			videoTrackName =  "V" + str(v)
			videoTrack = otio.schema.Track(kind = "Video", name = videoTrackName)
			timelineNew.tracks.append(videoTrack)

			a += 1
			audioTrackName =  "A" + str(a)
			audioTrack = otio.schema.Track(kind = "Audio", name = audioTrackName)
			timelineNew.tracks.append(audioTrack)

			# Add the video clips
			for each_item in each_seq:
				if isinstance(each_item, otio.schema.Clip):
					#print(each_item)
					#print(each_item.name, each_item.metadata)
					#print(each_item.media_reference)

					# A001_A055_1116A5_001.R3D
					name = each_item.name

					# Edit the frame range
					availableStartFrame = otio.opentime.to_frames(each_item.available_range().start_time)
					availableEndFrame = otio.opentime.to_frames(each_item.available_range().end_time_exclusive())
					availableDuration = availableEndFrame - availableStartFrame

					sourceStartFrame = otio.opentime.to_frames(each_item.source_range.start_time)
					sourceEndFrame = otio.opentime.to_frames(each_item.source_range.end_time_exclusive())
					sourceDuration = sourceEndFrame - sourceStartFrame

					visibleStartFrame = otio.opentime.to_frames(each_item.visible_range().start_time)
					visibleEndFrame = otio.opentime.to_frames(each_item.visible_range().end_time_exclusive())
					visibleDuration = visibleEndFrame - visibleStartFrame

					# Frame range used by the batch trim request
					requestStartFrame = visibleStartFrame
					requestEndFrame = visibleEndFrame
					if inOffset == "+":
						requestStartFrame += otio.opentime.to_frames(otio.opentime.from_timecode(inTime, fps))
					else:
						requestStartFrame -= otio.opentime.to_frames(otio.opentime.from_timecode(inTime, fps))

					if outOffset == "+":
						requestEndFrame += otio.opentime.to_frames(otio.opentime.from_timecode(outTime, fps))
					else:
						requestEndFrame -= otio.opentime.to_frames(otio.opentime.from_timecode(outTime, fps))

					requestDuration = requestEndFrame - requestStartFrame

					trim_clip = otio.schema.Clip()
					trim_clip.name = each_item.name

					# Defining a source range will clamp the edit so it doesn't stick when re-imported.
					# trim_clip.source_range = each_item.source_range


					print(each_item.source_range)
					# The source range is the edited and chopped down timeline clip range. The available range is the native footage frame range for the video file on disk.
					# trim_clip.source_range = otio.opentime.TimeRange(
# 						otio.opentime.from_frames(requestStartFrame, fps),
# 						otio.opentime.from_frames(requestDuration, fps)
# 					),

					print("[Lightfielder][media_reference]")
					#trim_clip.media_reference = otio.schema.ExternalReference(
					#	target_url = each_item.media_reference.target_url,
					#	available_image_bounds = None,
					#	metadata = each_item.media_reference.metadata,
					#)
					#trim_clip.media_reference = otio.schema.ExternalReference(
					#	target_url = each_item.media_reference.target_url,
					#	available_image_bounds = None,
					#	metadata = each_item.media_reference.metadata,
					#	available_range = otio.opentime.TimeRange(
					#		otio.opentime.from_frames(availableStartFrame, fps),
					#		otio.opentime.from_frames(availableDuration, fps)
					#	),
					#)

					trim_clip.media_reference = otio.schema.ExternalReference(
						target_url = each_item.media_reference.target_url,
						available_image_bounds = None,
						metadata = each_item.media_reference.metadata,
						available_range = otio.opentime.TimeRange(
							otio.opentime.from_frames(requestStartFrame, fps),
							otio.opentime.from_frames(requestDuration, fps)
						),
					)

					#print(trim_clip)
					clipNames += "[Clip] " + str(name) + "\t" + " [Footage Range] [Start/Duration] " + str(visibleStartFrame) + " / " + str(visibleDuration) + "\t" + "[Edited Range] [Start/Duration] " + str(requestStartFrame) + " / " + str(requestDuration) + "<br>\n"

					# Append the clip from the old timeline to the new timeline
					videoTrack.append(copy.deepcopy(trim_clip))
					audioTrack.append(copy.deepcopy(trim_clip))
# 		elif each_seq.kind == "Audio":
# 			a += 1
# 			audioTrackName =  "A" + str(a)
# 			audioTrack = otio.schema.Track(kind = "Audio", name = audioTrackName)
# 			timelineNew.tracks.append(audioTrack)
#
# 			# Add the audio clips
# 			for each_item in each_seq:
# 				if isinstance(each_item, otio.schema.Clip):
#
# 					#print(each_item)
# 					#print(each_item.name, each_item.metadata)
# 					#print(each_item.media_reference)
#
# 					# A001_A055_1116A5_001.R3D
# 					name = each_item.name
#
# 					# Append the clip from the old timeline to the new timeline
# 					audioTrack.append(copy.deepcopy(each_item))
	return timelineNew, clipNames

def TimelineImportOTIO(file, name):
	project = GetProject()
	mediapool = project.GetMediaPool()

	importSourceClips = True
	timelineNameFromFilename = True

	# Use the current folder to help relink content
	#sourceClipsFolders = mediapool.GetCurrentFolder()

	# EDL File name
	filepath = file

	# EDL file extension ".edl" or ".otio"
	newTimelineBaseName, newTimelineExt = os.path.splitext(filepath)

	# set the timeline name from the filename
	newTimelineName = name
	#newTimelineName = os.path.basename(newTimelineBaseName)

	print("[Lightfielder][Timeline][Import File] \"" + filepath + "\" [Timeline Name] " + str(newTimelineName) +  " [Automatically import source clips] " + str(importSourceClips))

	# Import the timeline as is
	#mediapool.ImportTimelineFromFile(filepath, {})

	mediapool.ImportTimelineFromFile(filepath, {
		"timelineName": newTimelineName,
		"importSourceClips": importSourceClips,
	})

	# Import the timeline
	#mediapool.ImportTimelineFromFile(filepath, {
	#	#"timelineName": newTimelineName,
	#	"importSourceClips": importSourceClips,
	#})


def WriteTimeline(file, timeline):
	# EDL file extension ".edl" or ".otio"
	timelineBaseName, timelineExt = os.path.splitext(file)
	fileOTIO = timelineBaseName + ".otio"
	result = otio.adapters.write_to_file(timeline, fileOTIO)
	print("[Lightfielder][Timeline Edited] [OTIO File Name] " + str(fileOTIO) + "\t[OTIO Write Status] " + str(result))

	return fileOTIO


def ImportCSV(file):
	emptyRows = 0
	resultStr = ""
	resultStr += "\n<h2>Import CSV Shotlog</h2>" + "\n"
	resultStr += "<p>" + str(file) + "</p>\n"
	print("\n[Lightfielder][Import CSV]")

	resultStr += "<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
	resultStr += "<tr><td>Clip</td><td>Shot ID</td><td>Date</td><td>Description</td></tr>\n"

	csvItems = []
	with open(app.MapPath(file), encoding = "utf-8-sig", newline = "") as f:
		reader = csv.reader(f)
		for row in reader:
			# Validate we have exactly 4 CSV rows, and that we don't have a ",," empty CSV row
			if len(row) >= 4 and (str(row[0]) != "" and str(row[1]) != "" and str(row[2]) != "" and str(row[3]) != ""):
				clip = str(row[0])
				shotid = str(row[1])
				date = str(row[2])
				description = str(row[3])

				# Ignore the shotlog.csv header row "clip,shot,description" entry
				if clip.lower() != "clip":
					csvItems.append([clip, shotid, date, description])
					resultStr += "<tr><td>" + str(clip) + "</td><td>" + str(shotid) + "</td><td>" + str(date) + "</td><td>" + str(description) + "</td></tr>\n"
			else:
				# Another CSV row is empty
				emptyRows += 1

	resultStr += "</table>\n"
	print(resultStr)

	resultStr += "<p>CSV Shotlog - Blank CSV row entries: " + str(emptyRows) + "\n"
	#print("[Lightfielder][Shotlog][Error] [Blank CSV row entries] " + str(emptyRows))
	return csvItems, resultStr


def SaveReportPreferencesLog(htmlDocument):
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))
	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")

	logFolderRel = "Lightfielder:/Logs/Projects/" + str(projectNameNoSpaces) + "/"
	logFolderAbs = app.MapPath(logFolderRel)

	logFileRel = str(logFolderRel) + str(timeStamp) + "_Preferences.html"
	logFileAbs = app.MapPath(logFileRel)

	# Create the intermediate directories on disk
	if not os.path.exists(logFolderAbs):
		try:
			# Make the dir
			os.makedirs(logFolderAbs)
			print("[Lightfielder][Preferences Report][Make Directory]", logFolderAbs)
		except OSError as error:
			print("[Lightfielder][Preferences Report][Make Directory Error]", error)
			return

	# Write to report log file
	f = open(logFileAbs, "a")
	if f is None:
		print("[Lightfielder][Preferences Report][Write Error] ", logFileAbs)
	else:
		print("[Lightfielder][Preferences Report][Write File] ", logFileAbs)
		f.write(htmlDocument)
		f.close()

def SaveReportCalibrationLog(message):
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))
	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")

	logFolderRel = "Lightfielder:/Logs/Projects/" + str(projectNameNoSpaces) + "/"
	logFolderAbs = app.MapPath(logFolderRel)

	logFileRel = str(logFolderRel) + str(timeStamp) + "_Still_Frames_Report.html"
	logFileAbs = app.MapPath(logFileRel)

	# Combine the HTML content
	css = """
		<style type="text/css">
			body {font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:12px; font-weight:400; font-style:normal; background-color: #2D2D2D; color: #9D9D9D;}
			h1 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:xx-large; font-weight:600;}
			h2 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:x-large; font-weight:400;}
			p, table, th, td {color: #9D9D9D; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;}
			a {text-decoration: underline; color:#8b9bd8;}
			p, li {white-space: pre-wrap;}
			hr {max-height: 3px; background-color: rgb(76, 154, 109); color: rgb(76, 154, 109);}
		</style>
"""
	htmlHeaderTxt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html>\n\t<head>\n\t\t<title>' + str(projectName) + '</title>\n' + str(css) + '\t</head>\n\t<body>\n<h1>Still Frames Export</h1>\n<hr/>\n'
	htmlFooterTxt = '\t</body>\n</html>\n'
	htmlDocument = str(htmlHeaderTxt) + str(message) + str(htmlFooterTxt)

	# Create the intermediate directories on disk
	if not os.path.exists(logFolderAbs):
		try:
			# Make the dir
			os.makedirs(logFolderAbs)
			print("[Lightfielder][Calibration Report][Make Directory]", logFolderAbs)
		except OSError as error:
			print("[Lightfielder][Calibration Report][Make Directory Error]", error)
			return

	# Write to report log file
	f = open(logFileAbs, "a")
	if f is None:
		print("[Lightfielder][Calibration Report][Write Error] ", logFileAbs)
	else:
		print("[Lightfielder][Calibration Report][Write File] ", logFileAbs)
		f.write(htmlDocument)
		f.close()


def SaveReportCreateEDLsLog(message):
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))
	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")

	logFolderRel = "Lightfielder:/Logs/Projects/" + str(projectNameNoSpaces) + "/"
	logFolderAbs = app.MapPath(logFolderRel)

	logFileRel = str(logFolderRel) + str(timeStamp) + "_Create_EDLs.html"
	logFileAbs = app.MapPath(logFileRel)

	# Combine the HTML content
	css = """
		<style type="text/css">
			body {font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:12px; font-weight:400; font-style:normal; background-color: #2D2D2D; color: #9D9D9D;}
			h1 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:xx-large; font-weight:600;}
			h2 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:x-large; font-weight:400;}
			p, table, th, td {color: #9D9D9D; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;}
			a {text-decoration: underline; color:#8b9bd8;}
			p, li {white-space: pre-wrap;}
			hr {max-height: 3px; background-color: rgb(76, 154, 109); color: rgb(76, 154, 109);}
		</style>
"""
	htmlHeaderTxt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html>\n\t<head>\n\t\t<title>' + str(projectName) + '</title>\n' + str(css) + '\t</head>\n\t<body>\n<h1>Create EDLs</h1>\n<hr/>\n'
	htmlFooterTxt = '\t</body>\n</html>\n'
	htmlDocument = str(htmlHeaderTxt) + str(message) + str(htmlFooterTxt)

	# Create the intermediate directories on disk
	if not os.path.exists(logFolderAbs):
		try:
			# Make the dir
			os.makedirs(logFolderAbs)
			print("[Lightfielder][Calibration Report][Make Directory]", logFolderAbs)
		except OSError as error:
			print("[Lightfielder][Calibration Report][Make Directory Error]", error)
			return

	# Write to report log file
	f = open(logFileAbs, "a")
	if f is None:
		print("[Lightfielder][Calibration Report][Write Error] ", logFileAbs)
	else:
		print("[Lightfielder][Calibration Report][Write File] ", logFileAbs)
		f.write(htmlDocument)
		f.close()


def SaveReportMetadataSyncLog(message):
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))
	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")

	logFolderRel = "Lightfielder:/Logs/Projects/" + str(projectNameNoSpaces) + "/"
	logFolderAbs = app.MapPath(logFolderRel)

	logFileRel = str(logFolderRel) + str(timeStamp) + "_Metadata_Sync.html"
	logFileAbs = app.MapPath(logFileRel)

	# Combine the HTML content
	css = """
		<style type="text/css">
			body {font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:12px; font-weight:400; font-style:normal; background-color: #2D2D2D; color: #9D9D9D;}
			h1 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:xx-large; font-weight:600;}
			h2 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:x-large; font-weight:400;}
			p, table, th, td {color: #9D9D9D; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;}
			a {text-decoration: underline; color:#8b9bd8;}
			p, li {white-space: pre-wrap;}
			hr {max-height: 3px; background-color: rgb(76, 154, 109); color: rgb(76, 154, 109);}
		</style>
"""
	htmlHeaderTxt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html>\n\t<head>\n\t\t<title>' + str(projectName) + '</title>\n' + str(css) + '\t</head>\n\t<body>\n<h1>Metadata Sync Log</h1>\n<hr/>\n'
	htmlFooterTxt = '\t</body>\n</html>\n'
	htmlDocument = str(htmlHeaderTxt) + str(message) + str(htmlFooterTxt)

	# Create the intermediate directories on disk
	if not os.path.exists(logFolderAbs):
		try:
			# Make the dir
			os.makedirs(logFolderAbs)
			print("[Lightfielder][Metadata Sync Log Report][Make Directory]", logFolderAbs)
		except OSError as error:
			print("[Lightfielder][Metadata Sync Log Report][Make Directory Error]", error)
			return

	# Write to report log file
	f = open(logFileAbs, "a")
	if f is None:
		print("[Lightfielder][Metadata Sync Log Report][Write Error] ", logFileAbs)
	else:
		print("[Lightfielder][Metadata Sync Log Report][Write File] ", logFileAbs)
		f.write(htmlDocument)
		f.close()

def SaveReportShotLog(message):
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))
	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")

	logFolderRel = "Lightfielder:/Logs/Projects/" + str(projectNameNoSpaces) + "/"
	logFolderAbs = app.MapPath(logFolderRel)

	logFileRel = str(logFolderRel) + str(timeStamp) + "_Shotlog_Import.html"
	logFileAbs = app.MapPath(logFileRel)

	# Combine the HTML content
	css = """
		<style type="text/css">
			body {font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:12px; font-weight:400; font-style:normal; background-color: #2D2D2D; color: #9D9D9D;}
			h1 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:xx-large; font-weight:600;}
			h2 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:x-large; font-weight:400;}
			p, table, th, td {color: #9D9D9D; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;}
			a {text-decoration: underline; color:#8b9bd8;}
			p, li {white-space: pre-wrap;}
			hr {max-height: 3px; background-color: rgb(76, 154, 109); color: rgb(76, 154, 109);}
		</style>
"""
	htmlHeaderTxt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html>\n\t<head>\n\t\t<title>' + str(projectName) + '</title>\n' + str(css) + '\t</head>\n\t<body>\n<h1>Shotlog</h1>\n<hr/>\n'
	htmlFooterTxt = '\t</body>\n</html>\n'
	htmlDocument = str(htmlHeaderTxt) + str(message) + str(htmlFooterTxt)

	# Create the intermediate directories on disk
	if not os.path.exists(logFolderAbs):
		try:
			# Make the dir
			os.makedirs(logFolderAbs)
			print("[Lightfielder][Shotlog Report][Make Directory]", logFolderAbs)
		except OSError as error:
			print("[Lightfielder][Shotlog Report][Make Directory Error]", error)
			return

	# Write to report log file
	f = open(logFileAbs, "a")
	if f is None:
		print("[Lightfielder][Shotlog Report][Write Error] ", logFileAbs)
	else:
		print("[Lightfielder][Shotlog Report][Write File] ", logFileAbs)
		f.write(htmlDocument)
		f.close()

def SaveReportLog(htmlDocument, logType):
	# LogType is a value like "Calibration"

	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))
	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")

	logFolderRel = "Lightfielder:/Logs/Projects/" + str(projectNameNoSpaces) + "/"
	logFolderAbs = app.MapPath(logFolderRel)

	logFileRel = str(logFolderRel) + str(timeStamp) + "_" + str(logType) + "_Report.html"
	logFileAbs = app.MapPath(logFileRel)

	# Create the intermediate directories on disk
	if not os.path.exists(logFolderAbs):
		try:
			# Make the dir
			os.makedirs(logFolderAbs)
			print("[Lightfielder][" + str(logType) + " Report][Make Directory]", logFolderAbs)
		except OSError as error:
			print("[Lightfielder][" + str(logType) + " Report][Make Directory Error]", error)
			return

	# Write to report log file
	f = open(logFileAbs, "a")
	if f is None:
		print("[Lightfielder][" + str(logType) + " Report][Write Error] ", logFileAbs)
	else:
		print("[Lightfielder][" + str(logType) + " Report][Write File] ", logFileAbs)
		f.write(htmlDocument)
		f.close()

def GenerateHTML(filePath, data):
	message = "\t\t<p>JSON File: " + str(filePath) + "</p><br>\n"
	message += "\t\t<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
	message += "\t\t\t<tr><td>Camera</td><td>k1</td><td>k2</td><td>p1</td><td>p2</td><td>k3</td></tr>\n"

	try:
		for key, value in data.items():
			cameraNum = int(key)
			params = value

			#print(key, "\n\t", value)
			print("[Lightfielder][" + str(cameraNum) + "]")

			k1, k2, p1, p2, k3 = params["camera_distortion"]
			matrix = params["camera_matrix"]
			reproj = params["reproj_error"]

			message += "\t\t\t<tr><td>" + str(cameraNum) + "</td><td>" + str(k1) + "</td><td>" + str(k2) + "</td><td>" + str(p1) + "</td><td>" + str(p2) + "</td><td>" + str(k3) + "</td></tr>\n"
	except StopIteration:
		pass

	message += "\t\t</table>\n"

	# Combine the HTML content
	css = """
		<style type="text/css">
			body {font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:12px; font-weight:400; font-style:normal; background-color: #2D2D2D; color: #9D9D9D;}
			h1 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:xx-large; font-weight:600;}
			h2 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:x-large; font-weight:400;}
			p, table, th, td {color: #9D9D9D; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;}
			a {text-decoration: underline; color:#8b9bd8;}
			p, li {white-space: pre-wrap;}
			hr {max-height: 3px; background-color: rgb(76, 154, 109); color: rgb(76, 154, 109);}
		</style>
"""
	htmlHeaderTxt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html>\n\t<head>\n\t\t<title>' + str("Calibration Report") + '</title>\n' + str(css) + '\t</head>\n\t<body>\n\t\t<h1>Calibration Report</h1>\n<hr/>\n'
	htmlFooterTxt = '\t</body>\n</html>\n'
	htmlDocument = str(htmlHeaderTxt) + str(message) + str(htmlFooterTxt)
	# print(htmlDocument)
	return htmlDocument

def ErrorWindow(status, message):
	ui = fu.UIManager
	error_disp = bmd.UIDispatcher(ui)

	error_dlg = error_disp.AddWindow({
		"WindowTitle": "",
		"WindowFlags": {"Window": True, "WindowStaysOnTopHint": True},
		"ID": "ErrorWin",
		"TargetID": "ErrorWin",
		"Geometry": [0, 85, 580, 624],
		# "MinimumSize": [0, 85, 580, 624],
		# "FixedSize": [0, 85, 580, 624],
		#"WindowModality": "WindowModal",
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
						"Text": "  " + str(status),
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
			ui.TextEdit({"ID": "ErrorTxt", "Text": message, "Weight": 1.0}),
			ui.VGap(10),
			ui.Button({
				"ID": "OKButton",
				"Text": "OK",
				"Weight": 0.01,
			}),
		]),
	])

	error_itm = error_dlg.GetItems()

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
		WindowPrefSave(error_dlg, "Lightfielder.ErrorWin.Geometry")
	error_dlg.On.ErrorWin.Hide = HideFunc

	# The window was closed
	def ErrorWinFunc(ev):
		error_disp.ExitLoop()
	error_dlg.On.ErrorWin.Close = ErrorWinFunc

	# Add your GUI element based event functions here:

	def OKButtonFunc(ev):
		print("[Lightfielder][Window][OK Button]")
		error_disp.ExitLoop()
	error_dlg.On.OKButton.Clicked = OKButtonFunc

	# Load the window preferences
	WindowPrefLoad(error_dlg, "Lightfielder.ErrorWin.Geometry")

	error_dlg.Show()
	error_disp.RunLoop()
	error_dlg.Hide()

	# Save the window preferences
	WindowPrefSave(error_dlg, "Lightfielder.ErrorWin.Geometry")

def ResultsWindow(status, message):
	ui = fu.UIManager
	results_disp = bmd.UIDispatcher(ui)

	results_dlg = results_disp.AddWindow({
		"WindowTitle": "",
		"WindowFlags": {"Window": True, "WindowStaysOnTopHint": True},
		"ID": "ResultsWin",
		"TargetID" : "ResultsWin",
		"Geometry": [0, 185, 580, 624],
		# "MinimumSize": [0, 185, 580, 624],
		# "FixedSize": [0, 185, 580, 624],
		#"WindowModality": "WindowModal",
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
						"Text": "  " + str(status),
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
			ui.TextEdit({"ID": "ErrorTxt", "Text": message, "Weight": 1.0}),
			ui.VGap(10),
			ui.Button({
				"ID": "OKButton",
				"Text": "OK",
				"Weight": 0.01,
			}),
		]),
	])

	results_itm = results_dlg.GetItems()

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
		WindowPrefSave(results_dlg, "Lightfielder.ResultsWin.Geometry")
	results_dlg.On.ResultsWin.Hide = HideFunc

	# The window was closed
	def CloseFunc(ev):
		print("[Lightfielder][Window][Closed]")
		results_disp.ExitLoop()
	results_dlg.On.ResultsWin.Close = CloseFunc

	# Add your GUI element based event functions here:

	def OKButtonFunc(ev):
		print("[Lightfielder][Window][OK Button]")
		results_disp.ExitLoop()
	results_dlg.On.OKButton.Clicked = OKButtonFunc

	# Load the window preferences
	WindowPrefLoad(results_dlg, "Lightfielder.ResultsWin.Geometry")

	results_dlg.Show()
	results_disp.RunLoop()
	results_dlg.Hide()

	# Save the window preferences
	WindowPrefSave(results_dlg, "Lightfielder.ResultsWin.Geometry")

# OpenTimelineIO
try:
	import opentimelineio as otio
except ModuleNotFoundError:
	currentOS = GetPlatform()
	messsage = ""
	if currentOS == "Mac":
		messsage = """The OTIO Python module is missing. The macOS Terminal based install commands for OpenTimelineIO and other libraries are:
pip3 install --upgrade pip
pip3 install OpenImageIO
pip3 install OpenTimelineIO
pip3 install PySide6
pip3 install virtualenv
"""
	elif currentOS == "Windows":
		messsage = """The OTIO Python module is missing. The Windows Command Prompt based install commands for OpenTimelineIO and other libraries are:
python3 -m pip install --upgrade pip
pip3 install OpenTimelineIO
pip3 install PySide6
pip3 install virtualenv
"""
	elif currentOS == "Linux":
		messsage = """The OTIO Python module is missing. The Linux Terminal based install commands for OpenTimelineIO and other libraries are:
sudo dnf update -y
sudo dnf install python3 python3-pip -y
pip3 install --upgrade pip
pip3 install OpenImageIO
pip3 install OpenTimelineIO
pip3 install PySide6
pip3 install virtualenv
"""

	ErrorWindow("OpenTimelineIO", messsage)
	exit()

try:
	dir(otio.adapters)
except AttributeError:
	currentOS = GetPlatform()
	messsage = ""
	if currentOS == "Mac":
		messsage = """The OTIO Python module is missing. The macOS Terminal based install commands for OpenTimelineIO and other libraries are:
pip3 install --upgrade pip
pip3 install OpenImageIO
pip3 install OpenTimelineIO
pip3 install PySide6
pip3 install virtualenv
"""
	elif currentOS == "Windows":
		messsage = """The OTIO Python module is missing. The Windows Command Prompt based install commands for OpenTimelineIO and other libraries are:
python3 -m pip install --upgrade pip
pip3 install OpenTimelineIO
pip3 install PySide6
pip3 install virtualenv
"""
	elif currentOS == "Linux":
		messsage = """The OTIO Python module is missing. The Linux Terminal based install commands for OpenTimelineIO and other libraries are:
sudo dnf update -y
sudo dnf install python3 python3-pip -y
pip3 install --upgrade pip
pip3 install OpenImageIO
pip3 install OpenTimelineIO
pip3 install PySide6
pip3 install virtualenv
"""

	ErrorWindow("OpenTimelineIO", messsage)
	exit()

# if __name__ == "__main__":
	# print("Do Something")
