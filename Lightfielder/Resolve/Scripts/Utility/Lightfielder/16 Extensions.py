"""
Lightfielder 16 Extensions.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Extensions allow 3rd party Python based plugins to extend the Lightfielder ecosystem.

The individual .py scripts are stored in the folder path:
Scripts:/Support/Lightfielder_Extensions/

Todo
- This is a work-in-progress script

"""

import platform
import sys, os

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

# Look for Extension python modules
ext_path = app.MapPath("Scripts:/Support/Lightfielder_Extensions/")
if not os.path.exists(ext_path):
	os.makedirs(ext_path)
if ext_path not in sys.path:
	sys.path.append(ext_path)
	# print(sys.path)

def CreateExtensions():
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
		"ID": "ExtensionsWin",
		"TargetID" : "ExtensionsWin",
		"Geometry": [500, 50, 745, 640],
		"MinimumSize": [745, 640],
		"FixedSize": [745, 640],
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
							"Text": "16 Extensions",
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
						"ID": "ExtendTxt",
						"Text": "Tip of the day: Extensions allow 3rd party Python based plugins to extend the Lightfielder ecosystem.",
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
				ui.HGroup({
					"Weight": 0.5,
				},[
					ui.Tree({
						"ID": "Tree",
						"SortingEnabled": True,
						"SelectionMode": "ExtendedSelection",
						"Weight": 1.0,
						"Events": {
							"CurrentItemChanged": True,
							"ItemChanged": True,
							"ItemActivated": True,
							"ItemClicked": True,
							"ItemDoubleClicked": True,
						},
						"MinimumSize": [100, 100],
					}),
				]),
			ui.TextEdit({
				"Weight": 1.0,
				"ID": "ExtText",
				"Text": "Lightfielder Extension Info",
				"PlaceholderText": "The extension details will be displayed here",
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
				"Weight": 0.01,
			},[
				ui.Button({
					"ID": "CloseButton",
					"Text": "Close",
					"Weight": 0.5,
				}),
				ui.Button({
					"ID": "SaveButton",
					"Text": "Save",
					"MinimumSize": [120, 32],
					"Weight": 0.5
				}),
				ui.Button({
					"ID": "PrevScriptButton",
					"Text": "<",
					"ToolTip": GetTooltip("Show the previous script.", "Open the previous script from the Lightfielder Toolbar"),
					"MinimumSize": [32, 32],
					"Weight": 0.01
				}),
				ui.Button({
					"ID": "NextScriptButton",
					"Text": ">",
					"ToolTip": GetTooltip("Show the next script.", "Open the next script from the Lightfielder Toolbar"),
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
			RefreshTree()

	# The window was hidden
	def HideFunc(ev):
		print("[Lightfielder][Window][Hidden]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.ExtensionsWin.Geometry")
	dlg.On.ExtensionsWin.Hide = HideFunc

	# The window was closed
	def CloseFunc(ev):
		print("[Lightfielder][Window][Closed]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.ExtensionsWin.Geometry")

		# Reset the progress caption
		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.ExtensionsWin.Close = CloseFunc

	def CloseButtonFunc(ev):
		print("[Lightfielder][Window][Close Button]")

		# Toggle the Toolbar button to the unpressed (off) state
		UnpressToolbarButton(dlg.ID, False)

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.ExtensionsWin.Geometry")

		# Save the export folder pref
		PrefSave(dlg)

		# Reset the progress caption
		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"

		disp.ExitLoop()
	dlg.On.CloseButton.Clicked = CloseButtonFunc

	def SaveButtonFunc(ev):
		# startTimer = datetime.datetime.now()
		# startTimeStamp = datetime.datetime.now().strftime("%B %d %Y @ %H:%M:%S")
		print("[Lightfielder][Preferences][Save Button]")

		# Save the window preferences
		WindowPrefSave(dlg, "Lightfielder.ExtensionsWin.Geometry")

		# Save the pref
		PrefSave(dlg)

		# itm["ProgressLabel"].Text = "  Progress: Saved Preferences [Wallclock " + GetTimeElapsed(startTimer) + "]"

		# Reset the progress caption
		itm["ProgressLabel"].Text = "  Progress: Awaiting User Input"
	dlg.On.SaveButton.Clicked = SaveButtonFunc

	def PrevScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Prev Item]")
		ProcessToolbarButton(ev, dlg, "Tool16", "Tool15")

		disp.ExitLoop()
	dlg.On.PrevScriptButton.Clicked = PrevScriptButtonFunc

	def NextScriptButtonFunc(ev):
		print("[Lightfielder][Toolbar][Show Next Item]")
		ProcessToolbarButton(ev, dlg, "Tool16", "Tool17")

		disp.ExitLoop()
	dlg.On.NextScriptButton.Clicked = NextScriptButtonFunc

	# Add your GUI element based event functions here:
	def HelpButtonFunc(ev):
		ShowHelpTopic("Docs/Scripts_16_Extensions.md")
	dlg.On.HelpButton.Clicked = HelpButtonFunc

	# Add a header row
	hdr = itm["Tree"].NewItem()
	hdr.Text[0] = "State"
	hdr.Text[1] = "Python Script"

	itm["Tree"].SetHeaderItem(hdr)

	# Number of columns in the Tree list
	itm["Tree"].ColumnCount = 2

	# Resize the Columns
	itm["Tree"].ColumnWidth[0] = 60
	itm["Tree"].ColumnWidth[1] = 380

	# Change the sorting order of the tree
	#itm["Tree"].SortByColumn(0, "DescendingOrder")
	itm["Tree"].SortByColumn(0, "AscendingOrder")

	def RefreshTree():
		print("[Lightfielder] Rebuilding the Extension Tree")
		# Remove the old tree entries
		itm["Tree"].Clear()

		# Add the items to the ComboBox menu
		for f in GetPyFiles(app.MapPath(ext_path)):
			# Fill the tree row
			itRow = itm["Tree"].NewItem()
			itRow.Text[0] = ""
			itRow.Text[1] = os.path.basename(f)
			print(f)

			# Toggle the checked state of the new row item
			itRow.CheckState[0] = "Checked"
			# itRow.CheckState[0] = "Unchecked"

			# Row color
			for c in range(int(itm["Tree"].ColumnCount)):
				itRow.TextColor[c] = GetColor("White")
				# itRow.BackgroundColor[c] = GetColor("Blue")
				# itRow.BackgroundColor[c] = GetColor("Brown")
				# itRow.BackgroundColor[c] = GetColor("Violet")
				# itRow.BackgroundColor[c] = GetColor("Green")

			# Add the item
			itm["Tree"].AddTopLevelItem(itRow)

	# The Tree view row was clicked on
	def TreeClickedFunc(ev):
		if ev["item"]:
			if ev["column"] >= 1:
				for f in GetPyFiles(app.MapPath(ext_path)):
					if ev["item"].Text[1] == os.path.basename(f):
						print("[Lightfielder][Extension Script] ", f)
						fp = open(f, "r")
						data = fp.read()
						itm["ExtText"].PlainText = data
	dlg.On.Tree.ItemClicked = TreeClickedFunc

	# Load the window preferences
	WindowPrefLoad(dlg, "Lightfielder.ExtViewerWin.Geometry")

	# Toggle the Toolbar button to the pressed (on) state
	UnpressToolbarButton(dlg.ID, True)

	# Add a close window hotkey event handler
	app.Execute(
	"""
	app:AddConfig('ExtensionsWin', {
		Target {
			ID = 'ExtensionsWin',
		},
		Hotkeys {
			Target = 'ExtensionsWin',
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
	WindowPrefSave(dlg, "Lightfielder.ExtViewerWin.Geometry")


if __name__ == "__main__":
	print("[Lightfielder][Extensions] ")
	# This is a work-in-progress script
	CreateExtensions()
