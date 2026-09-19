--[[--
Send to PTGui 2026-09-18 09.20 PM

--]]--

-- Find out the current operating system platform. The platform local variable should be set to either "Windows", "Mac", or "Linux".
local platform = (FuPLATFORM_WINDOWS and "Windows") or (FuPLATFORM_MAC and "Mac") or (FuPLATFORM_LINUX and "Linux")

------------------------------------------------------------------------------
-- parseSequenceFilename()
-- 2022-10-16 8.41 PM
--
-- Process Resolve Media Pool/Media page centric file paths like:
-- D:\Media\Image.[0001-0240].exr
-- D:\Media\Image.0001.exr
-- D:\Media\Image_0001.exr
-- D:\Media\Image.exr
-- D:\Media\Image.mp4
--
-- Code adapted from bmd.scriptlib function "bmd.parseFilename(filename)"
--
-- This is a great function for ripping a filepath into little bits
-- returns a table with the following
--
-- FullPath     : The raw, original path sent to the function
-- Path         : The path, without filename
-- FullName     : The name of the clip w\ extension
-- Name         : The name without extension
-- CleanName    : The name of the clip, without extension or sequence
-- SNumStart    : The original starting frame sequence string, or "" if no sequence
-- SNumEnd      : The original ending frame sequence string, or "" if no sequence
-- FrameStart   : The starting frame sequence as a numeric value, or nil if no sequence
-- FrameEnd     : The ending frame sequence as a numeric value, or nil if no sequence
-- Extension    : The raw extension of the clip
-- Padding      : Amount of padding in the sequence, or nil if no sequence
-- UN           : A true or false value indicating whether the path is a UNC path or not
------------------------------------------------------------------------------
function parseSequenceFilename(filename)
	local seq = {}
	seq.FullPath = filename
	string.gsub(seq.FullPath, "^(.+[/\\])(.+)", function(path, name) seq.Path = path;seq.FullName = name end)
	--string.gsub(seq.FullName, "^(.+)(%..+)%[%..+%]$", function(name, ext) seq.Name = name;seq.Extension = ext end)
	string.gsub(seq.FullName, "^(.+)(%..+)$", function(name, ext) seq.Name = name;seq.Extension = ext end)

	if not seq.Name then -- no extension?
		seq.Name = seq.FullName
	end

	if string.match(seq.Name, "%[.-%-.-%]$") then
		-- Match Video/Video + Audio clip types with image sequence filenames like: "/Path/Name.[####-####].ext"
		string.gsub(seq.Name, "^(.-)%[(%d+)%-(%d+)%]$", function(name, SNumStart, SNumEnd) seq.CleanName = name;seq.SNumStart = SNumStart;seq.SNumEnd = SNumEnd end)
	else
		-- Match Stills/Video/Video + Audio/Geometry/Subtitles clip types with filenames like: "/Path/Name.####.ext" or "/Path/Name.ext"
		string.gsub(seq.Name, "^(.-)(%d+)$", function(name, SNum) seq.CleanName = name;seq.SNumStart = SNum;seq.SNumEnd = SNum end)
	end

	if seq.SNumStart then
		seq.FrameStart = tonumber(seq.SNumStart)
		seq.Padding = string.len(seq.SNumStart)
	else
		seq.SNumStart = ""
		seq.CleanName = seq.Name
	end

	if seq.SNumEnd then
		seq.FrameEnd = tonumber(seq.SNumEnd)
	else
		seq.SNumEnd = ""
	end

	if seq.Extension == nil then seq.Extension = "" end
	seq.UNC = (string.sub(seq.Path, 1, 2) == [[\\]])

	return seq
end

------------------------------------------------------------------------------
-- inflateSequenceFilename()
-- 2022-10-16 10.01 PM
--
-- Generate the per-frame filenames for an image sequence defined in the Lua table
-- output from the parseSequenceFilename() function.
--
-- Returns a table with filename strings
------------------------------------------------------------------------------
function inflateSequenceFilename(tbl, sequenceMode, referenceFrameNum)
	local seq = {}
	local frames = 0

	if tbl and tbl.FrameStart and tbl.FrameEnd then
		if sequenceMode == 0 then
			-- Expand the full image sequence frame range
			for i = tonumber(tbl.FrameStart), tonumber(tbl.FrameEnd) do
				frames = frames + 1

				local paddedFrame = tostring(string.format('%0' .. tbl.Padding .. 'd', tonumber(i)))
				local file = tostring(tbl.Path) .. tostring(tbl.CleanName) .. paddedFrame .. tostring(tbl.Extension)

				seq[frames] = file
			end
		elseif sequenceMode == 1 then
			-- Use the start frame
			frames = frames + 1

			local paddedFrame = tostring(string.format('%0' .. tbl.Padding .. 'd', tonumber(tbl.FrameStart)))
			local file = tostring(tbl.Path) .. tostring(tbl.CleanName) .. paddedFrame .. tostring(tbl.Extension)

			seq[frames] = file
		elseif sequenceMode == 2 then
			-- Use the end frame
			frames = frames + 1

			local paddedFrame = tostring(string.format('%0' .. tbl.Padding .. 'd', tonumber(tbl.FrameEnd)))
			local file = tostring(tbl.Path) .. tostring(tbl.CleanName) .. paddedFrame .. tostring(tbl.Extension)

			seq[frames] = file
		else
			-- Use a fixed reference frame
			frames = frames + 1

			local paddedFrame = tostring(string.format('%0' .. tbl.Padding .. 'd', tonumber(referenceFrameNum)))
			local file = tostring(tbl.Path) .. tostring(tbl.CleanName) .. paddedFrame .. tostring(tbl.Extension)

			seq[frames] = file
		end
	elseif tbl then
		frames = frames + 1

		seq[frames] = tostring(tbl.FullPath)
	end

	return seq
end

function GenerateMediaList(prefs)
	if prefs.Cancel == true then
		return ""
	end

	local str = ""
	local frameNum = 0
	local tbl = bmd.readstring(args)
	for clipIndex, clipValue in ipairs(tbl) do
		if clipValue["Type"] == "Still" or clipValue["Type"] == "Video" or clipValue["Type"] == "Video + Audio" then
			local path = clipValue["File Path"]

			local clipTbl = parseSequenceFilename(path)
			local fileTbl = inflateSequenceFilename(clipTbl, prefs.SequenceProcess, prefs.ReferenceFrame)

			for i, v in ipairs(fileTbl) do
				frameNum = frameNum + 1
				str = str .. ' "' .. v .. '"'
			end
		end
	end

	-- print("\n[Clip File Path] " .. tostring(str) .. "\n")

	return str
end

function UserSettings()
	local prefsTbl = {}

	local ui = fu.UIManager
	local disp = bmd.UIDispatcher(ui)
	local width, height = 415, 320

	win = disp:AddWindow({
		ID = "settingsWin",
		TargetID = "settingsWin",
		WindowTitle = "Send to PTGui",
		Geometry = {0, 30, width, height},
		Spacing = 0,

		ui:VGroup{
			ID = "root",
			-- Add your GUI elements here:
			ui:Button{
				ID = "KartaVRIconButton",
				Weight = 0,
				IconSize = {200,94},
				Icon = ui:Icon{
					File = "Scripts:/Support/Kartaverse/KartaVR_Logo.png"
				},
				MinimumSize = {
					200,
					94,
				},
				Flat = true,
			},
			ui:TextEdit{
				Weight = 1.0,
				ID = "InfoTxt",
				Text = "This script opens up a new PTGui Pro session. The currently selected images from the Media Command window will be auto-loaded into the PTGui project.",
				StyleSheet = "QTextEdit { border: 0px; }",
				ReadOnly = true
			},
			ui:VGap(),
			ui:Label{
				Weight = 0.01,
				ID = "SquenceLabel",
				Text = "Image Sequence Processing: ",
			},
			ui:ComboBox{
				Weight = 0.01,
				ID = "SequenceCombo",
			},
			ui:VGroup{
				Weight = 0.01,
				ID = "ReferenceVGrp",
				ui:Label{
					Weight = 0.01,
					ID = "ReferenceLabel",
					Text = "Reference Frame Number: ",
				},
				ui:SpinBox{
					Weight = 0.01,
					ID = "ReferenceFrameSpinner",
					Value = 1,
					Minimum = 0,
					Maximum = 10000,
					Events = {
						ValueChanged = true,
					},
				},
			},
			ui:VGap(),
			ui:HGroup{
				Weight = 0.01,
				ui:Button{
					Weight = 0.01,
					ID = "CancelButton",
					Text = "Cancel",
					MinimumSize = {60, 24},
				},
				-- OK Button
				ui:Button{
					Weight = 0.01,
					ID = "OKButton",
					Text = "OK",
					MinimumSize = {40, 24},
				},
			},
		},
	})

	-- The window was closed
	function win.On.settingsWin.Close(ev)
		prefsTbl.Cancel = true
		disp:ExitLoop()
	end


	-- Add your GUI element based event functions here:
	itm = win:GetItems()

	-- Add the items to the ComboBox menu
	itm.SequenceCombo:AddItem("Load Full Image Sequence")
	itm.SequenceCombo:AddItem("Use the Start Frame")
	itm.SequenceCombo:AddItem("Use the End Frame")
	itm.SequenceCombo:AddItem("Use Static Reference Frame")

	-- Cancel button was pressed
	function win.On.CancelButton.Clicked(ev)
		prefsTbl.Cancel = true
		disp:ExitLoop()
	end

	-- The "OK" button was pressed
	function win.On.OKButton.Clicked(ev)
		prefsTbl.SequenceProcess = itm.SequenceCombo.CurrentIndex
		prefsTbl.ReferenceFrame = itm.ReferenceFrameSpinner.Value
		disp:ExitLoop()
	end

	-- The app:AddConfig() command that will capture the "Escape", "Control + W" or "Control + F4" hotkeys so they will close the window instead of closing the foreground composite.
	app:AddConfig("settingsWin", {
		Target {
			ID = "settingsWin",
		},

		Hotkeys {
			Target = "settingsWin",
			Defaults = true,

			CONTROL_W = "Execute{cmd = [[app.UIManager:QueueEvent(obj, 'Close', {})]]}",
			CONTROL_F4 = "Execute{cmd = [[app.UIManager:QueueEvent(obj, 'Close', {})]]}",
			ESCAPE = "Execute{cmd = [[app.UIManager:QueueEvent(obj, 'Close', {})]]}",
		},
	})

	win:Show()
	disp:RunLoop()
	win:Hide()

	app:RemoveConfig("settingsWin")
	collectgarbage()

	-- print("  [Prefs]")
	-- dump(prefsTbl)

	return prefsTbl
end

function OpenProgram(media, prefs)
	-- Viewer Variables
	local viewerProgram
	local command

	if prefs.Cancel == true then
		print("  [Canceled]")
		return
	end

	-- Open the Viewer tool
	if platform == "Windows" then
		-- Running on Windows
		viewerProgram = "C:\\Program Files\\PTGui\\PTGui.exe"
		command = 'start "" "' .. viewerProgram .. '" ' .. media

		print("\n[Launch Command] ", command)
		os.execute(command)
	elseif platform == "Mac" then
		-- Running on Mac
		viewerProgram = "/Applications/PTGui Pro.app"
		command = 'open -a "' .. viewerProgram .. '" --args ' .. media

		print("\n[Launch Command] ", command)
		os.execute(command)
	elseif platform == 'Linux' then
		-- Running on Linux
		print("  [Warning] PTGui compatibility has not been tested on Linux yet.")

		viewerProgram = "/opt/PTGui/PTGui"
		command = '"' .. viewerProgram .. '" ' .. media .. ' &'

		print("\n[Launch Command] ", command)
		os.execute(command)
	else
		print("[Platform] ", platform)
		print("There is an invalid platform defined in the local platform variable at the top of the code.")
	end
end

function Main()
	print("\n[Send To PTGui]")

	-- Check the settings
	prefs = UserSettings()

	-- Check the active selection and return a list of media files
	mediaList = GenerateMediaList(prefs)

	-- Open PTGui
	OpenProgram(mediaList, prefs)
end

Main()
