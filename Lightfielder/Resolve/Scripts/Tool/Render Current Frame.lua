--[[--
Render Current Frame.lua - 2026-09-02 07.10 PM

The "Render Current Frame" script will render the current frame using the actively selected node in Fusion Standalone/Resolve's Fusion page Nodes view.

This means you can output content in Resolve's Fusion Page directly to disk using nodes like the FBXExporter, Saver, LifeSaver, pioSaver, Vonk Ultra nodes, or custom EXRIO based Fuse.

--]]--

-- Is a Fusion comp open?
if comp then
	-- The "tool" variable is empty
	if not tool then
		-- Get the selected tool when running as a comp script
		tool = comp.ActiveTool
	end

	-- Was a node selected in the Nodes view?
	if tool then
		print('[Render Current Frame] ' .. tool.Name)

		-- Render only the selected tool
		local frameList = tostring(comp.CurrentTime) .. ".." ..  tostring(comp.CurrentTime)
		comp:Render({Tool = tool, FrameRange = frameList, Wait = true})
	else
		print('[Render Current Frame] [Selection Error] Please select a node before running this script.')
	end
else
	print('[Render Current Frame] [Comp Error] Please open a new Fusion composite before trying to render it.')
end
