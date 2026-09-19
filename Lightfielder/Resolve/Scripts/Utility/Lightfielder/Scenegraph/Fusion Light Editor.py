"""
Lightfielder Fusion Light Editor 2026-09-19 12.00 AM
By Andrew Hazelden <andrew@andrewhazelden.com>

Overview:
The Fusion Light Editor script streamlines the process of editing light parameters in a Fusion 3D workspace-based scene.

If a light is set to PassThrough mode, then it is listed in the Tree view with a "disabled" shading tint for informational purposes. You can still edit the light's parameters and toggle its PassThrough state.

Known Issues
Occasionally, the script will fail to launch, and the following error message will be displayed in the Console window:

Traceback (most recent call last):
  File "", line 411, in <module>
  disp.RunLoop()
  File "<nofile>", line 167, in RunLoop
  File "<nofile>", line 106, in Dispatch
KeyError: 'who'

The typical workaround for this issue is to try launching the script again a few times until the window is displayed, or to relaunch the Fusion program. The root cause of the issue is yet to be discovered.


Usage Note:
Turn on the "Auto Control Close tools" entry in the "Fusion > User Interface" preferences window if you want the Fusion Light Editor tool to auto-select the exact node you double-click on in the Tree view list.

Dev Todo List:
- Filter Lights: All vs Selected Lights
- Search: Look at Reactor to see how to filter a uiTree list
- AddNotify via Comp.Execute()

Resources:
The various light type icons were sourced from "Fusion.fuskin/Tools/Icons/3d/"

"""

from pprint import pprint

def LightEditor():
	comp = fu.GetCurrentComp()
	if comp:
		flow = comp.CurrentFrame.FlowView
		if flow:
		
			ui = fu.UIManager
			disp = bmd.UIDispatcher(ui)
			
			dlg = disp.AddWindow(
				{
					"WindowTitle": "Fusion Light Editor",
					"ID": "LightEditorWin",
					"TargetID": "LightEditorWin",
					"Geometry": [25, 140, 950, 470],
					"Spacing": 0,
				},
				[
					ui.VGroup(
						{
							"ID": "root",
							"Weight": 10.0,
						},
						[
							ui.Label(
								{
									"ID": "Label",
									"Text": "Single click a row to edit it. Double click a row entry to select the node in the Nodes view.",
									"Weight": 0.01,
								}
							),
							ui.Tree(
								{
									"ID": "Tree",
									"Weight": 1.0,
									"SortingEnabled": True,
									"Events": {
										"CurrentItemChanged": True,
										"ItemActivated": True,
										"ItemClicked": True,
										"ItemDoubleClicked": True,
									},
								}
							),
							ui.HGroup(
								{
									"ID": "row",
									"Weight": 0.01,
								},
								[
									ui.VGroup(
										[
											ui.CheckBox(
												{
													"ID": "EnableCheckbox",
													"Text": "Enable Light",
													"Weight": 0.01,
												}
											),
											ui.VGap(10),
											ui.Label(
												{
													"ID": "ColorLabel",
													"Text": "Color",
													"Weight": 0.01,
												}
											),
											ui.ColorPicker(
												{
													"ID": "Color",
													"Weight": 0.01,
													"Color": {
														"R": 1.0,
														"G": 1.0,
														"B": 1.0,
														"A": 1.0,
													},
												}
											),
										]
									),
									ui.VGroup(
										[
											ui.CheckBox(
												{
													"ID": "ShadowsCheckbox",
													"Text": "Enable Shadows",
													"Weight": 0.01,
												}
											),
											ui.VGap(10),
											ui.Label(
												{
													"ID": "ShadowColorLabel",
													"Text": "Shadow Color",
													"Weight": 0.01,
												}
											),
											ui.ColorPicker(
												{
													"ID": "ShadowColor",
													"Weight": 0.01,
													"Color": {
														"R": 1.0,
														"G": 1.0,
														"B": 1.0,
														"A": 1.0,
													},
												}
											),
										]
									),
									ui.VGroup(
										[
											ui.Label(
												{
													"ID": "DecayLabel",
													"Text": "Decay Type",
													"Weight": 0.01,
												}
											),
											ui.ComboBox(
												{
													"ID": "DecayTypeCombo",
													"Text": "Decay Menu",
													"Weight": 0.01,
												}
											),
											ui.Label(
												{
													"ID": "DecayRateLabel",
													"Text": "Decay Rate",
													"Weight": 0.01,
												}
											),
											ui.DoubleSpinBox(
												{
													"ID": "DecayRateSpin",
													"Weight": 0.01,
												}
											),
											ui.Label(
												{
													"ID": "DensityLabel",
													"Text": "Shadow Density",
													"Weight": 0.01,
												}
											),
											ui.DoubleSpinBox(
												{
													"ID": "DensitySpin",
													"Weight": 0.01,
												}
											),
										]
									),
									ui.VGroup(
										[
											ui.HGroup(
												{
													"ID": "Node",
													"Weight": 0.01,
												},
												[
													ui.Label(
														{
															"ID": "NodeLabel",
															"Text": "Node Name",
															"Weight": 0.01,
														}
													),
													ui.Label(
														{
															"ID": "OrigNodeName",
															"Text": "",
															"Weight": 0.01,
														}
													),
												],
											),
											ui.LineEdit(
												{
													"ID": "NodeName",
													"Text": "",
													"PlaceholderText": "Rename the Node",
													"Weight": 0.01,
												}
											),
											ui.Label(
												{
													"ID": "IntensityLabel",
													"Text": "Intensity",
													"Weight": 0.01,
												}
											),
											ui.DoubleSpinBox(
												{
													"ID": "IntensitySpin",
													"Weight": 0.01,
												}
											),
											ui.Button(
												{
													"ID": "PassthroughButton",
													"Text": "PassThrough Off",
													"Weight": 0.01,
													"IconSize": [16, 16],
													"MinimumSize": [16, 16],
													"Icon": ui.Icon(
														{
															"File": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/passthrough_cold.png"
														}
													),
													"Checkable": True,
													"Flat": True,
												}
											),
											ui.VGap(10),
											ui.Button(
												{
													"ID": "UpdateLightButton",
													"Text": "Update Light",
													"Weight": 0.01,
													"IconSize": [24, 24],
													"Icon": ui.Icon(
														{
															"File": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/refresh.png"
														}
													),
												}
											),
										]
									),
								],
							),
						],
					),
				],
			)
			
			itm = dlg.GetItems()
			
			
			# The window was closed
			def _close(ev):
				disp.ExitLoop()
			
			
			# Add your GUI element based event functions here:
			
			# Add the items to the ComboBox menu
			itm["DecayTypeCombo"].AddItem("No Decay")
			itm["DecayTypeCombo"].AddItem("Linear")
			itm["DecayTypeCombo"].AddItem("Quadratic")
			
			# Add a header row
			hdr = itm["Tree"].NewItem()
			
			hdr.Text[0] = "Enable"
			hdr.Text[1] = "ID"
			hdr.Text[2] = "Name"
			hdr.Text[3] = "Intensity"
			hdr.Text[4] = "Color"
			hdr.Text[5] = "Decay Type"
			hdr.Text[6] = "Decay Rate"
			hdr.Text[7] = "Shadows"
			hdr.Text[8] = "Shadow Color"
			hdr.Text[9] = "Density"
			
			hdr.Text[10] = "TX"
			hdr.Text[11] = "TY"
			hdr.Text[12] = "TZ"
			
			hdr.Text[13] = "RX"
			hdr.Text[14] = "RY"
			hdr.Text[15] = "RZ"
			
			
			itm["Tree"].SetHeaderItem(hdr)
			
			# Number of columns in the Tree list
			itm["Tree"].ColumnCount = 16
			
			# Resize the Columns
			itm["Tree"].ColumnWidth[0] = 56
			itm["Tree"].ColumnWidth[1] = 24
			itm["Tree"].ColumnWidth[2] = 200
			itm["Tree"].ColumnWidth[3] = 70
			itm["Tree"].ColumnWidth[4] = 100
			itm["Tree"].ColumnWidth[5] = 85
			itm["Tree"].ColumnWidth[6] = 85
			itm["Tree"].ColumnWidth[7] = 70
			itm["Tree"].ColumnWidth[8] = 120
			itm["Tree"].ColumnWidth[9] = 75
			# Transform
			itm["Tree"].ColumnWidth[10] = 75
			itm["Tree"].ColumnWidth[11] = 75
			itm["Tree"].ColumnWidth[12] = 75
			# Rotate
			itm["Tree"].ColumnWidth[13] = 75
			itm["Tree"].ColumnWidth[14] = 75
			itm["Tree"].ColumnWidth[15] = 75
			
			# Change the sorting order of the tree
			itm["Tree"].SortByColumn(2, "AscendingOrder")
			
			
			def RefreshTree():
				itm["Tree"].Clear()
			
				# List all Lights
				all_tools = comp.GetToolList(False)
				lights_id_dict = {
					"LightPoint": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/point_light.png",
					"LightSpot": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/spotlight.png",
					"LightDirectional": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/directional_light.png",
					"LightAmbient": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/ambient_light.png",
					"LightProjector": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/projector.png",
				}
				tools = [tool for tool in all_tools.values() if tool.ID in lights_id_dict.keys()]
			
				for tool in tools:
					itRow = itm["Tree"].NewItem()
					# Enabled
					if tool.GetInput("Enabled"):
						if tool.GetInput("Enabled") == 1:
							itRow.CheckState[0] = "Checked"
						else:
							itRow.CheckState[0] = "Unchecked"
					# Light Type
					itRow.Icon[1] = ui.Icon({"File": lights_id_dict.get(tool.ID)})
					# Fill columns
					itRow.Text[2] = str(tool.Name)
					itRow.Text[3] = str(tool.GetInput("Intensity"))
					itRow.Text[4] = str(
						str(round(tool.GetInput("Red"), 3))
						+ ", "
						+ str(round(tool.GetInput("Green"), 3))
						+ ", "
						+ str(round(tool.GetInput("Blue"), 3))
					)
			
					if tool.GetInput("DecayRate"):
						itRow.Text[6] = str(round(tool.GetInput("DecayRate"), 4))
			
					if tool.GetInput("ShadowLightInputs3D.ShadowColorRed") is not None:
						itRow.Text[8] = str(
							str(round(tool.GetInput("ShadowLightInputs3D.ShadowColorRed"), 3))
							+ ", "
							+ str(round(tool.GetInput("ShadowLightInputs3D.ShadowColorGreen"), 3))
							+ ", "
							+ str(round(tool.GetInput("ShadowLightInputs3D.ShadowColorBlue"), 3))
						)
			
					if tool.GetInput("ShadowLightInputs3D.ShadowDensity") is not None:
						itRow.Text[9] = str(
							round(tool.GetInput("ShadowLightInputs3D.ShadowDensity"), 3)
						)
			
					# DecayType
					if tool.GetInput("DecayType") is not None and tool.GetInput("DecayType") == 0:
						itRow.Text[5] = "No Decay"
					elif tool.GetInput("DecayType") is not None and tool.GetInput("DecayType") == 1:
						itRow.Text[5] = "Linear"
					elif tool.GetInput("DecayType") is not None and tool.GetInput("DecayType") == 2:
						itRow.Text[5] = "Quadratic"
			
					# ShadowLightInputs3D.ShadowsEnabled
					if tool.GetInput("ShadowLightInputs3D.ShadowsEnabled"):
						if tool.GetInput("ShadowLightInputs3D.ShadowsEnabled") == 1:
							itRow.CheckState[7] = "Checked"
						else:
							itRow.CheckState[7] = "Unchecked"
			
					# Transforms
					if tool.GetInput("Transform3DOp.Translate.X"):
						itRow.Text[10] = str(round(tool.GetInput("Transform3DOp.Translate.X"), 3))
						itRow.Text[11] = str(round(tool.GetInput("Transform3DOp.Translate.Y"), 3))
						itRow.Text[12] = str(round(tool.GetInput("Transform3DOp.Translate.Z"), 3))
			
					if tool.GetInput("Transform3DOp.Rotate.X"):
						itRow.Text[13] = str(round(tool.GetInput("Transform3DOp.Rotate.X"), 3))
						itRow.Text[14] = str(round(tool.GetInput("Transform3DOp.Rotate.Y"), 3))
						itRow.Text[15] = str(round(tool.GetInput("Transform3DOp.Rotate.Z"), 3))
			
					# PassThrough state
					if tool.GetAttrs()["TOOLB_PassThrough"]:
						itRow.Flags = {
							"ItemIsSelectable": True,
							"ItemIsEnabled": False,
							"ItemIsUserCheckable": False,
						}
					else:
						itRow.Flags = {
							"ItemIsSelectable": True,
							"ItemIsEnabled": True,
							"ItemIsUserCheckable": False,
						}
					itm["Tree"].AddTopLevelItem(itRow)
			
			
			def RefreshEditor(selTool):
				if int(selTool.GetInput("Enabled")) == 1:
					itm["EnableCheckbox"].Checked = True
				elif int(selTool.GetInput("Enabled")) == 0:
					itm["EnableCheckbox"].Checked = False
			
				itm["NodeName"].Text = selTool.Name
			
				if selTool.GetInput("Intensity") is None:
					itm["IntensitySpin"].Value = 0.0
				elif selTool.GetInput("Intensity") is not None:
					itm["IntensitySpin"].Value = selTool.GetInput("Intensity")
			
				if selTool.GetInput("ShadowLightInputs3D.ShadowDensity") is None:
					itm["DensitySpin"].Value = 0.0
				elif selTool.GetInput("ShadowLightInputs3D.ShadowDensity") is not None:
					itm["DensitySpin"].Value = selTool.GetInput("ShadowLightInputs3D.ShadowDensity")
			
				if selTool.GetInput("ShadowLightInputs3D.ShadowsEnabled") is None:
					itm["ShadowsCheckbox"].Checked = False
				elif int(selTool.GetInput("ShadowLightInputs3D.ShadowsEnabled")) == 1:
					itm["ShadowsCheckbox"].Checked = True
				elif int(selTool.GetInput("ShadowLightInputs3D.ShadowsEnabled")) == 0:
					itm["ShadowsCheckbox"].Checked = False
			
				if selTool.GetInput("DecayType") is None:
					itm["DecayTypeCombo"].CurrentIndex = 0
				elif selTool.GetInput("DecayType") == 0:
					itm["DecayTypeCombo"].CurrentIndex = 0
				elif selTool.GetInput("DecayType") == 1:
					itm["DecayTypeCombo"].CurrentIndex = 1
				elif selTool.GetInput("DecayType") == 2:
					itm["DecayTypeCombo"].CurrentIndex = 2
			
				if selTool.GetInput("DecayRate") is None:
					itm["DecayRateSpin"].Value = 0.0
				else:
					itm["DecayRateSpin"].Value = selTool.GetInput("DecayRate")
			
				if selTool.GetInput("Red") is not None:
					itm["Color"].Color = {
						"R": selTool.GetInput("Red"),
						"G": selTool.GetInput("Green"),
						"B": selTool.GetInput("Blue"),
						"A": 1.00,
					}
			
				if selTool.GetInput("ShadowLightInputs3D.ShadowColorRed") is not None:
					itm["ShadowColor"].Color = {
						"R": selTool.GetInput("ShadowLightInputs3D.ShadowColorRed"),
						"G": selTool.GetInput("ShadowLightInputs3D.ShadowColorGreen"),
						"B": selTool.GetInput("ShadowLightInputs3D.ShadowColorBlue"),
						"A": 1.00,
					}
			
				state = selTool.GetAttrs()["TOOLB_PassThrough"]
				if state:
					itm["PassthroughButton"].SetIcon(
						ui.Icon({"File": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/passthrough_hot.png"})
					)
					itm["PassthroughButton"].Text = "PassThrough On"
				else:
					itm["PassthroughButton"].SetIcon(
						ui.Icon({"File": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/passthrough_cold.png"})
					)
					itm["PassthroughButton"].Text = "PassThrough Off"
			
			
			def _item_clicked(ev):
				"""A Tree view row was clicked on"""
				sel = str(ev["item"].Text[2])
				itm["OrigNodeName"].Text = sel
				print("[Lightfielder][Edit] " + sel)
			
				RefreshEditor(comp.FindTool(sel))
			
			
			def _item_doubleclicked(ev):
				"""A Tree view row was double clicked on"""
				sel = str(ev["item"].Text[2])
				itm["OrigNodeName"].Text = sel
			
				selTool = comp.FindTool(sel)
				print("[Lightfielder][Selected] " + sel)
			
				# Select the Node in the Nodes view
				if flow is not None:
					flow.Select(None)
					flow.Select(selTool)
			
			
			def _passthrough_button(ev):
				"""Passthrough Icon Button"""
				orig = str(itm["OrigNodeName"].Text)
				selTool = comp.FindTool(orig)
			
				if selTool is None:
					print("[Lightfielder][Error] Please select a row entry for editing!")
					return
			
				state = itm["PassthroughButton"].Checked
				selTool.SetAttrs({"TOOLB_PassThrough": state})
			
				if state:
					itm["PassthroughButton"].SetIcon(
						ui.Icon({"File": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/passthrough_hot.png"})
					)
					itm["PassthroughButton"].Text = "PassThrough On"
				else:
					itm["PassthroughButton"].SetIcon(
						ui.Icon({"File": "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Light_Editor/passthrough_cold.png"})
					)
					itm["PassthroughButton"].Text = "PassThrough Off"
			
				print("[Lightfielder][PassThrough] " + str(state))
				RefreshTree()
			
			
			def _update_light_button(ev):
				"""Update Light Button"""
				orig = str(itm["OrigNodeName"].Text)
				print("[Lightfielder][Update] " + orig)
			
				sel = itm["NodeName"].Text
				selTool = comp.FindTool(orig)
			
				if sel == "" or selTool is None:
					print("[Lightfielder][Error] Please select a row entry for editing!")
					RefreshTree()
					return
			
				# Rename the node
				if sel != "" and sel != orig:
					selTool.SetAttrs({"TOOLS_Name": sel})
					itm["OrigNodeName"].Text = selTool.Name
			
				if itm["EnableCheckbox"].Checked:
					selTool.SetInput("Enabled", 1)
				else:
					selTool.SetInput("Enabled", 0)
			
				selTool.SetInput("Intensity", itm["IntensitySpin"].Value)
			
				if itm["ShadowsCheckbox"].Checked:
					selTool.SetInput("ShadowLightInputs3D.ShadowsEnabled", 1)
				else:
					selTool.SetInput("ShadowLightInputs3D.ShadowsEnabled", 0)
			
				selTool.SetInput("DecayType", itm["DecayTypeCombo"].CurrentIndex)
			
				selTool.SetInput("DecayRate", itm["DecayRateSpin"].Value)
			
				selTool.SetInput("ShadowLightInputs3D.ShadowDensity", itm["DensitySpin"].Value)
			
				selTool.SetInput("Red", itm["Color"].Color["R"])
				selTool.SetInput("Green", itm["Color"].Color["G"])
				selTool.SetInput("Blue", itm["Color"].Color["B"])
			
				selTool.SetInput(
					"ShadowLightInputs3D.ShadowColorRed", itm["ShadowColor"].Color["R"]
				)
				selTool.SetInput(
					"ShadowLightInputs3D.ShadowColorGreen", itm["ShadowColor"].Color["G"]
				)
				selTool.SetInput(
					"ShadowLightInputs3D.ShadowColorBlue", itm["ShadowColor"].Color["B"]
				)
			
				# Rebuild the tree view
				RefreshTree()
			
			
			dlg.On.LightEditorWin.Close = _close
			dlg.On.Tree.ItemClicked = _item_clicked
			dlg.On.Tree.ItemDoubleClicked = _item_doubleclicked
			dlg.On.PassthroughButton.Clicked = _passthrough_button
			dlg.On.UpdateLightButton.Clicked = _update_light_button
			
			comp.Execute(
				"""
			app:AddConfig('LightEditorWin', {
				Target {
					ID = 'LightEditorWin',
				},
				Hotkeys {
					Target = 'LightEditorWin',
					Defaults = true,
			
					CONTROL_W = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
					CONTROL_F4 = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
					ESCAPE = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
				},
			})
			"""
			)
			
			RefreshTree()
			
			dlg.Show()
			disp.RunLoop()
			dlg.Hide()
		else:
			print("[Lightfielder][Fusion Light Editor] Please load the Fusion node graph on the primary monitor. A flow was not detected automatically.\n")
	else:
		print("[Lightfielder][Fusion Light Editor] Please open a Fusion node graph.\n")

if __name__ == "__main__":
	LightEditor()
	print("[Done]")
