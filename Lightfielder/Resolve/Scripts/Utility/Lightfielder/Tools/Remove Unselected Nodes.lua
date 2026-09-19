--[[--
Remove Unselected Nodes  2026-09-18 11.46 PM (UTC -3)
By Andrew Hazelden (andrew@andrewhazelden.com)

Overview:
This script is used to quickly clean up a comp when you are doing repetitive experiments.

Any node that is unselected in the node graph will be instantly deleted.
As a result, this will leave you with only the currently selected nodes in the comp.

An undo point is defined when the script is run so you can revert the changes easily.

Usage:
1. Select several nodes in the flow area.
2. Launch the "Scripts > Remove Unselected Nodes " menu item.
3. All non-selected nodes will be removed from the node graph.

--]]--

function Main()
	print("[Remove Unselected Nodes]")
	flow = comp.CurrentFrame.FlowView

	-- Read the selection
	local selectedTool = comp.ActiveTool
	local allNodes = comp:GetToolList(false)
	local tools = comp:GetToolList(true)

	for i = #allNodes, 1, -1 do
		for j = 1, #tools do
			if allNodes[i] == tools[j] then
				table.remove(allNodes, i)
				break -- Exit once a match is found
			end
		end
	end

	-- Start Undo
	comp:StartUndo("Remove Unselected Nodes")

	-- Deselect all nodes
	flow:Select() 

	-- Remove Nodes
	for i = 1, #allNodes do
		allNodes[i]:Delete()
		-- print(allNodes[i].Name)
	end
	
	print(tostring(#allNodes) .. " nodes removed")
	
	-- Update the selection
	for i = 1, #tools do
		flow:Select(tools[i])
		-- print(tools[i].Name)
	end
	comp:SetActiveTool(selectedTool)

	-- End Undo
	comp:EndUndo()
end

Main()
print("[Done]")
