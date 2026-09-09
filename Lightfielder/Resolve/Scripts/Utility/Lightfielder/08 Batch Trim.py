"""
Lightfielder 08 Batch Trim.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Apply a Batch Trim to all of the clips in a timeline.

Script Usage:
1. Open a Resolve Edit page based timeline. Select the menu item: "Workspace > Scripts > Lightfielder > 08 Batch Trim".

2. Enter your In-Point and Out-Point values using "+10" for ten frames, "+10." for 10 seconds, and "+10.." for ten minutes.

3. Press the "Validate" button to check if enough frame handles exist on the footage in the timeline.

4. Press the "Apply" button to perform the edit.

Todo:
Increment an existing found timeline number counter that has the same name

Calculations:
- Validate in point direction change makes sense for the +/- motion

Auto Trim:
- RecordFrame - Use accumulated duration of the appended clips to stack them on each track

"""

import re
import datetime, tempfile, os, copy
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

def CreateTrimWindow():
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectSetting = project.GetSetting()

	# Get the timeline object
	timeline = GetTimeline()
	if timeline == None:
		ErrorWindow("Batch Trim", "Please open a Resolve timeline before running this script")
	else:
		# Get the timeline name
		timelineName = timeline.GetName()
		#print("[Lightfielder][Timeline Name] " + str(timelineName))

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
			"WindowTitle": "Lightfielder",
			"WindowFlags": {"Window": True, "WindowStaysOnTopHint": windowFloat},
			"ID": "TrimWin",
			"TargetID" : "TrimWin",
			"Geometry": [10, 110, 630, 745],
			"MinimumSize": [630, 745],
			"FixedSize": [630, 745],
			#"Spacing": 0,
			#"Margin": 0,
		},[
			ui.VGroup({
			},[
				# Add your GUI elements here:
				ui.VGroup({
					"Weight": 0.01,
					#"StyleSheet": "background-color: rgb(37, 37, 37);",
				},[
					ui.HGroup({
						"Weight": 0.5,
					},[
						ui.Label({
							"ID": "ViewLabel",
							"Text": "08 Batch Trim",
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
				ui.HGroup({
					"Weight": 0.01,
				},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "In-Point",
						"Weight": 0.01,
					}),
					ui.LineEdit({"ID": "InPointTxt",
						#"Text": "00:00:00:00",
						"PlaceholderText": "+HH.MM.SS.FF",
						"Weight": 0.5
					}),
					ui.Label({
						"ID": "ViewLabel",
						"Text": "Out-Point",
						"Weight": 0.01,
					}),
					ui.LineEdit({"ID": "OutPointTxt",
						#"Text": "00:00:00:00",
						"PlaceholderText": "+HH.MM.SS.FF",
						"Weight": 0.5
					}),
					ui.Button({
						"ID": "ValidateButton",
						"Text": "Validate",
						"Weight": 0.01
					}),
					ui.Button({
						"ID": "ApplyButton",
						"Text": "Apply",
						"Weight": 0.01
					})
				]),
					ui.HGroup({
					"Weight": 0.01,
				},[
					ui.CheckBox({
						"ID": "LockTo24HourTimecodeCheckbox",
						"Text": "Lock to 24 Hour Timecode",
						"Checked": True,
						"Weight": 0.1
					}),
					ui.CheckBox({
						"ID": "ClipColorCheckbox",
						"Text": "Clip Color",
						"Checked": True,
						"Weight": 0.1,
					}),
					ui.CheckBox({
						"ID": "PreserveGapCheckbox",
						"Text": "Preserve Gap",
						"Checked": False,
						"Weight": 0.1,
					}),
					ui.CheckBox({
						"ID": "RemoveEmptyTracksCheckbox",
						"Text": "Remove Empty Tracks",
						"ToolTip": "(WIP) Compact the video tracks in the timeline by removing any track that is missing \nits camera views. \n\nIf you had an array with 55 cameras, and 10 of the cameras were not set to \nrecord, you would receive a swizzled timeline created with only 45 video tracks \nand no empty video tracks.",
						"Checked": False,
						"Weight": 0.1,
					}),
					ui.HGap(20, 1),
# 					ui.CheckBox({
# 						"ID": "FlipRangesCheckbox",
# 						"Text": "Flip Ranges",
# 						"Checked": True,
# 						"Weight": 0.1,
# 					}),
# 					ui.CheckBox({
# 						"ID": "OTIOModeCheckbox",
# 						"Text": "OTIO",
# 						"Checked": False,
# 						"Weight": 0.1,
# 					}),
				]),
				ui.VGroup({
					"Weight": 10.0
				},[
					ui.TextEdit({
						"ID": "StatusLabel",
						"StyleSheet": "QTextEdit { color: grey; font-weight: bold; font-size: 14px; }",
						"ReadOnly": True,
						"Spacing": 0,
						"Margin": 0,
						"Weight": 1.0,
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
					"Weight": 0.1,
				},[
					
					ui.Button({
						"ID": "MainCloseButton",
						"Text": "Close",
						"Weight": 0.5,
					}),
					ui.HGap(20, 1),
					ui.Label({
						"ID": "AutoTrimLabel",
						"Text": "Auto Trim",
						"Weight": 0.1,
						#"MinimumSize": [120, 32],
					}),
					ui.ComboBox({
						"ID": "TrimModeCombo",
						"Text": "Mode",
						"Weight": 1.0,
					}),
					ui.Button({
						"ID": "AutoTrimGoButton",
						"Text": "Go",
						"MinimumSize": [60, 32],
						"Weight": 0.1
					}),
					#ui.HGap(20, 1),
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
			WindowPrefSave(dlg, "Lightfielder.TrimWin.Geometry")
		dlg.On.TrimWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.TrimWin.Geometry")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.TrimWin.Close = CloseFunc

		def MainCloseButtonFunc(ev):
			print("[Lightfielder][Window][Closed Button]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.TrimWin.Geometry")

			# Reset the progress caption
			# itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.MainCloseButton.Clicked = MainCloseButtonFunc

		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool8", "Tool7")

			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool8", "Tool9")

			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		# Auto Trim ComboBox
		itm["TrimModeCombo"].AddItem("Original Duration (Not in Sync)")
		# itm["TrimModeCombo"].AddItem("Minimal Timecode Sync")
		itm["TrimModeCombo"].AddItem("First Common Frame (Still Frames)")
		itm["TrimModeCombo"].AddItem("Middle Common Frame (Still Frames)")
		itm["TrimModeCombo"].AddItem("Last Common Frame (Still Frames)")
		# itm["TrimModeCombo"].AddItem("First Common Sequence (10 Seconds)")
		# itm["TrimModeCombo"].AddItem("Middle Common Sequence (10 Seconds)")
		# itm["TrimModeCombo"].AddItem("Last Common Sequence (10 Seconds)")

		# Add your GUI element based event functions here:

		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_08_Batch_Trim.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		def AutoTrimGoButtonFunc(ev):
			startTimer = datetime.datetime.now()
			itm["ProgressLabel"].Text = "  Progress: Go Button Pressed"

			# frame rate
			fps = GetProjectFrameRate()
			# fps = GetSensorFrameRate()
			# fps = 60
			# fps = 30
			# fps = 29.97
			# fps = 24

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
				print("[Lightfielder][Note] A frame offset of 1 was required for Resolve Studio v19.0.3+")
				#resultStr += "\n\n<p>Note: A frame offset of 1 was required for Resolve Studio v19.0.3+</p>\n"
				frameOffset = 1

			trimMode = itm["TrimModeCombo"].CurrentIndex
			trimModeName = itm["TrimModeCombo"].CurrentText
			clipColorMode = itm["ClipColorCheckbox"].Checked
			report = "[Completed][Auto Trim] " + str(trimModeName) + "<br>\n"

			res = app.GetResolve()
			project = GetProject()
			mediapool = project.GetMediaPool()

			# Get the timeline object
			timeline = GetTimeline()

			# Get the timeline name
			timelineName = timeline.GetName()

			itm["ProgressLabel"].Text = "  Progress: " + str(timelineName) + " [Wallclock " + GetTimeElapsed(startTimer) + "]"

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

			# Debug point
			# print("[Debug] Resolve got to this point in the code")

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

					# Debug point
					# print("[Debug] Resolve got to this point in the code - Convert to timecode to frames")
					# print("[mpStartTC]", mpStartTC, "[fps]", fps)
					# print("[mpEndTC]", mpEndTC, "[fps]", fps)

					# Convert to timecode to frames
					# print("sourceStartFrame")
					# print(otio.opentime.from_timecode(mpStartTC, fps))
					sourceStartFrame = otio.opentime.to_frames(otio.opentime.from_timecode(mpStartTC, fps))
					# print("sourceEndFrame")
					# print(otio.opentime.from_timecode(mpEndTC, fps))
					sourceEndFrame = otio.opentime.to_frames(otio.opentime.from_timecode(mpEndTC, fps))

					# Debug point
					# print("[Debug] Resolve got to this point in the code - GetLeftOffset")

					leftOffset = clip.GetLeftOffset()
					rightOffset = clip.GetRightOffset() - 1

					# Debug point
					# print("[Debug] Resolve got to this point in the code - cProp")

					#print(cProp)
					#print(clip.GetLeftOffset(),clip.GetRightOffset())
					#print("[Clip]", clipStart, clipEnd, " [MP] ", sourceStartFrame, sourceEndFrame, " [Handles] " , clip.GetLeftOffset(),clip.GetRightOffset())

					# Debug point
					# print("[Debug] Resolve got to this point in the code")

					clipItems.append([mpItem, i, leftOffset, rightOffset, sourceStartFrame, sourceEndFrame, clipColor])
					sRangeItems.append(list(range(sourceStartFrame, sourceEndFrame)))

			# Debug point
			# print("[Debug] Resolve got to this point in the code")

			# Create the new timeline
			newTimelineName = timelineName + " Trim"
			newTimeline = mediapool.CreateEmptyTimeline(newTimelineName)
			trackIndex = 1
			itm["ProgressLabel"].Text = "  Progress: " + str(newTimelineName) + " [Wallclock " + GetTimeElapsed(startTimer) + "]"

			# Get the track count
			if newTimeline is not None:
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

			# Debug point
			# print("[Debug] Resolve got to this point in the code")

			timelineStartTimecode = "01:00:00:00"
			timelineStartFrames = otio.opentime.to_frames(otio.opentime.from_timecode(timelineStartTimecode, fps))
			if newTimeline is not None:
				timelineStartFrames = newTimeline.GetStartFrame()
			else:
				print("[New Timeline] The '", newTimelineName, "' timeline creation task had an issue and returned an empty object.")
				itm["ProgressLabel"].Text = "  Progress: Timeline creation task had an issue and returned an empty object."
				itm["StatusLabel"].Text = report
				return

			# Check if the footage has a valid start frame - end frame range
			#print(sRangeItems)
			if len(sRangeItems) > 0:
				# Timecode Sync
				tStartFrame, tEndFrame, tDuration = IntersectFootageRanges(sRangeItems)
			else:
				report += "[Sync Issue] No Overlapping Frames<br>\n"
				itm["ProgressLabel"].Text = "  Progress: [Sync Issue] No Overlapping Frames"
				itm["StatusLabel"].Text = report
				return

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
				sequenceTenSeconds = int(10 * fps)
				if trimModeName == "Original Duration (Not in Sync)":
					# Trim Mode: Original Duration
					if prevTrackIndex != trackIndex:
						# Reset a new video track at the recordFrame starting position in the timeline
						trackRecordFrame = timelineStartFrames

						mpFootage = {
							"mediaPoolItem" : mpClip,
							#"startFrame": pStartFrame,
							#"endFrame" : pEndFrame,
							"recordFrame" : trackRecordFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
					else:
						mpFootage = {
							"mediaPoolItem" : mpClip,
							#"startFrame": pStartFrame,
							#"endFrame" : pEndFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)

					#trackRecordFrame += pDuration
					prevTrackIndex = clip[1]
				elif trimModeName == "Minimal Timecode Sync":
					# Trim Mode: Minimal Timecode Sync
					if len(sRangeItems) == 0:
						# Fallback to using Edit Page Source Range
						tStartFrame = sStartFrame
						tEndFrame = sEndFrame

					if prevTrackIndex != trackIndex:
						# Reset a new video track at the recordFrame starting position in the timeline
						trackRecordFrame = timelineStartFrames

						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame,
							"endFrame" : tEndFrame + frameOffset,
							"recordFrame" : trackRecordFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
					else:
						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame,
							"endFrame" : tEndFrame + frameOffset,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)

					#trackRecordFrame += sDuration
					prevTrackIndex = clip[1]
				elif trimModeName == "First Common Frame (Still Frames)":
					# Trim Mode: First Common Frame
					if len(sRangeItems) == 0:
						# Fallback to using Edit Page Source Range
						tStartFrame = sStartFrame
						tEndFrame = sStartFrame

					if prevTrackIndex != trackIndex:
						# Reset a new video track at the recordFrame starting position in the timeline
						trackRecordFrame = timelineStartFrames

						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame,
							"endFrame" : tStartFrame + frameOffset,
							"recordFrame" : trackRecordFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
					else:
						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame,
							"endFrame" : tStartFrame + frameOffset,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)

					#trackRecordFrame += sDuration
					prevTrackIndex = clip[1]
				elif trimModeName == 3:
					# Trim Mode: Middle Common Frame
					if len(sRangeItems) == "Middle Common Frame (Still Frames)":
						# Fallback to using Edit Page Source Range
						tStartFrame = sStartFrame + (sDuration * 0.5)
						tEndFrame = sStartFrame + (sDuration * 0.5)

					if prevTrackIndex != trackIndex:
						# Reset a new video track at the recordFrame starting position in the timeline
						trackRecordFrame = timelineStartFrames

						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame + (tDuration * 0.5),
							"endFrame" : tStartFrame + (tDuration * 0.5) + frameOffset,
							"recordFrame" : trackRecordFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
					else:
						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame + (tDuration * 0.5),
							"endFrame" : tStartFrame + (tDuration * 0.5) + frameOffset,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)

					#trackRecordFrame += sDuration
					prevTrackIndex = clip[1]
				elif trimModeName == "Last Common Frame (Still Frames)":
					# Trim Mode: Last Common Frame
					if len(sRangeItems) == 0:
						# Fallback to using Edit Page Source Range
						tStartFrame = sEndFrame
						tEndFrame = sEndFrame

					if prevTrackIndex != trackIndex:
						# Reset a new video track at the recordFrame starting position in the timeline
						trackRecordFrame = timelineStartFrames

						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tEndFrame,
							"endFrame" : tEndFrame + frameOffset,
							"recordFrame" : trackRecordFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
					else:
						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tEndFrame,
							"endFrame" : tEndFrame + frameOffset,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
				elif trimModeName == "First Common Sequence (10 Seconds)":
					# Trim Mode: First Common Sequence (10 Seconds)
					if len(sRangeItems) == 0:
						# Fallback to using Edit Page Source Range
						tStartFrame = sStartFrame
						tEndFrame = sStartFrame

					if prevTrackIndex != trackIndex:
						# Reset a new video track at the recordFrame starting position in the timeline
						trackRecordFrame = timelineStartFrames

						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame,
							"endFrame" : tStartFrame + frameOffset + sequenceTenSeconds,
							"recordFrame" : trackRecordFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
					else:
						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame,
							"endFrame" : tStartFrame + frameOffset + sequenceTenSeconds,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)

					#trackRecordFrame += sDuration
					prevTrackIndex = clip[1]
				elif trimModeName == "Middle Common Sequence (10 Seconds)":
					# Trim Mode: Middle Common Sequence (10 Seconds)
					if len(sRangeItems) == 0:
						# Fallback to using Edit Page Source Range
						tStartFrame = sStartFrame + (sDuration * 0.5)
						tEndFrame = sStartFrame + (sDuration * 0.5)

					if prevTrackIndex != trackIndex:
						# Reset a new video track at the recordFrame starting position in the timeline
						trackRecordFrame = timelineStartFrames

						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame + (tDuration * 0.5),
							"endFrame" : tStartFrame + (tDuration * 0.5) + frameOffset + sequenceTenSeconds,
							"recordFrame" : trackRecordFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
					else:
						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tStartFrame + (tDuration * 0.5),
							"endFrame" : tStartFrame + (tDuration * 0.5) + frameOffset + sequenceTenSeconds,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)

					#trackRecordFrame += sDuration
					prevTrackIndex = clip[1]
				elif trimModeName == "Last Common Sequence (10 Seconds)":
					# Trim Mode: Last Common Sequence (10 Seconds)
					if len(sRangeItems) == 0:
						# Fallback to using Edit Page Source Range
						tStartFrame = sEndFrame
						tEndFrame = sEndFrame

					if prevTrackIndex != trackIndex:
						# Reset a new video track at the recordFrame starting position in the timeline
						trackRecordFrame = timelineStartFrames

						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tEndFrame - sequenceTenSeconds,
							"endFrame" : tEndFrame + frameOffset,
							"recordFrame" : trackRecordFrame,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)
					else:
						mpFootage = {
							"mediaPoolItem" : mpClip,
							"startFrame": tEndFrame - sequenceTenSeconds,
							"endFrame" : tEndFrame + frameOffset,
							"trackIndex" : trackIndex
						}
						# Add the clip to the timeline
						timelineItem = mediapool.AppendToTimeline([mpFootage])
						#print("[Timeline Item] " + str(timelineItem) + " [Type] " + str(type(timelineItem)))

						# Add the clip color
						if clipColorMode == True and timelineItem[0] is not None:
							timelineItem[0].SetClipColor(pClipColor)

					#trackRecordFrame += sDuration
					prevTrackIndex = clip[1]
					
			itm["ProgressLabel"].Text = "  Progress: Completed Trim [Wallclock " + GetTimeElapsed(startTimer) + "]"
			itm["StatusLabel"].Text = report

			# Play the sound effect
			soundName = app.GetData("Lightfielder.SoundEffectsComplete")
			# soundName = app.GetData("Lightfielder.SoundEffectsError")
			if soundName != None:
				SoundEffectSelect(soundName)
		dlg.On.AutoTrimGoButton.Clicked = AutoTrimGoButtonFunc

		def ValidateButtonFunc(ev):
			timeline = GetTimeline()

			# Process timecode
			lockTo24HourTimecode = itm["LockTo24HourTimecodeCheckbox"].Checked
			inPointStr = str(itm["InPointTxt"].Text)
			OutPointStr = str(itm["OutPointTxt"].Text)
			#flipRangesMode = itm["FlipRangesCheckbox"].Checked
			flipRangesMode = False

			inTime, inOffset, inValid = FormatTimecode(inPointStr, lockTo24HourTimecode)
			outTime, outOffset, outValid = FormatTimecode(OutPointStr, lockTo24HourTimecode)

			clips, errorCount = ValidateClipRangesNative(timeline, inPointStr, OutPointStr, lockTo24HourTimecode, flipRangesMode)
			if errorCount == 0:
				report = "[Validate] <br>\n"
				report += "[Offset] InPoint: " + str(inOffset) + str(inTime) + "\t" + "OutPoint: " + str(outOffset) + str(outTime) + "<br>\n"
			else:
				report = "[Validate] " + str(errorCount) + " Trim Issues<br>\n"
				report += "[Offset] InPoint: " + str(inOffset) + str(inTime) + "\t" + "OutPoint: " + str(outOffset) + str(outTime) + "<br>\n"

				report += "<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">"
				report += "<tr><td>Clip</td><td>Track #</td><td>Missing In-Point</td><td>Missing Out-Point</td><td>Duration Frames</td></tr>"
				report += str(clips)
				report += "</table>"

			itm["StatusLabel"].Text = report
		dlg.On.ValidateButton.Clicked = ValidateButtonFunc

		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		def ApplyButtonFunc(ev):
			print("[Batch Trim]")
			report = "[Batch Trim]<br>\n"

			# Process timecode
			lockTo24HourTimecode = itm["LockTo24HourTimecodeCheckbox"].Checked
			inPointStr = str(itm["InPointTxt"].Text)
			OutPointStr = str(itm["OutPointTxt"].Text)
			clipColorMode = itm["ClipColorCheckbox"].Checked
			#flipRangesMode = itm["FlipRangesCheckbox"].Checked
			flipRangesMode = False

			inTime, inOffset, inValid = FormatTimecode(inPointStr, lockTo24HourTimecode)
			outTime, outOffset, outValid = FormatTimecode(OutPointStr, lockTo24HourTimecode)

			report += "[Offset] InPoint: " + str(inOffset) + str(inTime) + "\t" + "OutPoint: " + str(outOffset) + str(outTime) + "<br>\n"

# 			if itm["OTIOModeCheckbox"].Checked == True:
# 				# OTIO timeline trimming
# 				filepath, name = TimelineExport()
# 				if filepath:
# 					timelineIn = ReadTimeline(filepath)
# 					ReadTimelineClips(timelineIn)
# 					timelineName = TimelineRenameTrim(name)
# 					timelineOut, clips = ModifyTimelineOTIO(timelineIn, timelineName, inPointStr, OutPointStr, lockTo24HourTimecode)
# 					report += clips
#
# 					# Save the OTIO Timeline to disk
# 					fileOut = WriteTimeline(filepath, timelineOut)
#
# 					# Import the reformatted OTIO Timeline
# 					TimelineImportOTIO(fileOut, timelineName)
# 			else:
			# Native timeline trimming

			# Get the timeline object
			timeline = GetTimeline()

			# Get the timeline name
			timelineName = TimelineRenameTrim(timeline.GetName())
			timelineOut, clips = ModifyTimelineNative(timeline, timelineName, inPointStr, OutPointStr, lockTo24HourTimecode, clipColorMode, flipRangesMode)
			report += clips

			itm["StatusLabel"].Text = report
		dlg.On.ApplyButton.Clicked = ApplyButtonFunc

		def InPointTxtFunc(ev):
			lockTo24HourTimecode = itm["LockTo24HourTimecodeCheckbox"].Checked
			inTime, inOffset, inValid = FormatTimecode(str(itm["InPointTxt"].Text), lockTo24HourTimecode)
			outTime, outOffset, outValid = FormatTimecode(str(itm["OutPointTxt"].Text), lockTo24HourTimecode)

			report = ""
			report += "[Offset] InPoint: " + str(inOffset) + str(inTime) + "\t" + "OutPoint: " + str(outOffset) + str(outTime) + "<br>\n"

			itm["StatusLabel"].Text = report
		dlg.On.InPointTxt.TextChanged = InPointTxtFunc

		def OutPointTxtFunc(ev):
			lockTo24HourTimecode = itm["LockTo24HourTimecodeCheckbox"].Checked
			inTime, inOffset, inValid = FormatTimecode(str(itm["InPointTxt"].Text), lockTo24HourTimecode)
			outTime, outOffset, outValid = FormatTimecode(str(itm["OutPointTxt"].Text), lockTo24HourTimecode)

			report = ""
			report += "[Offset] InPoint: " + str(inOffset) + str(inTime) + "\t" + "OutPoint: " + str(outOffset) + str(outTime) + "<br>\n"

			itm["StatusLabel"].Text = report
		dlg.On.OutPointTxt.TextChanged = OutPointTxtFunc

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.TrimWin.Geometry")

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('TrimWin', {
			Target {
				ID = 'TrimWin',
			},
			Hotkeys {
				Target = 'TrimWin',
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
		WindowPrefSave(dlg, "Lightfielder.TrimWin.Geometry")

if __name__ == "__main__":
	if GetProject() and GetTimeline():
		CreateTrimWindow()
	else:
		print("[Lightfielder] Please open a Resolve project and timeline before running this script.")
		ErrorWindow("Lightfielder", "Please open a Resolve project and timeline before running this script.")
	print("[Done]")
