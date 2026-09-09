"""
Lightfielder 17 Jupyter Link 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Connects the active Resolve Studio session with the Jupyter Notebook IDE using Python.

This allows Jupyter to read data live from the Resolve project, and remote-control any Resolve scripting API function.

The default Jupyter file is located at:
Scripts:/Utility/Lightfielder/Presets/Jupyter/Jupyter for Resolve Studio.ipynb

* * *

Calibration Import:
JSON Data format:
01 {'camera_distortion': [-0.09579707185891037, 0.12186457730848849, -0.00016405437197997908, 0.00015909545310126505, 0.0], 'camera_matrix': [[8194.856074831321, 0.0, 1638.4779942456462], [0.0, 8193.145360070946, 3067.10171049854], [0.0, 0.0, 1.0]], 'reproj_error': 0.036654092718717994}

Brown-Conrady model output:
k1	k2	p1	p2	k3

"""

import subprocess
import re
import csv, os, json, datetime, math
import platform
import sys

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

startTimer = datetime.datetime.now()

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

def CreateJupyterWindow():
	presetsBasePath = app.MapPath("Scripts:/Utility/Lightfielder/Presets/Jupyter/")

	res = app.GetResolve()

	# Get the project name
	project = GetProject()
	if project is None:
		print("[Lightfielder] No Resolve project is open at this time.")
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
			"ID": "JupyterWin",
			"TargetID" : "JupyterWin",
			"Geometry": [500, 50, 485, 566],
			"MinimumSize": [485, 566],
			"FixedSize": [485, 566],
			# "Spacing": 0,
			# "Margin": 5,
		},[
			ui.VGroup({
				"ID": "Content",
				"Weight": 0.1,
			},[
				ui.VGroup({
					"Weight": 0.01,
				},[
					ui.HGroup({
						"Weight": 0.5,
					},[
						ui.Label({
							"ID": "ViewLabel",
							"Text": "17  Jupyter Link",
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
						"Text": "Tip of the day: Before you use this script, make sure you have already installed Python and Jupyter Notebook.",
						"ReadOnly": True,
						"StyleSheet": "QTextEdit { border: 0px; }",
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
				},[
					ui.Label({
						"ID": "JupyterCalibrationLabel",
						"Text": "  Jupyter Notebook",
						"StyleSheet": "QLabel { color: white; font-weight: bold; font-size: 14px; }",
						"Weight": 0.01,
					}),
				]),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.Label({"ID": "PresetLabel", "Text": "Preset", "MinimumSize": [64, 32], "Weight": 0.01,}),
					ui.ComboBox({
						"ID": "PresetCombo",
						"Text": "Preset",
						"Weight": 1.0,
					}),
					ui.Button({"ID": "OpenJupyterButton", "Text": "Open Jupyter", "ToolTip": "Launch the Jupyter Notebook WebUI with the active notebook preset.","MinimumSize": [150, 32], "Weight": 0.1}),
				]),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.Label({"ID": "BrowserLabel", "Text": "Browser", "MinimumSize": [64, 32], "Weight": 0.01,}),
					ui.ComboBox({
						"ID": "BrowserCombo",
						"Text": "Browser",
						"MinimumSize": [272, 32],
						"Weight": 1.0,
					}),
				]),
				ui.HGroup({
					"Weight": 0.1,
				},[
					ui.Button({"ID": "ShowPresetsFolderButton", "Text": "Show Presets Folder", "ToolTip": "This button opens up the \"Preset\" folder location where the active \nJupyter notebooks are defined in a new desktop folder browsing \nwindow.", "MinimumSize": [135, 32], "Weight": 0.1}),
					ui.Button({"ID": "ShowOutputFolderButton", "Text": "Show Output Folder", "ToolTip": "This button opens up the output folder location in a desktop folder browsing window. \nThe output folder property is defined in the \"06 Still Frames Export\" scripts user interface.", "MinimumSize": [135, 32], "Weight": 0.1}),
				]),
				ui.VGroup({
					"Weight": 0.1,
					"ID": "ImportTab",
					"Spacing": 10,
				},[
					ui.Label({
						"ID": "DividerLabel",
						"StyleSheet": "QLabel { max-height: 1px; background-color: rgb(68, 68, 68); }",
						"Spacing": 0,
						"Margin": 0,
						"Weight": 0.01,
					}),
					ui.Label({
						"ID": "CalibrationJSONImportLabel",
						"Text": "  Calibration JSON Import",
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
					ui.VGroup({
						"Weight": 0.1,
						"ID": "ExportTab",
						"Spacing": 10,
					},[
						ui.HGroup({
							"Weight": 1.0,
						},[
							ui.Label({"ID": "ImportFileLabel", "Text": "Calibration File", "Weight": 0.1, "MinimumSize": [90, 32],}),
							ui.LineEdit({"ID": "ImportFileLineTxt", "Text": "", "PlaceholderText": "Please enter a JSON filename.", "Weight": 0.9}),
							ui.Button({"ID": "ImportBrowseFileButton", "Text": "Browse", "MinimumSize": [100, 32], "Weight": 0.1}),
						]),
						ui.HGroup({
							"Weight": 0.1
						},[
							ui.Button({
								"ID": "ImportCloseButton",
								"Text": "Cancel",
								"Weight": 0.5,
							}),
							ui.Button({
								"ID": "ImportJSONButton",
								"Text": "Import JSON...",
								"MinimumSize": [120, 32],
								"Weight": 0.5
							}),
						]),
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
							"ID": "MainCloseButton",
							"Text": "Close",
							"Weight": 0.5,
						}),
# 						ui.Button({
# 							"ID": "PrepareExportButton",
# 							"Text": "Prepare Export...",
# 							"MinimumSize": [120, 25],
# 							"Weight": 0.5,
# 						}),
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

		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
		progressLabel = itm["ProgressLabel"]

		# Add the items to the Presets ComboBox menu
		itm["PresetCombo"].AddItem("New Session...")
		for file in sorted(os.listdir(presetsBasePath)):
			if file.endswith(".ipynb") and not file.startswith("."):
				presetFile = file
				itm["PresetCombo"].AddItem(presetFile)
				# print(presetFile)

		# Web Browsers
		if platform.system() == "Darwin":
			itm["BrowserCombo"].AddItem("Safari")
		itm["BrowserCombo"].AddItem("Chrome")
		itm["BrowserCombo"].AddItem("Firefox")

		def PrefSave(winDlg):
			# Save the prefs
			if winDlg != None:
				print("[Lightfielder][Preferences] Saved")
				# app.SetData("Lightfielder.ExportFolder", itm["ExportFolderLineTxt"].Text)
				app.SetData("Lightfielder.Browser", itm["BrowserCombo"].Text)

		def PrefLoad(winDlg):
			# Restore the prefs
			if winDlg != None:
				print("[Lightfielder][Preferences] Loaded")
				# print(app.GetData("Lightfielder"))
				# Footage Folder
				#pref = app.GetData("Lightfielder.ExportFolder")
				# if pref != None:
					# print(pref)
					# itm["ExportFolderLineTxt"].Text = pref
				pref = app.GetData("Lightfielder.Browser")
				if pref != None:
					print(pref)
					itm["BrowserCombo"].Text = pref

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
			WindowPrefSave(dlg, "Lightfielder.JupyterWin.Geometry")

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			# Save the export folder pref
			PrefSave(dlg)
		dlg.On.JupyterWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.JupyterWin.Geometry")

			# Save the export folder pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.JupyterWin.Close = CloseFunc

		def MainCloseButtonFunc(ev):
			print("[Lightfielder][Window][Close Button]")

			# Toggle the Toolbar button to the unpressed (off) state
			UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(dlg, "Lightfielder.JupyterWin.Geometry")

			# Save the export folder pref
			PrefSave(dlg)

			# Reset the progress caption
			itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

			disp.ExitLoop()
		dlg.On.MainCloseButton.Clicked = MainCloseButtonFunc

		# Add your GUI element based event functions here:

		def ShowPresetsFolderButtonFunc(ev):
			print("[Lightfielder][Show Presets Folder]")
			# Jupyter Presets Location

			# Create the temporary folder
			if not os.path.exists(presetsBasePath):
				os.makedirs(presetsBasePath)
				print("[Lightfielder][Make Directory] ", presetsBasePath)

			app.Execute('bmd.openfileexternal("Open", [[' + str(presetsBasePath) + ']])')
		dlg.On.ShowPresetsFolderButton.Clicked = ShowPresetsFolderButtonFunc

		def BrowserComboFunc(ev):
			print("[Lightfielder][Preferences][Browser] " + str(itm["BrowserCombo"].CurrentText))
			app.SetData("Lightfielder.Browser", itm["BrowserCombo"].Text)
		dlg.On.BrowserCombo.CurrentIndexChanged = BrowserComboFunc

		def ShowOutputFolderButtonFunc(ev):
			pref = app.GetData("Lightfielder.ExportFolder")
			if pref != None:
				# print(pref)
				ShowFolderFromFilepath(pref)
		dlg.On.ShowOutputFolderButton.Clicked = ShowOutputFolderButtonFunc

		def OpenJupyterButtonFunc(ev):
			presetName = itm["PresetCombo"].CurrentText
			presetAbsPath = ""
			if presetName != "New Session...":
				presetAbsPath = '"' + str(presetsBasePath) + str(presetName) + '"'
			print("\t[Lightfielder][Jupyter Preset File] \"" + str(presetName) + "\"")

			# Choose a default web-browser to use for Jupyter sessions
			browser = itm["BrowserCombo"].CurrentText
			# browser = "Safari"
			#browser = "Chrome"
			#browser = "Firefox"
			if platform.system() == "Darwin":
				# Build the launching command
				# open -a "/Library/Frameworks/Python.framework/Versions/3.10/bin/jupyter-notebook" --args --browser=Safari &
				jupyterPath = GetPythonBinFilepath("jupyter-notebook")
				# jupyterPath = "/Library/Frameworks/Python.framework/Versions/3.10/bin/jupyter-notebook"

				# Start the Jupyter local service using a default web-browser
				browserStr = "--browser=" + str(browser)
				args = 'open -a "' + str(jupyterPath) + '" --args ' + str(browserStr) + ' ' + presetAbsPath + ' &'
				print("[Lightfielder][Launching Jupyter] " + str(args))
				result = os.system(args)
				print(result)
			elif platform.system() == "Linux":
				# Build the launching command
				jupyterPath = GetPythonBinFilepath("jupyter-notebook")
				# jupyterPath = "$HOME/.local/bin/jupyter-notebook"

				# Start the Jupyter local service using a default web-browser
				browserStr = "--browser=" + str(browser)
				#args = 'xdg-open "' + str(jupyterPath) + '" ' + str(browserStr) + ' ' + presetAbsPath + ' &'
				args = '"' + str(jupyterPath) + '" ' + str(browserStr) + ' ' + presetAbsPath + ' &'
				print("[Lightfielder][Launching Jupyter] " + str(args))
				result = os.system(args)
				print(result)
			else:
				# Build the launching command
				jupyterPath = GetPythonBinFilepath("jupyter-notebook")

				args = '"' + str(jupyterPath) + '" ' + str(browserStr) + ' ' + presetAbsPath + ' &'

				print("[Lightfielder][Launching Jupyter] " + str(args))
				result = os.system(args)
				print(result)

			#disp.ExitLoop()
		dlg.On.OpenJupyterButton.Clicked = OpenJupyterButtonFunc

		def ImportBrowseFileButtonFunc(ev):
			selectedPath = fu.RequestFile()
			if selectedPath:
				itm["ImportFileLineTxt"].Text = str(selectedPath)
		dlg.On.ImportBrowseFileButton.Clicked = ImportBrowseFileButtonFunc

		def ImportJSONButtonFunc(ev):
			selectedPath = itm["ImportFileLineTxt"].Text
			if selectedPath:
				data = GetJSON(selectedPath)
				#print(json.dumps(data, ensure_ascii = True, indent = "\t"))
				if data:
					resultStr = GenerateHTML(selectedPath, data)
					SaveReportLog(resultStr)
					ResultsWindow("Complete", resultStr)
				else:
					ErrorWindow("JSON Error", "There was a JSON file parsing error")
			else:
				ErrorWindow("JSON Error", "Please enter the filename of a JSON calibration document")
		dlg.On.ImportJSONButton.Clicked = ImportJSONButtonFunc

		def ImportCloseButtonFunc(ev):
			disp.ExitLoop()
		dlg.On.ImportCloseButton.Clicked = ImportCloseButtonFunc

		def HelpButtonFunc(ev):
			ShowHelpTopic("Docs/Scripts_17_Jupyter_Link.md")
		dlg.On.HelpButton.Clicked = HelpButtonFunc

		def ConsoleButtonFunc(ev):
			if itm["ConsoleButton"].Checked == True:
				app.DoAction("Console_Show", {"Show": True})
			else:
				app.DoAction("Console_Show", {"Show": False})
		dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

		def PrevScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Prev Item]")
			ProcessToolbarButton(ev, dlg, "Tool17", "Tool16")

			disp.ExitLoop()
		dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

		def NextScriptButtonFunc(ev):
			print("[Lightfielder][Toolbar][Show Next Item]")
			ProcessToolbarButton(ev, dlg, "Tool17", "Tool22")

			disp.ExitLoop()
		dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

		# Load the window preferences
		WindowPrefLoad(dlg, "Lightfielder.JupyterWin.Geometry")

		# Load the export folder pref
		PrefLoad(dlg)

		# Toggle the Toolbar button to the pressed (on) state
		UnpressToolbarButton(dlg.ID, True)

		# Add a close window hotkey event handler
		app.Execute(
		"""
		app:AddConfig('JupyterWin', {
			Target {
				ID = 'JupyterWin',
			},
			Hotkeys {
				Target = 'JupyterWin',
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
		WindowPrefSave(dlg, "Lightfielder.JupyterWin.Geometry")

		# Save the export folder pref
		PrefSave(dlg)

if __name__ == "__main__":
	CreateJupyterWindow()