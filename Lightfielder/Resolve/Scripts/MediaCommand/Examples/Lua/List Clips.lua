-- Media Command Script

print("[List Clips]")
local tbl = bmd.readstring(args)
for clipIndex, clipValue in ipairs(tbl) do
	print(clipValue["Clip Name"])
end
