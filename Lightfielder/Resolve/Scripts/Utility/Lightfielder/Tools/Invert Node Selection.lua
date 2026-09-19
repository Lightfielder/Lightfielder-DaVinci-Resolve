--[[--
Invert Node Selection 2026-09-18 11.46 PM (UTC -3)
By Andrew Hazelden (andrew@andrewhazelden.com)

Overview:
Inverts the current selection in the node graph.

Usage:
1. Select several nodes in the flow area.
2. Launch the "Scripts > Invert Node Selection" menu item. 
3. All non-selected nodes will be selected in the node graph.

--]]--

function Main()
	print("[Invert Node Selection]")
	flow = comp.CurrentFrame.FlowView

	-- Read the selection
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
	comp:StartUndo("Invert Node Selection")

	-- Deselect all nodes
	flow:Select() 

	-- Update the selection
	for i = 1, #allNodes do
		flow:Select(allNodes[i])
		-- print(allNodes[i].Name)
	end

	print(tostring(#allNodes) .. " nodes selected")
	-- End Undo
	comp:EndUndo()
end

Main()
print("[Done]")
