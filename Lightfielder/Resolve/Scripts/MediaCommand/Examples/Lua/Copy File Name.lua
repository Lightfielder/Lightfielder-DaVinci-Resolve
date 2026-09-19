-- Media Command Script

function GenerateMediaList()
	local str = ""

	local tbl = bmd.readstring(args)
	for clipIndex, clipValue in ipairs(tbl) do
		if clipValue["Type"] == "Still" or clipValue["Type"] == "Video" or clipValue["Type"] == "Video + Audio" or clipValue["Type"] == "Geometry" then
			local path = clipValue["File Name"]
			if path ~= nil and path ~= "" then
				str = str .. tostring(path) .. "\n"
			end
		end
	end

	str = str .. "\n"
	return str
end

function Main()
	print("\n[Copy File Name]")

	-- Check the active selection and return a list of media files
	mediaList = GenerateMediaList()

	-- Copy the list of paths into the clipboard buffer
	bmd.setclipboard(mediaList)

	-- Display the list of paths in the console
	print(mediaList)
end

Main()
