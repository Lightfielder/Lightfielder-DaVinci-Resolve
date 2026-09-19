--[[--
Lightfielder 18 Media Command.lua 2026-09-18 09.19 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Media Command is a scriptable interface for batch processing content that resides in your Resolve Media Pool. This streamlines the process of selecting footage and running automation scripts on those specific items.

When Media Command is launched, it automatically scans for Lua and Python scripts that are located inside the "Scripts:/MediaCommand/" folder. These items are added to the "Command Script" menu in the interface.

If you are a long-time Fusion user, you will find that the Media Command script was designed to give your Media page content management operations the same power and flexibility you have when you use a Fusion page "tool" script in the Fusion nodes view context.


## Search Controls

The "Type:" ComboMenu allows you to limit the tree view to only show media of a certain format. The menu options are: "All", "Still", "Video", "Video + Audio", "Audio", "Compound", "Fusion", "Generator", "Geometry", "Stereo", "Subtitle", and "Timeline".

The "Search:" text field allows you to narrow down the results in the tree view with plain-text search of the "Clip Name" and "File Name" records.

The "Select: (All) (None) (Invert)" buttons can be used to quickly modify the footage that is selected in the tree view. It is worth noting that the select buttons work on the content that is visible in the tree view at the current moment so you can apply the select buttons to only the filtered search results, and those selections will remain active when you later flip back to the full unfiltered list of content in the tree view.


## View Controls

The "Keep Open" button is active the Media Command window will remain open after a script is launched. This is handy if you need to batch process multiple clips in rapid succession. If this button is inactive the Media Command window will close each time a script is run.

The "Console" button toggles the visibility of the Console window. If you need to troubleshoot a script there is likely useful diagnostic information already visible in the Console.

The "Refresh" button allows you to reload the tree view listing. This is something you might want to do after modifying the content in the Media Pool/Media page, or if you have changed the currently active bin.


## Script Controls

The "Command Script:" ComboMenu allows you to select a Lua or Python script you would like to run.

The (Edit) button will open the active command script using the script editor defined in the Fusion preferences.

The (Go!) button will run the active command script and use it to process the media that is selected in the tree view.



## Creating a Media Command Script

When a script is launched, it has an "args" global variable that holds a plain-text-formatted Lua table structure.

Note: If you are using Python scripting in Resolve v18, you might have to set Resolve to use Python 2.7 if the built-in API command "bmd.readstring()" is unable to convert a plain-text formatted table into a Python dict. This is done in the "Fusion > Fusion Settings..." menu item. Switch to the "Script" section on the left side of the view and then enable the "Default Python Version > Python 2.7" option in the window.
Edit 2022-11-11: The Resolve v18.1 release fixed a Python 3 scripting API issue so the above mentioned "bmd.readstring()" related bug is.. now resolved. :)

## Bundled Scripts

Copy File Name.lua
Copies the file names from the selected footage into the clipboard buffer.

Copy File Path.lua
Copies the absolute file path from the selected footage into the clipboard buffer.

Copy JSON.lua
Copies the clip properties as JSON-formatted data into the clipboard buffer.

Copy Lua Table.lua
Copies the clip properties as Lua table-formatted data into the clipboard buffer.

List Args
Outputs a Lua table/Python dict with the active clip properties to the Console window.

List Clips
Outputs the clip name from the selected footage to the Console window.

XR/Send to PTGui.lua
Opens a new PTGui session where the currently selected images are auto-loaded into the project.


## Script Syntax

List Args.py Example Script:

# Media Command Script

from pprint import pprint

print("\n\n[List Args]")
pprint(args)

print("\n\n[Dict Content]")
pprint(bmd.readstring(args))

* * *

List Clips.py Example Script:

# Media Command Script

print("\n\n[List Clips]")
dct = bmd.readstring(args)
for clipIndex, clipValue in dct.iteritems():
	print(clipValue["Clip Name"])

* * *

List Args.lua Example Script:

-- Media Command Script

print("[List Args]")
dump(bmd.readstring(args))

* * *

List Clips.lua Example Script:

-- Media Command Script

print("[List Clips]")
local tbl = bmd.readstring(args)
for clipIndex, clipValue in ipairs(tbl) do
	print(clipValue["Clip Name"])
end

* * *

Media Pool Clip Property:

{
	IDT = "",
	["Input Color Space"] = "Project",
	["Input LUT"] = "",
	["Input Sizing Preset"] = "None",
	Keyword = "",
	In = "",
	["Online Status"] = "Online",
	Out = "",
	PAR = "Square",
	["Proxy Media Path"] = "",
	["Reel Name"] = "",
	Resolution = "2048x2048",
	["Roll/Card"] = "",
	["S3D Sync"] = "",
	["Sample Rate"] = "",
	Scene = "",
	Shot = "",
	["Slate TC"] = "00:00:00:00",
	["Start KeyKode"] = "",
	["Start TC"] = "00:00:00:00",
	MediaID = db6ad95d-7112-4204-bd5f-70beb3008ba6
	Angle = "",
	["Synced Audio"] = "",
	Take = "",
	Usage = "0",
	["V-FLIP"] = "Off",
	["Video Codec"] = "JPEG",
	["Alpha mode"] = "None",
	["Noise Reduction"] = "",
	Type = "Still",
	Start = "2",
	Sharpness = "",
	["Drop frame"] = "0",
	Proxy = "None",
	["Enable Deinterlacing"] = "0",
	["Offline Reference"] = "",
	["Audio Bit Depth"] = "",
	["Audio Ch"] = "0",
	["Audio Codec"] = "",
	["Audio Offset"] = "",
	["Bit Depth"] = "8",
	["Camera #"] = "",
	["Clip Color"] = "",
	["Clip Name"] = "fulldome_2K.jpg",
	["Super Scale"] = 1,
	["Data Level"] = "Auto",
	Comments = "",
	["Date Created"] = "Tue Aug 23 2022 00:23:45",
	["Date Modified"] = "Tue Aug 23 00:23:45 2022",
	Description = "",
	Duration = "00:00:00:01",
	End = "2",
	["End TC"] = "00:00:00:01",
	FPS = 24,
	["Field Dominance"] = "Auto",
	["File Name"] = "fulldome_2K.jpg",
	["File Path"] = "/Users/vfx/Reactor/Deploy/Macros/KartaVR/Images/fulldome_2K.jpg",
	Flags = "",
	Format = "JPEG",
	Frames = "1",
	["Date Added"] = "Sat Oct 1 2022 23:18:29",
	["Good Take"] = "",
	["H-FLIP"] = "Off"
},

--]]--

-- Find out the current operating system platform. The platform local variable should be set to either "Windows", "Mac", or "Linux".
local platform = (FuPLATFORM_WINDOWS and 'Windows') or (FuPLATFORM_MAC and 'Mac') or (FuPLATFORM_LINUX and 'Linux')

g_FilterText = ""
g_Type = 0
g_FilterCount = 0

function GetMedia()
	local res = app:GetResolve()
	-- local res = Resolve()
	if res ~= nil then
		local pm = res:GetProjectManager()
		local project = pm:GetCurrentProject()
		local mp = project:GetMediaPool()
		local folder = mp:GetCurrentFolder()

		return folder:GetClips()
	else
		print("[Error] Could not connect to Resolve session.")
	end

	return nil
end


-- Find out the current directory from a file path
-- Example: print(Dirname('/Volumes/Media/image.0000.exr'))
function Dirname(filename)
	return filename:match("(.*[/\\])")
end

-- Scan for Lua and Python scripts in the Media Command folder.
-- Example: local tbl = ScriptScan()
function ScriptScan()
	path = "Lightfielder:/Resolve/Scripts/MediaCommand/"
	pathAbsolute = app:MapPath(path)

	if not bmd.direxists(pathAbsolute) then
		bmd.createdir(pathAbsolute)
		if not bmd.direxists(pathAbsolute) then
			error(string.format("[Create Dir] Failed to create directory: %s", pathAbsolute))
		end
	end

	-- Expand the virtual PathMap segments and parse the output into a list of files
	mp = MultiPath("MediaCommand:")

	-- Create a Lua table that holds a (fake) virtual PathMap table for the folder
	mp:Map({["MediaCommand:"] = pathAbsolute})

	-- Scan the folder recursively
	-- Example: mp:ReadDir(string pattern, boolean recursive, boolean flat hierarchy)
	luaFiles = mp:ReadDir("*.lua", true, true)
	pyFiles = mp:ReadDir("*.py", true, true)

	-- Combine the lua and py directory listings into one table
	local tbl = {}
	for i, file in ipairs(luaFiles) do
		table.insert(tbl, file)
	end
	for i, file in ipairs(pyFiles) do
		table.insert(tbl, file)
	end

	-- Sort the scripts alphabetically
	table.sort(tbl, function(a,b) return a.FullPath < b.FullPath end)

	return tbl
end


-- Usage: FillTree(ui, itm.Tree, "Unchecked")
-- Usage: FillTree(ui, itm.Tree, "Checked")
function FillTree(ui, tree, checked)
	tree:Clear()

	-- Add a header row.
	hdr = tree:NewItem()

	hdr.Text[0] = "Select"
	hdr.Text[1] = "Type"
	hdr.Text[2] = "Clip Name"
	hdr.Text[3] = "File Name"
	hdr.Text[4] = "File Path"
	hdr.Text[5] = "Format"
	hdr.Text[6] = "FPS"
	hdr.Text[7] = "Reel Name"
	hdr.Text[8] = "Scene"
	hdr.Text[9] = "Shot"
	hdr.Text[10] = "Take"

	tree:SetHeaderItem(hdr)

	-- Number of columns in the Tree list
	tree.ColumnCount = 10

	-- Resize the Columns
	tree.ColumnWidth[0] = 60
	tree.ColumnWidth[1] = 125
	tree.ColumnWidth[2] = 190
	tree.ColumnWidth[3] = 302
	tree.ColumnWidth[4] = 600
	tree.ColumnWidth[5] = 100
	tree.ColumnWidth[6] = 100
	tree.ColumnWidth[7] = 100
	tree.ColumnWidth[8] = 100
	tree.ColumnWidth[9] = 100
	tree.ColumnWidth[10] = 100

	-- Change the sorting order of the tree
	tree:SortByColumn(2, "AscendingOrder")
	-- tree:SortByColumn(2, "DescendingOrder")

	local clips = GetMedia()

	for clipIndex, clipValue in ipairs(clips) do
		prop = clipValue:GetClipProperty()
		-- Type: "Still", "Video", "Audio", "Video + Audio", "Geometry", "Generator", "Timeline", "Compound", "Fusion", "Subtitle", "Stereo"
		local clipType = prop["Type"]
		local clipName = prop["Clip Name"]
		local clipID = clipValue:GetMediaId()
		local fileName = prop["File Name"]
		local filePath = prop["File Path"]
		local clipFormat = prop["Format"]
		local clipFPS = prop["FPS"]
		local clipReelName = prop["Reel Name"]
		local clipScene = prop["Scene"]
		local clipShot = prop["Shot"]
		local clipTake = prop["Take"]

		-- Add a new row entry to the list
		itRow = tree:NewItem();

		itRow.Text[0] = ""
		itRow.Text[1] = clipType
		itRow.Text[2] = clipName
		itRow.Text[3] = fileName
		itRow.Text[4] = filePath
		itRow.Text[5] = clipFormat
		itRow.Text[6] = clipFPS
		itRow.Text[7] = clipReelName
		itRow.Text[8] = clipScene
		itRow.Text[9] = clipShot
		itRow.Text[10] = clipTake

		-- Uncheck the new row item
		itRow.CheckState[0] = checked

		-- Type icon
		itRow.Icon[1] = ui:Icon{
			File = "Lightfielder:/Resolve/Scripts/Utility/Lightfielder/Icons/Type/" .. tostring(clipType) .. ".png"
		}

		-- Pass the clip index to the table row as custom data
		itRow:SetData(0, "UserRole", clipIndex)

		tree:AddTopLevelItem(itRow)
	end

	return clips
end

-- Build the Script menu
-- Usage: FillScripts(itm.ScriptMenuCombo)
function FillScripts(menu)
	local scriptsTbl = ScriptScan()
	for i, script in ipairs(scriptsTbl) do
		menu:AddItem(script.FullPath)
	end

	-- print("[Scripts]")
	-- dump(scriptsTbl)

	return scriptsTbl
end

-- Show the ui:Tree View
function MediaCommand()
	local checked = "Unchecked"
	-- local checked = "Checked"

	local ui = fu.UIManager
	local disp = bmd.UIDispatcher(ui)
	-- local width, height = 1600,600
	-- local width, height = 1400,400
	local width, height = 1400,430

	win = disp:AddWindow({
		ID = "MediaCommandWin",
		TargetID = "MediaCommandWin",
		WindowTitle = "Media Command",
		Geometry = {415, 30, width, height},
		Spacing = 0,

		ui:VGroup{
			ID = "root",
			-- Add your GUI elements here:

			-- Tree View Controls
			ui:HGroup{
				Weight = 0.001,
				ui:Label{
					Weight = 0.001,
					ID = "TypeLabel",
					Text = "Type: ",
				},
				ui:ComboBox{
					Weight = 0.01,
					ID = "TypeCombo",
					Text = "Type",
				},
				-- Search
				ui:Label{
					Weight = 0.001,
					ID = "SearchLabel",
					Text = "Search: ",
				},
				ui:LineEdit{
					Weight = 1.0,
					ID = "SearchText",
				},
				-- Add some space
				-- ui:HGap(),
				ui:Label{
					Weight = 0.001,
					ID = "SelectLabel",
					Text = "Select: ",
				},
				ui:Button{
					Weight = 0.01,
					ID = "SelectAllButton",
					Text = "All",
					MinimumSize = {40, 24},
				},
				ui:Button{
					Weight = 0.01,
					ID = "SelectNoneButton",
					Text = "None",
					MinimumSize = {40, 24},
				},
				ui:Button{
					Weight = 0.01,
					ID = "SelectInvertButton",
					Text = "Invert",
					MinimumSize = {40, 24},
				},
				-- Add some space
				-- ui:HGap(),
				ui:Label{
					Weight = 0.001,
					ID = "ViewLabel",
					Text = "View: ",
				},
				-- Keep Open Button
				ui:Button{
					Weight = 0.01,
					ID = "KeepOpenButton",
					Text = "Keep Open",
					MinimumSize = {80, 24},
					Checkable = true,
				},
				ui:Button{
					Weight = 0.01,
					ID = "ConsoleButton",
					Text = "Console",
					MinimumSize = {80, 24},
					Checkable = true,
				},
				ui:Button{
					Weight = 0.01,
					ID = "RefreshButton",
					Text = "Refresh",
					MinimumSize = {60, 24},
				},
			},
			ui:Tree{
				ID = "Tree",
				SortingEnabled = true,
				Events = {
					CurrentItemChanged = true,
					ItemActivated = true,
					ItemChanged = true,
					ItemClicked = true,
					ItemDoubleClicked = true,
				},
			},
			ui:HGroup{
				Weight = 0.01,
				-- Script Menu
				ui:Label{
					ID = "ScriptLabel",
					Text = "Command Script:",
					Weight = 0.01
				},
				ui:ComboBox{
					Weight = 1.0,
					ID = "ScriptMenuCombo",
					Text = "ScriptMenu",

				},
				-- Edit Button
				ui:Button{
					Weight = 0.01,
					ID = "EditButton",
					Text = "Edit",
					MinimumSize = {40, 24},
				},
				-- Go Button
				ui:Button{
					Weight = 0.01,
					ID = "GoButton",
					Text = "Go!",
					MinimumSize = {40, 24},
				},
			},
		},
	})

	-- The window was closed
	function win.On.MediaCommandWin.Close(ev)
		disp:ExitLoop()
	end

	-- Add your GUI element based event functions here:
	itm = win:GetItems()

	-- Build the Script menu
	FillScripts(itm.ScriptMenuCombo)

	-- Add the Type ComboMenu entries
	itm.TypeCombo:AddItem("All")
	itm.TypeCombo:AddItem("Still")
	itm.TypeCombo:AddItem("Video")
	itm.TypeCombo:AddItem("Video + Audio")
	itm.TypeCombo:AddItem("Audio")
	itm.TypeCombo:AddItem("Compound")
	itm.TypeCombo:AddItem("Fusion")
	itm.TypeCombo:AddItem("Generator")
	itm.TypeCombo:AddItem("Geometry")
	itm.TypeCombo:AddItem("Stereo")
	itm.TypeCombo:AddItem("Subtitle")
	itm.TypeCombo:AddItem("Timeline")

	-- Turn on the Keep Open button by default
	itm.KeepOpenButton.Checked = true

	-- Fill the tree with Media Pool clips
	local clips = FillTree(ui, itm.Tree, checked)

	function win.On.TypeCombo.CurrentIndexChanged(ev)
		g_Type = itm.TypeCombo.CurrentText
		FilterTree(itm.Tree, clips)
	end

	function win.On.SearchText.TextChanged(ev)
		g_FilterText = ev.Text
		FilterTree(itm.Tree, clips)

		if g_FilterText and g_FilterText ~= "" then
			itm.MediaCommandWin.WindowTitle = "Media Command | Searching for \"" .. tostring(g_FilterText) .. "\" | " .. tostring(g_FilterCount) .. (g_FilterCount == 1 and " item found" or " items found")
		else
			itm.MediaCommandWin.WindowTitle = "Media Command"
		end
	end

	-- Edit button was clicked
	function win.On.EditButton.Clicked(ev)
		local scriptPath = itm.ScriptMenuCombo.CurrentText
		-- local scriptPath = app:MapPath('Lightfielder:/Resolve/Scripts/Utility/Lightfielder/18 Media Command.lua')

		-- Open the script using Fusion's default editor in the Fusion preferences.
		editorPath = fu:GetPrefs('Global.Script.EditorPath')
		if editorPath == nil or editorPath == "" then
			comp:Print('[Script Error] The "Editor Path" is empty. Please choose a text editor in the Fusion Preferences "Global and Default Settings > Script > Editor Path" section.\n')
			app:ShowPrefs("PrefsScript")
		else
			-- Open the script for editing
			OpenDocument('Edit Script', editorPath, scriptPath)
		end
	end


	-- A Tree view row was clicked on
	function win.On.Tree.ItemClicked(ev)
		if ev.item then
			local id = ev.item:GetData(0, "UserRole")
			-- print(id)
			if ev.column >= 1 then
				if ev.item.CheckState[0] == "Checked" then
					-- Remove the item
					ev.item.CheckState[0] = "Unchecked"
				elseif ev.item.CheckState[0] == "Unchecked" then
					-- Add the item
					ev.item.CheckState[0] = "Checked"
				end
			end
		end
	end

	-- The Select "All" button was pressed
	function win.On.SelectAllButton.Clicked(ev)
		-- print("[Select All]")

		for i = 0, itm.Tree:TopLevelItemCount() - 1 do
			local item = itm.Tree:TopLevelItem(i)

			if item.Hidden == false then
				-- Add the item
				item.CheckState[0] = "Checked"
				local id = item:GetData(0, "UserRole")
			end
		end
	end

	-- The Select "None" button was pressed
	function win.On.SelectNoneButton.Clicked(ev)
		-- print("[Select None]")

		for i = 0, itm.Tree:TopLevelItemCount() - 1 do
			local item = itm.Tree:TopLevelItem(i)
			if item.Hidden == false then
				-- Remove the item
				item.CheckState[0] = "Unchecked"
				local id = item:GetData(0, "UserRole")
			end
		end
	end

	-- The Select "Invert" button was pressed
	function win.On.SelectInvertButton.Clicked(ev)
		-- print("[Select Invert]")

		for i = 0, itm.Tree:TopLevelItemCount() - 1 do
			local item = itm.Tree:TopLevelItem(i)
			local id = item:GetData(0, "UserRole")
			-- print(id)
			if item.Hidden == false then
				if item.CheckState[0] == "Checked" then
					-- Remove the item
					item.CheckState[0] = "Unchecked"
				elseif item.CheckState[0] == "Unchecked" then
					-- Add the item
					item.CheckState[0] = "Checked"
				end
			end
		end
	end
	
	-- The "Console" button was toggled
	function win.On.ConsoleButton.Clicked(ev)
		if itm.ConsoleButton.Checked == true then
			-- Show the Console window
			app:DoAction("Console_Show", {show = true})
		else
			-- Hide the Console window
			app:DoAction("Console_Show", {show = false})
		end
	end

	-- The "Refresh" button was pressed
	function win.On.RefreshButton.Clicked(ev)
		-- Build the Script menu
		-- FillScripts(itm.ScriptMenuCombo)
		
		-- Fill the tree with Media Pool clips
		clips = FillTree(ui, itm.Tree, checked)
	end

	-- The "Go" button was pressed
	function win.On.GoButton.Clicked(ev)
		-- After pressing "Go!" should the Media Command window stay open?
		if itm.KeepOpenButton.Checked == false then
			disp:ExitLoop()
		end
		
		-- Hide the Media Command window while the script is running
		-- win:Hide()

		-- Create the clip selection table
		local clipSelect = {}
		for i = 0, itm.Tree:TopLevelItemCount() - 1 do
			local item = itm.Tree:TopLevelItem(i)
			local id = item:GetData(0, "UserRole")
			-- print(id)

			-- The item needs to be visible and checked
			if item.CheckState[0] == "Checked" and item.Hidden == false then
				-- Grab the clip property table
				local clipTbl = clips[id]:GetClipProperty()

				-- Append the MediaID tag into the clip property table
				clipTbl["MediaID"] = clips[id]:GetMediaId()

				-- Append the clip property table
				table.insert(clipSelect, clipTbl)
			end
		end

--		print("\n[Media Items]")
--		for id, v in pairs(clipSelect) do
--			print(v["Clip Name"])
--		end

		-- print("\n[Media Table]")
		-- dump(clipSelect)

		-- Convert the Lua table into a plain text output
		argsString = bmd.writestring(clipSelect)

		-- Get the selected script
		local scriptPath = itm.ScriptMenuCombo.CurrentText
		print("\n[Media Command Script] " .. tostring(scriptPath))

		-- Launch the script
		app:RunScript(scriptPath, {args = argsString})

		-- Restore the Media Command window
		-- win:Show()
	end

	-- The app:AddConfig() command that will capture the "Escape", "Control + W" or "Control + F4" hotkeys so they will close the window instead of closing the foreground composite.
	app:AddConfig("MediaCommandWin", {
		Target {
			ID = "MediaCommandWin",
		},

		Hotkeys {
			Target = "MediaCommandWin",
			Defaults = true,

			CONTROL_W = "Execute{cmd = [[app.UIManager:QueueEvent(obj, 'Close', {})]]}",
			CONTROL_F4 = "Execute{cmd = [[app.UIManager:QueueEvent(obj, 'Close', {})]]}",
			ESCAPE = "Execute{cmd = [[app.UIManager:QueueEvent(obj, 'Close', {})]]}",
		},
	})

	-- Make the go button the default input
	itm.GoButton:SetFocus("OtherFocusReason")

	win:Show()
	disp:RunLoop()
	win:Hide()

	app:RemoveConfig("MediaCommandWin")
	collectgarbage()
end

function TypeCheck(str)
	if g_Type == "All" then
		return 1
	elseif g_Type == str then
		return 1
	else
		return 0
	end
end

function FilterTree(tree, clips)
	tree.UpdatesEnabled = false
	tree.SortingEnabled = false

	local key = g_FilterText:lower()
	g_FilterCount = 0

	for i = 0, tree:TopLevelItemCount() - 1 do
		local item = tree:TopLevelItem(i)
		local id = item:GetData(0, "UserRole")
		-- print(id)

		-- Grab the clip property table
		local clipTbl = clips[id]:GetClipProperty()
		-- Search through the Clip Name and File Name elements
		if (clipTbl["Clip Name"]:lower():match(key) or clipTbl["File Name"]:lower():match(key)) and TypeCheck(clipTbl["Type"]) == 1 then
			g_FilterCount = g_FilterCount + 1
			item.Hidden = false
		else
			item.Hidden = true
		end
	end

	tree.UpdatesEnabled = true
	tree.SortingEnabled = true
end

function OpenDocument(title, appPath, docPath)
	if platform == 'Windows' then
		-- Running on Windows
		command = 'start "" "' .. appPath .. '" "' .. docPath .. '" &'
	elseif platform == 'Mac' then
		-- Running on Mac
		command = 'open -a "' .. appPath .. '" "' .. docPath .. '" &'
	 elseif platform == "Linux" then
		-- Running on Linux
		command = '"' .. appPath .. '" "' .. docPath .. '" &'
	else
		print('[Error] There is an invalid Fusion platform detected')
		return
	end

	print('[' .. title .. '] [App] "' .. appPath .. '" [Document] "' .. docPath .. '"\n')
	-- comp:Print('[Launch Command] ' .. tostring(command) .. '\n')
	os.execute(command)
end

function Main()
	MediaCommand()
	-- print("[Done]\n")
end

Main()
