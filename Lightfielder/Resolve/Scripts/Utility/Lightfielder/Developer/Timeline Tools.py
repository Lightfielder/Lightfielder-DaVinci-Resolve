"""
Lightfielder Timeline 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Automate .edl and .otio formatted timeline importing tasks.

Script Usage:
1. Create a new Resolve project and add the Bin folder structure you desire. Select the menu item: "Workspace > Scripts > Lightfielder > 03 Timeline Import".

2. Use the "Source File" text field to select either a Sony CMX 3600 .edl or an OpenTimelineIO .otio formatted timeline. The Browse button displays a file picking dialog.

Customize any settings you would like such as the "Automatically set timeline name from filename" checkbox, or the "Automatically import source clips into the media pool" checkbox.

If you have the "Automatically set timeline name from filename" checkbox disabled then you can manually specify the name of your imported timeline using the "Timeline Name" text field.

3. Click the "Import EDL" button to continue.

Timeline Operations:

The "Import External Folders" button allows you to select the base Resolve project folder on disk and import those folders into the Bin window. This will only bring in the empty folder structure. No files are imported during this process. This is a great way to clone a previous Resolve project folder hierarchy if you want to create a new Bin preset for a new project you are starting.

The "Create External Folders" button is used to export the current bin hierarchy by creating those folder structures on disk.

The "Import R3D Footage" button allows you to select a base folder that holds footage on disk. All the .R3D files in this folder hierarchy will be imported into your current Resolve Bin folder.

The "Create Empty Timeline" button will add a new timeline to the Media page. The timeline takes its name from the "Timeline Name" text field contents. If no new timeline is created it likely means the Timeline Name is not a unique value in this project such as "Timeline 1".


Tip: Quickly Resize Video Track Height
If you want to quickly resize the height of a video track use the "Shift key + Mouse Scroll Wheel Rotate" hotkey to zoom the track height. The area in the timeline that your mouse cursor is over will define if the video or audio tracks are zoomed taller/shorter.


Todo:
- Batch Trim Window:
	- Add two buttons with confirm dialogs: "Minimal Timecode Sync" vs "Pure Shots"
- Need to auto increment the timeline # in the name field if it exists
- Add an option to move it into a "##_Timelines" folder in the bin.
- Scan for missing media in current bin folder.
- Logging Events Timestamp: Date.now()
- RED Import - Add Reel info to media pool from the clip name letters "AA" - "EJ"

"""
import os

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
	if project is None:
		print("[Lightfielder] No Resolve project is open at this time.")
		ErrorWindow("Lightfielder", "No Resolve project is open at this time.")
		exit()
	else:
		return project

def GetMediaPool():
	resolve = app.GetResolve()
	projectManager = resolve.GetProjectManager()
	project = projectManager.GetCurrentProject()
	mediaPool = project.GetMediaPool()
	return mediaPool

def GetFolder(parentFolder, childFolder, mediaPool):
	for folder in parentFolder.GetSubFolderList():
		if folder.GetName() == childFolder:
			return folder
	else:
		return mediaPool.AddSubFolder(parentFolder, childFolder)

def ImportR3DFiles(dirPath):
	# Check what type of footage to import
	mediaFormat = app.GetData("Lightfielder.MediaFormat") or "R3D"

	matches = []
	for root, dirnames, filenames in os.walk(dirPath):
		for file in filenames:
			# The double parenthesis are used in the endswith() function to make the file types into a tupple like list
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
	return matches

def FolderWindow():
	ui = fu.UIManager
	folder_disp = bmd.UIDispatcher(ui)

	folder_dlg = folder_disp.AddWindow({
		"WindowTitle": "",
		"ID": "FolderWin",
		"TargetID" : "FolderWin",
		"Geometry": [0, 85, 630, 135],
		"MinimumSize": [0, 85, 630, 135],
		"MinimumSize": [0, 85, 630, 135],
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
						"Text": "  Select a Folder",
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
				ui.Label({"ID": "FolderLabel", "Text": "Folder Name:", "Weight": 0.1}),
				ui.LineEdit({"ID": "FolderTxt", "Text": "", "PlaceholderText": "Please enter a folder name", "Weight": 0.9}),
				ui.Button({"ID": "BrowseButton", "Text": "Browse", "Geometry": [0, 0, 30, 50], "Weight": 0.1}),
			]),
			ui.VGap(10),
			ui.HGroup({"Weight": 0.0,},[
				ui.Button({
					"ID": "CloseButton",
					"Text": "Cancel",
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

	folder_itm = folder_dlg.GetItems()

	# The window was closed
	def FolderWinFunc(ev):
		folder_disp.ExitLoop()
	folder_dlg.On.FolderWin.Close = FolderWinFunc

	# Add your GUI element based event functions here:

	def OKButtonFunc(ev):
		print("[Lightfielder][Window][OK Button]")
		folder_disp.ExitLoop()
	folder_dlg.On.OKButton.Clicked = OKButtonFunc

	def CloseButtonFunc(ev):
		print("[Lightfielder][Window][Close Button]")
		folder_itm["FolderTxt"].Text = ""
		folder_disp.ExitLoop()
	folder_dlg.On.CloseButton.Clicked = CloseButtonFunc

	def BrowseButtonFunc(ev):
		selectedPath = fu.RequestDir()
		if selectedPath:
			folder_itm["FolderTxt"].Text = str(selectedPath)
	folder_dlg.On.BrowseButton.Clicked = BrowseButtonFunc

	folder_dlg.Show()
	folder_disp.RunLoop()
	folder_dlg.Hide()

	# When the window is closed send back the folder name
	return str(folder_itm["FolderTxt"].Text)


def CreateTimelineImportWindow():
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
			"ID": "TimelineWin",
			"TargetID" : "TimelineWin",
			"Geometry": [500, 50, 485, 440],
			"MinimumSize": [485, 440],
			"FixedSize": [485, 440],
			#"Spacing": 0,
			#"Margin": 5,
		},[
			ui.VGroup({
				"ID": "Content",
				"Weight": 1.0,
			},[
				ui.Label({
					"ID": "ViewLabel",
					"Text": "  Timeline Tools",
					"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
					"Margin": 0,
					"Spacing": 0,
					"Weight": 0.01,
				}),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 3px; background-color: rgb(76, 154, 109); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.Label({"ID": "TimelineNameLabel", "Text": "Timeline Name", "Weight": 0.1, "MinimumSize": [105, 22],}),
					ui.LineEdit({"ID": "TimelineTxt", "Text": "Timeline 1", "PlaceholderText": "Please enter a timeline name.", "Weight": 0.9}),
				]),
				ui.VGroup({
					"Weight": 0.1,
				},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "  Load EDL",
						"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
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
					"ID": "TimeTab",
					"Spacing": 10,
				},[
					ui.HGroup({
						"Weight": 1.0,
					},[
						ui.Label({"ID": "EDLFilenameLabel", "Text": "Source File", "Weight": 0.1, "MinimumSize": [80, 32],}),
						ui.LineEdit({"ID": "FileLineTxt", "Text": "", "PlaceholderText": "Please enter an .edl or .otio filename.", "Weight": 0.9}),
						ui.Button({"ID": "BrowseEDLButton", "Text": "Browse", "MinimumSize": [100, 32], "Weight": 0.1}),
					]),
					ui.CheckBox({
						"ID": "TimelineNameFromFilenameCheckbox",
						"Text": "Automatically set timeline name from filename",
						"Checked": True,
					}),
					ui.CheckBox({
						"ID": "ImportSourceClipsCheckbox",
						"Text": "Automatically import source clips into media pool",
						"Checked": True,
					}),
					ui.HGroup({
						"Weight": 0.1
					},[
						ui.HGap(20, 1),
						ui.Button({"ID": "ImportEDLButton", "Text": "Import EDL", "MinimumSize": [100, 32], "Weight": 0.1}),
					]),
					ui.VGroup({
						"Weight": 0.1,
					},[
						ui.HGroup({},[
							ui.Label({
								"ID": "ViewLabel",
								"Text": "  Operations",
								"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
								"Weight": 0.01,
							}),
						]),
						ui.Label({
							"ID": "DividerLabel",
							"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
							"Spacing": 0,
							"Margin": 0,
							"Weight": 0.01,
						}),
					]),
					ui.HGroup({
						"Weight": 0.1,
					},[
						ui.Button({"ID": "CreateEmptyTimelineButton", "Text": "Create Empty Timeline", "MinimumSize": [150, 32], "Weight": 0.1}),
						ui.Button({"ID": "AddTracksButton", "Text": "Add Extra Video Tracks", "MinimumSize": [150, 32], "Weight": 0.1}),
						ui.HGap(20, 1),
					]),
					ui.HGroup({
						"Weight": 0.1,
					},[
						ui.Button({"ID": "ImportExternalFoldersButton", "Text": "Import External Folders", "MinimumSize": [150, 32], "Weight": 0.1}),
						ui.Button({"ID": "CreateExternalFoldersButton", "Text": "Create External Folders", "MinimumSize": [150, 32], "Weight": 0.1}),
						ui.Button({"ID": "ImportR3DFootageButton", "Text": "Import R3D Footage", "MinimumSize": [150, 32], "Weight": 0.1}),
						#ui.HGap(20, 1),
					]),
				]),
			]),
		])

		itm = dlg.GetItems()

		# Resize the window
		dlg.RecalcLayout()

		# The window was hidden
		#def HideFunc(ev):
		#	print("[Lightfielder][Window][Hidden]")
		#dlg.On.TimelineWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")
			disp.ExitLoop()
		dlg.On.TimelineWin.Close = CloseFunc

		def BrowseEDLButtonFunc(ev):
			selectedPath = fu.RequestFile()
			if selectedPath:
				itm["FileLineTxt"].Text = str(selectedPath)
		dlg.On.BrowseEDLButton.Clicked = BrowseEDLButtonFunc

		def ImportEDLButtonFunc(ev):
			project = GetProject()
			mediapool = project.GetMediaPool()

			#trackLayout = int(itm["TrackLayoutCombo"].CurrentIndex)
			trackLayout = 0

			#importSourceClips = itm["ImportSourceClipsCheckbox"].Checked
			importSourceClips = False
			timelineNameFromFilename = itm["TimelineNameFromFilenameCheckbox"].Checked

			#"sourceClipsFolders": List of Media Pool folder objects
			#"sourceClipsPath": string, specifies a filesystem path to search for source clips if the media is inaccessible in their original path and if "importSourceClips" is True

			# Use the current folder to help relink content
			#sourceClipsFolders = mediapool.GetCurrentFolder()

			# EDL File name
			filepath = str(app.MapPath(itm["FileLineTxt"].Text or ""))

			# EDL file extension ".edl" or ".otio"
			newTimelineBaseName, newTimelineExt = os.path.splitext(filepath)

			# Timeline Name from text field
			newTimelineName = itm["TimelineTxt"].Text

			# Checkbox to set the timeline name from the filename
			if timelineNameFromFilename:
				newTimelineName = os.path.basename(newTimelineBaseName)

			#print("[Lightfielder][Import EDL] [File] \"" + filepath + "\" [Timeline Name] " + str(newTimelineName) + " [Track Layout] " + str(trackLayout) +  " [Automatically import source clips] " + str(importSourceClips))
			print("[Lightfielder][Import EDL] [File] \"" + filepath + "\" [Timeline Name] " + str(newTimelineName) +  " [Automatically import source clips] " + str(importSourceClips))

			if filepath == "":
				print("[Lightfielder][Import EDL] [Error] No EDL file was selected.")
			else:
				mediapool.ImportTimelineFromFile(filepath, {
					"timelineName": newTimelineName,
					"importSourceClips": importSourceClips,
					"sourceClipsPath": "/Users/vfx/Desktop/ID0001/03_footage/"
				})

# 				if trackLayout == 0:
# 					# Just import the timeline as is
# 					mediapool.ImportTimelineFromFile(filepath, {
# 						"timelineName": newTimelineName,
# 						"importSourceClips": importSourceClips,
# 					})
# 				else:
# 					# Todo: Add an OTIO processing stage then import the modified timeline
# 					mediapool.ImportTimelineFromFile(filepath, {
# 						"timelineName": newTimelineName,
# 						"importSourceClips": importSourceClips,
# 					})
		dlg.On.ImportEDLButton.Clicked = ImportEDLButtonFunc

		def CreateEmptyTimelineButtonFunc(ev):
			project = GetProject()
			mediapool = project.GetMediaPool()

			# Todo: Need to auto increment the timeline # in the name field if it exists
			# Add an option to move it into a "##_Timelines" folder in the bin.
			timelineName = itm["TimelineTxt"].Text
			timeline = mediapool.CreateEmptyTimeline(timelineName)
		dlg.On.CreateEmptyTimelineButton.Clicked = CreateEmptyTimelineButtonFunc

		def AddTracksButtonFunc(ev):
			# Get the number of cameras views in the array
			maxCameras = GetMaxNumberOfCameras()

			# Get the timeline object
			timeline = GetTimeline()
			if timeline is None:
				print("[Lightfielder] No Resolve timeline is open at this time.")
			else:
				# Get the timeline name
				timelineName = timeline.GetName()
				#print("[Timeline Name] " + str(timelineName))

				# Get the track count
				timelineVideoTrackCount = timeline.GetTrackCount("video")
				if timelineVideoTrackCount <= maxCameras:
					trackGoal = maxCameras - timelineVideoTrackCount
					for x in range(trackGoal):
						timeline.AddTrack("video")
				timelineAudioTrackCount = timeline.GetTrackCount("audio")
				if timelineAudioTrackCount <= maxCameras:
					trackGoal = maxCameras - timelineAudioTrackCount
					# Add the required audio tracks
					for x in range(trackGoal):
						timeline.AddTrack("audio")
		dlg.On.AddTracksButton.Clicked = AddTracksButtonFunc

		def MinimalTimecodeSyncButtonFunc(ev):
			# Get the timeline object
			timeline = GetTimeline()
			if timeline is None:
				print("[Lightfielder] No Resolve timeline is open at this time.")
			else:
				# Get the timeline name
				timelineName = timeline.GetName()
		dlg.On.MinimalTimecodeSyncButton.Clicked = MinimalTimecodeSyncButtonFunc


		def ImportR3DFootageButtonFunc(ev):
			mediapool = GetMediaPool()
			rootFolder = mediapool.GetRootFolder()
			# Todo - Add a file dialog.
			dirPath = FolderWindow()
			fileList = ImportR3DFiles(dirPath)
			#for f in fileList:
			#	print(f)
			mpItems = mediapool.ImportMedia(fileList)
			clipCount = 0
			print("[Lightfielder][Imported R3D Footage]")
			for mpItem in mpItems:
				clipCount = clipCount + 1
# 				clipName = str(clip.GetName())
# 				clipColor = str(clip.GetClipColor())
# 				clipDuration = str(clip.GetDuration())

				mpProp = mpItem.GetClipProperty()

				mpID = mpItem.GetMediaId()
				mpFPS = str(mpItem.GetClipProperty("FPS"))
				mpOnline = str(mpItem.GetClipProperty("Online Status"))
				mpRes = str(mpItem.GetClipProperty("Resolution"))
				mpFile = str(mpItem.GetClipProperty("File Path"))

				clipReelName = str(mpItem.GetClipProperty("Reel Name"))
				clipScene = str(mpItem.GetClipProperty("Scene"))
				clipShot = str(mpItem.GetClipProperty("Shot"))
				clipTake = str(mpItem.GetClipProperty("Take"))

				print("\t[Lightfielder][" + str(clipCount) + "] [File]" + str(mpFile))
		dlg.On.ImportR3DFootageButton.Clicked = ImportR3DFootageButtonFunc

		def ImportExternalFoldersButtonFunc(ev):
			mediapool = GetMediaPool()
			rootFolder = mediapool.GetRootFolder()

			# Todo - Add a file dialog.
			#dirPath = "/Users/vfx/Desktop/ID0001"
			dirPath = FolderWindow()
			if (dirPath != None) and (dirPath != ""):
				# Scan the sub-folder hiearchy
				for path, dirs, files in os.walk(dirPath):
					relPath = path.replace(dirPath, "")
					#print(path)
					#print(relPath)
					# Create the Media Pool Bins
					binSubFolders = relPath.split("/")
					parentFolder = rootFolder
					for f in binSubFolders:
						if (f != None) and (f != ""):
							parentFolder = GetFolder(parentFolder, f, mediapool)
		dlg.On.ImportExternalFoldersButton.Clicked = ImportExternalFoldersButtonFunc

		def CreateExternalFoldersButtonFunc(ev):
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

			# Todo - Add a file dialog.
			#baseFolder = "/Users/vfx/Desktop/ID0001"
			baseFolder = FolderWindow()
			if (baseFolder != None) and (baseFolder != ""):
				# Build the bin paths
				GetSubFolder(rootFolder, "")

				# Build the directories
				for binItemPath in binFolderItems:
					# Example: "/Users/vfx/Desktop/Bins/01_delivery/render_checks"
					directoryPath = app.MapPath(baseFolder + "/" + binItemPath)

					# Create the intermediate directories on disk for the tree item
					if not os.path.exists(directoryPath):
						try:
							print("\t[Lightfielder][Bin][Make Directory]", directoryPath)
							os.makedirs(directoryPath)
						except OSError as error:
							print("\t[Lightfielder][Bin][Make Directory Error]", error)
					else:
						print("\t[Lightfielder][Bin][Directory Exists]", directoryPath)

			# Reveal folders on disk
			app.Execute('bmd.openfileexternal("Open", [[' + str(baseFolder) + ']])')
		dlg.On.CreateExternalFoldersButton.Clicked = CreateExternalFoldersButtonFunc

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('TimelineWin', {
			Target {
				ID = 'TimelineWin',
			},
			Hotkeys {
				Target = 'TimelineWin',
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
	CreateTimelineImportWindow()
