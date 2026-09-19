--[[--
List Node Inputs and Outputs.lua 2026-09-18 11.54 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

This comp script lists all of the input and output attributes for the nodes in the Fusion comp. The output is written to a JSON file named "NodeReport.json" that is saved in your user account's home folder:

$HOME/NodeReport.json


If you select a single node that node's information is written to the JSON file. If no nodes are selected in the nodes view, then all of the active nodes in the comp will have their information written to the JSON file.

Sample JSON Output:

{
"vFileSystemFileOpen1":{
	"Inputs":{
		"EndRenderScript":{
		"INPI_UserData":0,
		"INPI_SubType":0,
		"INPI_IC_Steps":0,
		"INPI_IC_DisplayedPrecision":0,
		"INPS_ID":"EndRenderScript",
		"INPN_Default":0,
		"INPN_DefaultX":0,
		"INPN_DefaultY":0,
		"INPB_TextEditControl_SuppressTab":false,
		"INPB_TextEditControl_ReadOnly":false,
		"INPB_TextEditControl_Wrap":false,
		"INPI_TextEditControl_Lines":10,
		"INPB_IgnoreVisible":0,
		"INPS_IC_Label":"",
		"INPB_IC_NoReset":1,
		"INPB_IC_NoLabel":1,
		"INPB_IC_SkipNest":false,
		"INPB_IC_ForceWrap":false,
		"INPI_IC_FixedWidth":0,
		"INPB_PC_Visible":false,
		"INPN_IC_Center":0,
		"INPS_Name":"End Render Script",
		"INPN_UserData3":0,
		"INPN_UserData2":0,
		"INPS_DataType":"Text",
		"INPB_External":false,
		"INPB_Active":false,
		"INPB_Required":true,
		"INPB_Connected":false,
		"INPI_Priority":0,
		"INPI_PC_GrabPriority":0,
		"INPB_Disabled":false,
		"INPB_DoNotifyChanged":true,
		"INPB_Integer":false,
		"INPI_NumSlots":1,
		"INPB_ForceNotify":false,
		"INPB_InitialNotify":false,
		"INPB_Passive":false,
		"INPB_InteractivePassive":false,
		"INPB_SendRequest":true,
		"INPB_GetRequirements":true,
		"INPB_ForceSecondaryTimeNotify":false,
		"INPN_MinAllowed":-1000000,
		"INPN_MaxAllowed":1000000,
		"INPN_MinScale":0,
		"INPN_MaxScale":1,
		"INPI_IC_ControlGroup":0,
		"INPI_IC_ControlID":0,
		"INPI_IC_ControlPage":1,
		"INPI_PC_ControlGroup":0,
		"INPI_PC_ControlID":0,
		"INPS_ICS_ControlPage":"Common",
		"INPN_ICD_Width":0,
		"INPB_OpMenu":false,
		"INPB_IC_TimeType":false,
		"INPB_IC_StepRestrict":false,
		"INPB_IC_Visible":false,
		"INPID_InputControl":"TextEditControl",
		"INPB_PC_FastSampleRate":false
	},
	...

Note:
If you want to automate the process of creating one of every type of node in your Fusion comp, you can use the following code snippet in Fusion Studio:

-- Cedric's "Create All Nodes.lua" Script:
reg_map = fusion:GetRegList()  -- dict[int, Registry]
for _i, reg in ipairs(reg_map) do
	comp:AddTool(reg.ID)
end

--]]--

print("\n-----------------------------------")
print("List Node Inputs and Outputs - v1.0")
print("-----------------------------------\n")
-- Add the platform specific folder slash character
osSeparator = package.config:sub(1,1)

-- Find out the current operating system platform. The platform variable should be set to either 'Windows', 'Mac', or 'Linux'.
platform = (FuPLATFORM_WINDOWS and 'Windows') or (FuPLATFORM_MAC and 'Mac') or (FuPLATFORM_LINUX and 'Linux')

-- Location to save the JSON formatted log file
local nodeReportPath = ""
if platform == "Windows" then
	nodeReportPath = tostring(os.getenv("USERPROFILE"))
else
	-- Mac and Linux
	nodeReportPath = tostring(os.getenv("HOME"))
end
nodeReportPath = nodeReportPath .. tostring(osSeparator) .. "NodeReport.json"
	
-- Grab a list of the selected nodes. 
local tools = comp:GetToolList(true)

-- If no nodes are selected process all nodes in the comp instead
if table.getn(tools) == 0 then
	tools = comp:GetToolList()
end

print("[Node Count] ", table.getn(tools))
if tools ~= nil then
	local nodes = {}
	for key, value in pairs(tools) do
		nodes[value.Name] = {}

		-- Inputs
		nodes[value.Name]["Inputs"] = {}
		x = value:GetInputList()
		for i, inp in pairs(x) do
			nodes[value.Name]["Inputs"][inp:GetAttrs().INPS_ID] = {}
			nodes[value.Name]["Inputs"][inp:GetAttrs().INPS_ID] = inp:GetAttrs()
		end

		-- Outputs
		nodes[value.Name]["Outputs"] = {}
		y = value:GetOutputList()
		for i, outs in pairs(y) do
			nodes[value.Name]["Outputs"][outs:GetAttrs().OUTS_ID] = {}
			nodes[value.Name]["Outputs"][outs:GetAttrs().OUTS_ID] = outs:GetAttrs()
		end
	end
	
	-- Sort the table alphabetically
	--table.sort(nodes)
	
	-- Display the Lua table formatted results in the Console window
	-- dump(nodes)
	
	-- Encode the data as a JSON string
	local json = require("dkjson")
	local json_str = json.encode(nodes, {indent = true})

	-- Display the JSON encoded results in the Console window
	--dump(json_str)
	
	-- Write the info to disk
	local directory = nodeReportPath:match("(.*[/\\])")
	if bmd.fileexists(directory) == false then
		bmd.createdir(directory)
		print('[Created Directory]', folder)
	end

	print("[Writing Report] ", nodeReportPath)
	fp = io.open(nodeReportPath, "w")
	if fp == nil then
		error(string.format("directory does not exist: %s", directory))
	end
	fp:write(json_str)
	fp:close()
	
	print("[Opening file]")
	bmd.openfileexternal('Open', nodeReportPath)
else
	error("Please select a node in the comp before running this script.")
end
