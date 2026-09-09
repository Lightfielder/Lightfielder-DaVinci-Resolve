"""
Lightfielder 12 Video Track Solo.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Solo a video track in the Edit page.

Script Usage:
1. Open a Resolve Edit page based timeline. Select the menu item: "Workspace > Scripts > Lightfielder > 12 Video Track Solo".

2. The Stack Solo script has a Solo View "SpinBox" control with a number input field and up/down arrows that let you navigate between the 50 camera views.

A video track that is disabled has a red colored filmstrip icon with a diagonal slash through it. The enabled video track is shown with a gray colored filmstrip icon.

3. If you click in the "Solo View" input field in the Stack Solo script you can use the up/down cursor keys to cycle the values. The mouse scroll wheel can also be used to cycle the values if you place the cursor pointer over the "Solo View" input field.

You can also toggle the enabled/disabled state of all video tracks with the "All On" and "All Off" Buttons.

"""

import sys, os

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

def CreateWindow():
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectSetting = project.GetSetting()

	# Get the timeline object
	timeline = GetTimeline()

	if timeline == None:
		ErrorWindow("Video Track Solo", "Please open a Resolve timeline before running this script")
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
			"WindowTitle": "Lightfielder",
			"WindowFlags": {"Window": True, "WindowStaysOnTopHint": windowFloat},
			"ID": "VideoTrackSoloWin",
			"TargetID" : "VideoTrackSoloWin",
			"Geometry": [10, 185, 485, 200],
			"MinimumSize": [485, 200],
			"FixedSize": [485, 200],
			#"Spacing": 0,
			#"Margin": 0,
		},[
			ui.VGroup({
				 "ID": "Content",
				 "Weight": 1.0,
			},[
				ui.VGroup({
					"Weight": 2.0,
					# "Weight": 0.01,
				},[
					ui.HGroup({
						"Weight": 0.5,
					},[
						ui.Label({
							"ID": "ViewLabel",
							"Text": "12 Video Track Solo",
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
					"Weight": 1.0,
				},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "Solo View",
						"Weight": 0.01,
					}),
					ui.SpinBox({
						"ID": "ViewSpinner",
						"Minimum": 1,
						"Maximum": 50,
						"MinimumSize": [54, 32],
						"Weight": 1.0,
					}),
					ui.Button({
						"ID": "OnButton",
						"Text": "All On",
						"StyleSheet": "QTextEdit { border: 1px solid black; }",
						"MinimumSize": [80, 32],
						"MaximumSize": [80, 32],
						"Weight": 0.01,
					}),
					ui.Button({
						"ID": "OffButton",
						"Text": "All Off",
						"StyleSheet": "QTextEdit { border: 1px solid black; }",
						"MinimumSize": [80, 32],
						"MaximumSize": [80, 32],
						"Weight": 0.01,
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
					ui.HGroup({
						"Weight": 0.1
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
			WindowPrefSave(dlg, "Lightfielder.VideoTrackSoloWin.Geometry")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
		dlg.On.VideoTrackSoloWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.VideoTrackSoloWin.Geometry")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.VideoTrackSoloWin.Close = CloseFunc

		# Add your GUI element based event functions here:

		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_12_Video_Track_Solo.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		def OnButtonFunc(ev):
			# Read the current Resolve page
			page = resolve.GetCurrentPage()

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

			# Part 1 - Butterfly to the edit page and back to apply the track soloing
			if (page ==  "color") or (page ==  "deliver"):
				resolve.OpenPage("edit")

			# Get the track count
			timelineVideoTrackCount = timeline.GetTrackCount("video")
			itm['ViewSpinner'].Maximum = timelineVideoTrackCount
			print("[Lightfielder][All On] " + str(timelineVideoTrackCount))
			itm["ProgressLabel"].Text = "  Progress: All On"

			for i in range(int(timelineVideoTrackCount + 1)):
				if timeline.GetIsTrackEnabled("video", i) == False:
					timeline.SetTrackEnable("video", i, True)

			# Part 2 - Butterfly to the edit page and back to apply the track soloing
			if (page ==  "color") or (page ==  "deliver"):
				resolve.OpenPage(page)
		dlg.On.OnButton.Clicked = OnButtonFunc

		def OffButtonFunc(ev):
			# Read the current Resolve page
			page = resolve.GetCurrentPage()

			# Part 1 - Butterfly to the edit page and back to apply the track soloing
			if (page ==  "color") or (page ==  "deliver"):
				resolve.OpenPage("edit")

			# Read the current Resolve page
			page = resolve.GetCurrentPage()

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
			itm['ViewSpinner'].Maximum = timelineVideoTrackCount
			print("[Lightfielder][All Off] " + str(timelineVideoTrackCount))
			itm["ProgressLabel"].Text = "  Progress: All Off"
			
			for i in range(int(timelineVideoTrackCount + 1)):
				if timeline.GetIsTrackEnabled("video", i) == True:
					timeline.SetTrackEnable("video", i, False)

			# Part 2 - Butterfly to the edit page and back to apply the track soloing
			if (page ==  "color") or (page ==  "deliver"):
				resolve.OpenPage(page)
		dlg.On.OffButton.Clicked = OffButtonFunc

		def ViewSpinnerFunc(ev):
			# Read the current Resolve page
			page = resolve.GetCurrentPage()

			# Part 1 - Butterfly to the edit page and back to apply the track soloing
			if (page ==  "color") or (page ==  "deliver"):
				resolve.OpenPage("edit")

			# Read the current Resolve page
			page = resolve.GetCurrentPage()

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

			viewNum = itm['ViewSpinner'].Value
			itm["ProgressLabel"].Text = "  Progress: Solo Video Track #" + str(viewNum)

			# Get the track count
			timelineVideoTrackCount = timeline.GetTrackCount("video")

			itm['ViewSpinner'].Maximum = timelineVideoTrackCount
			print("[Lightfielder][Solo View]\t" + str(viewNum))

			for i in range(int(timelineVideoTrackCount + 1)):
				if viewNum == (i):
					if timeline.GetIsTrackEnabled("video", i) == False:
						timeline.SetTrackEnable("video", i, True)
				else:
					if timeline.GetIsTrackEnabled("video", i) == True:
						timeline.SetTrackEnable("video", i, False)

			# Part 2 - Butterfly to the edit page and back to apply the track soloing
			if (page ==  "color") or (page ==  "deliver"):
				resolve.OpenPage(page)
		dlg.On.ViewSpinner.ValueChanged = ViewSpinnerFunc

		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		def CloseButtonFunc(ev):
			print("[Lightfielder][Window][Close Button]")
	
			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
	
			disp.ExitLoop()
		dlg.On.CloseButton.Clicked = CloseButtonFunc
	
		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool12", "Tool11")
	
			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc
	
		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool12", "Tool13")

			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.VideoTrackSoloWin.Geometry")

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('VideoTrackSoloWin', {
			Target {
				ID = 'VideoTrackSoloWin',
			},
			Hotkeys {
				Target = 'VideoTrackSoloWin',
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
		WindowPrefSave(dlg, "Lightfielder.VideoTrackSoloWin.Geometry")

if __name__ == "__main__":
	if GetProject() and GetTimeline():
		CreateWindow()
	else:
		print("[Lightfielder] Please open a Resolve project and timeline before running this script.")
		ErrorWindow("Lightfielder", "Please open a Resolve project and timeline before running this script.")
	print("[Lightfielder][Done]")
