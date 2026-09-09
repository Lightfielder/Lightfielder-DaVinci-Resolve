"""
Lightfielder 07 Create EDLs.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Creates new editing timelines with the multi-view content placed vertically across many tracks, or in a single horizontal track.

Script Usage:

1. Open Resolve. Select the menu item: "Workspace > Scripts > Lightfielder > 07 Create EDLs"  • OR Select Tool Bar then click "06 Create EDLs" button.

2. Use the "CSV Source File" text field to select a .csv (Comma Separated Value) formatted shotlog file.

3. The "Shot Type" checkboxes let you globally enable/disable takes based upon the Shotlog.csv description field content. Select if the shot type is either a "Calibration", "Post-Calibration", "HDRI", or "Content" output.

4. The tree view's "Active" checkbox column lets you enable the processing of individual takes. The Select "All", "None", and "Invert" buttons allow you to quickly toggle the Tree view selection.

5. Click the "Prepare EDLs…" button to prepare new timelines.

6. When you go to export your finished edited and color graded content, the Resolve Deliver page uses a set of export presets that are paired against the shot type:

- Calibration
- Post-Calibration
- Content
- HDRI

Notes:
- Added code to deal with the Resolve Studio v19.0.3 "off by one" frame correction change for Adding clips to timeline items issue:
https://www.steakunderwater.com/wesuckless/viewtopic.php?p=52659#p52659

Todo:
- Add catch/try to range intersection comparison
- Validate the CSV uiTree list limit is applied to the timeline creation matching
- Write elapsed time to the report window
- Validate if there are zero clips to add to a timeline
- Validate if the deliver page preset exists before running the timeline creation job
- uiTree list to allow multiple timeline selection
- Allow On/Off timeline selection
- Allow per-entry output location data entry
- Allow saving this queue list info to a .json file that can be used to rebuild a cloud render preset list

- Deliver - Trigger script at end of render - use a python script to add the rendered footage into the "01_Delivery/still_frame" folder.

* * *

Calibration Import:
JSON Data format:
01 {'camera_distortion': [-0.09579707185891037, 0.12186457730848849, -0.00016405437197997908, 0.00015909545310126505, 0.0], 'camera_matrix': [[8194.856074831321, 0.0, 1638.4779942456462], [0.0, 8193.145360070946, 3067.10171049854], [0.0, 0.0, 1.0]], 'reproj_error': 0.036654092718717994}

Brown-Conrady model output:
k1	k2	p1	p2	k3

"""

import subprocess
import re
import csv, os, json, datetime, math
import platform
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

startTimer = datetime.datetime.now()

def GenerateHTML(filePath, data):
	message = "\t\t<p>JSON File: " + str(filePath) + "</p><br>\n"
	message += "\t\t<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
	message += "\t\t\t<tr><td>Camera</td><td>k1</td><td>k2</td><td>p1</td><td>p2</td><td>k3</td></tr>\n"

	try:
		for key, value in data.items():
			cameraNum = int(key)
			params = value

			#print(key, "\n\t", value)
			print("[" + str(cameraNum) + "]")

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

def CreateEDLWindow():
	presetsBasePath = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Calibration/")

	res = app.GetResolve()

	# Get the project name
	project = GetProject()
	if project is None:
		print("[Lightfielder] No Resolve project is open at this time.")
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
			"ID": "CreateEDLWin",
			"TargetID" : "CreateEDLWin",
			"Geometry": [500, 50, 495, 730],
			"MinimumSize": [482, 730],
			"FixedSize": [482, 730],
			# "Spacing": 0,
			# "Margin": 5,
		},[
			ui.VGroup({
				"ID": "Content",
				"Weight": 0.1,
			},[
				ui.VGroup({
					"Weight": 0.01,
				},[
					ui.HGroup({
						"Weight": 0.5,
					},[
						ui.Label({
							"ID": "ViewLabel",
							"Text": "07 Create EDLs",
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
						"ID": "ExportTxt",
						"Text": "Tip of the day: Make sure to verify the \"Project Settings > Color Management > Output Color Space\" preference lines up with your Deliver page JPEG/TIF/EXR output format.",
						"ReadOnly": True,
						"StyleSheet": "QTextEdit { border: 0px; }",
						"Weight": 0.01,
					}),
					ui.Label({
						"ID": "DividerLabel",
						"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
						"Spacing": 0,
						"Margin": 0,
						"Weight": 0.01,
					}),
				]),
				ui.VGroup({
					"Weight": 0.1,
					"ID": "ExportTab",
					"Spacing": 10,
				},[
					ui.HGroup({
						"Weight": 0.1,
					},[
						ui.Button({
							"ID": "ShowCSVFilenameButton",
							"Flat": True,
							"MinimumSize": [100, 32],
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
						ui.Button({"ID": "BrowseFileButton",
							"Text": "Browse",
							"MinimumSize": [100, 32],
							"Weight": 0.1
						}),
					]),
					ui.HGroup({
						"Weight": 0.1,
					},[
						ui.Label({
							"ID": "FrameSelectionLabel",
							"Text": "Frame Selection",
							"Weight": 0.1,
							"MinimumSize": [100, 32],
						}),
						ui.ComboBox({
							"ID": "FrameSelectionCombo",
							"Text": "Mode",
							"Weight": 1.0,
						}),
					]),
					ui.HGroup({
						"Weight": 0.1,
					},[
						ui.Label({
							"ID": "TrackLayoutLabel",
							"Text": "Track Layout",
							"Weight": 0.1,
							"MinimumSize": [100, 32],
						}),
						ui.ComboBox({
							"ID": "TrackLayoutCombo",
							"Text": "Track Layout",
							"ToolTip": "Should the multi-view footage from each take be added to the new timeline \nwith a vertical track positioning, or horizontal track positioning for each clip? \n\nThe vertical option places the ~55 camera views into video track V1 to V55. \nThe horizontal option places all ~55 camera view clips sequentially into \nvideo track V1.",
							"Weight": 1.0
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
# 						ui.CheckBox({
# 							"ID": "RigSectionAsClipColorCheckbox",
# 							"Text": "Rig Section as Clip Color",
# 							"ToolTip": "Use the rig section value as the basis of the clip color",
# 							"Checked": False,
# 						}),
						ui.CheckBox({
							"ID": "CreateOneTimelineCheckbox",
							"Text": "Create One Timeline",
							"ToolTip": "(WIP) Assemble a single timeline with the clips added from all takes and for all of the shot types.",
							"Checked": False,
						}),
						ui.CheckBox({
							"ID": "FuzzyR3DDateMatchingCheckbox",
							"Text": "Fuzzy R3D Date Matching",
							"ToolTip": "(WIP) When this option is enabled the Shotlog CSV date field will be considered \na match with the R3D filename date value if they are within 1 day +/-.",
							"Checked": False,
						}),
						ui.VGap(20),
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
							"Weight": 1.0,
							"Events": {
								"CurrentItemChanged": True,
								"ItemChanged": True,
								"ItemActivated": True,
								"ItemClicked": True,
								"ItemDoubleClicked": True,
							},
							"MinimumSize": [100, 100],
							#"MinimumSize": [100, 400],
						}),
					]),
# 					ui.HGroup({
# 						"Weight": 0.1,
# 					},[
# 						ui.Label({"ID": "ExportFolderLabel", "Text": "Output Folder", "Weight": 0.1, "MinimumSize": [100, 32],}),
# 						ui.LineEdit({"ID": "ExportFolderLineTxt", "Text": "", "PlaceholderText": "Please enter a folder path.", "Weight": 0.9}),
# 						ui.Button({"ID": "ExportBrowseFolderButton", "Text": "Browse", "MinimumSize": [100, 32], "Weight": 0.1}),
# 					]),
# 					ui.HGroup({
# 						"Weight": 0.1,
# 					},[
# 						ui.CheckBox({
# 							"ID": "AddToRenderQueueCheckbox",
# 							"Text": "Add to Render Queue",
# 							"Checked": False,
# 						}),
# 						ui.CheckBox({
# 							"ID": "StartRenderingCheckbox",
# 							"Text": "Auto Start Rendering in Queue",
# 							"Checked": False,
# 						}),
# 					]),
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
							"Weight": 0.5,
						}),
						ui.Button({
							"ID": "PrepareExportButton",
							"Text": "Prepare EDLs...",
							"MinimumSize": [120, 25],
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

		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
		progressLabel = itm["ProgressLabel"]

		# Frame Selection
		itm["FrameSelectionCombo"].AddItem("Original Duration (Not in Sync)")
		# itm["FrameSelectionCombo"].AddItem("Minimal Timecode Sync")
		itm["FrameSelectionCombo"].AddItem("First Common Frame (Still Frames)")
		itm["FrameSelectionCombo"].AddItem("Middle Common Frame (Still Frames)")
		itm["FrameSelectionCombo"].AddItem("Last Common Frame (Still Frames)")
		# itm["FrameSelectionCombo"].AddItem("(First Common Sequence (10 Seconds)")
		# itm["FrameSelectionCombo"].AddItem("Middle Common Sequence (10 Seconds)")
		# itm["FrameSelectionCombo"].AddItem("Last Common Sequence (10 Seconds)")

		# Timeline build direction
		itm["TrackLayoutCombo"].AddItem("To Vertical Stack")
		itm["TrackLayoutCombo"].AddItem("To Horizontal Stack")
		itm["TrackLayoutCombo"].CurrentIndex = 0

# 		# Add the items to the Presets ComboBox menu
# 		itm["PresetCombo"].AddItem("New Session...")
# 		for file in sorted(os.listdir(presetsBasePath)):
# 			if file.endswith(".ipynb") and not file.startswith("."):
# 				presetFile = file
# 				itm["PresetCombo"].AddItem(presetFile)
# 				# print(presetFile)

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

		def PrefSave(winDlg):
			# Save the prefs
			if winDlg != None:
				print("[Lightfielder][Preferences] Saved")
				#app.SetData("Lightfielder.ExportFolder", itm["ExportFolderLineTxt"].Text)
				app.SetData("Lightfielder.Calibration", itm["ShotTypeCalibrationCheckbox"].Checked)
				app.SetData("Lightfielder.Post-Calibration", itm["ShotTypePostCalibrationCheckbox"].Checked)
				app.SetData("Lightfielder.HDRI", itm["ShotTypeHDRICheckbox"].Checked)
				app.SetData("Lightfielder.Content", itm["ShotTypeContentCheckbox"].Checked)
				app.SetData("Lightfielder.FuzzyR3DDateMatching", itm["FuzzyR3DDateMatchingCheckbox"].Checked)
# 				app.SetData("Lightfielder.RigSectionAsClipColor", itm["RigSectionAsClipColorCheckbox"].Checked)
				app.SetData("Lightfielder.CSVFile", itm["FileLineTxt"].Text)
				#print(app.GetData("Lightfielder"))

		def PrefLoad(winDlg):
			# Restore the prefs
			if winDlg != None:
				# print("[Lightfielder][Preferences] Loaded")
				# print(app.GetData("Lightfielder"))
				# Footage Folder
				#pref = app.GetData("Lightfielder.ExportFolder")
				#if pref != None:
				#	# print(pref)
				#	itm["ExportFolderLineTxt"].Text = pref
				# ShotType
				pref = app.GetData("Lightfielder.Calibration")
				if pref != None:
					# print(pref)
					itm["ShotTypeCalibrationCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.Post-Calibration")
				if pref != None:
					# print(pref)
					itm["ShotTypePostCalibrationCheckbox"].Checked = pref
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
# 				pref = app.GetData("Lightfielder.RigSectionAsClipColor")
# 				if pref != None:
# 					# print(pref)
# 					itm["RigSectionAsClipColorCheckbox"].Checked = pref
				pref = app.GetData("Lightfielder.CSVFile")
				if pref != None:
					# print(pref)
					itm["FileLineTxt"].Text = pref
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
			WindowPrefSave(dlg, "Lightfielder.CreateEDLWin.Geometry")

			# Save the export folder pref
			PrefSave(dlg)
		dlg.On.CreateEDLWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.CreateEDLWin.Geometry")

			# Save the export folder pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.CreateEDLWin.Close = CloseFunc

		def CloseButtonFunc(ev):
			print("[Lightfielder][Window][Close Button]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.CreateEDLWin.Geometry")

			# Save the export folder pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.CloseButton.Clicked = CloseButtonFunc

		# Add your GUI element based event functions here:

		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_07_Create_EDLs.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		def ShotTypePostCalibrationCheckboxFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if ("post calibration" in item.Text[4].lower() or "post-calibration" in item.Text[4].lower()):
					if itm["ShotTypePostCalibrationCheckbox"].Checked:
						item.CheckState[0] = "Checked"
					else:
						item.CheckState[0] = "Unchecked"
		dlg.On.ShotTypePostCalibrationCheckbox.Clicked = ShotTypePostCalibrationCheckboxFunc

		def ShotTypeCalibrationCheckboxFunc(ev):
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if ("calibration" in item.Text[4].lower() and ("post calibration" not in item.Text[4].lower() and "post-calibration" not in item.Text[4].lower())):
					if itm["ShotTypeCalibrationCheckbox"].Checked:
						item.CheckState[0] = "Checked"
					else:
						item.CheckState[0] = "Unchecked"
		dlg.On.ShotTypeCalibrationCheckbox.Clicked = ShotTypeCalibrationCheckboxFunc

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

			itm["ProgressLabel"].Text = "  Progress: Updated \"Fuzzy R3D Date Matching\""
		dlg.On.FuzzyR3DDateMatchingCheckbox.Clicked = FuzzyR3DDateMatchingCheckboxFunc

		# The "Type Color" checkbox was clicked on
		def TypeColorCheckboxFunc(ev):
			RefreshTree()
		dlg.On.TypeColorCheckbox.Clicked = TypeColorCheckboxFunc

# 		def RigSectionAsClipColorCheckboxFunc(ev):
# 			print("[Lightfielder][Preferences] Rig Section as Clip Color" + str(itm["RigSectionAsClipColorCheckbox"].Checked))
# 			PrefSave(dlg)
# 			
# 			# Write the preferences to disk
# 			app.SavePrefs()
# 		dlg.On.RigSectionAsClipColorCheckbox.Clicked = RigSectionAsClipColorCheckboxFunc

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

		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool7", "Tool6")

			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool7", "Tool8")

			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		def PrepareExportButtonFunc(ev):
			res = app.GetResolve()
			project = GetProject()
			mediapool = project.GetMediaPool()
			# res.OpenPage("edit")

			ShotTypeItems = []
			csvShotIDCheckedItems = []
			csvClipIDCheckedItems = []

			# frame rate
			fps = GetProjectFrameRate()
			# fps = GetSensorFrameRate()
			# fps = 60
			# fps = 30
			# fps = 29.97
			# fps = 24

			# Get the number of cameras views in the array
			maxCameras = GetMaxNumberOfCameras()

			# Enabled Shots from CSV List
			for c in range(int(itm["Tree"].TopLevelItemCount())):
				item = itm["Tree"].TopLevelItem(c)
				if item.CheckState[0] == "Checked":
					csvClipIDCheckedItems.append(item.Text[1])
					csvShotIDCheckedItems.append(item.Text[2])

			# Check the track orientation
			trackLayout = int(itm["TrackLayoutCombo"].CurrentIndex)

			print("[Lightfielder][Prepare Export]")
			processResult = ""
			resultStr = ""
			resultStr += "\n<h1>Start Processing</h1>\n"

			# Deal with the Resolve Studio v19.0.3 "off by one" frame correction change for Adding clips to timeline items issue:
			# https://www.steakunderwater.com/wesuckless/viewtopic.php?p=52659#p52659
			resolveVersion = str(app.GetAttrs()["FUSIONS_Version"]).split(".")
			frameOffset = 0

			# Check what type of footage to import
			mediaFormat = app.GetData("Lightfielder.MediaFormat") or "R3D"

			# Look for Resolve 19.0.3+
			if int(resolveVersion[0]) == 19:
				if (int(resolveVersion[1]) == 0):
					if (int(resolveVersion[2]) >= 3):
						print("[Lightfielder][Note] A frame offset of 1 was required for Resolve Studio v19.0.3+")
						resultStr += "\n\n<p>Note: A frame offset of 1 was required for Resolve Studio v19.0.3+</p>\n"
						frameOffset = 1
				if (int(resolveVersion[1]) >= 1):
					print("[Lightfielder][Note] A frame offset of 1 was required for Resolve Studio v19.0.3+")
					resultStr += "\n\n<p>Note: A frame offset of 1 was required for Resolve Studio v19.0.3+</p>\n"
					frameOffset = 1
			if int(resolveVersion[0]) >= 20:
				print("[Lightfielder][Note] A frame offset of 1 was required for Resolve Studio v19.0.3+")
				resultStr += "\n\n<p>Note: A frame offset of 1 was required for Resolve Studio v19.0.3+</p>\n"
				frameOffset = 1

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

			print("[csvShotIDCheckedItems]")
			print(csvShotIDCheckedItems)
			print("[csvClipIDCheckedItems]")
			print(csvClipIDCheckedItems)

			resultStr += "\n<p>Frame Selection: " + str(itm["FrameSelectionCombo"].CurrentText) + "</p>\n"
			resultStr += "\n<p>Track Layout: " + str(itm["TrackLayoutCombo"].CurrentText) + "</p>" + "\n"
			startTimer = datetime.datetime.now()
			startTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")
			timelineTimeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")
			resultStr += "\n<p>" + str(startTimeStamp) + " (HH:MM:SS)</p>\n"

			footageBinName, footageBin = FindFootageBin()
			print("[Lightfielder][Footage Bin] [Name] " + str(footageBinName))

			# Scan inside the footage folder
			if footageBin is None:
				resultStr += "<p>Warning: The \"footage\" bin is missing!</p>\n"
			else:
				for ShotType in ShotTypeItems:
					# Bin folders
					FilepathItems = []
					FolderItems = []
					mpItems = []
					mpR3DItems = []
					clipItems = []
					shotIDItems = []

					# First Common Frame/Middle Common Frame/Last Common Frame
					frameSelectionMode = itm["FrameSelectionCombo"].CurrentText

					# Get the number of cameras views in the array
					maxCameras = GetMaxNumberOfCameras()

					def GetSubFolder(parentFolder, path):
						for folder in parentFolder.GetSubFolderList():
							if path != "":
								updatedPath = str(path) + "/" + str(folder.GetName())
							else:
								updatedPath = str(folder.GetName())
							FilepathItems.append(updatedPath)
							FolderItems.append(folder)

							# Scan Deeper
							GetSubFolder(folder, updatedPath)

					# Build the folder paths
					GetSubFolder(footageBin, "")

					#print("[Footage]")
					if FolderItems is not None:
						for folder in FolderItems:
							# print(folder.GetName())
							clips = folder.GetClips()
							for key in clips:
								mpItem = clips[key]
								mpItems.append(mpItem)
					if mpItems is not None:
						for mpItem in mpItems:
							mpFile = str(mpItem.GetClipProperty("File Path"))
							# All media in the bins
							# print(mpFile)
							# print(".")
							# Filter down to only show the media in the bins
							if not mpFile.startswith("."):
								if mediaFormat == "R3D" and mpFile.endswith(('.R3D', '.r3d')):
									# Red Digital Cinema R3D RAW
									mpR3DItems.append(mpItem)
								elif mediaFormat == "Movie" and mpFile.endswith(('.MOV', '.mov', '.MP4', '.mp4', '.MKV', '.mkv')):
									# Quicktime, MP4, MKV video
									mpR3DItems.append(mpItem)
								elif (mediaFormat == "Image Sequence" or mediaFormat == "Still Frame") and mpFile.endswith(('.PNG', '.png', '.JPEG', '.jpeg', '.JPG', '.jpg', '.EXR', '.exr', '.DPX', '.dpx', '.TIF', '.TIFF', '.tif', '.tiff')):
									# PNG, JPEG, EXR, DPX, TIFF,
									mpR3DItems.append(mpItem)
								else:
									# Fallback: Unknown media format from the preferences
									# Red Digital Cinema R3D RAW
									if mpFile.endswith(('.R3D', '.r3d')):
										mpR3DItems.append(mpItem)
					
					resultStr += "\n<h2>" + str(ShotType) + " Shot List</h2>" + "\n"
					resultStr += "<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
					resultStr += "<tr><td>Shot ID</td></tr>\n"
					if mpR3DItems is not None:
						for mpClip in mpR3DItems:
							mpShotType = mpClip.GetMetadata("Shot Type")
							if mpShotType == str(ShotType).lower():
								shot = mpClip.GetMetadata("Shot")
								if shot not in shotIDItems:
									# Check if the shot is checked in the CSV uiTree
									if shot in csvShotIDCheckedItems:
										clip = mpClip.GetMetadata("Clip Number")
										# Check if the clip is checked in the CSV uiTree
										if clip in csvClipIDCheckedItems:
											shotIDItems.append(shot)
											resultStr += "\t<tr><td>" + str(shot) + "</td>\n"
											# print(".")
					resultStr += "</table>"

					# Build the r3d media pool clip list
					#resultStr += "\n<h2>Media</h2>" + "\n"
					#resultStr += "<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
					#resultStr += "<tr><td>Clip ID</td><td>Shot ID</td><td>Angle</td><td>Shot Type</td><td>Description</td><td>File</td><td>Start Frame</td></tr>\n"

					if mpR3DItems is not None:
						counter = 0
						shot_counter = 0
						clipItemsCount = len(mpR3DItems or "")
						for sID in shotIDItems:
							# Build a list of the frame ranges for media in one clip ID/ShotID combo
							sRangeItems = []
							# Increment the timeline start frame by each shot to allow vertical timelines
							# timelineStartFrames + shot_counter
							# Scan the shot ID for the frame ranges
							for mpClip in mpR3DItems:
								mpShotType = mpClip.GetMetadata("Shot Type")
								if mpShotType == str(ShotType).lower():
									shot = mpClip.GetMetadata("Shot")
									# print("[Shot] ", shot)
									if sID == shot:
										mpStartTC = str(mpClip.GetClipProperty("Start TC"))
										mpEndTC = str(mpClip.GetClipProperty("End TC"))
										# print("[Start] ", mpStartTC, "[End] ", mpEndTC)
										# Convert to timecode to frames
										sourceStartFrame = otio.opentime.to_frames(otio.opentime.from_timecode(mpStartTC, fps))
										sourceEndFrame = otio.opentime.to_frames(otio.opentime.from_timecode(mpEndTC, fps))
										sRangeItems.append(list(range(sourceStartFrame, sourceEndFrame)))
							# Check if the footage has a valid start frame - end frame range
							if len(sRangeItems) > 0:
								# print(sRangeItems)
								trackIndex = 1
								for mpClip in mpR3DItems:
									mpShotType = mpClip.GetMetadata("Shot Type")
									if mpShotType == str(ShotType).lower():
										shot = mpClip.GetMetadata("Shot")
										# print("[Shot] ", shot)
										if sID == shot:
											shotName = "ID_" + str(shot)

											# Frame values
											sStartFrame, sEndFrame, sDuration = IntersectFootageRanges(sRangeItems)

											# Generate timecode output from frames
											sStartTimecode = otio.opentime.to_timecode(otio.opentime.from_frames(sStartFrame, fps))
											sEndTimecode = otio.opentime.to_timecode(otio.opentime.from_frames(sEndFrame, fps))

											#resultStr += "[Media][Range] " + str(sStartFrame) + "-" + str(sEndFrame) + " [Duration] " + str(sDuration) + "<br>\n"
											#resultStr += "[Media][Range] " + str(sStartTimecode) + "-" + str(sEndTimecode) + " [Duration] " + str(sDuration) + "<br>\n"

											mpDuration = mpClip.GetClipProperty("Duration")
											mpFile = str(app.MapPath(mpClip.GetClipProperty("File Path")))
											mpProp = mpClip.GetClipProperty()

											# Grab the media pool clip name for a .r3d file
											# print(mpClip.GetName())

											# Grab the basefilename from the media pool clip absolute filename
											mediaBasename = os.path.basename(str(app.MapPath(mpFile)))
											# print(mediaBasename)

											description = mpClip.GetMetadata("Description")
											clip = mpClip.GetMetadata("Clip Number")
											camNum = mpClip.GetMetadata("Camera Position")
											angle = mpClip.GetClipProperty("Angle")
											mpStartTC = str(mpClip.GetClipProperty("Start TC"))
											mpEndTC = str(mpClip.GetClipProperty("End TC"))
											mpDuration = mpClip.GetClipProperty("Duration")
											#print(mpStartTC, mpEndTC, mpDuration)

											#timelineName = str(shotName) + "_" + str(clipName) + str(useageName)
											timelineName = "Timeline_" + str(ShotType).lower() + "_"  + str(shotName) + "_C" + str(clip) + "_" + timelineTimeStamp

											# Create a new timeline at "03_timelines/still_frames/ID_<Shot ID>_C_<Clip ID>"
											newBinName, newBin = FindTimelineShotTypeBin(str(ShotType).lower())
											mediapool.SetCurrentFolder(newBin)
											timeline = FindTimelineByName(newBin, timelineName)
											if timeline is None:
												timeline = mediapool.CreateEmptyTimeline(timelineName)
												timelineBinPath = str(footageBinName) + "/" + str(newBinName) + "/" + str(timelineName)
												# Build the timeline name
												resultStr += "\n<h2>Timeline Creation: </h2>\n"
												resultStr += "<p>" + str(timelineName) + "<p>"
												resultStr += "<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
												resultStr += "<tr><td>Single Frame Timeline</td></tr>\n"
												resultStr += "<tr><td>" + str(timelineBinPath) + "</td></tr>\n"
												resultStr += "</table>"

											timelineStartTimecode = "01:00:00:00"
											timelineStartFrames = otio.opentime.to_frames(otio.opentime.from_timecode(timelineStartTimecode, fps)) + shot_counter
											timeline = GetTimeline()
											if timeline is not None:
												timelineStartFrames = timeline.GetStartFrame() + shot_counter

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

											#resultStr += "</table>"
											startFrameUsed = 0
											sequenceTenSeconds = int(10 * fps)
											if frameSelectionMode == "Original Duration (Not in Sync)":
												# Original Duration
												if trackLayout == 0:
													# Build vertical stacked timelines
													startFrameUsed = sStartFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"recordFrame" : timelineStartFrames,
														"trackIndex" : trackIndex
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
													trackIndex += 1
												else:
													# Build horizontally stacked timelines
													startFrameUsed = sStartFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"trackIndex" : 1
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
											if frameSelectionMode == "Minimal Timecode Sync":
												# Minimal Timecode Sync
												if trackLayout == 0:
													# Build vertical stacked timelines
													startFrameUsed = sStartFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame,
														# "endFrame" : sEndFrame,
														"endFrame" : sEndFrame + frameOffset,
														"recordFrame" : timelineStartFrames,
														"trackIndex" : trackIndex
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
													trackIndex += 1
												else:
													# Build horizontally stacked timelines
													startFrameUsed = sStartFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame,
														# "endFrame" : sEndFrame,
														"endFrame" : sEndFrame + frameOffset,
														"trackIndex" : 1
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
											if frameSelectionMode == "First Common Frame (Still Frames)":
												# First Common Frame
												if trackLayout == 0:
													# Build vertical stacked timelines
													startFrameUsed = sStartFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame,
														# "endFrame" : sStartFrame,
														"endFrame" : sStartFrame + frameOffset,
														"recordFrame" : timelineStartFrames,
														"trackIndex" : trackIndex
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
													trackIndex += 1
												else:
													# Build horizontally stacked timelines
													startFrameUsed = sStartFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame,
														# "endFrame" : sStartFrame,
														"endFrame" : sStartFrame + frameOffset,
														"trackIndex" : 1
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
											if frameSelectionMode == "Middle Common Frame (Still Frames)":
												# Middle Common Frame
												if trackLayout == 0:
													# Build vertical stacked timelines
													startFrameUsed = sStartFrame + (sDuration * 0.5)
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame + (sDuration * 0.5),
														# "endFrame" : sStartFrame + (sDuration * 0.5),
														"endFrame" : sStartFrame + (sDuration * 0.5) + frameOffset,
														"recordFrame" : timelineStartFrames,
														"trackIndex" : trackIndex
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
													trackIndex += 1
												else:
													# Build horizontally stacked timelines
													startFrameUsed = sStartFrame + (sDuration * 0.5)
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame + (sDuration * 0.5),
														# "endFrame" : sStartFrame + (sDuration * 0.5),
														"endFrame" : sStartFrame + (sDuration * 0.5) + frameOffset,
														"trackIndex" : 1
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
											if frameSelectionMode == "Last Common Frame (Still Frames)":
												# Last Common Frame
												if trackLayout == 0:
													# Build vertical stacked timelines
													startFrameUsed = sEndFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sEndFrame,
														# "endFrame" : sEndFrame,
														"endFrame" : sEndFrame + frameOffset,
														"recordFrame" : timelineStartFrames,
														"trackIndex" : trackIndex
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
													trackIndex += 1
												else:
													# Build horizontally stacked timelines
													startFrameUsed = sEndFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sEndFrame,
														# "endFrame" : sEndFrame,
														"endFrame" : sEndFrame + frameOffset,
														"trackIndex" : 1
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
											if frameSelectionMode == "(First Common Sequence (10 Seconds)":
												# First Common Sequence (10 Seconds)
												if trackLayout == 0:
													# Build vertical stacked timelines
													startFrameUsed = sStartFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame,
														# "endFrame" : sStartFrame,
														"endFrame" : sStartFrame + frameOffset + sequenceTenSeconds,
														"recordFrame" : timelineStartFrames,
														"trackIndex" : trackIndex
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
													trackIndex += 1
												else:
													# Build horizontally stacked timelines
													startFrameUsed = sStartFrame
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame,
														# "endFrame" : sStartFrame,
														"endFrame" : sStartFrame + frameOffset + sequenceTenSeconds,
														"trackIndex" : 1
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
											if frameSelectionMode == "Middle Common Sequence (10 Seconds)":
												# Middle Common Sequence (10 Seconds)
												if trackLayout == 0:
													# Build vertical stacked timelines
													startFrameUsed = sStartFrame + (sDuration * 0.5)
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame + (sDuration * 0.5),
														# "endFrame" : sStartFrame + (sDuration * 0.5),
														"endFrame" : sStartFrame + (sDuration * 0.5) + frameOffset + sequenceTenSeconds,
														"recordFrame" : timelineStartFrames,
														"trackIndex" : trackIndex
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
													trackIndex += 1
												else:
													# Build horizontally stacked timelines
													startFrameUsed = sStartFrame + (sDuration * 0.5)
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sStartFrame + (sDuration * 0.5),
														# "endFrame" : sStartFrame + (sDuration * 0.5),
														"endFrame" : sStartFrame + (sDuration * 0.5) + frameOffset + sequenceTenSeconds,
														"trackIndex" : 1
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
											if frameSelectionMode == "Last Common Sequence (10 Seconds)":
												# Last Common Sequence (10 Seconds)
												if trackLayout == 0:
													# Build vertical stacked timelines
													startFrameUsed = sEndFrame - sequenceTenSeconds
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sEndFrame - sequenceTenSeconds,
														# "endFrame" : sEndFrame,
														"endFrame" : sEndFrame + frameOffset,
														"recordFrame" : timelineStartFrames,
														"trackIndex" : trackIndex
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
													trackIndex += 1
												else:
													# Build horizontally stacked timelines
													startFrameUsed = sEndFrame - sequenceTenSeconds
													mpFootage = {
														"mediaPoolItem" : mpClip,
														"startFrame": sEndFrame - sequenceTenSeconds,
														# "endFrame" : sEndFrame,
														"endFrame" : sEndFrame + frameOffset,
														"trackIndex" : 1
													}
													# Add the clip to the timeline
													mediapool.AppendToTimeline([mpFootage])
											# resultStr += "<tr><td>" + str(clip) + "</td><td>" + str(shot) + "</td><td>" + str(angle) + "</td><td>" + str(mpShotType) + "</td><td>" + str(description) + "</td><td>" + str(mpFile) + "</td><td>" + str(startFrameUsed) + "</td></tr>\n"

											counter += 1
											if int(counter) % 5 == 0:
												itm["ProgressLabel"].Text = "  Progress: Build Timeline - Comparing Clips (" + str(counter) + " of " + str(clipItemsCount) + ") [" + str(shotName) + "] [Wallclock " + GetTimeElapsed(startTimer) + "]"
							shot_counter += 1
						resultStr += "</table>\n"

						# Todo: Scan all media pool items for the metadata "Shot Type" tag so you don't need to use the CSV file
# 						itm["ProgressLabel"].Text = "  Progress: Adding to Render Queue"

						# Old code starts here
# 						timeline = GetTimeline()

						# Add something to the render queue
						# Render Preset
# 						presetName = ""
# 						if str(ShotType).lower() == "calibration":
# 							presetName = "Calibration"
# 						elif str(ShotType).lower() == "hdri":
# 							presetName = "HDRI"
# 						else:
# 							presetName = "Content"

						# Render Location
						#path = app.MapPath(itm["ExportFolderLineTxt"].Text + "/" + ShotType)
						#print("[Output Location] " + str(path))

						# Add a new render job
# 						res.OpenPage("deliver")

# 						presets = project.GetRenderPresetList()
# 						if presetName == "":
							# Use the default settings
							# Output location
							#project.SetRenderSettings({"TargetDir": path})

							#project.SetCurrentRenderFormatAndCodec(renderFormat, renderCodec)
# 							addToRenderQueue = itm["AddToRenderQueueCheckbox"].Checked
# 							if addToRenderQueue:
# 								project.AddRenderJob()
# 						elif presetName in presets:
							# Use thr HDRI or Calibration preset
# 							if presetName != "":
# 								project.LoadRenderPreset(presetName)

							# Output location
# 							project.SetRenderSettings({"TargetDir": path})

							#project.SetCurrentRenderFormatAndCodec(renderFormat, renderCodec)

							# Add to Render Queue
# 							addToRenderQueue = itm["AddToRenderQueueCheckbox"].Checked
# 							if addToRenderQueue:
# 								project.AddRenderJob()
							#disp.ExitLoop()
# 						else:
# 							print("[Requested Preset Missing] " + str(presetName))
# 							ErrorWindow("Deliver Preset Missing", "The Deliver page custom preset named \"" + str(ShotType) + "\" is missing. Please add the Lightfielder Deliver Presets. This step is covered in the \"Lightfielder Resolve Scripts\" documentation guide.")

# 			startRendering = itm["StartRenderingCheckbox"].Checked
# 			if startRendering:
# 				project.StartRendering()

			resultStr += "\n<h2>Completed Processing</h2>\n"
			endTimer = datetime.datetime.now()
			endTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")
			resultStr += "\n<p>" + str(endTimeStamp) + " (HH:MM:SS)</p>\n"

			elapsedTime = (endTimer - startTimer).total_seconds()
			mins, secs = divmod(elapsedTime, 60)
			timeFormatted = "Elapsed Time: " + str(math.ceil(mins)).zfill(2) + " Minutes " + str(math.ceil(secs)).zfill(2) + " Seconds"
			resultStr += "\n<p>" + str(timeFormatted) + "</p>\n"

			itm["ProgressLabel"].Text = "  Progress: Completed Processing [Wallclock " + GetTimeElapsed(startTimer) + "]"

			# Play the sound effect
			soundName = app.GetData("Lightfielder.SoundEffectsComplete")
			# soundName = app.GetData("Lightfielder.SoundEffectsError")
			if soundName != None:
				SoundEffectSelect(soundName)

			#print(resultStr)
			SaveReportCreateEDLsLog(resultStr)
			ResultsWindow("Prepare Export Complete", resultStr)
		dlg.On.PrepareExportButton.Clicked = PrepareExportButtonFunc

		def ImportCloseButtonFunc(ev):
			disp.ExitLoop()
		dlg.On.ImportCloseButton.Clicked = ImportCloseButtonFunc

		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.CreateEDLWin.Geometry")

		# Load the export folder pref
		PrefLoad(dlg)

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('CreateEDLWin', {
			Target {
				ID = 'CreateEDLWin',
			},
			Hotkeys {
				Target = 'CreateEDLWin',
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
		WindowPrefSave(dlg, "Lightfielder.CreateEDLWin.Geometry")
		# Save the export folder pref
		PrefSave(dlg)

if __name__ == "__main__":
	CreateEDLWindow()
