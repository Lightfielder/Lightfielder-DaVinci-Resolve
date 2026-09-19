--[[--
Create All Data Nodes 2026-09-18 11.57 PM (UTC -3)

This script is based upon Cedric Duriau's earlier "Create All Nodes" Lua Script:
https://gist.github.com/cedricduriau/125cd3b84ab72cc1afc85ebfe943193c#file-fusion_createallnodes-lua

--]]--

reg_map = fusion:GetRegList()  -- dict[int, Registry]

-- Total Nodes
node_count = 0
for _i, reg in ipairs(reg_map) do
	if reg.ID:match("^Fuse.v")	then
		node_count = node_count + 1
	end
end
print("[Vonk] [Create All Data Nodes] ", node_count)

-- Add the nodes
for _i, reg in ipairs(reg_map) do
	if reg.ID:match("^Fuse.v")	then
		print("[" .. _i .. "] ", reg.ID)
		comp:AddTool(reg.ID)
	end
end
