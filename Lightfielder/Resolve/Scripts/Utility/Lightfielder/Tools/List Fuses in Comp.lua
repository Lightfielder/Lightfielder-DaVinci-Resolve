print("[Lightfielder] [List Fuses in Comp]")

tools = comp:GetToolList(false)

-- Add the nodes
for _i, tool in ipairs(tools) do
	if tool.ID:match("^Fuse")  then
		print(string.format("[%03d] [Node Name] %30s [Reg ID] %30s", _i, tool.Name, tool.ID))
	end
end
