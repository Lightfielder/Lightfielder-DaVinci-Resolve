"""
Lightfielder 09 EDL Stack Swizzle.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Converts a multi-view video track layout between a horizontal stack (HStack) and vertical stack (VStack) timeline format.

Script Usage:

1. Open Resolve. Select the menu item: "Workspace > Scripts > Lightfielder > 11 EDL Stack Swizzle".

2. The "Convert Track" ComboBox menu item allows you to select between a "To Vertical Stack" or "To Horizontal Stack" option.

3. Click on the "Go" button to generate a new OpenTimelineIO formatted VSTACK or HSTACK timeline output. A status dialog will show the clips that were processed when creating the new timeline.


Relinking Media:
If the imported OTIO based vertically stacked timeline has clips listed as "Media Offline" that can be solved using the Media page. Right click on the imported "VStack" or "HStack" timeline, and select the "Timelines > Reconform From Bins…" menu item.

In the "Conform from Bins" dialog enable the "Conform Options" you prefer. For OTIO timeline based clip relinking, a good initial choice is to enable the "File Name" checkbox.

Select the Conform Bins on the left where your footage is stored in the media pool. Then click the OK button.

If the relinking process succeeded, the footage in your timeline should be loaded and the clips will have a blue color.

"""

import re
import datetime
import tempfile, os
import copy
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

startTimer = datetime.datetime.now()

def ModifyTimelineToVStack(timelineOld, name):
	timelineNew = otio.schema.Timeline(name = name)

	#print("[Timeline Name]")
	#print(timelineNew.name)

	#print("[Clips]")
	clipNames = ""

	# Scan the old timeline
	v = 0
	a = 0
	for each_seq in timelineOld.tracks:
		for each_item in each_seq:
			if isinstance(each_item, otio.schema.Clip):
				#print(each_item)
				#print(each_item.name, each_item.metadata)
				#print(each_item.media_reference)

				# A001_A055_1116A5_001.R3D
				name = each_item.name

				# Fix broken URs in clip filepaths
				#target_url_fix = each_item.media_reference.target_url
				#target_url_fix = target_url_fix.replace("file:", "")
				#target_url_fix = str(target_url_fix.replace("//", "/"))
				#target_url_fix = "file://" + str(target_url_fix)
				#each_item.media_reference.target_url = target_url_fix
				target_url = each_item.media_reference.target_url

				if each_seq.kind == "Video":
					#if each_seq.kind == "Video":
					#elif each_seq.kind == "Audio":
					# Track Counter
					v = v + 1
					a = a + 1

					# Create an OTIO track
					videoTrackName =  "V" + str(v)
					videoTrack = otio.schema.Track(name = videoTrackName, kind = "Video")
					timelineNew.tracks.append(videoTrack)

					audioTrackName =  "A" + str(a)
					audioTrack = otio.schema.Track(name = audioTrackName, kind = "Audio")
					timelineNew.tracks.append(audioTrack)

					clipNames += "[Modify Clip] [Kind] " + str(each_seq.kind) + "\t[" + str(videoTrackName) + "]\t" + str(name) + "\t[Target URL] " + str(target_url) + "\n"

					# Append the clip from the old timeline to the new timeline
					videoTrack.append(copy.deepcopy(each_item))
					audioTrack.append(copy.deepcopy(each_item))
				#elif each_seq.kind == "Audio":
	return timelineNew, clipNames

def ModifyTimelineToHStack(timelineOld, name):
	timelineNew = otio.schema.Timeline(name = name)

	#print("[Timeline Name]")
	#print(timelineNew.name)

	#print("[Clips]")
	clipNames = ""

	# Create an OTIO track
	videoTrack = otio.schema.Track(kind = "Video")
	videoTrackName =  "V" + str(1)
	videoTrack.name = videoTrackName
	timelineNew.tracks.append(videoTrack)

	audioTrack = otio.schema.Track(kind = "Audio")
	audioTrackName =  "A" + str(1)
	audioTrack.name = audioTrackName
	timelineNew.tracks.append(audioTrack)

	# Scan the old timeline
	v = 0
	a = 0
	for each_seq in timelineOld.tracks:
		for each_item in each_seq:
			if isinstance(each_item, otio.schema.Clip):
				#print(each_item)
				#print(each_item.name, each_item.metadata)
				#print(each_item.media_reference)

				# A001_A055_1116A5_001.R3D
				name = each_item.name

				# Fix broken URs in clip filepaths
				#target_url_fix = each_item.media_reference.target_url
				#target_url_fix = target_url_fix.replace("file:", "")
				#target_url_fix = str(target_url_fix.replace("//", "/"))
				#target_url_fix = "file://" + str(target_url_fix)
				#each_item.media_reference.target_url = target_url_fix

				target_url = each_item.media_reference.target_url

				if each_seq.kind == "Video":
					clipNames += "[Modify Clip] [Kind] " + str(each_seq.kind) + "\t[" + str(videoTrackName) + "]\t" + str(name) + "\t[Target URL] " + str(target_url) + "\n"

					# Clip Counter
					v = v + 1
					a = a + 1

					# Append the clip from the old timeline to the new timeline
					videoTrack.append(copy.deepcopy(each_item))

					# Append the clip from the old timeline to the new timeline
					audioTrack.append(copy.deepcopy(each_item))
				#elif each_seq.kind == "Audio":
	return timelineNew, clipNames

def CreateEDLStackSwizzleWindow():
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
		"ID": "EDLStackSwizzleWin",
		"TargetID" : "EDLStackSwizzleWin",
		"Geometry": [500, 185, 602, 245],
		"MinimumSize": [602, 245],
		"FixedSize": [602, 245],
	},[
		ui.VGroup({
			"ID": "Content",
			"Weight": 1.0,
		},[
			ui.VGroup({
				"Weight": 0.01,
			},[
				ui.HGroup({
					"Weight": 0.5,
				},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "09 EDL Stack Swizzle",
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
			ui.VGroup({
				"Weight": 0.1,
				"ID": "TimeTab",
				"Spacing": 10,
			},[
				ui.HGroup({
					"Weight": 1.0,
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
				ui.HGroup({
					"Weight": 0.1
				},[
					ui.CheckBox({
						"ID": "ClipColorCheckbox",
						"Text": "Clip Color",
						"ToolTip": "When the Swizzle operation is performed, the new timeline \nwill retain the individual clip colors tags on the footage.",
						"Checked": True,
						"Weight": 0.1,
					}),
					ui.CheckBox({
						"ID": "PreserveGapCheckbox",
						"Text": "Preserve Gap",
						"ToolTip": "(WIP) When the Swizzle operation is performed, this option will \nmaintain the space (gap) between separate clips in the timeline.",
						"Checked": False,
						"Weight": 0.1,
					}),
					ui.CheckBox({
						"ID": "AssignAngleToTrackNameCheckbox",
						"Text": "Assign Angle to Track Name",
						"ToolTip": "(WIP) Rename the video tracks from \"V1 to V55\" over to directly using the camera array geometry \nbased camera angle name like \"A1 to E5\" or \"A110 to Z977\" as the actual track name. \n\nThis makes it a heck of a lot easier on the Edit page to know what angle you are looking at \nwhen individual video tracks are soloed, or the CCS is used to enable and disable tracks.",
						"Checked": False,
						"Weight": 0.1,
					}),
					ui.CheckBox({
						"ID": "RemoveEmptyTracksCheckbox",
						"Text": "Remove Empty Tracks",
						"ToolTip": "(WIP) When a Vertical Stack is created, compact the video tracks in the timeline \nby removing any track that is missing its camera views. \n\nIf you had an array with 55 cameras, and 10 of the cameras were not set to \nrecord, you would receive a swizzled timeline created with only 45 video tracks \nand no empty video tracks.",
						"Checked": False,
						"Weight": 0.1,
					}),
					ui.CheckBox({
						"ID": "OTIOModeCheckbox",
						"Text": "OTIO",
						"ToolTip": "When the Swizzle operation is performed, the timeloine will be created using a temporary \nOpenTimelineIO .otio file that is written to disk, then re-imported into the Media Pool.",
						"Checked": False,
						"Weight": 0.1,
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
						"Weight": 0.5,
					}),
					ui.Button({
						"ID": "GoButton",
						"Text": "Go",
						"MinimumSize": [60, 32],
						"Weight": 0.5
					}),
					# ui.HGap(20, 1),
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
	itm["TrackLayoutCombo"].AddItem("To Vertical Stack")
	itm["TrackLayoutCombo"].AddItem("To Horizontal Stack")
	itm["TrackLayoutCombo"].CurrentIndex = 1

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
		WindowPrefSave(dlg, "Lightfielder.EDLStackSwizzleWin.Geometry")
	dlg.On.EDLStackSwizzleWin.Hide = HideFunc

	# The window was closed
	def CloseFunc(ev):
		print("[Lightfielder][Window][Closed]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.EDLStackSwizzleWin.Geometry")

		# Reset the progress caption
		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.EDLStackSwizzleWin.Close = CloseFunc

	def CloseButtonFunc(ev):
		print("[Lightfielder][Window][Close Button]")

		# Reset the progress caption
		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.CloseButton.Clicked = CloseButtonFunc

	def PrevScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Prev Item]")
		ProcessToolbarButton(ev, dlg, "Tool9", "Tool8")

		disp.ExitLoop()
	dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

	def NextScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Next Item]")
		ProcessToolbarButton(ev, dlg, "Tool9", "Tool10")

		disp.ExitLoop()
	dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

	# Add your GUI element based event functions here:

	def HelpButtonFunc(ev):
		ShowHelpTopic("Docs/Scripts_09_EDL_Stack_Swizzle.md")
	dlg.On.HelpButton.Clicked = HelpButtonFunc

	def ShowTempButtonFunc(ev):
		print("[Lightfielder][Show Temp Folder]")
		res = app.GetResolve()

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

		app.Execute('bmd.openfileexternal("Open", [[' + str(tempDirAbs) + ']])')
	dlg.On.ShowTempButton.Clicked = ShowTempButtonFunc

	def GoButtonFunc(ev):
		startTimer = datetime.datetime.now()
		itm["ProgressLabel"].Text = "  Progress: Go Button Pressed"

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

		clipColorMode = itm["ClipColorCheckbox"].Checked

		# Deal with the Resolve Studio v19.0.3 "off by one" frame correction change for Adding clips to timeline items issue:
		# https://www.steakunderwater.com/wesuckless/viewtopic.php?p=52659#p52659
		resolveVersion = str(app.GetAttrs()["FUSIONS_Version"]).split(".")
		frameOffset = 0

		# Look for Resolve 19.0.3+
		if int(resolveVersion[0]) == 19:
			if (int(resolveVersion[1]) == 0):
				if (int(resolveVersion[2]) >= 3):
					print("[Lightfielder][Note] A frame offset of 1 was required for Resolve Studio v19.0.3+")
					#resultStr += "\n\n<p>Note: A frame offset of 1 was required for Resolve Studio v19.0.3+</p>\n"
					frameOffset = 1
			if (int(resolveVersion[1]) >= 1):
				print("[Lightfielder][Note] A frame offset of 1 was required for Resolve Studio v19.0.3+")
				#resultStr += "\n\n<p>Note: A frame offset of 1 was required for Resolve Studio v19.0.3+</p>\n"
				frameOffset = 1
		if int(resolveVersion[0]) >= 20:
			print("[Lightfielder][Note] frame offset of 1 was required for Resolve Studio v19.0.3+")
			#resultStr += "\n\n<p>Note: A frame offset of 1 was required for Resolve Studio v19.0.3+</p>\n"
			frameOffset = 1

		if itm["OTIOModeCheckbox"].Checked == True:
			# OTIO Timeline Swizzle Mode
			print("[Lightfielder][EDL Stack Swizzle] OTIO")

			# Read the EDL
			filepath, name = TimelineExport()
			timelineIn = ReadTimeline(filepath)
			ReadTimelineClips(timelineIn)

			# Check the track orientation
			trackLayout = int(itm["TrackLayoutCombo"].CurrentIndex)
			timelineName = TimelineRename(name, trackLayout)
			if trackLayout == 0:
				# Create an OTIO VSTACK Timeline
				timelineOut, clips = ModifyTimelineToVStack(timelineIn, timelineName)
			else:
				# Create an OTIO HSTACK Timeline
				timelineOut, clips = ModifyTimelineToHStack(timelineIn, timelineName)

			# Save the OTIO Timeline to disk
			fileOut = WriteTimeline(filepath, timelineOut)

			# Import the reformatted OTIO Timeline
			TimelineImport(fileOut, timelineName)

			# Relink media

			# Close the window
			# disp.ExitLoop()

			itm["ProgressLabel"].Text = "  Progress: OTIO formatted timeline was created sucessfully"
			completeMessage = "The new OTIO formatted timeline was created sucessfully.\n" + "\n[OTIO Filename]\n" + str(fileOut) + "\n\n[Timeline Name]\n" + str(timelineOut.name) + "\n\n[Clips]\n" + str(clips)

			ErrorWindow("Completed", completeMessage)

			# Reveal folder on disk
			baseFolder = os.path.dirname(fileOut)
			app.Execute('bmd.openfileexternal("Open", [[' + str(baseFolder) + ']])')
		else:
			# Native Timeline Swizzle Mode
			print("[Lightfielder][EDL Stack Swizzle] Native")

			# frame rate
			fps = GetProjectFrameRate()
			# fps = GetSensorFrameRate()
			# fps = 60
			# fps = 30
			# fps = 29.97
			# fps = 24

			# Get the number of cameras views in the array
			maxCameras = GetMaxNumberOfCameras()

			res = app.GetResolve()
			project = GetProject()
			mediapool = project.GetMediaPool()

			# Get the timeline object
			timeline = GetTimeline()

			# Get the timeline name
			timelineName = timeline.GetName()

			# Get the track count
			timelineVideoTrackCount = timeline.GetTrackCount("video")

			# Store the current timeline clips
			clipItems = []

			counter = 1
			# Get the track structure
			for i in range(1, int(timelineVideoTrackCount) + 1):
				# Get the clips in the track
				clips = timeline.GetItemListInTrack("video", i)
				clipItemsCount = len(clips or "")
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

					# print("[Clip] ", dir(clip))
					# print("[Clip Properties] ", cProp)
					# print(clip.GetLeftOffset(),clip.GetRightOffset())
					print("[Lightfielder][Clip]", clipStart, clipEnd, " [MP] ", sourceStartFrame, sourceEndFrame, " [Handles] " , clip.GetLeftOffset(), clip.GetRightOffset())

					counter += 1
					if int(counter) % 5 == 0:
						itm["ProgressLabel"].Text = "  Progress: Get Clip Properties (" + str(counter) + ") Video Track [" + str(i) + "] [Wallclock " + GetTimeElapsed(startTimer) + "]"

					# mpClip, StartFrame, EndFrame, RecordFrame, TrackIndex
					#clipItems.append([mpItem, sourceStartFrame, sourceEndFrame, i])
					clipItems.append([mpItem, sourceStartFrame, sourceEndFrame, i, clipColor])
					# This was the previous function that was used:
					# clipItems.append([mpItem, leftOffset, rightOffset, i, clipColor])

			# print("[Timeline Items]")
			# print(clipItems)

			# Create the new timeline
			newTimelineName = timelineName + " Swizzle"
			newTimeline = mediapool.CreateEmptyTimeline(newTimelineName)
			trackIndex = 1

			itm["ProgressLabel"].Text = "  Progress: " + str(newTimelineName) + " [Wallclock " + GetTimeElapsed(startTimer) + "]"

			timelineStartTimecode = "01:00:00:00"
			timelineStartFrames = otio.opentime.to_frames(otio.opentime.from_timecode(timelineStartTimecode, fps))
			if newTimeline is not None:
				timelineStartFrames = newTimeline.GetStartFrame()
			else:
				print("[Lightfielder][New Timeline] The '", newTimelineName, "' timeline creation task had an issue and returned an empty object.")
				# itm["ProgressLabel"].Text = "  Progress: Timeline creation task had an issue and returned an empty object."

			itm["ProgressLabel"].Text = "  Progress: Adding Video and Audio Tracks [Wallclock " + GetTimeElapsed(startTimer) + "]"

			# Get the track count
			timelineVideoTrackCount = newTimeline.GetTrackCount("video")
			if timelineVideoTrackCount <= maxCameras:
				trackGoal = maxCameras - timelineVideoTrackCount
				# Add the required video tracks
				for x in range(trackGoal):
					newTimeline.AddTrack("video")
			timelineAudioTrackCount = newTimeline.GetTrackCount("audio")
			if timelineAudioTrackCount <= maxCameras:
				trackGoal = maxCameras - timelineAudioTrackCount
				# Add the required audio tracks
				for x in range(trackGoal):
					newTimeline.AddTrack("audio")

			counter = 1
			clipItemsCount = len(clipItems or "")
			for clip in clipItems:
				trackLayout = int(itm["TrackLayoutCombo"].CurrentIndex)
				mpClip = clip[0]
				sStartFrame = clip[1]
				sEndFrame = clip[2]
				pClipColor = clip[4]
				print("[Lightfielder][Track] ", trackIndex, "[Range] ", sStartFrame, " to ", sEndFrame)
				# print("Lightfielder][Clip Attributes] ", clip)

				if trackLayout == 0:
					# Build vertical stacked timelines
					mpFootage = {
						"mediaPoolItem" : mpClip,
						"startFrame": sStartFrame,
						"endFrame" : sEndFrame + frameOffset,
						"recordFrame" : timelineStartFrames,
						"trackIndex" : trackIndex
					}
					# Add the clip to the timeline
					timelineItem = mediapool.AppendToTimeline([mpFootage])
					#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

					# Add the clip color
					if clipColorMode == True and timelineItem[0] is not None:
						timelineItem[0].SetClipColor(pClipColor)
					trackIndex += 1
				else:
					# Build horizontally stacked timelines
					mpFootage = {
						"mediaPoolItem" : mpClip,
						"startFrame": sStartFrame,
						"endFrame" : sEndFrame + frameOffset,
						"trackIndex" : 1
					}
					# Add the clip to the timeline
					timelineItem = mediapool.AppendToTimeline([mpFootage])
					#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

					# Add the clip color
					if clipColorMode == True and timelineItem[0] is not None:
						timelineItem[0].SetClipColor(pClipColor)
				counter += 1
				if int(counter) % 5 == 0:
					itm["ProgressLabel"].Text = "  Progress: Add Clip (" + str(counter) + " of " + str(clipItemsCount) + ") Track Index [" + str(i) + "] [Wallclock " + GetTimeElapsed(startTimer) + "]"

			itm["ProgressLabel"].Text = "  Progress: Completed Swizzle [Wallclock " + GetTimeElapsed(startTimer) + "]"

			# Play the sound effect
			soundName = app.GetData("Lightfielder.SoundEffectsComplete")
			# soundName = app.GetData("Lightfielder.SoundEffectsError")
			if soundName != None:
				SoundEffectSelect(soundName)
	dlg.On.GoButton.Clicked = GoButtonFunc

	def ConsoleButtonFunc(ev):
		if itm["ConsoleButton"].Checked == True:
			app.DoAction("Console_Show", {"Show": True})
		else:
			app.DoAction("Console_Show", {"Show": False})
	dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

	# Load the window preferences
	WindowPrefLoad(dlg, "Lightfielder.EDLStackSwizzleWin.Geometry")

	# Toggle the Toolbar button to the pressed (on) state
	UnpressToolbarButton(dlg.ID, True)

	# Add a close window hotkey event handler
	app.Execute(
	"""
	app:AddConfig('EDLStackSwizzleWin', {
		Target {
			ID = 'EDLStackSwizzleWin',
		},
		Hotkeys {
			Target = 'EDLStackSwizzleWin',
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
	WindowPrefSave(dlg, "Lightfielder.EDLStackSwizzleWin.Geometry")

if __name__ == "__main__":
	if GetProject() and GetTimeline():
		CreateEDLStackSwizzleWindow()
	else:
		print("[Lightfielder] Please open a Resolve project and timeline before running this script.")
		ErrorWindow("Lightfielder", "Please open a Resolve project and timeline before running this script.")
	print("[Lightfielder][Done]")
