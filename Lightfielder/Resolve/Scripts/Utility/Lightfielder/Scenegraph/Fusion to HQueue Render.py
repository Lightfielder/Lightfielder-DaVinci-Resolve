# Customize the HQueue connection details:
port = "5000"

server = "localhost"
#server = "10.20.30.1"
#server = "10.20.30.2"
#server = "10.20.30.3"
#server = "10.20.30.4"
#server = "10.20.30.5"

# Render Farm Operating System
# The "Auto" setting uses the Fusion Studio submitter system's architecture to define the FarmOS value automatically.
farmOS = "Auto"
# farmOS = "macOS"
# farmOS = "Windows"
# farmOS = "Linux"

"""
Lightfielder Fusion to HQueue Render 2026-09-19 12.17 AM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

## Overview

This script allows Fusion Studio to submit compositing jobs for rendering via Houdini HQueue.

## Open Source Software License

- LGPL 3.0 License

## Known Issues

The script currently works with macOS and Linux based HQueue Client render nodes.

Windows support is currently under development. On Windows, the following error is reported by HQueue when a job is run:

	[WinError 2] The system cannot find the file specified 
	ERROR: Could not run command.

## Usage

Step 1. Open the HQueue management webpage. (Typically this defaults to "http://localhost:5000"). Use the HQueue webUI to create an HQueue "Client Group" called "Fusion".

Step 2. Open a Fusion comp. Select the "Utility > Lightfielder > Scenegraph > Fusion to HQueue Render" menu item to submit a Fusion composite to your render farm.

Set the "Frames Per Task" value to define how large of a frame chunk you want each job task to use. A value of zero sets the job to render as a single job task.

# Todo List
- Store the HQueue server address and port number in the fusion prefs
- Store the render frame range values in the comp level custom data record. Restore these values the next time the HQueue Render dialog is run.
- Add "Frameset" as a text field to allow custom render regions to be entered
- Add "submittedBy" to the Job Spec

"""

# HQueue Logo
LogoBase64 = """<img width='135' height='20' src='data:image/png;base64,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'/>"""

def Main():
	# Start - End Render Range
	startFrame = str(comp.GetAttrs()["COMPN_RenderStart"])
	endFrame = str(comp.GetAttrs()["COMPN_RenderEnd"])
	stepByFrame = str(comp.GetAttrs()["COMPI_RenderStep"])

	ui = fu.UIManager
	disp = bmd.UIDispatcher(ui)

	dlg = disp.AddWindow({
		"WindowTitle": "HQueue Render", 
		"ID": "HQueue", 
		"TargetID" : "HQueue",
		"Geometry": [100, 100, 450, 400], 
		"Spacing": 10,
		},[
		ui.VGroup({"ID": "root",},[
			# Add your GUI elements here:
			ui.TextEdit({ 
				"ID": "Logo",
				"Text": LogoBase64,
				"ReadOnly": True,
				"StyleSheet": "QTextEdit { border: 0px; }",
			}),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "HQueueServerAddressLabel", "Text": "HQueue Server Address",}),
				ui.LineEdit({"ID": "HQueueServerAddress", "Text": str(server), "PlaceholderText": "Enter a hostname or IPv4 address"}),
			]),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "HQueueServerPortLabel", "Text": "HQueue Server Port",}),
				ui.LineEdit({"ID": "HQueueServerPort", "Text": str(port), "PlaceholderText": "Enter a port number like 5000"}),
			]),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "JobNameLabel", "Text": "Job Name",}),
				ui.LineEdit({"ID": "JobName", "Text": "Fusion Render Node", "PlaceholderText": ""}),
			]),
			ui.Label({"ID": "JobDescriptionLabel", "Text": "Job Description",}),
			ui.TextEdit({ 
				"ID": "JobDescription",
				"Text": "",
				"PlaceholderText": "Please enter a job comment.",
			}),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "PriorityLabel", "Text": "Priority"}),
				ui.SpinBox({"ID": "Priority", "Maximum": 10, "Minimum": 0, "Value": 5}),
			]),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "FramesPerTaskLabel", "Text": "Frames Per Task",}),
				ui.SpinBox({"ID": "FramesPerTask"}),
			]),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "FrameRangeLabel", "Text": "Frame Range",}),
				ui.ComboBox({"ID": "FrameRange"}),
			]),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "StartFrameLabel", "Text": "Start Frame",}),
				ui.LineEdit({"ID": "StartFrame", "Text": str(startFrame), "PlaceholderText": ""}),
				ui.Label({"ID": "EndFrameLabel", "Text": "End Frame",}),
				ui.LineEdit({"ID": "EndFrame", "Text": str(endFrame), "PlaceholderText": ""}),
				ui.Label({"ID": "StepByFrameLabel", "Text": "Step By",}),
				ui.LineEdit({"ID": "StepByFrame", "Text": str(stepByFrame), "PlaceholderText": ""}),
			]),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "WriteLogfileLabel", "Text": "Write Logfile",}),
				ui.CheckBox({"ID": "WriteLogfile"}),
			]),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "FarmOSLabel", "Text": "Farm OS",}),
				ui.ComboBox({"ID": "FarmOS"}),
			]),
			ui.HGroup({"Spacing": 0,},[
				ui.Label({"ID": "FusionVersionLabel", "Text": "Fusion Render Node Version",}),
				ui.ComboBox({"ID": "FusionVersion"}),
			]),
			ui.HGroup({"Spacing": 0,},[

			ui.Button({"ID": "CancelButton", "Text": "Cancel"}),
			ui.Button({"ID": "SubmitButton", "Text": "Submit"}),
			]),
		]),
	])

	itm = dlg.GetItems()

	# The window was closed
	def CloseWindow(ev):
		disp.ExitLoop()
	dlg.On.HQueue.Close = CloseWindow

	# Add your GUI element based event functions here:

	def FrameRangeChange(ev):
		if itm["FrameRange"].CurrentIndex == 0:
			# Start-End Render Range
			itm["StartFrame"].Text = str(comp.GetAttrs()["COMPN_RenderStart"])
			itm["EndFrame"].Text = str(comp.GetAttrs()["COMPN_RenderEnd"])
			itm["StepByFrame"].Text = str(comp.GetAttrs()["COMPI_RenderStep"])

			itm["StartFrameLabel"].Visible = False
			itm["StartFrame"].Visible = False
			itm["EndFrameLabel"].Visible = False
			itm["EndFrame"].Visible = False
			itm["StepByFrameLabel"].Visible = False
			itm["StepByFrame"].Visible = False
			dlg.RecalcLayout()
		elif itm["FrameRange"].CurrentIndex == 1:
			# Start-End Global Range
			itm["StartFrame"].Text = str(comp.GetAttrs()["COMPN_GlobalStart"])
			itm["EndFrame"].Text = str(comp.GetAttrs()["COMPN_GlobalEnd"])
			itm["StepByFrame"].Text = str(comp.GetAttrs()["COMPI_RenderStep"])

			itm["StartFrameLabel"].Visible = False
			itm["StartFrame"].Visible = False
			itm["EndFrameLabel"].Visible = False
			itm["EndFrame"].Visible = False
			itm["StepByFrameLabel"].Visible = False
			itm["StepByFrame"].Visible = False
			dlg.RecalcLayout()
		elif itm["FrameRange"].CurrentIndex == 2:
			# Specific Frame Range
			itm["StartFrame"].Text = str(comp.GetAttrs()["COMPN_RenderStart"])
			itm["EndFrame"].Text = str(comp.GetAttrs()["COMPN_RenderEnd"])
			itm["StepByFrame"].Text = str(comp.GetAttrs()["COMPI_RenderStep"])

			itm["StartFrameLabel"].Visible = True
			itm["StartFrame"].Visible = True
			itm["EndFrameLabel"].Visible = True
			itm["EndFrame"].Visible = True
			itm["StepByFrameLabel"].Visible = True
			itm["StepByFrame"].Visible = True

			dlg.RecalcLayout()
	dlg.On.FrameRange.CurrentIndexChanged = FrameRangeChange

	def SubmitButton(ev):
		print("[Lightfielder][HQueue Render] Job Submitted")
		Submit(itm)
		disp.ExitLoop()
	dlg.On.SubmitButton.Clicked = SubmitButton

	def CancelButton(ev):
		print("[Lightfielder][HQueue Render] Cancelled")
		disp.ExitLoop()
	dlg.On.CancelButton.Clicked = CancelButton

	# Add items to the ComboBox menu
	itm["FarmOS"].AddItem("Auto")
	itm["FarmOS"].AddItem("macOS")
	itm["FarmOS"].AddItem("Windows")
	itm["FarmOS"].AddItem("Linux")
	itm["FarmOS"].CurrentText = farmOS

	# Add items to the ComboBox menu
	itm["FusionVersion"].AddItem("9")
	itm["FusionVersion"].AddItem("16")
	itm["FusionVersion"].AddItem("17")
	itm["FusionVersion"].AddItem("18")
	itm["FusionVersion"].AddItem("19")
	itm["FusionVersion"].AddItem("20")
	itm["FusionVersion"].AddItem("21")
	itm["FusionVersion"].CurrentText = "21"

	# Add items to the ComboBox menu
	itm["FrameRange"].AddItem("Start-End Render Range")
	itm["FrameRange"].AddItem("Start-End Global Range")
	itm["FrameRange"].AddItem("Specific Frame Range")
	itm["FrameRange"].CurrentText = "Start-End Render Range"

	comp.Execute("""
app:AddConfig('HQueue', {
	Target {
		ID = 'HQueue',
	},
	Hotkeys {
		Target = 'HQueue',
		Defaults = true,

		CONTROL_W = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
		CONTROL_F4 = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
		ESCAPE = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
	},
})""")

	dlg.Show()
	disp.RunLoop()
	dlg.Hide()


def Submit(itm):
	import xmlrpc.client
	import webbrowser
	import sys, os

	# Connect to the HQueue server
	server = "http://" + str(itm["HQueueServerAddress"].Text) + ":" + str(itm["HQueueServerPort"].Text)
	print("[Lightfielder][HQueue Server] " + str(server))
	hq = xmlrpc.client.ServerProxy(server)

	try:
		hq.ping()
		print("[Lightfielder][HQueue Server] Connection successfull")
	except ConnectionRefusedError:
		print("[[Lightfielder]HQueue Server] Not available")

	print("[Lightfielder][Render Range] [Start] " + str(itm["StartFrame"].Text) + " [End] " + str(itm["EndFrame"].Text) + " [Step By] " + str(itm["StepByFrame"].Text))

	# Fusion Render Node executable selection
	FusionPath = ""
	shell = ""
	if (itm["FarmOS"].CurrentText == "Auto" and sys.platform == "win32") or itm["FarmOS"].CurrentText == "Windows":
		# Windows
		FusionPath = '"C:\\Program Files\\Blackmagic Design\\Fusion Render Node ' + str(itm["FusionVersion"].CurrentText) + '\\FusionRenderNode.exe"'
		shell = "bash"
	elif (itm["FarmOS"].CurrentText == "Auto" and sys.platform == "darwin") or itm["FarmOS"].CurrentText == "macOS":
		# macOS
		FusionPath = "'/Applications/Blackmagic Fusion " + str(itm["FusionVersion"].CurrentText) + " Render Node/Fusion Render Node.app/Contents/MacOS/Fusion Render Node'"
		shell = "bash"
	elif (itm["FarmOS"].CurrentText == "Auto" and sys.platform == "linux") or itm["FarmOS"].CurrentText == "Linux":
		# Linux
		FusionPath = "'/opt/BlackmagicDesign/FusionRenderNode" + str(itm["FusionVersion"].CurrentText) + "/FusionRenderNode'"
		shell = "bash"

	# Dynamic chunk sizing
	renderTasks = []
	framesPerTaskStep = int(float(itm["FramesPerTask"].Value))

	if framesPerTaskStep == 0:
		# Single job for all frames
		#compPrefix = str(comp.GetAttrs()["COMPS_Name"]).replace(".comp", "")
		#logFolder = app.MapPath("Temp:/KartaLink/" + compPrefix + "/")
		#logFilepath = logFolder + compPrefix + "_log." + str(framesPerTaskStep) + ".txt"
		#if not os.path.exists(logFolder):
		#	try:
		#		print("\t[Lightfielder][HQueue Render][Make Log Directory]", logFolder)
		#		os.makedirs(logFolder)
		#	except OSError as error:
		#		print("\t[Lightfielder][HQueue Render][Make Log Directory Error]", logFolder)

		logFilepath = str(comp.GetAttrs()["COMPS_FileName"]).replace(".comp", "") + "." + str(framesPerTaskStep).zfill(4) + ".txt"

		logString = ""
		jobCommandString = ""
		if (itm["FarmOS"].CurrentText == "Auto" and sys.platform == "win32") or itm["FarmOS"].CurrentText == "Windows":
			# Windows
			if itm["WriteLogfile"].Checked:
				logString = ' -log "' + logFilepath + '" -cleanlog '
			jobCommandString = FusionPath + ' "' + str(comp.GetAttrs()["COMPS_FileName"]) + '" -render -start ' + str(itm["StartFrame"].Text) + ' -end ' + str(itm["EndFrame"].Text) + ' -step ' + str(itm["StepByFrame"].Text) + logString + ' -verbose -status -quit'
		else:
			# macOS and Linux
			if itm["WriteLogfile"].Checked:
				logString = " -log '" + logFilepath + "' -cleanlog "
			jobCommandString = FusionPath + " '" + str(comp.GetAttrs()["COMPS_FileName"]) + "' -render -start " + str(itm["StartFrame"].Text) + " -end " + str(itm["EndFrame"].Text) + " -step " + str(itm["StepByFrame"].Text) + logString + " -verbose -status -quit"
				
		#print("[Command]")
		#print(jobCommandString)

		renderTasks.append({
			"name": "Render (Frames: " + str(int(float(itm["StartFrame"].Text))) + "-" + str(int(float(itm["EndFrame"].Text))) + ")",
			"shell": shell,
			"command": jobCommandString
		})
	else:
		start = int(float(itm["StartFrame"].Text))
		end = int(float(itm["EndFrame"].Text)) + 1
		for frame in range(start, end, framesPerTaskStep):
			frameStep = frame + (framesPerTaskStep - 1)
			# Limit the last chunk duration to the actual frame range, for situations when the frame step is not a multiple of the end frame value
			if frameStep > end:
				frameStep = end - 1

			#compPrefix = str(comp.GetAttrs()["COMPS_Name"]).replace(".comp", "")
			#logFolder = app.MapPath("Temp:/KartaLink/" + compPrefix + "/")
			#logFilepath = logFolder + compPrefix + "_log." + str(frame).zfill(4) + ".txt"
			#if not os.path.exists(logFolder):
			#	try:
			#		print("\t[HQueue Render][Make Log Directory]", logFolder)
			#		os.makedirs(logFolder)
			#	except OSError as error:
			#		print("\t[HQueue Render][Make Log Directory Error]", logFolder)

			logFilepath = str(comp.GetAttrs()["COMPS_FileName"]).replace(".comp", "") + "." + str(frame).zfill(4) + ".txt"

			logString = ""
			jobCommandString = ""
			if (itm["FarmOS"].CurrentText == "Auto" and sys.platform == "win32") or itm["FarmOS"].CurrentText == "Windows":
				# Windows
				if itm["WriteLogfile"].Checked:
					logString = ' -log "' + logFilepath + '" -cleanlog '
				jobCommandString = FusionPath + ' "' + str(comp.GetAttrs()["COMPS_FileName"]) + '" -render -start ' + str(frame) + ' -end ' + str(frameStep) + ' -step ' + str(itm["StepByFrame"].Text) + logString + ' -verbose -status -quit'
			else:
				# macOS and Linux
				if itm["WriteLogfile"].Checked:
					logString = " -log '" + logFilepath + "' -cleanlog "
				jobCommandString = FusionPath + " '" + str(comp.GetAttrs()["COMPS_FileName"]) + "' -render -start " + str(frame) + " -end " + str(frameStep) + " -step " + str(itm["StepByFrame"].Text) + logString + " -verbose -status -quit"

			#print("[Command]")
			#print(jobCommandString)

			renderTasks.append({
				"name": "Render (Frames: " + str(int(float(frame))) + "-" + str(int(float(frameStep))) + ")",
				"shell": shell,
				"tags": ["single"],
				"command": jobCommandString,
				"conditions": [{ 
					"type" : "client", 
					"name": "group", 
					"op": "==", 
					"value": "Fusion"
				}]
			})

	# Define a job that renders an fusion comp
	job_spec = {
		"name": str(itm["JobName"].Text) + " -> " + str(comp.GetAttrs()["COMPS_FileName"]),
		"description": str(itm["JobDescription"].PlainText),
		"priority": int(itm["Priority"].Value),
		"shell": shell,
		"tags": ["single"], 
		"children": renderTasks,
		"conditions": [{ 
			"type" : "client", 
			"name": "group", 
			"op": "==", 
			"value": "Fusion"
		}]
	}

	print("[HQueue Server] Job Spec")
	print(job_spec)

	job_ids = hq.newjob(job_spec)

	job_ids_string = str(job_ids[0]).replace("[", "").replace("]", "")
	print("[HQueue Server] [Job ID] " + str(job_ids_string))

	# Job URL Example: http://localhost:5000/jobs/view/337
	url = server + "/jobs/view/" + str(job_ids_string)
	print("[HQueue Server] [Status Webpage] " + str(url))
	webbrowser.open(url)

if __name__ == "__main__":
	comp = fu.CurrentComp
	Main()
