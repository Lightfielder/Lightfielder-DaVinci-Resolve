"""
Lightfielder 03 Shotlog Pre-Flight.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

The pre-flight script detects common issues that occur with the Shotlog.csv file, Technisync JSON file and the imported multi-view R3D footage.

The script can optionally create a diagnostics package that adds a Media Pool CSV export to help catch issues with footage ingest and metadata tagging.

Todo
- This is a work-in-progress script

"""

import platform
import sys, os, csv, datetime, math, json

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

def ShotlogPreFlightWindow():
	presetsBasePath = app.MapPath("Scripts:/Utility/Lightfielder/Presets/ShotlogPreFlight/")

	# Get the project name
	res = app.GetResolve()
	project = GetProject()
	if project is None:
		print("[Lightfielder] No Resolve project is open at this time.")
		exit()
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
			"ID": "ShotlogPreFlightWin",
			"TargetID" : "ShotlogPreFlightWin",
			"Geometry": [500, 50, 540, 710],
			"MinimumSize": [540, 710],
			"FixedSize": [540, 710],
			#"Spacing": 0,
			#"Margin": 5,
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
						"Text": "03 Shotlog Pre-Flight",
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
					"Text": "This dialog is the future home of an interface for detecting common issues that occur with the Shotlog.csv file, Technisync JSON file and the imported multi-view R3D footage. It also offers guidance for ways to work through the problems that are solvable.",
					"ReadOnly": True,
					"StyleSheet": "QTextEdit { border: 0px; }",
					"MinimumSize": [470, 80],
					"Weight": 0.4,
				}),
				ui.Label({
					"ID": "DividerLabel",
					"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
					"Spacing": 0,
					"Margin": 0,
					"Weight": 0.01,
				}),
				ui.HGroup({
					"Weight": 2.0,
				},[
					ui.Tree({
						"ID": "Tree",
						"SortingEnabled": True,
						"SelectionMode": "ExtendedSelection",
						"Weight": 2.0,
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
						"MinimumSize": [120, 32],
						"Weight": 0.5
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

		hdr = itm["Tree"].NewItem()
		hdr.Text[0] = "Active"
		hdr.Text[1] = "Category"
		hdr.Text[2] = "Task"
		hdr.Text[3] = "Description"
		hdr.Text[4] = "Result"

		itm["Tree"].SetHeaderItem(hdr)

		# Number of columns in the Tree list
		itm["Tree"].ColumnCount = 5

		# Resize the Columns
		itm["Tree"].ColumnWidth[0] = 60
		itm["Tree"].ColumnWidth[1] = 100
		itm["Tree"].ColumnWidth[2] = 200
		itm["Tree"].ColumnWidth[3] = 250
		itm["Tree"].ColumnWidth[4] = 70

		# Change the sorting order of the tree
		#itm["Tree"].SortByColumn(0, "DescendingOrder")
		itm["Tree"].SortByColumn(0, "AscendingOrder")

		def RefreshTree():
			print("[Lightfielder] Rebuilding the Tree")
			# Remove the old tree entries
			itm["Tree"].Clear()

		# Resize the window
		dlg.RecalcLayout()

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
			WindowPrefSave(dlg, "Lightfielder.ShotlogPreFlightWin.Geometry")
		dlg.On.ShotlogPreFlightWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.ShotlogPreFlightWin.Geometry")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.ShotlogPreFlightWin.Close = CloseFunc

		def CloseButtonFunc(ev):
			print("[Lightfielder][Window][Close Button]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.ShotlogPreFlightWin.Geometry")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.CloseButton.Clicked = CloseButtonFunc

		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool3", "Tool2")

			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool3", "Tool4")

			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		# Add your GUI element based event functions here:
		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_03_Shotlog_PreFlight.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		def GoButtonFunc(ev):
			startTimer = datetime.datetime.now()
			startTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")

			print("\n[Lightfielder][Shotlog Pre-Flight][Start Processing]")
			itm["ProgressLabel"].Text = "  Progress: Started Pre-Flight [Wallclock " + GetTimeElapsed(startTimer) + "]"
			resultStr = ""
			resultStr += "\n<h2>Shotlog Pre-Flight</h2>" + "\n"
			
			resultStr += "\nTasks tbd..." + "\n"

			# resultStr += "<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
			# resultStr += "<tr><td>Active</td><td>Category</td><td>Task</td><td>Description</td><td>Result</td></tr>\n"
			# resultStr += "<tr><td>&#9745;</td><td></td><td></td><td></td><td></td></tr>\n"
			# resultStr += "</table>\n"

			#print("\n[Lightfielder][Shotlog][Start Processing]")
			itm["ProgressLabel"].Text = "  Progress: Started Pre-Flight Process [Wallclock " + GetTimeElapsed(startTimer) + "]"
			
			resultStr += "\n<h2>Completed Pre-Flight Process</h2>\n"
			endTimer = datetime.datetime.now()
			endTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")
			resultStr += "\n<p>" + str(endTimeStamp) + " (HH:MM:SS)</p>\n"
			
			elapsedTime = (endTimer - startTimer).total_seconds()
			mins, secs = divmod(elapsedTime, 60)
			timeFormatted = "Elapsed Time: " + str(math.ceil(mins)).zfill(2) + " Minutes " + str(math.ceil(secs)).zfill(2) + " Seconds"
			resultStr += "\n<p>" + str(timeFormatted) + "</p>\n"
			
			itm["ProgressLabel"].Text = "  Progress: Completed Pre-Flight Process [Wallclock " + GetTimeElapsed(startTimer) + "]"

			# Play the sound effect
			# soundName = app.GetData("Lightfielder.SoundEffectsError")
			soundName = app.GetData("Lightfielder.SoundEffectsComplete")
			if soundName != None:
				SoundEffectSelect(soundName)

			ResultsWindow("Shotlog Pre-Flight Complete", resultStr)
		dlg.On.GoButton.Clicked = GoButtonFunc

		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.ShotlogPreFlightWin.Geometry")

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('ShotlogPreFlightWin', {
			Target {
				ID = 'ShotlogPreFlightWin',
			},
			Hotkeys {
				Target = 'ShotlogPreFlightWin',
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
		WindowPrefSave(dlg, "Lightfielder.ShotlogPreFlightWin.Geometry")


if __name__ == "__main__":
	print("[Lightfielder][Shotlog Pre-Flight] ")

	# This is a work-in-progress script
	ShotlogPreFlightWindow()
