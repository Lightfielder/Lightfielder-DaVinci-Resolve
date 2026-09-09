"""
Lightfielder Apply Dewarp Comp to Timeline Clips 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Import an external Fusion .comp file and attach it to each of the clips in a timeline.
This allows the use of OFX plugins, FusionSDK plugins, Fusion nodes, fuses, and macros as image dewarping tools.

"""

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

def ImportFusion():
	compFile = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Dewarp/kvrBrownConrady.comp")
	# compFile = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Dewarp/LensDistortFusion.comp")
	# compFile = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Dewarp/RELensUltraWideOFX.comp")
	print("[Lightfielder][Dewarp Preset] " + str(compFile))

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
	print("[Track Count]", timelineVideoTrackCount)

	# Get the track structure
	for i in range(int(timelineVideoTrackCount + 1)):
		trackName = timeline.GetTrackName("video", i + 1)

		# Get the clips in the track
		clips = timeline.GetItemListInTrack("video", i + 1)
		if clips != None:
			for clip in clips:
				if clip != None:
					result = clip.ImportFusionComp(compFile)
					if result != None:
						print(result)
						print(result.GetAttrs())

if __name__ == "__main__":
	ImportFusion()
