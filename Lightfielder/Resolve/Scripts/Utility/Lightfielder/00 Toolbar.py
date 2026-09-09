"""
Lightfielder 00 Toolbar.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

The Lightfielder Toolbar cuts down the effort needed to access the "Workspace > Scripts > Lightfielder > " menu items. It acts as a launcher interface for starting the Resolve based Python scripts.

Tip: Hold down the shift key when clicking on a toolbar item to force-reload the script. This is handy if you have edited the script and want to refresh the view to show the changes.

Tip: When the Toolbar window "X" close box is clicked, if the shift modifier key is held down at the same moment, the extra floating palette windows are force-closed at the same time, too. This makes it a quick task to de-clutter your workspace if you need to focus on something else.

Copyright:
Icons by Fork Awesome (https://forkaweso.me/Fork-Awesome/icons/) used under an SIL open-source font license.

Todo:
- position windows relative to the toolbar
- Use a global variable, or an app based preference, or UI manager based window moving to position function to place the floating view near the toolbar
- Refresh the state of the other toolbar buttons

"""

import platform
import sys, os

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

def CreateToolbarWindow():
	# Create a new UI Manager window
	toolbarUI = fu.UIManager
	toolbarDisp = bmd.UIDispatcher(toolbarUI)

	# Should this window float above all other views
	windowFloat = True
	# The toolbar right now should stay always floating and we will apply this to all other script views.
	#windowFloat = app.GetData("Lightfielder.WindowStaysOnTop")
	#if windowFloat is None:
	#	windowFloat = True

	def GetWindow(tool):
		return toolbarUI.FindWindow(tool)

	def InitButtonState():
		# Look for clicked buttons
		toolItems = GetTools()
		for t in toolItems:
			winName = GetWindowIDFromToolNum(t)
			winItm = GetWindow(winName)
			#if winItm != None:
			#	print("[Lightfielder][Toolbar][Button][" + str(winName) + "]", winItm)
			# Toggle the button On/Off state for the active toolbar items
			if winItm != None:
				toolbarItm[t].Checked = True
				#print("[Lightfielder][Toolbar][Button][" + str(winName) + "] Window Active")
			elif winItm == None or winItm == "":
				toolbarItm[t].Checked = False
				#print("[Lightfielder][Toolbar][Button][" + str(winName) + "] Window Inactive")

	# Force close any previously open Toolbar windows
	winName = "ToolbarWin"
	winItm = GetWindow(winName)
	if winItm != None or winItm == "":
		winItm.Show()
		winItm.Raise()
		winItm.ActivateWindow()
		winGeo = GetWindowGeometry(winName)
		print("[Lightfielder][Toolbar][Raise Window] " + str(winName) + "\t[Geo] " + str(winGeo))
	else:
		# Lightfielder Icons Folder
		iconFolderPathMap = "Scripts:/Utility/Lightfielder/Icons/Toolbar/"
		iconMinimumSize = [46, 32]

		# Create the new window
		toolbarDlg = toolbarDisp.AddWindow({
			"WindowTitle": LFGetVersion("Lightfielder Toolbar v"),
			"WindowFlags": {"Window": True, "WindowStaysOnTopHint": windowFloat},
			"ID": "ToolbarWin",
			"TargetID" : "ToolbarWin",
			"Geometry": [10, 110, 580, 90],
			"MinimumSize": [580, 90],
			"FixedSize": [580, 90],
			# "Spacing": 0,
			# "Margin": 0,
		},[
			toolbarUI.VGroup({
			},[
				# Add your GUI elements here:
				toolbarUI.HGroup({
					"Weight": 1.0,
				},[
					toolbarUI.Button({
						"ID": "Tool1",
						"Text": " 01",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool1")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool1"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool2",
						"Text": " 02",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool2")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool2"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool3",
						"Text": " 03",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool3")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool3"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool4",
						"Text": " 04",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool4")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool4"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool5",
						"Text": " 05",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool5")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool5"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool6",
						"Text": " 06",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool6")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool6"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool7",
						"Text": " 07",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool7")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool7"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool8",
						"Text": " 08",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool8")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool8"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool9",
						"Text": " 09",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool9")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool9"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool10",
						"Text": " 10",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool10")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool10"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool11",
						"Text": " 11",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool11")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool11"))}),
						"Weight": 0.01
					})
				]),
				toolbarUI.HGroup({
					"Weight": 1.0,
				},[
					toolbarUI.Button({
						"ID": "Tool12",
						"Text": " 12",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool12")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool12"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool13",
						"Text": " 13",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool13")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool13"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool14",
						"Text": " 14",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool14")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool14"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool15",
						"Text": " 15",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool15")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool15"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool16",
						"Text": " 16",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool16")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool16"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool17",
						"Text": " 17",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool17")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool17"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool18",
						"Text": " 18",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool18")),
						"MinimumSize": iconMinimumSize,
						"Checkable": False,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool18"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool19",
						"Text": " 19",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool19")),
						"MinimumSize": iconMinimumSize,
						"Checkable": False,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool19"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool20",
						"Text": " 20",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool20")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool20"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool21",
						"Text": " 21",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool21")),
						"MinimumSize": iconMinimumSize,
						"Checkable": False,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool21"))}),
						"Weight": 0.01
					}),
					toolbarUI.Button({
						"ID": "Tool22",
						"Text": " 22",
						"ToolTip": str(GetWindowTitleFromToolNum("Tool22")),
						"MinimumSize": iconMinimumSize,
						"Checkable": True,
						"Icon": toolbarUI.Icon({"File": str(iconFolderPathMap) + str(GetIconFromToolNum("Tool22"))}),
						"Weight": 0.01
					})
				]),
			])
		])

		toolbarItm = toolbarDlg.GetItems()

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

		# The window was hidden
		def HideFunc(ev):
			infoWinName = "ToolbarWin"
			infoWinGeo = GetWindowGeometry(infoWinName)
	
			print("[Lightfielder][Toolbar][Hiding Window]\t[Geo] " + str(infoWinGeo))
			# Toggle the Toolbar button to the unpressed (off) state
			# UnpressToolbarButton(dlg.ID, False)

			# Save the window preferences
			WindowPrefSave(toolbarDlg, "Lightfielder.ToolbarWin.Geometry")
		toolbarDlg.On.ToolbarWin.Hide = HideFunc

		# The window was closed
		def CloseFunc(ev):
			print("[Lightfielder][Window][Closed]")

			# Save the window preferences
			WindowPrefSave(toolbarDlg, "Lightfielder.ToolbarWin.Geometry")

			# When the Toolbar window "X" close box is clicked, if the shift modifier key is held down at the same moment, then force-close all the extra floating palette windows at the same time, too.
			buttonModifier = ev["modifiers"]["ShiftModifier"]
			if buttonModifier == True:
				toolItems = GetTools()
				for t in toolItems:
					winName = GetWindowIDFromToolNum(t)
					winItm = GetWindow(winName)
					infoWinGeo = GetWindowGeometry(tool)
					print("[Lightfielder][Toolbar][Closing Window] All\t[Modifiers] Detected Shift Key\t[Geo] " + str(infoWinGeo))
					if winItm != None and winItm != "":
						# print("[Lightfielder][Toolbar][Button][" + str(winName) + "]", winItm)
						# print("[Lightfielder][Toolbar][Button][" + str(winName) + "] Window Inactive")

						# Toggle the button Off state for the active toolbar items
						toolbarItm[t].Checked = False

						# Save the window preferences
						WindowPrefSave(winItm, "Lightfielder." + str(winName) + " .Geometry")
						winItm.Close()

						# Quit the current Resolve session
						app.Quit()
			else:
				infoWinName = "ToolbarWin"
				infoWinGeo = GetWindowGeometry(infoWinName)
				print("[Lightfielder][Toolbar][Closing Window]\t[Geo] " + str(infoWinGeo))
				# print(ev["modifiers"])

			toolbarDisp.ExitLoop()
		toolbarDlg.On.ToolbarWin.Close = CloseFunc

		# Add your GUI element based event functions here:
		def ToolFunc(ev):
			buttonName = ev["who"]
			# buttonState = ev["On"]
			buttonModifier = ev["modifiers"]["ShiftModifier"]
			buttonModifierControl = ev["modifiers"]["ControlModifier"]
			# buttonModifierControl = ev["modifiers"]["AltModifier"]

			# Look up the script name
			selectedScript = app.MapPath(GetToolScript(buttonName))

			# Run the Python script if the window is not already open
			winName = GetWindowIDFromToolNum(buttonName)
			winItm = GetWindow(winName)
			infoWinGeo = GetWindowGeometry(winName)
			if winName == "Docs":
				if buttonModifierControl == True:
					# Hold down the control key when clicking on a toolbar item to edit the script in a programmer's text editor
					# This feature requires the "xdg-open" package to be installed on Linux.
					print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Edit this Window] " + str(winName) + " \t[Script Edit] " + str(selectedScript) + "\t[Geo] " + str(infoWinGeo))
					ExternalEditor(selectedScript)
				else:
					print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Run the Script] " + str(selectedScript) + "\t[Geo] " + str(infoWinGeo))
					execfile(selectedScript)
			elif winName == "Console":
				print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "]")
				app.DoAction("Console_Show")
# 					if toolbarItm[buttonName].Checked != False:
# 						# Checked - Show the Console window
# 						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "]")
# 						app.DoAction("Console_Show", {"show" : True})
# 					elif toolbarItm[buttonName].Checked == False:
# 						# Unchecked - Hide the Console window
# 						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "]")
# 						app.DoAction("Console_Show", {"show" : False})
			elif toolbarItm[buttonName].Checked != False:
				# The button was just checked so show the window or run the script
				if winItm == None or winItm == "":
					if buttonModifierControl == True:
						# Hold down the control key when clicking on a toolbar item to edit the script in a programmer's text editor
						# This feature requires the "xdg-open" package to be installed on Linux.
						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Edit this Window] " + str(winName) + "\t[Script Edit] " + str(selectedScript) + "\t[Geo] " + str(infoWinGeo))
						ExternalEditor(selectedScript)
					else:
						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Run the Script] " + str(selectedScript) + "\t[Geo] " + str(infoWinGeo))
						execfile(selectedScript)
				elif winItm != None:
					if buttonModifier == False and buttonModifierControl == False:
						# Save the window preferences
						WindowPrefSave(winItm, "Lightfielder." + str(winName) + " .Geometry")
						winItm.Show()
						winItm.Raise()
						winItm.ActivateWindow()
						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Show Window] " + str(winName) + "\t[Geo] " + str(infoWinGeo))
					elif buttonModifierControl == True:
						# Hold down the control key when clicking on a toolbar item to edit the script in a programmer's text editor
						# This feature requires the "xdg-open" package to be installed on Linux.
						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Edit this Window] " + str(winName) + "\t[Script Edit] " + str(selectedScript)  + "\t[Geo] " + str(infoWinGeo))
						ExternalEditor(selectedScript)
					else:
						# Hold down the shift key when clicking on a toolbar item to force-reload the script
						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Reload Window] " + str(winName) + "\t[Script] " + str(selectedScript) + "\t[Geo] " + str(infoWinGeo))
						# Save the window preferences
						WindowPrefSave(winItm, "Lightfielder." + str(winName) + " .Geometry")
						winItm.Close()
						execfile(selectedScript)
			elif toolbarItm[buttonName].Checked == False:
				# If the button is unchecked then hide the window if the window is open
				if winItm != None:
					if buttonModifier == False and buttonModifierControl == False:
						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Hide Window] " + str(winName) + "\t[Geo] " + str(infoWinGeo))
						# Save the window preferences
						WindowPrefSave(winItm, "Lightfielder." + str(winName) + " .Geometry")
						winItm.Hide()
					elif buttonModifierControl == True:
						# Hold down the control key when clicking on a toolbar item to edit the script in a programmer's text editor
						# This feature requires the "xdg-open" package to be installed on Linux.
						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "][Edit this Window] " + str(winName) + "\t[Script Edit] " + str(selectedScript) + "\t[Geo] " + str(infoWinGeo))
						ExternalEditor(selectedScript)
					else:
						# If the button is unchecked hold down the shift key to force-close the window if the window is open
						print("[Lightfielder][Toolbar][Button][" + str(buttonName) + "] [Close Window] " + str(winName)  + "\t[Geo] " + str(infoWinGeo))
						# Save the window preferences
						WindowPrefSave(winItm, "Lightfielder." + str(winName) + " .Geometry")
						winItm.Close()
			# Todo: Refresh the state of the other toolbar buttons

		toolbarDlg.On.Tool1.Clicked = ToolFunc
		toolbarDlg.On.Tool2.Clicked = ToolFunc
		toolbarDlg.On.Tool3.Clicked = ToolFunc
		toolbarDlg.On.Tool4.Clicked = ToolFunc
		toolbarDlg.On.Tool5.Clicked = ToolFunc
		toolbarDlg.On.Tool6.Clicked = ToolFunc
		toolbarDlg.On.Tool7.Clicked = ToolFunc
		toolbarDlg.On.Tool8.Clicked = ToolFunc
		toolbarDlg.On.Tool9.Clicked = ToolFunc
		toolbarDlg.On.Tool10.Clicked = ToolFunc
		toolbarDlg.On.Tool11.Clicked = ToolFunc
		toolbarDlg.On.Tool12.Clicked = ToolFunc
		toolbarDlg.On.Tool13.Clicked = ToolFunc
		toolbarDlg.On.Tool14.Clicked = ToolFunc
		toolbarDlg.On.Tool15.Clicked = ToolFunc
		toolbarDlg.On.Tool16.Clicked = ToolFunc
		toolbarDlg.On.Tool17.Clicked = ToolFunc
		toolbarDlg.On.Tool18.Clicked = ToolFunc
		toolbarDlg.On.Tool19.Clicked = ToolFunc
		toolbarDlg.On.Tool20.Clicked = ToolFunc
		toolbarDlg.On.Tool21.Clicked = ToolFunc
		toolbarDlg.On.Tool22.Clicked = ToolFunc

		# Toggle the button On/Off state for the active toolbar items
		InitButtonState()

		# Load the window preferences
		WindowPrefLoad(toolbarDlg, "Lightfielder.ToolbarWin.Geometry")

		# Refresh the window layout
		dlg:RecalcLayout()

		# Add a close window hotkey event handler
# 		app.Execute(
# 		"""
# 		app:AddConfig('ToolbarWin', {
# 			Target {
# 				ID = 'ToolbarWin',
# 			},
# 			Hotkeys {
# 				Target = 'ToolbarWin',
# 				Defaults = true,
# 
# 				CONTROL_W = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
# 				CONTROL_F4 = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
# 			},
# 		})
# 		""")

		toolbarDlg.Show()
		
		infoWinName = "ToolbarWin"
		infoWinGeo = GetWindowGeometry(infoWinName)
		print("[Lightfielder][Toolbar][Create Window] " + str(infoWinName) + "\t\t[Geo] " + str(infoWinGeo))

		toolbarDisp.RunLoop()
		toolbarDlg.Hide()

		# Save the window preferences
		WindowPrefSave(toolbarDlg, "Lightfielder.ToolbarWin.Geometry")

def execfile(filepath, globals = None, locals = None):
	try:
		app.RunScript(filepath)
	except SystemExit:
		print("[Lightfielder][Toolbar][Exception] A Python \"System Exit\" exception was called")

if __name__ == "__main__":
	CreateToolbarWindow()
	print("[Lightfielder][Toolbar][Done]")
