"""
Lightfielder Render Log 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Create a JSON encoded log file for the current Deliver page render job.

Script Usage:
1. Switch to the Deliver page.

2. In the Render Settings dialog, click on the "Video" tab. Expand the "Advanced Settings" section.

3. Enable the "[x] Trigger script at" checkbox and set it to "[End] of render job". In the Script combobox menu select the "RenderLog" entry.

When a new render queue item is rendered to disk, a JSON formatted render log file will be written to the "Lightfielder:/Log/" folder with a filename like:
$HOME/Lightfielder/Logs/Projects/<Project Name>/<YYYY-MM-DD>_<HH.MM.SS.SSSSSS>_<Timeline Name>_<Job Name>.json

The token values are expanded to create a filename like:
$HOME/Lightfielder/Logs/Projects/New_Project/2023-Jun-02_12.37.50.855323_Timeline_1_Job_1.json

Installation:
1. Copy the "Render Log.py" script to the folder "$HOME/Lightfielder/Resolve/Scripts/Deliver/". (You will need to make the final Lightfielder folder in this filepath.)

2. Restart Resolve Studio once to enable the script.

"""

import os
import datetime
import json
import re

def GetProject():
	# Get the current Resolve timeline
	res = app.GetResolve()
	projectManager = res.GetProjectManager()
	project = projectManager.GetCurrentProject()
	return project

def GetTimeline():
	project = GetProject()
	timeline = project.GetCurrentTimeline()

	if not timeline:
		if project.GetTimelineCount() > 0:
			timeline = project.GetTimelineByIndex(1)
			project.SetCurrentTimeline(timeline)

	return timeline

def GetRenderJob(project, jobId):
	jobList = project.GetRenderJobList()
	for jobDetail in jobList:
		if jobDetail["JobId"] == jobId:
			return jobDetail
	return ""

def GetLogFolder():
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))

	tempDirRel = "Lightfielder:/Logs/Projects/" + str(projectNameNoSpaces) + "/"
	tempDirAbs = app.MapPath(tempDirRel)

	# Create the temporary folder
	if not os.path.exists(tempDirAbs):
		os.makedirs(tempDirAbs)
		print("[Lightfielder][RenderLog][Make Directory] ", tempDirAbs)

	return tempDirAbs

def SplitMediaFilename(clipName):
	# Todo: For image sequences we will have to handle more than 3 digits of frame numbers

	# Check what type of footage to import
	mediaFormat = app.GetData("Lightfielder.MediaFormat") or "R3D"

	# AA-JE
	viewCol = ""
	viewRow = ""

	# 001-999
	clipID = ""
	dateID = ""

	# .r3d sub-clip items
	subClip = 0

	# Regular expressions matching pattern for a RED filename like "F001_D050_0309BX_001.R3D"
	# The revised RED filename appears to have an extra trailing month/day field digit "01286" vs the earlier "0309".
	# (?P<extra>[0-9]*)                    # Extra 0-9 (This is new and optional)
	#(?P<month>[0-9][0-9])                 # Month 01-12
	#(?P<day>[0-9][0-9])                   # Day 01-31

	# Sub-cliping sequence naming example:
	# A001_A004_1003RH_008.R3D
	# A001_A004_1003RH_001.R3D
	# A001_A004_1003RH_004.R3D
	# A001_A004_1003RH_006.R3D
	# A001_A004_1003RH_003.R3D
	# A001_A004_1003RH_005.R3D
	# A001_A004_1003RH_002.R3D
	# A001_A004_1003RH_007.R3D

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

	# verify the clip name doesn't start with period meaning an invisible UNIX file
	if not clipName.startswith("."):
		# Process a regular expression based named group
		# print("\t\t[Lightfielder][Media RegEx] "      + str(clipName))
		pat = re.compile(pattern, re.VERBOSE)
		mat = pat.match(clipName)
		result = None
		if mat != None or mat == "":
			m = mat.groupdict()
			if m != None:
				# print("\t\t[Lightfielder][Media Pattern] " + str(pattern))
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
			print("\t\t\t[Lightfielder][Media Match Error] Empty Pattern. Check the shotlog CSV formatting and media filenames for changes.")

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


def WriteLog(details, status):
	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")
	timeNow = str(datetime.datetime.now())

	# Get the timeline object
	timeline = GetTimeline()

	# Get the timeline name
	timelineName = timeline.GetName()
	timelineNameNoSpaces = str(timelineName.replace(" ", "_"))
	#print("[Lightfielder][Timeline Name] " + str(timelineName))

	# Build the filename
	logExt = "json"

	# Job 1
	renderJob = str(details["RenderJobName"])

	# Clips
	clips = GetClips()

	# 2023-May-08_16.48.52_Timeline_1_Job 1.json
	logFilename = str(timeStamp) + "_" + str(timelineNameNoSpaces) + "_" + str(renderJob) + "." + str(logExt)

	logPathRel = GetLogFolder() + str(logFilename.replace(" ", "_"))
	logPathAbs = app.MapPath(logPathRel)

	jsonData = {
		"version": 1,
		"time": timeNow,
		"rendersettings": details,
		"status": status,
		"footage": clips
	}

	# Import the JSON preset file
	try:
		with open(logPathAbs, "w") as f:
			# Todo: Add a try element to catch JSON formatting errors in the presets
			# json.dump(data, f, ensure_ascii = True, indent = 4, sort_keys = True)
			json.dump(jsonData, f, ensure_ascii = True, indent = "\t")
			print("[Lightfielder][RenderLog] " + str(logPathAbs))
	except OSError as error:
		print("\t[Lightfielder][RenderLog][JSON Save Error]", error)

if __name__ == "__main__":
	project = GetProject()

	# Verify this script was run as a Trigger script, not as a Workspace > Script > Deliver menu item.
	try:
		# Read the current job in the render queue
		# Note: "job" is a global variable available in the trigger script context
		jobDetails = GetRenderJob(project, job)

		jobStatus = project.GetRenderJobStatus(job)

		# Write a JSON formatted render log to disk
		WriteLog(jobDetails, jobStatus)
	except NameError:
		print("[Lightfielder][Error] \"Render Log.py\"  needs to be run as a Deliver page Trigger script.")
