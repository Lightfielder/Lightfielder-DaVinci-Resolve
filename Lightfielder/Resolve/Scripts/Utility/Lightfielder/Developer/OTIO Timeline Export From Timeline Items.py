"""
Lightfielder OTIO Timeline Export 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

"""

import tempfile, os

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

def GetTimeline():
	project = GetProject()
	timeline = project.GetCurrentTimeline()

	if not timeline:
		if project.GetTimelineCount() > 0:
			timeline = project.GetTimelineByIndex(1)
			project.SetCurrentTimeline(timeline)

	return timeline

def GetProject():
	# Get the current Resolve timeline
	res = app.GetResolve()
	projectManager = res.GetProjectManager()
	project = projectManager.GetCurrentProject()
	return project

def TimelineExport():
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectSetting = project.GetSetting()

	# Get the timeline object
	timeline = GetTimeline()

	# Get the timeline name
	timelineName = timeline.GetName()
	#print("[Timeline Name] " + str(timelineName))

	ot_timeline = otio.schema.Timeline()
	ot_timeline.name = timelineName

	# Get the timeline settings
	timelineSetting = timeline.GetSetting()

	# Get the track count
	timelineVideoTrackCount = timeline.GetTrackCount("video")

	# Get the track structure
	for i in range(int(timelineVideoTrackCount + 1)):
		trackName = timeline.GetTrackName("video", i + 1)

		# Create an OTIO track
		ot_track = otio.schema.Track()
		ot_track.name = "V" + str(i + 1)
		ot_timeline.tracks.append(ot_track)

		# Get the clips in the track
		clips = timeline.GetItemListInTrack("video", i + 1)
		for clip in clips:
			# Get the clip values
			clipName = str(clip.GetName())
			clipColor = str(clip.GetClipColor())
			clipDuration = float(clip.GetDuration())
			clipStart = float(clip.GetStart())
			clipEnd = float(clip.GetEnd())
			clipEnabled = str(clip.GetClipEnabled())

			mpItem = clip.GetMediaPoolItem()
			mpProp = mpItem.GetClipProperty()
			mpID = mpItem.GetMediaId()
			mpFPS = float(mpItem.GetClipProperty("FPS"))
			mpStart = float(mpItem.GetClipProperty("Start"))
			mpStartTC = str(mpItem.GetClipProperty("Start TC"))
			mpEnd = float(mpItem.GetClipProperty("End"))
			mpDuration = float(mpEnd) - float(mpStart)
			# mpDuration = str(mpItem.GetClipProperty("Duration"))
			mpOnline = str(mpItem.GetClipProperty("Online Status"))
			mpRes = str(mpItem.GetClipProperty("Resolution"))
			mpResWH = mpRes.split("x")
			mpFile = str(mpItem.GetClipProperty("File Path"))

			mpParentFolder = os.path.dirname(mpFile)

			clipReelName = str(mpItem.GetClipProperty("Reel Name"))
			clipScene = str(mpItem.GetClipProperty("Scene"))
			clipShot = str(mpItem.GetClipProperty("Shot"))
			clipTake = str(mpItem.GetClipProperty("Take"))

			print(mpProp)

			# Create an OTIO clip on the new track
			available_image_bounds = otio.schema.Box2d(
				otio.schema.V2d(0.0, 0.0),
				otio.schema.V2d(float(mpResWH[0]), float(mpResWH[1]))
			)

			ot_clip = otio.schema.Clip()
			ot_clip.name = os.path.basename(str(mpFile))
			print("[media_reference]")
# 			ot_clip.media_reference = otio.schema.ExternalReference(
# 				target_url = "file://" + str(mpFile),
# 				available_image_bounds = available_image_bounds,
# 				available_range = otio.opentime.TimeRange(
# 					start_time = otio.opentime.from_frames(mpStart, mpFPS),
# 					duration = otio.opentime.from_frames(mpDuration, mpFPS)
# 				)
# 			)
			ot_clip.media_reference = otio.schema.ExternalReference(
				target_url = "file://" + str(mpFile),
				available_image_bounds = available_image_bounds,
				available_range = otio.opentime.TimeRange(
					start_time = otio.opentime.from_frames(clipStart, mpFPS),
					duration = otio.opentime.from_frames(clipDuration, mpFPS)
				)
			)

			# Source range is the edited and chopped down timeline clip range
			print("[source_range]")
			ot_clip.source_range = otio.opentime.TimeRange(
				start_time = otio.opentime.from_frames(clipStart, mpFPS),
				duration = otio.opentime.from_frames(1, mpFPS)
			)

			ot_track.append(ot_clip)

	tempDirAbs = app.MapPath("/Users/vfx/Desktop/")
	if not os.path.exists(tempDirAbs):
		os.makedirs(tempDirAbs)
		print("[Lightfielder][Make Directory] ", tempDirAbs)

	ot_temp_file = os.path.join(tempDirAbs, "Timeline.otio")
	try:
		result = otio.adapters.write_to_file(ot_timeline, ot_temp_file)
	finally:
		print("[Lightfielder][File Name] " + str(ot_temp_file))

def CreateExportWindow():
	# Should this window float above all other views
	windowFloat = app.GetData("Lightfielder.WindowStaysOnTop")
	if windowFloat is None:
		windowFloat = True

	# Create a new UI Manager window
	ui = fu.UIManager
	disp = bmd.UIDispatcher(ui)

	dlg = disp.AddWindow({
		"WindowTitle": "OTIO Timeline Export",
		"ID": "ExportWin",
		"TargetID" : "ExportWin",
		"Geometry": [10, 110, 230, 55],
		"MinimumSize": [10, 110, 230, 55],
		"FixedSize": [10, 110, 230, 55],
	},[
		ui.VGroup({"Spacing": 0,},[
			# Add your GUI elements here:
			ui.HGroup({"Weight": 0.1,},[
				ui.Button({
					"ID": "ExportButton",
					"Text": "Timeline Export...",
					"Weight": 0.5,
				}),
				ui.Button({
					"ID": "ConsoleButton",
					"Text": "Console",
					"Weight": 0.5,
					"Checkable": True,
				}),
			]),
		]),
	])

	# Resize the window
	dlg.RecalcLayout()

	itm = dlg.GetItems()

	# The window was closed
	def CloseFunc(ev):
		print("[Lightfielder][Window][Closed]")
		
		disp.ExitLoop()
	dlg.On.ExportWin.Close = CloseFunc

	# Add your GUI element based event functions here:

	def ExportButtonFunc(ev):
		print("[Lightfielder][Timeline Export]")
		TimelineExport()
	dlg.On.ExportButton.Clicked = ExportButtonFunc

	def ConsoleButtonFunc(ev):
		if itm["ConsoleButton"].Checked == True:
			app.DoAction("Console_Show", {"Show": True})
		else:
			app.DoAction("Console_Show", {"Show": False})
	dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

	# Add a close window hotkey event handler
	app.Execute(
	"""
	app:AddConfig('ExportWin', {
		Target {
			ID = 'ExportWin',
		},
		Hotkeys {
			Target = 'ExportWin',
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

if __name__ == "__main__":
	# OpenTimelineIO
	try:
		import opentimelineio as otio
	except ModuleNotFoundError:
		ErrorWindow("OpenTimelineIO","""The OTIO Python module is missing. The macOS & Linux Terminal based install commands for OpenTimelineIO are:
	pip3 install --upgrade pip
	pip3 install OpenTimelineIO
	pip3 install PySide6
		""")
		exit()
	
	try:
		print(dir(otio.adapters))
	except AttributeError:
		ErrorWindow("OpenTimelineIO","""The OTIO Python module is missing. The macOS & Linux Terminal based install commands for OpenTimelineIO are:
	pip3 install --upgrade pip
	pip3 install OpenTimelineIO
	pip3 install PySide6
		""")
		exit()

	CreateExportWindow()
