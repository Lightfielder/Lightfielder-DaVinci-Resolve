"""
Lightfielder 11 Log Viewer.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Open the Lightfielder HTML logfiles for review

"""

import os
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

def CreateLogViewer():
	baseLogProjects = "Lightfielder:/Logs/Projects/"

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
		"ID": "LogViewerWin",
		"TargetID" : "LogViewerWin",
		"Geometry": [100, 100, 600, 615],
		"MinimumSize": [600, 615],
		"FixedSize": [600, 615],
		"Spacing": 10,
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
							"Text": "11 Log Viewer",
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
			ui.HGroup({
				"Weight": 0.01,
				"Spacing": 0,
			},[
				ui.Button({
					"ID": "ShowLogFileButton",
					"Flat": True,
					"MinimumSize": [112, 32],
					"Text": "HTML Log File",
					"ToolTip": GetTooltip("Show the HTML file","Clicking this text label will open the base folder where the HTML file is located in a desktop folder browsing window. \nShift-clicking the text label will open the file in a web browser. Command-clicking will open the file in a text editor."),
						
					"Weight": 0.01,
				}),
				ui.ComboBox({
					"Weight": 0.85,
					"ID": "LogFileCombo",
					"Text": "Log File"
				}),
			]),
			ui.TextEdit({
				"ID": "LogText",
				"Text": "Lightfielder Log File Contents",
				"PlaceholderText": "The log file content will be displayed here",
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
		WindowPrefSave(dlg, "Lightfielder.LogViewerWin.Geometry")
	dlg.On.LogViewerWin.Hide = HideFunc

	# The window was closed
	def CloseFunc(ev):
		print("[Lightfielder][Window][Closed]")

		# Toggle the Toolbar button to the unpressed (off) state

		UnpressToolbarButton(dlg.ID, False)
		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.LogViewerWin.Geometry")

		# Reset the progress caption
		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.LogViewerWin.Close = CloseFunc

	def CloseButtonFunc(ev):
		print("[Lightfielder][Window][Close Button]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.LogViewerWin.Geometry")

		# Save the export folder pref
		PrefSave(dlg)

		# Reset the progress caption
		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.CloseButton.Clicked = CloseButtonFunc

	def PrevScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Prev Item]")
		ProcessToolbarButton(ev, dlg, "Tool11", "Tool10")

		disp.ExitLoop()
	dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

	def NextScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Next Item]")
		ProcessToolbarButton(ev, dlg, "Tool11", "Tool12")

		disp.ExitLoop()
	dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

	# Add your GUI element based event functions here:

	def LogProjectAndFilename(file):
		if file is not None:
			# Trim an absolute filepath down to the log Project folder name and the logfilename
			parentFolderPath = os.path.dirname(app.MapPath(file))
			parentFolderBasename = os.path.basename(parentFolderPath)
			fileBasename = os.path.basename(file)
	
			folderAndFile = str(parentFolderBasename) + os.sep + str(fileBasename)
			# print("[Lightfielder][Project and Log] ", folderAndFile)
			return folderAndFile
		else:
			return ""

	def HelpButtonFunc(ev):
		ShowHelpTopic("Docs/Scripts_11_Log_Viewer.md")
	dlg.On.HelpButton.Clicked = HelpButtonFunc
	
	def RefreshButtonFunc(ev):
		# Refresh the LogFileCombo menu and the document view
		
		# Clear out the old LogFileCombo menu contents
		itm["LogFileCombo"].Clear()

		# Scan all the sub-folders inside the Logs/Project folder
		for file in GetHTMLFiles(app.MapPath(baseLogProjects)):
			# Keep the project folder name component
			logFile = LogProjectAndFilename(file)
			# Add the items to the ComboBox menu
			itm["LogFileCombo"].AddItem(logFile)
			# print("[Lightfielder][Log] ", logFile, "[Abs File]", file)
	dlg.On.RefreshButton.Clicked = RefreshButtonFunc

	def ShowLogFileButtonFunc(ev):
		buttonModifier = ev["modifiers"]["ShiftModifier"]
		buttonModifierControl = ev["modifiers"]["ControlModifier"]

		# Scan all sub-folders inside the "Lightfielder:/Logs/Project/" folder
		for file in GetHTMLFiles(app.MapPath(baseLogProjects)):
			if file.endswith(str(itm["LogFileCombo"].CurrentText)):
				# print("[Lightfielder][Log] ", file, "[Menu Item]", str(itm["LogFileCombo"].CurrentText))
		
				if buttonModifier == True:
					# shift was held down so open the OS default program for this filetype
					 ShowInDefaultProgram(file)
				elif buttonModifierControl == True:
					# Command/Control was held down so open the programmer's text editor
					ExternalEditor(file)
				else:
					# Label was clicked on with no modifier keys so open the containing folder in the operating system's folder browsing view
					ShowFolderFromFilepath(file)

				# Exit the for loop
				break
	dlg.On.ShowLogFileButton.Clicked = ShowLogFileButtonFunc

	def ConsoleButtonFunc(ev):
		if itm["ConsoleButton"].Checked == True:
			app.DoAction("Console_Show", {"Show": True})
		else:
			app.DoAction("Console_Show", {"Show": False})
	dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

	def LogFileComboFunc(ev):
		# A "Log File" menu item was selected
		# print("[Lightfielder][Log] ", itm["LogFileCombo"].CurrentText)

		# Scan all sub-folders inside the "Lightfielder:/Logs/Project/" folder
		for file in GetHTMLFiles(app.MapPath(baseLogProjects)):
			if file.endswith(str(itm["LogFileCombo"].CurrentText)):
				# print("[Lightfielder][Log] ", file, "[Menu Item]", str(itm["LogFileCombo"].CurrentText))

				f = open(file, "r")
				data = f.read()
				itm["LogText"].HTML = data
				# print(data)

				# Exit the for loop
				break
	dlg.On.LogFileCombo.CurrentIndexChanged = LogFileComboFunc

	# Add the items to the ComboBox menu
	for file in GetHTMLFiles(app.MapPath(baseLogProjects)):
		# Keep the project folder name component
		logFile = LogProjectAndFilename(file)
		itm["LogFileCombo"].AddItem(logFile)
		# print("[Lightfielder][Log] ", logFile)

	# Load the window preferences
	WindowPrefLoad(dlg, "Lightfielder.LogViewerWin.Geometry")

	# Toggle the Toolbar button to the pressed (on) state
	UnpressToolbarButton(dlg.ID, True)

	# Add a close window hotkey event handler
	app.Execute(
	"""
	app:AddConfig('LogViewerWin', {
		Target {
			ID = 'LogViewerWin',
		},
		Hotkeys {
			Target = 'LogViewerWin',
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
	WindowPrefSave(dlg, "Lightfielder.LogViewerWin.Geometry")

if __name__ == "__main__":
	CreateLogViewer()
