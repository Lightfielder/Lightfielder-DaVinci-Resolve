"""
Lightfielder 22 About Lightfielder.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Shows an about dialog with details about the toolset:

Lightfielder is a multi-view workflow automation toolset that streamlines the creation of volumetric experiences inside of tools like BMD DaVinci Resolve Studio. It is designed to help video editors and colorists be more productive as they work with planar and polar grid array filmed multi-view content. 

The Python scripted tools help automate common tasks that can be tedious and time consuming to carry out manually. This makes creative tasks run smoothly when processing stacks of footage from large camera arrays.

"""

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

def CreateAboutWindow():
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
		"ID": "AboutWin",
		"TargetID" : "AboutWin",
		"Geometry": [500, 50, 600, 410],
		"MinimumSize": [600, 410],
		"FixedSize": [600, 410],
		# "Spacing": 0,
		# "Margin": 5,
	},[
		ui.VGroup({
			"ID": "Content",
			"Weight": 0.1,
		},[
			ui.HGroup({
				"Weight": 0.01,
			},[
				ui.Label({
					"ID": "ViewLabel",
					"Text": "22  About Lightfielder",
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
			ui.Label({
				"ID": "LFLabel",
				"Text": "Lightfielder for DaVinci Resolve",
				"StyleSheet": "QLabel {font-weight: bold; font-size: 36px; }",
				"Alignment": {"AlignHCenter": True,},
				"WordWrap": True,
				"Margin": 0,
				"Spacing": 0,
				"Weight": 0.01,
			}),
			ui.Label({
				"ID": "VersionLabel",
				"Text":  LFGetVersion("Version "),
				"StyleSheet": "QLabel {font-weight: bold; font-size: 12px; }",
				"Alignment": {"AlignHCenter": True,},
				"WordWrap": True,
				"Margin": 0,
				"Spacing": 0,
				"Weight": 0.01,
			}),
			ui.Label({
				"ID": "EditionLabel",
				"Text": "Jaguarshark Edition",
				"StyleSheet": "QLabel {font-weight: bold; font-size: 12px; color: rgb(76, 154, 109);}",
				"Alignment": {"AlignHCenter": True,},
				"WordWrap": True,
				"Margin": 0,
				"Spacing": 0,
				"Weight": 0.01,
			}),
			ui.TextEdit({
				"ID": "ExportTxt",
				"Text": """Lightfielder is a multi-view workflow automation toolset that streamlines the creation of volumetric experiences inside of tools like BMD DaVinci Resolve Studio. It is designed to help video editors and colorists be more productive as they work with planar and polar grid array filmed multi-view content. 

The Python scripted tools help automate common tasks that can be tedious and time consuming to carry out manually. This makes creative tasks run smoothly when processing stacks of footage from large camera arrays.""",
				"ReadOnly": True,
				"StyleSheet": "QTextEdit { border: 0px; }",
				"Weight": 2.0,
			}),
			ui.Label({
				"ID": "URLLabel",
				"Text": """Copyright © 2022-""" + str(datetime.datetime.now().year) + """ Lightfielder<br><a href="https://github.com/Lightfielder" style="color: rgb(139,155,216)">https://github.com/Lightfielder</a>""",
				"StyleSheet": "QLabel {font-weight: bold; font-size: 12px; }",
				"Alignment": {"AlignHCenter": True,},
				"WordWrap": True,
				"OpenExternalLinks": True,
				"Margin": 0,
				"Spacing": 0,
				"Weight": 0.01,
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
				ui.Button({
					"ID": "MainCloseButton",
					"Text": "Close",
					"Weight": 0.5,
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
		WindowPrefSave(dlg, "Lightfielder.AboutWin.Geometry")

		# Reset the progress caption
		# itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		# Save the export folder pref
		PrefSave(dlg)
	dlg.On.AboutWin.Hide = HideFunc

	# The window was closed
	def CloseFunc(ev):
		print("[Lightfielder][Window][Closed]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.AboutWin.Geometry")

		# Save the export folder pref
		PrefSave(dlg)

		disp.ExitLoop()
	dlg.On.AboutWin.Close = CloseFunc

	def MainCloseButtonFunc(ev):
		print("[Lightfielder][Window][Close Button]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.AboutWin.Geometry")

		# Save the export folder pref
		PrefSave(dlg)

		disp.ExitLoop()
	dlg.On.MainCloseButton.Clicked = MainCloseButtonFunc

	# Add your GUI element based event functions here:

	def HelpButtonFunc(ev):
		ShowHelpTopic("Docs/Scripts_22_About_Lightfielder.md")
	dlg.On.HelpButton.Clicked = HelpButtonFunc

	def ConsoleButtonFunc(ev):
		if itm["ConsoleButton"].Checked == True:
			app.DoAction("Console_Show", {"Show": True})
		else:
			app.DoAction("Console_Show", {"Show": False})
	dlg.On.ConsoleButton.Clicked = ConsoleButtonFunc

	def PrevScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Prev Item]")
		ProcessToolbarButton(ev, dlg, "Tool22", "Tool17")

		disp.ExitLoop()
	dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

	def NextScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Next Item]")
		ProcessToolbarButton(ev, dlg, "Tool22", "Tool1")

		disp.ExitLoop()
	dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

	# Load the window preferences
	WindowPrefLoad(dlg, "Lightfielder.AboutWin.Geometry")

	# Load the export folder pref
	PrefLoad(dlg)

	# Toggle the Toolbar button to the pressed (on) state
	UnpressToolbarButton(dlg.ID, True)

	# Add a close window hotkey event handler
	app.Execute(
	"""
	app:AddConfig('AboutWin', {
		Target {
			ID = 'AboutWin',
		},
		Hotkeys {
			Target = 'AboutWin',
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
	WindowPrefSave(dlg, "Lightfielder.AboutWin.Geometry")

	# Save the export folder pref
	PrefSave(dlg)

if __name__ == "__main__":
	CreateAboutWindow()
