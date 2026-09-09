"""
Lightfielder 10 EDL Checker.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Quickly spot issues with a timeline before a long render is started.

Todo:
Check for offline media and have error handling.

Grade Yes/No Column
Disabled video tracks could shade the tree rows for clips that match that track #
Double clicking a row could hop the playhead to that clip
A "Show in Media Pool" option could allow one to trace back the timeline clip to the media pool item
A "Reveal File" option could allow one to see the parent folder in a Finder/Explorer/Nautilus view

"""

import datetime
import os
import subprocess
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

def CreateEDLCheckerWindow():
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectSetting = project.GetSetting()

	# Get the timeline object
	timeline = GetTimeline()
	if timeline is None:
		ErrorWindow("EDL Checker", "Please open a Resolve timeline before running this script")
	else:
		# Get the timeline name
		timelineName = timeline.GetName()
		#print("[Timeline Name] " + str(timelineName))

		# Get the timeline settings
		timelineSetting = timeline.GetSetting()

		# Get the track count
		timelineVideoTrackCount = timeline.GetTrackCount("video")

		# Should this window float above all other views
		windowFloat = app.GetData("Lightfielder.WindowStaysOnTop")
		if windowFloat is None:
			windowFloat = True

		# Create a new UI Manager window
		ui = fu.UIManager
		disp = bmd.UIDispatcher(ui)

		dlg = disp.AddWindow({
			"WindowTitle": "Lightfielder | Timeline Name: " + str(timelineName),
			"WindowFlags": {"Window": True, "WindowStaysOnTopHint": windowFloat},
			"ID": "EDLChecker",
			"TargetID" : "EDLChecker",
			"Geometry": [100, 100, 590, 615],
			"MinimumSize": [590, 615],
			"FixedSize": [590, 615],
			"Spacing": 0,
		},[
			ui.VGroup({"ID": "root",},[
				# Add your GUI elements here:
				ui.VGroup({
					"Weight": 0.01,
				},[
					ui.HGroup({
						"Weight": 0.5,
					},[
						ui.Label({
							"ID": "ViewLabel",
							"Text": "10 EDL Checker",
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
				]),
				ui.HGroup({"Spacing": 0, "Weight": 0.01,},[
					ui.Label({
					"ID": "Label",
						"Text": "Validate the media in a EDL timeline.",
						"Weight": 0.8,
					}),
					ui.VGap(10),
					ui.HGroup({"Spacing": 0, "Weight": 0.1,},[
						ui.CheckBox({
							"ID": "ClipColorCheckbox",
							"Text": "Clip Color",
							"Checked": True,
						}),
# 						ui.CheckBox({
# 							"ID": "TrackCheckbox",
# 							"Text": "Track State",
# 							"Checked": True,
# 						}),
					]),
				]),
				ui.Tree({
					"ID": "Tree",
					"SortingEnabled": True,
					"Weight": 0.5,
					"Events": {
						"CurrentItemChanged": True,
						"ItemActivated": True,
						"ItemClicked": True,
						"ItemDoubleClicked": True,
					},
				}),
				ui.TextEdit({
					"ID": "ReportTxt",
					"Text": "",
					"PlaceholderText": "EDL Report.",
					"Weight": 1.5,
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
						"ID": "RefreshButton",
						"Text": "Refresh",
						"Weight": 0.01,
						"MaximumSize": [86, 24],
						"IconSize": [24, 24],
						"Icon": ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Pre-Flight/refresh.png"}),
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
			WindowPrefSave(dlg, "Lightfielder.EDLChecker.Geometry")
		dlg.On.EDLExportWin.Hide = HideFunc

		# The window was closed
		def Closefunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.EDLChecker.Geometry")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.EDLChecker.Close = Closefunc

		def CloseButtonFunc(ev):
			print("[Lightfielder][Window][Close Button]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.EDLChecker.Geometry")

			# Save the export folder pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.CloseButton.Clicked = CloseButtonFunc

		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool10", "Tool9")

			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool10", "Tool11")

			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		# Add your GUI element based event functions here:

		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_10_EDL_Checker.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		# Add a header row
		hdr = itm["Tree"].NewItem()

		hdr.Text[0] = "#"
		hdr.Text[1] = "Date Recorded"
		hdr.Text[2] = "Clip Name"
		hdr.Text[3] = "Clip Num"
		hdr.Text[4] = "Shot"
		hdr.Text[5] = "Shot Type"
		hdr.Text[6] = "Description"
		hdr.Text[7] = "Angle"
		hdr.Text[8] = "Camera Position"
		hdr.Text[9] = "Clip Duration"
		hdr.Text[10] = "Start Frame"
		hdr.Text[11] = "End Frame"
		hdr.Text[12] = "Start TC"
		hdr.Text[13] = "End TC"
		hdr.Text[14] = "FPS"
		hdr.Text[15] = "Resolution"
		hdr.Text[16] = "Online Status"
		hdr.Text[17] = "Track"
		hdr.Text[18] = "Track Locked"
		hdr.Text[19] = "Track Enabled"
		hdr.Text[20] = "Clip Enabled"
		hdr.Text[21] = "Clip Color"
		hdr.Text[22] = "File Name"
		hdr.Text[23] = "Reel Name"
		hdr.Text[24] = "Take"
		hdr.Text[25] = "Scene"

		itm["Tree"].SetHeaderItem(hdr)

		# Number of columns in the Tree list
		itm["Tree"].ColumnCount = 26

		# Resize the Columns
		itm["Tree"].ColumnWidth[0] = 70
		itm["Tree"].ColumnWidth[1] = 115
		itm["Tree"].ColumnWidth[2] = 190
		itm["Tree"].ColumnWidth[3] = 60
		itm["Tree"].ColumnWidth[4] = 55
		itm["Tree"].ColumnWidth[5] = 100
		itm["Tree"].ColumnWidth[6] = 250
		itm["Tree"].ColumnWidth[7] = 50
		itm["Tree"].ColumnWidth[8] = 108
		itm["Tree"].ColumnWidth[9] = 90
		itm["Tree"].ColumnWidth[10] = 100
		itm["Tree"].ColumnWidth[11] = 100
		itm["Tree"].ColumnWidth[12] = 105
		itm["Tree"].ColumnWidth[13] = 105
		itm["Tree"].ColumnWidth[14] = 60
		itm["Tree"].ColumnWidth[15] = 75
		itm["Tree"].ColumnWidth[16] = 85
		itm["Tree"].ColumnWidth[17] = 100
		itm["Tree"].ColumnWidth[18] = 90
		itm["Tree"].ColumnWidth[19] = 95
		itm["Tree"].ColumnWidth[20] = 85
		itm["Tree"].ColumnWidth[21] = 70
		itm["Tree"].ColumnWidth[22] = 1065
		itm["Tree"].ColumnWidth[23] = 100
		itm["Tree"].ColumnWidth[24] = 100
		itm["Tree"].ColumnWidth[25] = 100

		def RefreshTree():
			itm["Tree"].Clear()

			# Get the project name
			project = GetProject()
			projectName = project.GetName()
			projectSetting = project.GetSetting()

			# Get the timeline object
			timeline = GetTimeline()

			# Get the timeline name
			timelineName = timeline.GetName()
			#print("[Timeline Name] " + str(timelineName))

			# Get the timeline settings
			timelineSetting = timeline.GetSetting()

			# Get the track count
			timelineVideoTrackCount = timeline.GetTrackCount("video")

			clipOnlineCount = 0
			clipOfflineCount = 0

			clipCount = 0
			clipColorCount = 0
			clipDisableCount = 0

			clipTotalDuration = 0
			clipAverageDuration = 0
			clipMaxDuration = 0
			clipMinDuration = -1

			disabledTrackCount = -1
			lockedTrackCount = 0

			# Get the track structure
			for i in range(int(timelineVideoTrackCount + 1)):
				trackName = timeline.GetTrackName("video", i + 1)

				# Check for a disabled track
				trackEnabled = str(timeline.GetIsTrackEnabled("video", i + 1))
				if timeline.GetIsTrackEnabled("video", i + 1) == False:
					disabledTrackCount = disabledTrackCount + 1

				# Check for a locked track
				trackLock = str(timeline.GetIsTrackLocked("video", i + 1))
				if timeline.GetIsTrackLocked("video", i + 1) == True:
					lockedTrackCount = lockedTrackCount + 1

				# Get the clips in the track
				clips = timeline.GetItemListInTrack("video", i + 1)
				if clips is not None:
					for clip in clips:
						# Get the clip values
						clipCount = clipCount + 1
						clipName = str(clip.GetName())
						clipColor = str(clip.GetClipColor())
						clipDuration = str(clip.GetDuration())
						clipStart = str(clip.GetStart())
						clipEnd = str(clip.GetEnd())
						clipEnabled = str(clip.GetClipEnabled())

						mpItem = clip.GetMediaPoolItem()
						if mpItem is None:
							mpOnline = "Offline"
							clipOfflineCount = clipOfflineCount + 1

							# Fill the tree row
							itRow = itm["Tree"].NewItem()

							itRow.Text[0] = "{0:02d}".format(clipCount)
							itRow.Text[1] = clipName
							itRow.Text[8] = clipDuration
							itRow.Text[9] = clipStart
							itRow.Text[10] = clipEnd
							itRow.Text[15] = mpOnline
							itRow.Text[20] = clipColor

							itm["Tree"].AddTopLevelItem(itRow)
						else:
							mpProp = mpItem.GetClipProperty()
							mpID = mpItem.GetMediaId()
							mpFPS = str(mpItem.GetClipProperty("FPS"))
							mpOnline = str(mpItem.GetClipProperty("Online Status"))
							mpRes = str(mpItem.GetClipProperty("Resolution"))
							mpFile = str(mpItem.GetClipProperty("File Path"))

							mpParentFolder = os.path.dirname(mpFile)

							clipStartTC = str(mpItem.GetClipProperty("Start TC"))
							clipEndTC = str(mpItem.GetClipProperty("End TC"))
							clipReelName = str(mpItem.GetClipProperty("Reel Name"))
							clipScene = str(mpItem.GetClipProperty("Scene"))
							clipShot = str(mpItem.GetClipProperty("Shot"))
							clipTake = str(mpItem.GetClipProperty("Take"))
							clipDescription = str(mpItem.GetClipProperty("Description"))
							clipAngle = str(mpItem.GetClipProperty("Angle"))
							mpShotType = str(mpItem.GetMetadata("Shot Type"))
							mpCamNum = str(mpItem.GetMetadata("Camera Position"))
							mpClipNum = str(mpItem.GetMetadata("Clip Number"))
							mpDateRecorded = str(mpItem.GetMetadata("Date Recorded"))

							# Number of timeline clips with a color tag
							if len(clipColor):
								clipColorCount = clipColorCount + 1

							# Footage online vs offline state
							if mpOnline == "Online":
								clipOnlineCount = clipOnlineCount + 1
							elif mpOnline == "Offline":
								clipOfflineCount = clipOfflineCount + 1

							# Clip timing stats
							clipTotalDuration = clipTotalDuration + clip.GetDuration()

							if clipMaxDuration <= clip.GetDuration():
								clipMaxDuration = clip.GetDuration()

							if clipMinDuration <= 0:
								clipMinDuration = clip.GetDuration()
							elif clipMinDuration > clip.GetDuration():
								clipMinDuration = clip.GetDuration()

							# Timeline Clip Disabled
							if clip.GetClipEnabled() == False:
								clipDisableCount = clipDisableCount + 1

							# Fill the tree row
							itRow = itm["Tree"].NewItem()

							#itRow.Text[0] = "{0:02d}".format(clipCount)
							itRow.Text[0] = "{0:04d}".format(clipCount)
							itRow.Text[1] = mpDateRecorded
							itRow.Text[2] = clipName
							itRow.Text[3] = mpClipNum
							itRow.Text[4] = clipShot
							itRow.Text[5] = mpShotType
							itRow.Text[6] = clipDescription
							itRow.Text[7] = clipAngle
							itRow.Text[8] = mpCamNum
							itRow.Text[9] = clipDuration
							itRow.Text[10] = clipStart
							itRow.Text[11] = clipEnd
							itRow.Text[12] = clipStartTC
							itRow.Text[13] = clipEndTC
							itRow.Text[14] = mpFPS
							itRow.Text[15] = mpRes
							itRow.Text[16] = mpOnline
							itRow.Text[17] = trackName
							itRow.Text[18] = trackLock
							itRow.Text[19] = trackEnabled
							itRow.Text[20] = clipEnabled
							itRow.Text[21] = clipColor
							itRow.Text[22] = mpFile
							itRow.Text[23] = clipReelName
							itRow.Text[24] = clipTake
							itRow.Text[25] = clipScene

							# Track Lock
							if trackLock == "True":
								itRow.Icon[17] = ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Pre-Flight/locked-track.png"})
							else:
								itRow.Icon[17] = ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Pre-Flight/unlocked-track.png"})

							# Track Enabled
							if trackEnabled == "False":
								itRow.Icon[18] = ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Pre-Flight/disabled-track.png"})
							else:
								itRow.Icon[18] = ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Pre-Flight/enabled-track.png"})

							# Clip Enabled
							if clipEnabled == "False":
								itRow.Icon[19] = ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Pre-Flight/disabled-track.png"})
							else:
								itRow.Icon[19] = ui.Icon({"File": "Scripts:/Utility/Lightfielder/Icons/Pre-Flight/enabled-track.png"})

							# Apply the clip color
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

							if itm["ClipColorCheckbox"].Checked == True:
								# Display Clip Colors in the tree view
								TxtColor = ""
								if clipColor != "":
									TxtColor = White
									#TxtColor = Black

								for c in range(int(itm["Tree"].ColumnCount)):
									itRow.TextColor[c] = TxtColor
									itRow.BackgroundColor[c] = GetColor(clipColor)
									#itRow.TextColor[c] = GetColor(clipColor)


			# 				# Clip or Track Disabled
			# 				if itm["TrackCheckbox"].Checked == True and (clip.GetClipEnabled() == False or timeline.GetIsTrackEnabled("video", i + 1) == False):
			# 				#if itm["TrackCheckbox"].Checked == True:
			# 					itRow.Flags = {
			# 						"ItemIsSelectable": True,
			# 						"ItemIsEnabled": False,
			# 						"ItemIsUserCheckable": False,
			# 					}
			# 				else:
			# 					itRow.Flags = {
			# 						"ItemIsSelectable": True,
			# 						"ItemIsEnabled": True,
			# 						"ItemIsUserCheckable": False,
			# 					}

							itm["Tree"].AddTopLevelItem(itRow)

			# Build the report log
			clipAverageDuration = 0
			if clipCount >= 1:
				clipAverageDuration = clipTotalDuration / clipCount

			if clipCount == 0:
				clipMinDuration = 0

			# Stylesheet inspired by Roger Magnusson's ClassBrowser.lua
			report = """<body bgcolor='#212121'>
			<style>
				body { font-family: Segoe UI, SegoeUI, Segoe WP, Helvetica Neue, Helvetica, Tahoma, Arial, sans-serif; }
				h1 { color: #D0D0D0; font-size: 40px; font-weight: 600; }
				h2 { color: #D0D0D0; margin-top: 24px; font-size: 28px; font-weight: 600; }
				h3 { color: #D0D0D0; font-size: 16px; font-weight: 400; }
				td { font-size: 13px; font-weight: 400; vertical-align: text-top; }
				th { font-size: 24px; font-weight: 600; }
				pre { white-space: pre-wrap; }
			</style>"""

			report = report + "<h2>EDL Log</h2>\n"
			report = report + "Date: " + str(datetime.datetime.now()) + "<br>\n"
			report = report + str(app.GetResolve().GetProductName()) + ": " + str(app.GetResolve().GetVersionString()) + "\n"
			report = report + "<hr />\n"

			report = report + "<h2>Project</h2>\n"
			report = report + "Project Name: " + str(projectName) + "<br>\n"
			report = report + "Color Science: " + str(str(projectSetting["colorScienceMode"])) + "<br>\n"
			report = report + "Color Space Input: " + str(str(projectSetting["colorSpaceInput"])) + "<br>\n"
			report = report + "Color Space Output: " + str(str(projectSetting["colorSpaceOutput"])) + "\n"
			report = report + "<hr />\n"

			report = report + "<h2>Timeline</h2>\n"
			report = report + "Name: " + str(timelineName) + "<br>\n"
			report = report + "Resolution: " + str(projectSetting["timelineResolutionWidth"]) + "x" + str(projectSetting["timelineResolutionHeight"]) + "<br>\n"
			report = report + "FPS: " + str(projectSetting["timelineFrameRate"]) + "<br>\n"
			report = report + "Disabled Tracks: " + str(disabledTrackCount) + "<br>\n"
			report = report + "Locked Tracks: " + str(lockedTrackCount) + "\n"
			report = report + "<hr />\n"

			report = report + "<h2>Footage</h2>\n"
			report = report + "Total Clips: " + str(clipCount) + "<br>\n"
			report = report + "Colored Clips: " + str(clipColorCount) + "<br><br>\n"

			report = report + "Online Clips: " + str(clipOnlineCount) + "<br>\n"
			report = report + "Offline Clips: " + str(clipOfflineCount) + "<br>\n"
			report = report + "Disabled Clips: " + str(clipDisableCount) + "<br><br>\n"

			report = report + "Average Clip Duration: " + str(int(clipAverageDuration)) + " frames<br>\n"
			report = report + "Max Clip Duration: " + str(int(clipMaxDuration)) + " frames<br>\n"
			report = report + "Min Clip Duration: " + str(int(clipMinDuration)) + " frames\n"
			report = report + "<hr />\n"
			report = report + "</body>\n"

			itm["ReportTxt"].Text = report

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
			# subprocess.call(args)
			subprocess.Popen(args)

		RefreshTree()

	# 	def TrackCheckboxFunc(ev):
	# 		RefreshTree()
	# 	dlg.On.TrackCheckbox.Clicked = TrackCheckboxFunc

		def ClipColorCheckboxFunc(ev):
			RefreshTree()
		dlg.On.ClipColorCheckbox.Clicked = ClipColorCheckboxFunc

		def RefreshButtonFunc(ev):
			RefreshTree()
		dlg.On.RefreshButton.Clicked = RefreshButtonFunc

		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		# A Tree view row was clicked on
		def TreeItemClickedFunc(ev):
			print("[Lightfielder][Single Clicked] " + str(ev["item"].Text[0]))
		dlg.On.Tree.ItemClicked = TreeItemClickedFunc

		# A Tree view row was double clicked on
		def TreeItemDoubleClickedFunc(ev):
			path = str(ev["item"].Text[13])
			print("[Lightfielder][Double Clicked] " + str(ev["item"].Text[0]) + " [File] " + str(path))

			# Open the parent folder in Finder/Nautilus/Explorer
			Command(path)
		dlg.On.Tree.ItemDoubleClicked = TreeItemDoubleClickedFunc

		# Change the sorting order of the tree
		#itm["Tree"].SortByColumn(0, "DescendingOrder")
		itm["Tree"].SortByColumn(0, "AscendingOrder")

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.EDLChecker.Geometry")

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('EDLChecker', {
			Target {
				ID = 'EDLChecker',
			},
			Hotkeys {
				Target = 'EDLChecker',
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
		WindowPrefSave(dlg, "Lightfielder.EDLChecker.Geometry")

if __name__ == '__main__':
	if GetProject() and GetTimeline():
		CreateEDLCheckerWindow()
	else:
		print("[Lightfielder] Please open a Resolve project and timeline before running this script.")
		ErrorWindow("Lightfielder", "Please open a Resolve project and timeline before running this script.")
	print("[Lightfielder][Done]")
