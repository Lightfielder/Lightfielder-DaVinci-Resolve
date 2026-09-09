"""
Lightfielder 15 EDL Export.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Prepares a new Delivery page render job for "Individual Clip" mode based output.

Note: This is a work-in-progress script

Script Usage:
1. Open Resolve. Select the menu item: "Workspace > Scripts > Lightfielder > 15 EDL Export"

2. Choose the settings you would like to use.

3. Click the "Prepare Export..." button to continue.

Todo:
- uiTree list to allow multiple timeline selection
- Allow On/Off timeline selection
- Allow per-entry output location data entry
- Allow saving this queue list info to a .json file that can be used to rebuild a cloud render preset list

- Deliver - Trigger script at end of render - use a python script to add the rendered footage into the "01_Delivery/Calibration" folder.

"""

import subprocess
import re
import os, json, datetime, math
import platform
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

def SaveReportEDLExportLog(htmlDocument):
	# Get the project name
	project = GetProject()
	projectName = project.GetName()
	projectNameNoSpaces = str(projectName.replace(" ", "_"))
	timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H.%M.%S.%f")

	logFolderRel = "Lightfielder:/Logs/Projects/" + str(projectNameNoSpaces) + "/"
	logFolderAbs = app.MapPath(logFolderRel)

	logFileRel = str(logFolderRel) + str(timeStamp) + "_EDL_Export.html"
	logFileAbs = app.MapPath(logFileRel)

	# Create the intermediate directories on disk
	if not os.path.exists(logFolderAbs):
		try:
			# Make the dir
			os.makedirs(logFolderAbs)
			print("[Lightfielder][Report][Make Directory]", logFolderAbs)
		except OSError as error:
			print("[Lightfielder][Report][Make Directory Error]", error)
			return

	# Write to report log file
	f = open(logFileAbs, "a")
	if f is None:
		print("[Lightfielder][Report][Write Error] ", logFileAbs)
	else:
		print("[Lightfielder][Report][Write File] ", logFileAbs)
		f.write(htmlDocument)
		f.close()

def GenerateHTML(filePath, data):
	message = "\t\t<p>JSON File: " + str(filePath) + "</p><br>\n"
	message += "\t\t<table border=\"0\" color=\"#CDCDCD\" bgcolor=\"#1F1F1F\" cellpadding=\"2\">\n"
	message += "\t\t\t<tr><td>Camera</td><td>k1</td><td>k2</td><td>p1</td><td>p2</td><td>k3</td></tr>\n"

	try:
		for key, value in data.items():
			cameraNum = int(key)
			params = value

			#print(key, "\n\t", value)
			print("[" + str(cameraNum) + "]")

			k1, k2, p1, p2, k3 = params["camera_distortion"]
			matrix = params["camera_matrix"]
			reproj = params["reproj_error"]

			message += "\t\t\t<tr><td>" + str(cameraNum) + "</td><td>" + str(k1) + "</td><td>" + str(k2) + "</td><td>" + str(p1) + "</td><td>" + str(p2) + "</td><td>" + str(k3) + "</td></tr>\n"
	except StopIteration:
		pass

	message += "\t\t</table>\n"

	# Combine the HTML content
	css = """
		<style type="text/css">
			body {font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:12px; font-weight:400; font-style:normal; background-color: #2D2D2D; color: #9D9D9D;}
			h1 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:xx-large; font-weight:600;}
			h2 {color: #9D9D9D; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;  font-size:x-large; font-weight:400;}
			p, table, th, td {color: #9D9D9D; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;}
			a {text-decoration: underline; color:#8b9bd8;}
			p, li {white-space: pre-wrap;}
			hr {max-height: 3px; background-color: rgb(76, 154, 109); color: rgb(76, 154, 109);}
		</style>
"""
	htmlHeaderTxt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html>\n\t<head>\n\t\t<title>' + str("Calibration Report") + '</title>\n' + str(css) + '\t</head>\n\t<body>\n\t\t<h1>Calibration Report</h1>\n<hr/>\n'
	htmlFooterTxt = '\t</body>\n</html>\n'
	htmlDocument = str(htmlHeaderTxt) + str(message) + str(htmlFooterTxt)
	# print(htmlDocument)
	return htmlDocument

def CreateEDLExportWindow():
	presetsBasePath = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Calibration/")

	# Get the project name
	res = app.GetResolve()
	project = GetProject()
	if project is None:
		print("[Lightfielder] Please open a Resolve timeline before running this script.")
		ErrorWindow("Lightfielder", "Please open a Resolve timeline before running this script.")
		exit()
	else:
		projectName = project.GetName()

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
			"ID": "EDLExportWin",
			"TargetID" : "EDLExportWin",
			"Geometry": [500, 50, 630, 232],
			"MinimumSize": [630, 232],
			"FixedSize": [630, 232],
			#"Spacing": 0,
			#"Margin": 5,
		},[
			ui.VGroup({
				"ID": "Content",
				"Weight": 1.0,
			},[
				ui.HGroup({
					"Weight": 0.5,
				},[
					ui.Label({
						"ID": "ViewLabel",
						"Text": "15 EDL Export",
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
					"ID": "ExportTxt",
					"Text": "This dialog is the future home of an interface for quickly exporting EDL files.",
					"ReadOnly": True,
					"StyleSheet": "QTextEdit { border: 0px; }",
					"Weight": 1.0,
				}),
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
			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
		
			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.EDLExportWin.Geometry")
		dlg.On.EDLExportWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.EDLExportWin.Geometry")

			disp.ExitLoop()
		dlg.On.EDLExportWin.Close = CloseFunc
	
		def CloseButtonFunc(ev):
			print("[Lightfielder][Window][Close Button]")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
	
			disp.ExitLoop()
		dlg.On.CloseButton.Clicked = CloseButtonFunc
		
		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool15", "Tool14")
	
			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc
	
		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool15", "Tool16")
	
			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		# Add your GUI element based event functions here:

		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_15_EDL_Export.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		def GoButtonFunc(ev):
			print("[Lightfielder][EDL Export] Go Button")
			itm["ProgressLabel"].Text = "  Progress: (WIP) Preparing timeline export..."

			# Play the sound effect
			soundName = app.GetData("Lightfielder.SoundEffectsComplete")
			# soundName = app.GetData("Lightfielder.SoundEffectsError")
			if soundName != None:
				SoundEffectSelect(soundName)
		dlg.On.GoButton.Clicked = GoButtonFunc

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.EDLExportWin.Geometry")

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('EDLExportWin', {
			Target {
				ID = 'EDLExportWin',
			},
			Hotkeys {
				Target = 'EDLExportWin',
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
		WindowPrefSave(dlg, "Lightfielder.EDLExportWin.Geometry")

if __name__ == "__main__":
	CreateEDLExportWindow()
