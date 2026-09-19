"""
Lightfielder Fusion OpenUSD Outliner 2026-09-19 12.19 AM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Overview:
This script lets you browse the disk-based OpenUSD stage hierarchy in Fusion using uLoader nodes.

Usage:
Step 1. Open a USD-based .comp file in Resolve Studio / Fusion Studio v18.5-21.1+.

Step 2. Run the "Scripts > USD Outliner" menu item.

Installation:
Step 1. Start by installing Python 64-Bit v3.10 - 3.14+ using the installer downloaded from the official Python.org site.

Step 2. Then use Python's pip package manager to install the usd-core package:

pip install usd-core
or 

pip3 install usd-core


Known Issues:
It looks like Fusion Studio v18.5's Python3 interpreter freaks out if the Console window is used to import the OpenUSD based "pxr" Python module.

You can test this bug by opening a Fusion Console window. Switch to the "py3" mode. Then paste in and run the following Python 3 code that will result in a crash of Fusion:
from pxr import Usd, Sdf, UsdGeom, UsdShade

"""
from pxr import Usd, Sdf, UsdGeom, UsdShade
import sys, os
	
def RefreshTree(itm, comp):
	itm["Tree"].Clear()

	# List all USD Nodes
	tools = []
	tools.extend(comp.GetToolList(False, "uLoader").values())

	for tool in tools:
		toolName = str(tool.Name)
		if tool.GetInput("Filename") is not None:
			usdFile = str(tool.GetInput("Filename"))
			print("[Lightfielder][Node] " + str(toolName) + " [File] " + str(usdFile))

# 			itRow = itm["Tree"].NewItem()
# 			itRow.Text[0] = toolName
# 			itRow.Text[1] = usdFile
# 
# 			itm["Tree"].AddTopLevelItem(itRow)

			usdStage = Usd.Stage.Open(comp.MapPath(usdFile))
			for prims in usdStage.Traverse():
				itRow = itm["Tree"].NewItem()

				primType = prims.GetTypeName()
				primName = prims.GetName()
				primPath = prims.GetPrimPath()
				primRef = prims.GetPrim()
				primXform = UsdGeom.Xform(primRef)
				#primPurpose = primXform.Get()

				# Example: [Xform] /PointCloudGroup/locator1
				#print("\t[Lightfielder][" + str(primType) + "] " + str(primPath))

				itRow.Text[0] = toolName
				itRow.Text[3] = usdFile
				itRow.Text[1] = str(primType)
				itRow.Text[2] = str(primPath)

				itm["Tree"].AddTopLevelItem(itRow)

def CreateUsdWindow():
	if fu is None:
		print("[Lightfielder][FuScript Error] Please open up the Resolve Studio / Fusion Studio GUI before running this script.")
	else:
		comp = fu.GetCurrentComp()
		if comp is None:
			print("[Lightfielder][FuScript Error] Please open up a Fusion .comp file.")
		else:
			flow = comp.CurrentFrame.FlowView

			ui = fu.UIManager
			disp = bmd.UIDispatcher(ui)
	
			dlg = disp.AddWindow({"WindowTitle": "USD Outliner", "ID": "UsdOutliner", "TargetID" : "UsdOutliner", "Geometry": [25, 140, 1160, 300], "Spacing": 0,},[
				ui.VGroup({"ID": "root", "Weight": 10.0,},[
					ui.HGroup({"ID": "root", "Weight": 0.1,},[
						ui.Label({"ID": "Label", "Text": "Double click a row entry to select the node in the Nodes view.", "Weight": 0.01,}),
						ui.HGap(20, 1),
						ui.Button({
							"Weight": 0.01,
							"ID": "RefreshButton",
							"Text": "Refresh View",
						}),
					]),
					ui.Tree({
						"ID": "Tree",
						"Weight": 1.0,
						"SortingEnabled": True,
						"Events": {
							"CurrentItemChanged": True,
							"ItemActivated": True,
							"ItemClicked": True,
							"ItemDoubleClicked": True,
						},
					}),
				]),
			])

			itm = dlg.GetItems()

			# The window was closed
			def CloseFunc(ev):
				disp.ExitLoop()
			dlg.On.UsdOutliner.Close = CloseFunc

			# A Tree view row was clicked on
			def ClickFunc(ev):
				sel = str(ev["item"].Text[0])
				selTool = comp.FindTool(sel)
				print("[Lightfielder][Selected] " + sel)

				if flow is not None:
					flow.Select(None)
					flow.Select(selTool)
			dlg.On.Tree.ItemDoubleClicked = ClickFunc

			# The Refresh Button was clicked in the GUI
			def RefreshButtonFunc(ev):
				comp = fu.GetCurrentComp()
				flow = comp.CurrentFrame.FlowView

				RefreshTree(itm, comp)
			dlg.On.RefreshButton.Clicked = RefreshButtonFunc

			# Add a header row
			hdr = itm["Tree"].NewItem()

			hdr.Text[0] = "Node"
			hdr.Text[1] = "Type"
			hdr.Text[2] = "Prim Path"
			hdr.Text[3] = "File"
			
			itm["Tree"].SetHeaderItem(hdr)

			# Number of columns in the Tree list
			itm["Tree"].ColumnCount = 4

			# Resize the Columns
			itm["Tree"].ColumnWidth[0] = 120
			itm["Tree"].ColumnWidth[1] = 75
			itm["Tree"].ColumnWidth[2] = 410
			itm["Tree"].ColumnWidth[3] = 525

			# Change the sorting order of the tree
			itm["Tree"].SortByColumn(0, "AscendingOrder")

			RefreshTree(itm, comp)

			comp.Execute("""
	app:AddConfig('UsdOutliner', {
		Target {
			ID = 'UsdOutliner',
		},
		Hotkeys {
			Target = 'UsdOutliner',
			Defaults = true,

			CONTROL_W = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
			CONTROL_F4 = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
			ESCAPE = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
		},
	})""")

			dlg.Show()
			disp.RunLoop()
			dlg.Hide()

if __name__ == "__main__":
	CreateUsdWindow()
	print("[Done]")
