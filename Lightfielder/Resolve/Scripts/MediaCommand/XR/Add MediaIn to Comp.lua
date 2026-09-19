--[[--
Add MediaIn to Comp 2026-09-18 09.20 PM

Note: If you are importing Multi-Part or Multi-Channel EXRs you will have to customize the newly created MediaIn node's "Layer" attribute.

--]]--

-- Create a MediaIn node
comp = fusion:GetCurrentComp()
if comp then
    -- Undo stack
    comp:StartUndo("Add MediaIn to Comp")

    -- Read the clip data
	local tbl = bmd.readstring(args)
	for clipIndex, clipValue in ipairs(tbl) do
		if clipValue["Type"] == "Still" or clipValue["Type"] == "Video" or clipValue["Type"] == "Video + Audio" then
            -- Deselect all nodes
            comp.CurrentFrame.FlowView:Select()

            -- Add a MediaIn node to the foreground comp
            local tool = comp:AddTool("MediaIn", -32768, -32768)

            -- Read the MediaIn tag from the clip Lua table
            local id = clipValue["MediaID"] or ""
            tool["MediaID"][fu.TIME_UNDEFINED] = id

            -- Add MediaProps CustomData from the clip Lua table
            local path = clipValue["File Path"]
            tool:SetData("MediaProps.MEDIA_PATH", path)

            local name = clipValue["File Name"]
            tool:SetData("MediaProps.MEDIA_NAME", name)

            local typ = clipValue["Format"]
            tool:SetData("MediaProps.MEDIA_FORMAT_TYPE", typ)

            -- Add a comments from the clip Lua table
            tool["Comments"][fu.TIME_UNDEFINED] = args
		end
	end

    -- Undo Stack
    comp:EndUndo()
else
    print("[Error] A Fusion page comp must be active for this script to function. Please create a new Media Pool or Timeline based Fusion comp and then re-run this script again.")
end