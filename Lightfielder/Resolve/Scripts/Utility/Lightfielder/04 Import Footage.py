"""
Lightfielder 04 Import Footage.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Import R3D footage into the Resolve media page.

Script Usage:

1. Create a new Resolve project and add the Bin folder structure you desire. Copy a shotlog.csv file into the on-disk project folder hierarchy. A good place to store a shotlog file might be the "08_Documents" folder.

2. Select the menu item: "Workspace > Scripts > Lightfielder > 04 Import Footage".

3. Use the "CSV Source File" text field to select a .csv (Comma Separated Value) formatted shotlog file. Use the "Footage Folder" text field to select a R3D footage folder.

4. Press the "Go" button to process the data.

CSV Formatting
The shotlog.csv column 1 "clip" heading matches up against the R3D file's clip number found in the 2nd number grouping. The shotlog clip value lets you look up the shot number on the same CSV row. The shot number is then used to break down the footage into sub-folders in the Resolve bin's "02_footage" bin. This shot number is also used with the EDL creation process to create the timelines.

shotlog1.csv:
clip,shot,date,description
004,001,1003,calibration

R3D Clip Name:
A001_A004_1003RH_001.R3D

shotlog2.csv:
clip,shot,date,description
50,01325,0309,calibration

R3D Clip Name:
A001_A050_0309RH_001.R3D

R3D Clip Naming:
http://docs.red.com/955-0047/MediaOperationGuide/Content/5_Eject_And_Format_Media/Clip_Naming_Convention.htm

RED filename "J001_E050_0309BX_001.R3D"
J = Camera View Row
E = Camera View Column
050 = Clip Number 50
0309 = Day/Month

Clip Metadata
The following Resolve Media page clip-level metadata records are populated from the shotlog.csv and R3D filename by the Shotlog Python script:
Angle           (AA-JE)         [CCS View]
Camera Position (01-50)         [CCS View Number]
Clip Number     (001-999)       [Shotlog Clip ID]
Description     ("calibration, "hdri", or a content description)  [Shotlog Description]
Shot            (00001-99999)   [Shotlog Shot ID]

R3D sub-clip sequence naming example:
"J001_E050_0309BX.RDC/J001_E050_0309BX_[001-008].R3D"

R3D sub-clip filenames on disk:
J001_E050_0309BX_001.R3D
J001_E050_0309BX_002.R3D
J001_E050_0309BX_003.R3D
J001_E050_0309BX_004.R3D
J001_E050_0309BX_005.R3D
J001_E050_0309BX_006.R3D
J001_E050_0309BX_007.R3D
J001_E050_0309BX_008.R3D

# Todo Sooner:
- Apply a Lamda sort to the shot ID field in the R3D filename so the same ID number if filled up without winding back and forth in the media pool bin

# Todo later
- Validate if there are zero clips added to the bin
- Verify if the function GetMissingViews(cID, clips) needs the dID and DateID fields added for matching
- Validate CSV files with the wrong number of headings
- Validate if the first cell of the CSV clip ID is leading zero padded
- Validate the intersected footage timecode "trim range" is applied correctly per-clip
- Validate project frame rate (24 vs 29.97) is the same as the footage frame rate (29.97). Otherwise an offset will exist.
- Validate OpenTimelineIO frame rate with drop frame timecode - fix off by +/- 1 frame start point issue
- Protect against double adding media to an old timeline
- Save the footage path and CSV Source file entries in the preferences to be restored. Change the labels to flat uiButtons so 1-click will clear out the values.
- Add a "Title" textfield for an entry like "energetic_rockergirl"
- Have a Checkbox for "Overwrite Calibration Timelines".
- Have a Checkbox option for "Limit R3D Import to Shotlog Footage"

- In the create a calibration timeline shotlog dialog, the (case insensitive) "calibration" shotlog description items are the only shots used

"""

import re
import csv, os, datetime, math, json
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

startTimer = datetime.datetime.now()

def ImportMedia(csvItems, mediaFolder, footageBin, footageBinName, progressLabel, shotCheckedItems, clipCheckedItems, cameraArrayGeometry, cameraJSONConfigViews):
	resultStr = ""
	resultStr += "\n<h2>Import R3D Media to Media Pool</h2>" + "\n"
	#print("\n[Lightfielder][Shotlog][Import R3D Media to Media Pool]")

	res = app.GetResolve()
	project = GetProject()
	mediapool = project.GetMediaPool()

	resultStr += "<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
	resultStr += "<tr><td>Shot ID</td><td>Date</td><td>File</td><td>R3D Subclip</td></tr>\n"

	mpClipInfo = []
	mpClipItems = []
	missingItems = []
	redMediaItems = GetMediaFiles(mediaFolder)
	redMediaItemCount = len(redMediaItems)
	counter = 0

	# Debug exit point:
	# print(redMediaItems)
	# return mpClipItems, "Done"

	for media in redMediaItems:
		# Debug exit point:
		# print(media, csvItems, cameraArrayGeometry)
		# return mpClipItems, "Done"

		# Parse the media filename and the shotlog CSV for the clip id and shot id
		shot, clip, date, angle, description, subClip = MatchClipToShot(media, csvItems, cameraArrayGeometry)
		shotName = "ID_" + str(shot)

		# Debug exit point:
		# print(shot, clip, date, angle, description, subClip)
		# return mpClipItems, "Done"

		camNum = 99
		if cameraArrayGeometry == 0 or cameraArrayGeometry == 1:
			# Planar Grid or Wedge array
			# Convert the CCS View letter (AA-JE) into a camera number (1-50)
			camNum = GetCameraName(angle)
		elif cameraArrayGeometry == 2:
			# Polar array
			# Count the sorted list in linear order
			try:
				# print("\n\n[Camera Lookup]", angle, "[Index] ", cameraJSONConfigViews.index(angle) + 1)
				camNum = cameraJSONConfigViews.index(angle) + 1
			except ValueError:
				print("[Camera View Index] not found for:", angle)
				pass

		# Create the "Shot ID" Bin
		if shot != None and int(shot) in shotCheckedItems:
			if clip != None and int(clip) in clipCheckedItems:
				print(shotName, shot, clip, date, angle, description, subClip)
				# Change the active bin to "03_footage/ID_<Shot ID>/"

				fShotBin = CreateFootageShotIdBin(shotName, footageBin)
				mediapool.SetCurrentFolder(fShotBin)
				counter += 1
				if int(counter) % 5 == 0:
					progressLabel.Text = "  Progress: Import Media (" + str(counter) + " of " + str(redMediaItemCount) + ") [" + str(shotName) + "] [Wallclock " + GetTimeElapsed(startTimer) + "]"
				# Check if an existing item is in the bin
				existingFile, existingClip = FindVideoClipPath(fShotBin, media)
				if existingFile == media:
					# print("\t[Media Pool] [Exists] " + str(existingFile))
					mpClipItems.append(existingClip)
				elif subClip == 1:
					# This is the first subclip item
					mpItems = mediapool.ImportMedia(media)
					if mpItems != None:
						for mpItem in mpItems:
							mpClipItems.append(mpItem)
							mpClipName = mpItem.GetClipProperty("Clip Name")
							#print("\t[Media Pool] " + str(footageBinName) + "/" + str(shotName) + "/" + str(mpClipName))
							filePath = str(footageBinName) + "/" + str(shotName) + "/" + str(mpClipName)
							#resultStr +=  str(filePath) + "<br>\n"
							resultStr += "<tr><td>" + str(shotName) + "</td><td>" + str(date) + "</td><td>" + str(filePath) + "</td><td>" + str(subClip) + "</td></tr>\n"
							counter += 1
							progressLabel.Text = "  Progress: Import Media (" + str(counter) + " of " + str(redMediaItemCount) + ") [" + str(shotName) + "] [Wallclock " + GetTimeElapsed(startTimer) + "]"
#				elif subClip != 1:
#					# This is the 2+ subclip item
#					# print("\t\t[Subclip][Skipping R3D] " + str(media) + " [Subclip Item] " + str(subClip))

	resultStr += "</table>\n"

	# Sort the media pool items by: Clip ID, CCS View Col/Row, subClip
	mpClipItems = sorted(mpClipItems, key=lambda clip: SplitMediaFilename(clip.GetClipProperty("Clip Name"), cameraArrayGeometry))

	progressLabel.Text = "  Progress: Parse Clip IDs"
	resultStr += "\n<h2>Parse Clip IDs</h2>" + "\n"
	print("\n[Parse Clip IDs]")

	resultStr += "<table border=\"0\" cellpadding=\"2\">\n"
	resultStr += "<tr><td>Clip ID</td><td>View Count</td><td>Missing Camera Data</td></tr>\n"
	if cameraArrayGeometry == 0 or cameraArrayGeometry == 1:
		# Planar Grid or Wedge Geometry:
		for row in csvItems:
			# Count how many pieces of footage with the same clip ID are in the mediapool items list
			# print(row)
			csvClipID = str(row[0])
			if int(csvClipID) in clipCheckedItems:
				progressLabel.Text = "  Progress: Parse Clip ID (" + str(csvClipID) + ") [Wallclock " + GetTimeElapsed(startTimer) + "]"
				clipCount = GetClipIDCount(csvClipID, mpClipItems, cameraArrayGeometry)

				# Track the missing cameras in a clip ID
				missingItems = GetMissingViews(csvClipID, mpClipItems, cameraArrayGeometry, cameraJSONConfigViews)
				missingStr = ' '.join(missingItems)

				if missingStr != "":
					# There are missing camera views
					resultStr += "<tr><td bgcolor=\"#EB6E01\" style=\"color:#000000;\">" + str(csvClipID) + "</td><td  bgcolor=\"#EB6E01\" style=\"color:#000000;\">" + str(clipCount) + "</td><td  bgcolor=\"#EB6E01\" style=\"color:#000000;\">" + str(missingStr) + "</td></tr>\n"
				else:
					# All camera views present
					resultStr += "<tr><td>" + str(csvClipID) + "</td><td>" + str(clipCount) + "</td><td>" + str(missingStr) + "</td></tr>\n"
				# Debug
				# resultStr += "[Clip ID] " + str(csvClipID) + " "
				# resultStr += "[View Count] " + str(clipCount) + " "
				# resultStr += "[Missing Views] " + str(missingStr) + "<br>\n"
				# print("\t[Clip ID] " + str(csvClipID) + "\t[View Count] " + str(clipCount) + "\t[Missing Views] " + str(missingStr))
	elif cameraArrayGeometry == 2:
		# Polar Geometry:
		for row in csvItems:
			# Count how many pieces of footage with the same clip ID are in the mediapool items list
			# print(row)
			csvClipID = str(row[0])
			if int(csvClipID) in clipCheckedItems:
				progressLabel.Text = "  Progress: Parse Clip ID (" + str(csvClipID) + ") [Wallclock " + GetTimeElapsed(startTimer) + "]"
				clipCount = GetClipIDCount(csvClipID, mpClipItems, cameraArrayGeometry)

				# Track the missing cameras in a clip ID

				missingItems = GetMissingViews(csvClipID, mpClipItems, cameraArrayGeometry, cameraJSONConfigViews)
				# print(missingItems)
				# missingStr = ""
				missingStr = ' '.join(missingItems)

				# Get the number of cameras views in the array
				maxCameras = GetMaxNumberOfCameras()

				if clipCount != maxCameras:
					# There are missing camera views
					# missingStr = str(50 - clipCount)
					resultStr += "<tr><td bgcolor=\"#EB6E01\" style=\"color:#000000;\">" + str(csvClipID) + "</td><td  bgcolor=\"#EB6E01\" style=\"color:#000000;\">" + str(clipCount) + "</td><td  bgcolor=\"#EB6E01\" style=\"color:#000000;\">" + str(missingStr) + "</td></tr>\n"
				else:
					# All camera views present
					resultStr += "<tr><td>" + str(csvClipID) + "</td><td>" + str(clipCount) + "</td><td></td></tr>\n"
				# Debug
				# resultStr += "[Clip ID] " + str(csvClipID) + " "
				# resultStr += "[View Count] " + str(clipCount) + " "
				# resultStr += "[Missing Views] " + str(missingStr) + "<br>\n"
				# print("\t[Clip ID] " + str(csvClipID) + "\t[View Count] " + str(clipCount) + "\t[Missing Views] " + str(missingStr))
	resultStr += "</table>\n"

	print(resultStr)
	return mpClipItems, resultStr, missingItems

def ImportFootageWindow():
	# Get the project name
	project = GetProject()
	if project is None:
		print("[Lightfielder] No Resolve project is open at this time.")
	else:
		projectName = project.GetName()
		projectSetting = project.GetSetting()
		
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
			"ID": "ImportFootageWin",
			"TargetID" : "ImportFootageWin",
			"Geometry": [10, 185, 540, 710],
			"MinimumSize": [540, 710],
			"FixedSize": [540, 710],
			# "Spacing": 0,
			# "Margin": 5,
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
						"Text": "04 Import Footage",
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
				ui.TextEdit({
					"ID": "Txt",
					"Text": "Tip of the day: The fastest way to import footage is to use the \"Media Storage\" panel. Right-click on the footage you would like to bring into the footages/source folder and select the \"Add Folder and SubFolder into MediaPool (Create Bins)\" contextual menu item.",
					"ReadOnly": True,
					"StyleSheet": "QTextEdit { border: 0px; }",
					"Weight": 0.1,
				}),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.Button({
						"ID": "ShowFootageFolderButton",
						"Flat": True,
						"MinimumSize": [145, 32],
						"Text": "Footage Folder",
						"ToolTip": GetTooltip("Show the footage folder","Clicking this text label will open the base folder where the R3D source footage is located in \na desktop folder browsing window. This requires a folder path to be entered in the text field."),
						"Weight": 0.01,
					}),
					ui.LineEdit({
						"ID": "FolderLineTxt",
						"Text": "",
						"PlaceholderText": "Please enter a R3D footage folder",
						"ToolTip": "Enter the folder location where the R3D source footage is stored. \nThis can be a local filepath, or a mapped folder on a NAS based \nnetwork storage volume.",
						"Weight": 0.9
					}),
					ui.Button({"ID": "BrowseFolderButton", "Text": "Browse", "MinimumSize": [100, 32], "Weight": 0.1}),
				]),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.Button({
						"ID": "ShowCSVFilenameButton",
						"Flat": True,
						"MinimumSize": [145, 32],
						"Text": "CSV Source File",
						"ToolTip": GetTooltip("Show the CSV file","Clicking this text label will open the base folder where the Shotlog CSV file is located in a desktop folder browsing window. This requires a file \npath to be entered in the text field. Shift-clicking the text label will open the file in the default spreadsheet app. Command-clicking will open the file \nin a text editor."),
						"Weight": 0.01,
					}),
					ui.LineEdit({
						"ID": "FileLineTxt",
						"Text": "",
						"PlaceholderText": "Please enter a shotlog.csv filename",
						"ToolTip": "The shotlog CSV file provides essential details for the R3D filename based clip \nnumber, filming date, as well as the shot number, description (shot type).",
						"Weight": 0.9
					}),
					ui.Button({"ID": "BrowseFileButton", "Text": "Browse", "MinimumSize": [100, 32], "Weight": 0.1}),
				]),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.Button({
						"ID": "ShowCameraArrayGeometryButton",
						"Flat": True,
						"MinimumSize": [145, 32],
						"Text": "Camera Array Geometry",
						"ToolTip":  GetTooltip("Edit the camera rig settings", "Clicking this text label will open the \"01 Preferences\" window. This allows you to quickly adjust \nthe remainder of the camera rig settings like the \"Number of Cameras\", the \"Media Format\", \nand the Sensor / Project Frame Rate details as well."),
						"Weight": 0.01,
					}),
					ui.ComboBox({
						"ID": "CameraArrayGeometryCombo",
						"Text": "Mode",
						"ToolTip": "What era of volumetric camera rig design and R3D filename based view labelleing are we using?\nThe A1-E5 format was used from 2022-2024, and the polar layout was used from 2024-2026+.",
						"Weight": 1.0,
					}),
				]),
				ui.HGroup({
					"Weight": 0.1,
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
						"ToolTip": "The Technisync JSON configuration file provides essential details \nfor each R3D camera like the camera angle name, frame rate, etc.",
						"Weight": 0.9
					}),
					ui.Button({"ID": "JSONBrowseFileButton", "Text": "Browse", "MinimumSize": [100, 32], "Weight": 0.1}),
				]),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.Label({
						"ID": "ShotTypeLabel",
						"Text": "Shot Type",
						"ToolTip": "The individual \"Shot Type\" checkbox controls allow you to filter the content \nto process by quickly enabling/disabling the \"Active\" checkbox selections \nbased upon the details in the shotlog CSV file description fields.",
						"Weight": 0.1,
						"MinimumSize": [100, 32],
					}),
					ui.CheckBox({
						"ID": "ShotTypeCalibrationCheckbox",
						"Text": "Calibration",
						"ToolTip": "The individual \"Shot Type\" checkbox controls allow you to filter the content \nto process by quickly enabling/disabling the \"Active\" checkbox selections \nbased upon the details in the shotlog CSV file description fields.",
						"Checked": True,
					}),
					ui.CheckBox({
						"ID": "ShotTypePostCalibrationCheckbox",
						"Text": "Post-Calibration",
						"ToolTip": "The individual \"Shot Type\" checkbox controls allow you to filter the content \nto process by quickly enabling/disabling the \"Active\" checkbox selections \nbased upon the details in the shotlog CSV file description fields.",
						"Checked": True,
					}),
					ui.CheckBox({
						"ID": "ShotTypeHDRICheckbox",
						"Text": "HDRI",
						"ToolTip": "The individual \"Shot Type\" checkbox controls allow you to filter the content \nto process by quickly enabling/disabling the \"Active\" checkbox selections \nbased upon the details in the shotlog CSV file description fields.",
						"Checked": False,
					}),
					ui.CheckBox({
						"ID": "ShotTypeContentCheckbox",
						"Text": "Content",
						"ToolTip": "The individual \"Shot Type\" checkbox controls allow you to filter the content \nto process by quickly enabling/disabling the \"Active\" checkbox selections \nbased upon the details in the shotlog CSV file description fields.",
						"Checked": False,
					}),
				]),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.CheckBox({
						"ID": "TypeColorCheckbox",
						"Text": "Shot Type Color",
						"ToolTip": "Should the shotlog items be shown in the list with \ncolor tags applied based upon the shot type?",
						"Checked": True,
					}),
					ui.CheckBox({
						"ID": "AddMediaToSourcesFolderCheckbox",
						"Text": "Add Media to Sources Folder",
						"ToolTip": "(WIP) When this option is enabled the imported media is placed in the Media bin \n\"03-footages/source/\" folder without a \"ID_####\" subfolder.",
						"Checked": False,
					}),
					ui.CheckBox({
						"ID": "FuzzyR3DDateMatchingCheckbox",
						"Text": "Fuzzy R3D Date Matching",
						"ToolTip": "(WIP) When this option is enabled the Shotlog CSV date field will be considered \na match with the R3D filename date value if they are within 1 day +/-.",
						"Checked": False,
					}),
					ui.VGap(40),
				]),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.VGap(10),
					ui.Label({"ID": "SelectLabel", "Text": "Select ", "Weight": 0.1, "MinimumSize": [60, 24],}),
					ui.Button({
						"ID": "SelectAllButton",
						"Text": "All",
						"ToolTip": "Select all the items in the shotlog, and uncheck their \"Active\" checkbox state.",
						"Weight": 0.01,
						"MinimumSize": [50, 24],
					}),
					ui.Button({
						"ID": "SelectNoneButton",
						"Text": "None",
						"ToolTip": "Deselct all the items in the shotlog, and uncheck their \"Active\" checkbox state.",
						"Weight": 0.01,
						"MinimumSize": [50, 24],
					}),
					ui.Button({
						"ID": "SelectInvertButton",
						"Text": "Invert",
						"ToolTip": "Toggle the \"Active\" checkbox state for all items in the shotlog. The Invert action \nmeans that items that were previously checked will become unchecked, and \nitems that were previously unchecked will become checked.",
						"Weight": 0.01,
						"MinimumSize": [50, 24],
					}),
				]),
				ui.HGroup({
					"Weight": 20.0,
				},[
					ui.Tree({
						"ID": "Tree",
						"SortingEnabled": True,
						"SelectionMode": "ExtendedSelection",
						"Weight": 20.0,
						"Events": {
							"CurrentItemChanged": True,
							"ItemChanged": True,
							"ItemActivated": True,
							"ItemClicked": True,
							"ItemDoubleClicked": True,
						},
						"MinimumSize": [100, 200],
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
					"Weight": 0.01
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
					"Weight": 0.01
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
		])

		itm = dlg.GetItems()

		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		# Camera Array Geometry
		itm["CameraArrayGeometryCombo"].AddItem("Planar Grid (A1-E5)")
		itm["CameraArrayGeometryCombo"].AddItem("Wedge 3M (A1-E5) ")
		itm["CameraArrayGeometryCombo"].AddItem("Polar (A110-Z977)")

		# Add a header row
		hdr = itm["Tree"].NewItem()
		hdr.Text[0] = "Active"
		hdr.Text[1] = "Clip #"
		hdr.Text[2] = "Shot"
		hdr.Text[3] = "Date"
		hdr.Text[4] = "Description"

		itm["Tree"].SetHeaderItem(hdr)

		# Number of columns in the Tree list
		itm["Tree"].ColumnCount = 5

		# Resize the Columns
		itm["Tree"].ColumnWidth[0] = 60
		itm["Tree"].ColumnWidth[1] = 50
		itm["Tree"].ColumnWidth[2] = 70
		itm["Tree"].ColumnWidth[3] = 70
		itm["Tree"].ColumnWidth[4] = 380

		# Change the sorting order of the tree
		#itm["Tree"].SortByColumn(0, "DescendingOrder")
		itm["Tree"].SortByColumn(0, "AscendingOrder")

		def RefreshTree():
			print("[Lightfielder] Rebuilding the CSV Tree")
			# Remove the old tree entries
			itm["Tree"].Clear()

			# Rebuild the tree entries
			shotlogFile = itm["FileLineTxt"].Text
			if shotlogFile != "" and os.path.exists(app.MapPath(shotlogFile)):
				csvItems, csvResult = ImportCSV(app.MapPath(shotlogFile))
				for row in csvItems:
					# Validate we have 4+ CSV rows, and that we don't have a ",," empty CSV row
					if len(row) >= 4 and (str(row[0]) != "" and str(row[1]) != "" and str(row[2]) != "" and str(row[3]) != ""):
						# Count how many pieces of footage with the same clip ID are in the mediapool items list
						csvClipID = str(row[0]).zfill(3)
						csvShot = str(row[1]).zfill(4)
						csvDate = str(row[2]).zfill(4)
						csvDescription = str(row[3])

						# Fill the tree row
						itRow = itm["Tree"].NewItem()

						if csvClipID != "" and csvClipID != "000":
							itRow.Text[0] = ""
							itRow.Text[1] = csvClipID
							itRow.Text[2] = csvShot
							itRow.Text[3] = csvDate
							itRow.Text[4] = csvDescription

							# Toggle the checked state of the new row item
# Toggle the checked state of the new row item
							itRow.CheckState[0] = "Unchecked"
							if ("post calibration" in csvDescription.lower() or "post-calibration" in csvDescription.lower()) and itm["ShotTypePostCalibrationCheckbox"].Checked:
								# print("[Post=Calibration] ")
								itRow.CheckState[0] = "Checked"
							elif ("calibration" in csvDescription.lower()) and itm["ShotTypeCalibrationCheckbox"].Checked:
								# print("[Calibration] ")
								itRow.CheckState[0] = "Checked"
							if (("hdri" in csvDescription.lower()) or ("light probe" in csvDescription.lower())) and itm["ShotTypeHDRICheckbox"].Checked:
								# print("[Calibration] ")
								itRow.CheckState[0] = "Checked"
							if ((("hdri" in csvDescription.lower()) or ("light probe" in csvDescription.lower())) and ("calibration" in csvDescription.lower())) and itm["ShotTypeContentCheckbox"].Checked:
								# print("[Content] " )
								itRow.CheckState[0] = "Unchecked"
							if itm["TypeColorCheckbox"].Checked == True:
								for c in range(int(itm["Tree"].ColumnCount)):
									itRow.TextColor[c] = GetColor("White")
									if ("post-calibration" in csvDescription.lower() or "post calibration" in csvDescription.lower()):
										itRow.BackgroundColor[c] = GetColor("Violet")
									elif ("calibration" in csvDescription.lower()):
										itRow.BackgroundColor[c] = GetColor("Brown")
									elif ("hdri" in csvDescription.lower()) or ("light probe" in csvDescription.lower()):
										itRow.BackgroundColor[c] = GetColor("Blue")
									else:
										itRow.BackgroundColor[c] = GetColor("Green")
							itm["Tree"].AddTopLevelItem(itRow)

		# Resize the window
		dlg.RecalcLayout()

		def PrefSave(winDlg):
			# Save the prefs
			if winDlg != None:
				print("[Lightfielder][Preferences] Saved")
				app.SetData("Lightfielder.FootageFolder", itm["FolderLineTxt"].Text)
				app.SetData("Lightfielder.JSONCameraConfigFile", itm["JSONCameraConfigFileLineTxt"].Text)
				app.SetData("Lightfielder.ArrayGeometry", itm["CameraArrayGeometryCombo"].CurrentIndex)
				app.SetData("Lightfielder.CSVFile", itm["FileLineTxt"].Text)
				app.SetData("Lightfielder.Calibration", itm["ShotTypeCalibrationCheckbox"].Checked)
				app.SetData("Lightfielder.Post-Calibration", itm["ShotTypePostCalibrationCheckbox"].Checked)
				app.SetData("Lightfielder.HDRI", itm["ShotTypeHDRICheckbox"].Checked)
				app.SetData("Lightfielder.Content", itm["ShotTypeContentCheckbox"].Checked)
				app.SetData("Lightfielder.FuzzyR3DDateMatching", itm["FuzzyR3DDateMatchingCheckbox"].Checked)
				app.SetData("Lightfielder.AddMediaToSourcesFolder", itm["AddMediaToSourcesFolderCheckbox"].Checked)
				# print(app.GetData("Lightfielder"))

		def PrefLoad(winDlg):
			# Restore the prefs
			if winDlg != None:
				# print("[Lightfielder][Preferences] Loaded")
				# print(app.GetData("Lightfielder"))
				# Footage Folder
				pref = app.GetData("Lightfielder.FootageFolder")
				if pref != None:
					# print(pref)
					itm["FolderLineTxt"].Text = pref
				# CSV File
				pref = app.GetData("Lightfielder.CSVFile")
				if pref != None:
					# print(pref)
					itm["FileLineTxt"].Text = pref
				pref = app.GetData("Lightfielder.JSONCameraConfigFile")
				if pref != None:
					# print(pref)
					itm["JSONCameraConfigFileLineTxt"].Text = pref
				pref = app.GetData("Lightfielder.ArrayGeometry")
				if pref != None:
					# print(pref)
					itm["CameraArrayGeometryCombo"].CurrentIndex = pref
				# ShotType
				pref = app.GetData("Lightfielder.Post-Calibration")
				if pref != None:
					# print(pref)
					itm["ShotTypePostCalibrationCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.Calibration")
				if pref != None:
					# print(pref)
					itm["ShotTypeCalibrationCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.HDRI")
				if pref != None:
					# print(pref)
					itm["ShotTypeHDRICheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.Content")
				if pref != None:
					# print(pref)
					itm["ShotTypeContentCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.FuzzyR3DDateMatching")
				if pref != None:
					# print(pref)
					itm["FuzzyR3DDateMatchingCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.AddMediaToSourcesFolder")
				if pref != None:
					# print(pref)
					itm["AddMediaToSourcesFolderCheckbox"].Checked = pref
				RefreshTree()

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
			WindowPrefSave(dlg, "Lightfielder.ImportFootageWin.Geometry")

			# Save the CSV and Footage folder pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
		dlg.On.ImportFootageWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.ImportFootageWin.Geometry")

			# Save the CSV and Footage folder pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.ImportFootageWin.Close = CloseFunc

		def MainCloseButtonFunc(ev):
			print("[Lightfielder][Window][Close Button]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.ImportFootageWin.Geometry")

			# Save the CSV and Footage folder pref
			PrefSave(dlg)

			disp.ExitLoop()
		dlg.On.MainCloseButton.Clicked = MainCloseButtonFunc

		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool4", "Tool3")

			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool4", "Tool5")

			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		# Add your GUI element based event functions here:

		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_04_Import_Footage.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		# Click on the filename text label to open the filename in an external editor, or open the containing folder in the operating system's folder browsing view
		def ShowCSVFilenameButtonFunc(ev):
			buttonModifier = ev["modifiers"]["ShiftModifier"]
			buttonModifierControl = ev["modifiers"]["ControlModifier"]

			if buttonModifier == True:
				# shift was held down so open the OS default program for this filetype
				 ShowInDefaultProgram(itm["FileLineTxt"].Text)
			elif buttonModifierControl == True:
				# Command/Control was held down so open the programmer's text editor
				ExternalEditor(itm["FileLineTxt"].Text)
			else:
				# Label was clicked on with no modifier keys so open the containing folder in the operating system's folder browsing view
				ShowFolderFromFilepath(itm["FileLineTxt"].Text)
		dlg.On.ShowCSVFilenameButton.Clicked = ShowCSVFilenameButtonFunc

		def ShowCameraArrayGeometryButtonFunc(ev):
			ShowPrefsWindow(True)
		dlg.On.ShowCameraArrayGeometryButton.Clicked = ShowCameraArrayGeometryButtonFunc

		# Show a file browsing dialog to select the CSV file
		def BrowseFileButtonFunc(ev):
			# CSV Source File Browse Button
			selectedPath = fu.RequestFile()
			if selectedPath:
				# Push the filepath into the "CSV Source File" text field
				itm["FileLineTxt"].Text = str(app.MapPath(selectedPath))

				# Reset the shot type initial state
				itm["ShotTypeCalibrationCheckbox"].Checked = False
				itm["ShotTypePostCalibrationCheckbox"].Checked = False
				itm["ShotTypeHDRICheckbox"].Checked = False
				itm["ShotTypeContentCheckbox"].Checked = False

				# Import the CSV data into the tree view
				RefreshTree()

				# Filter the shot types
				calibrationExists = False
				postCalibrationExists = False
				hdriExists = False
				contentExists = False

				# Check the CSV description field values
				for c in range(int(itm["Tree"].TopLevelItemCount())):
					item = itm["Tree"].TopLevelItem(c)
					if ("calibration" in item.Text[4].lower() and ("post calibration" not in item.Text[4].lower() and "post-calibration" not in item.Text[4].lower())):
						if calibrationExists == False:
							calibrationExists = True
					if ("post calibration" in item.Text[4].lower() or "post-calibration" in item.Text[4].lower()):
						if postCalibrationExists == False:
							postCalibrationExists = True
					if (("hdri" in item.Text[4].lower()) or ("light probe" in item.Text[4].lower())):
						if hdriExists == False:
							hdriExists = True
					if (("hdri" not in item.Text[4].lower()) and ("light probe" not in item.Text[4].lower())) and ("calibration" not in item.Text[4].lower()):
						if contentExists == False:
							contentExists = True

				# Enable the shot types that exist in the csv import
				itm["ShotTypeCalibrationCheckbox"].Checked = calibrationExists
				itm["ShotTypePostCalibrationCheckbox"].Checked = postCalibrationExists
				itm["ShotTypeHDRICheckbox"].Checked = hdriExists
				itm["ShotTypeContentCheckbox"].Checked = contentExists

				# Force a checkbox selection state update
				SelectAllButtonFunc(ev)
			# Save the prefs
			PrefSave(dlg)
		dlg.On.BrowseFileButton.Clicked = BrowseFileButtonFunc

		def BrowseFolderButtonFunc(ev):
			# Footage Folder Browse Button
			selectedPath = fu.RequestDir()
			if selectedPath:
				itm["FolderLineTxt"].Text = str(app.MapPath(selectedPath))
			# Save the prefs
			PrefSave(dlg)
		dlg.On.BrowseFolderButton.Clicked = BrowseFolderButtonFunc

		# Click on the footage folder text label to open the folder in the operating system's folder browsing view
		def ShowFootageFolderButtonFunc(ev):
			ShowFolderFromFilepath(itm["FolderLineTxt"].Text)
		dlg.On.ShowFootageFolderButton.Clicked = ShowFootageFolderButtonFunc

		# Click on the filename text label to open the filename in an external editor, or open the containing folder in the operating system's folder browsing view
		def ShowJSONFilenameButtonFunc(ev):
			buttonModifier = ev["modifiers"]["ShiftModifier"]
			buttonModifierControl = ev["modifiers"]["ControlModifier"]

			if buttonModifier == True:
				# shift was held down so open the OS default program for this filetype
				 ShowInDefaultProgram(itm["JSONCameraConfigFileLineTxt"].Text)
			elif buttonModifierControl == True:
				# Command/Control was held down so open the programmer's text editor
				ExternalEditor(itm["JSONCameraConfigFileLineTxt"].Text)
			else:
				# Label was clicked on with no modifier keys so open the containing folder in the operating system's folder browsing view
				ShowFolderFromFilepath(itm["JSONCameraConfigFileLineTxt"].Text)
		dlg.On.ShowJSONFilenameButton.Clicked = ShowJSONFilenameButtonFunc

		# Show a file browsing dialog to select the JSON file
		def JSONBrowseFileButtonFunc(ev):
			selectedPath = fu.RequestFile()
			if selectedPath:
				itm["JSONCameraConfigFileLineTxt"].Text = selectedPath
				if os.path.isfile(app.MapPath(selectedPath)):
					if selectedPath.endswith(".json") and not selectedPath.startswith("."):
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
			else:
				itm["ShowJSONFilenameButton"].Visible = True
				itm["JSONCameraConfigFileLineTxt"].Visible = True
				itm["JSONBrowseFileButton"].Visible = True
				itm["JSONSourceGroup"].Visible = True
			dlg:RecalcLayout()
		dlg.On.CameraArrayGeometryCombo.CurrentIndexChanged = CameraArrayGeometryComboFunc

		def ShotTypeCalibrationCheckboxFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if ("calibration" in item.Text[4].lower() and ("post calibration" not in item.Text[4].lower() and "post-calibration" not in item.Text[4].lower())):
					if itm["ShotTypeCalibrationCheckbox"].Checked:
						item.CheckState[0] = "Checked"
					else:
						item.CheckState[0] = "Unchecked"
		dlg.On.ShotTypeCalibrationCheckbox.Clicked = ShotTypeCalibrationCheckboxFunc

		def ShotTypePostCalibrationCheckboxFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if ("post calibration" in item.Text[4].lower() or "post-calibration" in item.Text[4].lower()):
					if itm["ShotTypePostCalibrationCheckbox"].Checked:
						item.CheckState[0] = "Checked"
					else:
						item.CheckState[0] = "Unchecked"
		dlg.On.ShotTypePostCalibrationCheckbox.Clicked = ShotTypePostCalibrationCheckboxFunc

		def ShotTypeHDRICheckboxFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if (("hdri" in item.Text[4].lower()) or ("light probe" in item.Text[4].lower())):
					if itm["ShotTypeHDRICheckbox"].Checked:
						item.CheckState[0] = "Checked"
					else:
						item.CheckState[0] = "Unchecked"
		dlg.On.ShotTypeHDRICheckbox.Clicked = ShotTypeHDRICheckboxFunc

		def ShotTypeContentCheckboxFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if (("hdri" not in item.Text[4].lower()) and ("light probe" not in item.Text[4].lower())) and ("calibration" not in item.Text[4].lower()):
					if itm["ShotTypeContentCheckbox"].Checked:
						item.CheckState[0] = "Checked"
					else:
						item.CheckState[0] = "Unchecked"
		dlg.On.ShotTypeContentCheckbox.Clicked = ShotTypeContentCheckboxFunc

		# The Select "All" button was pressed - Limit Select All by Shot Type so "Calibration + All" will select all calibration items
		def SelectAllButtonFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)

				item.CheckState[0] = "Unchecked"
				if ("post calibration" in item.Text[4].lower() or "post-calibration" in item.Text[4].lower()) and itm["ShotTypePostCalibrationCheckbox"].Checked:
					item.CheckState[0] = "Checked"
				elif ("calibration" in item.Text[4].lower() and ("post calibration" not in item.Text[4].lower() or "post-calibration" not in item.Text[4].lower())) and itm["ShotTypeCalibrationCheckbox"].Checked:
					item.CheckState[0] = "Checked"
				elif (("hdri" in item.Text[4].lower()) or ("light probe" in item.Text[4].lower())) and itm["ShotTypeHDRICheckbox"].Checked:
					item.CheckState[0] = "Checked"
				elif (("hdri" not in item.Text[4].lower()) and ("light probe" not in item.Text[4].lower())) and ("calibration" not in item.Text[4].lower()) and itm["ShotTypeContentCheckbox"].Checked:
					item.CheckState[0] = "Checked"
		dlg.On.SelectAllButton.Clicked = SelectAllButtonFunc

		# The Select "None" button was pressed
		def SelectNoneButtonFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				item.CheckState[0] = "Unchecked"
		dlg.On.SelectNoneButton.Clicked = SelectNoneButtonFunc

		# The Select "Invert" button was pressed
		def SelectInvertButtonFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if ("post-calibration" in item.Text[4].lower() or "post calibration" in item.Text[4].lower()):
					if itm["ShotTypePostCalibrationCheckbox"].Checked:
						if item.CheckState[0] == "Unchecked":
							item.CheckState[0] = "Checked"
						else:
							item.CheckState[0] = "Unchecked"
				elif ("calibration" in item.Text[4].lower()):
					if itm["ShotTypeCalibrationCheckbox"].Checked:
						if item.CheckState[0] == "Unchecked":
							item.CheckState[0] = "Checked"
						else:
							item.CheckState[0] = "Unchecked"
				if (("hdri" in item.Text[4].lower()) or ("light probe" in item.Text[4].lower())):
					if itm["ShotTypeHDRICheckbox"].Checked:
						if item.CheckState[0] == "Unchecked":
							item.CheckState[0] = "Checked"
						else:
							item.CheckState[0] = "Unchecked"
				if (("hdri" not in item.Text[4].lower()) and ("light probe" not in item.Text[4].lower())) and ("calibration" not in item.Text[4].lower()):
					if itm["ShotTypeContentCheckbox"].Checked:
						if item.CheckState[0] == "Unchecked":
							item.CheckState[0] = "Checked"
						else:
							item.CheckState[0] = "Unchecked"
		dlg.On.SelectInvertButton.Clicked = SelectInvertButtonFunc

		def FuzzyR3DDateMatchingCheckboxFunc(ev):
			print("[Lightfielder][Preferences] Updated \"Fuzzy R3D Date Matching\"")
			PrefSave(dlg)

			# Write the preferences to disk
			app.SavePrefs()

			itm = dlg.GetItems()
			itm["ProgressLabel"].Text = "  Progress: Updated \"Fuzzy R3D Date Matching\""
		dlg.On.FuzzyR3DDateMatchingCheckbox.Clicked = FuzzyR3DDateMatchingCheckboxFunc
		
		def AddMediaToSourcesFolderCheckboxFunc(ev):
			print("[Lightfielder][Preferences] Updated \"Add Media To Sources Folder\"")
			PrefSave(dlg)

			# Write the preferences to disk
			app.SavePrefs()

			itm = dlg.GetItems()
			itm["ProgressLabel"].Text = "  Progress: Updated \"Add Media To Sources Folder\""
		dlg.On.AddMediaToSourcesFolderCheckbox.Clicked = AddMediaToSourcesFolderCheckboxFunc

		# The "Type Color" checkbox was clicked on
		def TypeColorCheckboxFunc(ev):
			RefreshTree()
		dlg.On.TypeColorCheckbox.Clicked = TypeColorCheckboxFunc

		# The Tree view row was clicked on
		def TreeClickedFunc(ev):
			if ev["item"]:
				if ev["column"] >= 1:
					if ev["item"].CheckState[0] == "Checked":
						# Remove the item
						ev["item"].CheckState[0] = "Unchecked"
					elif ev["item"].CheckState[0] == "Unchecked":
						# Add the item
						ev["item"].CheckState[0] = "Checked"
		dlg.On.Tree.ItemClicked = TreeClickedFunc

		def GoButtonFunc(ev):
			cameraArrayGeometry = itm["CameraArrayGeometryCombo"].CurrentIndex
			PrefSave(dlg)
			# Write the preferences to disk
			app.SavePrefs()

			ShotTypeItems = []
			resultStr = ""
			
			resultStr += "\n<h2>Start Processing</h2>\n"
			startTimer = datetime.datetime.now()
			startTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")
			resultStr += "\n<p>" + str(startTimeStamp) + " (HH:MM:SS)</p>\n"

			resultStr += "\n<p>Camera Array Geometry: Menu Item #" + str(cameraArrayGeometry) + " - " + str(itm["CameraArrayGeometryCombo"].CurrentText) + "</p>\n"

			resultStr += "\n<h2>Shot Types:</h2>\n"
			resultStr += "<ul>\n"
			if itm["ShotTypeCalibrationCheckbox"].Checked:
				resultStr += "\t<li>Calibration</li>\n"
				ShotTypeItems.append("Calibration")
			if itm["ShotTypePostCalibrationCheckbox"].Checked:
				resultStr += "\t<li>Post-Calibration</li>\n"
				ShotTypeItems.append("Post-Calibration")
			if itm["ShotTypeHDRICheckbox"].Checked:
				resultStr += "\t<li>HDRI</li>\n"
				ShotTypeItems.append("HDRI")
			if itm["ShotTypeContentCheckbox"].Checked:
				resultStr += "\t<li>Content</li>\n"
				ShotTypeItems.append("Content")
			resultStr += "</ul>\n"

			#print("\n[Lightfielder][Shotlog][Start Processing]")
			itm["ProgressLabel"].Text = "  Progress: Started Processing"

			shotlogFile = str(app.MapPath(itm["FileLineTxt"].Text))
			mediaFolder = str(app.MapPath(itm["FolderLineTxt"].Text))
			jsonCameraConfigFile = str(app.MapPath(itm["JSONCameraConfigFileLineTxt"].Text))
			cameraJSONConfigViews = GetJSONConfigViews(jsonCameraConfigFile, "records")
			# Debug print the JSON list content
			#if cameraJSONConfigViews != None:
			#	for c in cameraJSONConfigViews:
			#		print("\t", c)

			# Debug exit point:
			#return

			# Enabled Shots from CSV List
			csvShotIDCheckedItems = []
			csvClipIDCheckedItems = []
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if item.CheckState[0] == "Checked":
					csvClipIDCheckedItems.append(int(item.Text[1]))
					csvShotIDCheckedItems.append(int(item.Text[2]))
			# print("[csvClipIDCheckedItems]")
			# print(csvClipIDCheckedItems)
			# print("[csvShotIDCheckedItems]")
			# print(csvShotIDCheckedItems)

			# Debug exit point:
			# return

			if (shotlogFile == "") and (mediaFolder == ""):
				itm["ProgressLabel"] = "  Progress: \"Footage Folder\" and \"CSV Source File\" text fields are empty."
			elif (shotlogFile == ""):
				itm["ProgressLabel"] = "  Progress: \"CSV Source File\" text field is empty."
			elif (mediaFolder == ""):
				itm["ProgressLabel"] = "  Progress: \"Footage Folder\" text field is empty."
			elif (cameraArrayGeometry == 2) and (jsonCameraConfigFile == ""):
				# The polar array needs a JSON camera cofig file
				itm["ProgressLabel"] = "  Progress: \"JSON Source File\" text field is empty."
			else:
				processResult, missingItems = ProcessShotlog(shotlogFile, mediaFolder, itm["ProgressLabel"], csvShotIDCheckedItems, csvClipIDCheckedItems, cameraArrayGeometry, cameraJSONConfigViews)

				resultStr += str(processResult)
				resultStr += "\n<h2>Completed Processing</h2>\n"

				endTimer = datetime.datetime.now()
				endTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")
				resultStr += "\n<p>" + str(endTimeStamp) + " (HH:MM:SS)</p>\n"

				elapsedTime = (endTimer - startTimer).total_seconds()
				mins, secs = divmod(elapsedTime, 60)
				timeFormatted = "Elapsed Time: " + str(math.ceil(mins)).zfill(2) + " Minutes " + str(math.ceil(secs)).zfill(2) + " Seconds"
				resultStr += "\n<p>" + str(timeFormatted) + "</p>\n"

				itm["ProgressLabel"] = "  Progress: Completed Processing [Wallclock " + GetTimeElapsed(startTimer) + "]"

				# Play the sound effect
				soundName = app.GetData("Lightfielder.SoundEffectsComplete")
				if len(missingItems) >= 1:
					# Camera views are missing
					soundName = app.GetData("Lightfielder.SoundEffectsError")
				if soundName != None:
					SoundEffectSelect(soundName)

				# dlg.Hide()
				SaveReportShotLog(resultStr)
				ResultsWindow("Import Footage Complete", resultStr)

				# Close the window
				# disp.ExitLoop()
		dlg.On.GoButton.Clicked = GoButtonFunc

		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.ImportFootageWin.Geometry")

		# Load the CSV and Footage folder pref
		PrefLoad(dlg)

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('ImportFootageWin', {
			Target {
				ID = 'ImportFootageWin',
			},
			Hotkeys {
				Target = 'ImportFootageWin',
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
		WindowPrefSave(dlg, "Lightfielder.ImportFootageWin.Geometry")
		# Save the CSV and Footage folder pref
		PrefSave(dlg)

def ProcessShotlog(shotlogFile, shotlogMediaFolder, progressLabel, shotCheckedItems, clipCheckedItems, cameraArrayGeometry, cameraJSONConfigViews):
	# frame rate
	fps = GetProjectFrameRate()
	# fps = GetSensorFrameRate()
	# fps = 60
	# fps = 30
	# fps = 29.97
	# fps = 24

	logResultStr = ""

	project = GetProject()
	mediapool = project.GetMediaPool()

	progressLabel.Text = "  Progress: Locating Bins"
	# Find the footage folder
	timelinesBinName, timelinesBin = FindTimelineBin()
	timelinesStillFramesBinName, timelinesStillFramesBin = FindTimelineStillFramesBin()

	footageBinName, footageBin = FindFootageBin()
	#print("[Lightfielder][Timelines Bin] [Name] " + str(timelinesBinName))
	#print("[Lightfielder][Timelines Still Frames Bin] [Name] " + str(timelinesStillFramesBinName))
	#print("[Lightfielder][Footage Bin] [Name] " + str(footageBinName))

	# Parse the CSV File for Shot IDs
	progressLabel.Text = "  Progress: Import CSV"
	# Find the foot
	csvItems, csvResult = ImportCSV(app.MapPath(shotlogFile))
	#print(csvItems)
	logResultStr += str(csvResult)

	# Debug return
	# return logResultStr

	# Import the R3D files
	progressLabel.Text = "  Progress: Import Media"
	importResult = ""

	# Debug return
	# return logResultStr

	clipItems, importResult, missingItems = ImportMedia(csvItems, shotlogMediaFolder, footageBin, footageBinName, progressLabel, shotCheckedItems, clipCheckedItems, cameraArrayGeometry, cameraJSONConfigViews)
	logResultStr += str(importResult)

	#print(logResultStr)
	return logResultStr, missingItems

if __name__ == "__main__":
	ImportFootageWindow()
