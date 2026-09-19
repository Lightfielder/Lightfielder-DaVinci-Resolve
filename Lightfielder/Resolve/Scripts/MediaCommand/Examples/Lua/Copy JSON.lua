-- Media Command Script

local json = require("dkjson")

function Main()
	print("\n[Copy JSON]")

	-- Create a JSON formatted output from the clip property data
	local tbl = bmd.readstring(args)
	local str = json.encode(tbl, {indent = true})

	-- Copy the JSON encoded string into the clipboard buffer
	bmd.setclipboard(str)

	-- Display the JSON formatted output in the console
	print(str)
end

Main()
