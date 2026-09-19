--[[--
Lightfielder Fusion Render Time Profiler 2026-09-19 12.20 AM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Based on Sven Neve's "RenderTimeViz_Ultra.lua" script.

# Overview

Quickly view the render time for each of the nodes in your BMD Fusion Studio composite. This helps optimize your comps to be more efficient by tracking down the slowest operations in the comp that are sucking up the most clock cycles.

--]]--

function round(num)
	return math.floor(num + 0.5)
end

function hsv(h, s, v)
	h = h * 360
	if s == 0 then
		r = v
		g = v
		b = v
		return {r, g, b}
	end

	h = h / 60
	i = math.floor(h)
	f = h - i
	p = v * (1 - s)
	q = v * (1 - s * f)
	t = v * (1 - s * (1 - f))

	if i == 0 then
			r = v
			g = t
			b = p
	elseif i == 1 then
			r = q
			g = v
			b = p
		elseif i == 2 then
			r = p
			g = v
			b = t
		elseif i == 3 then
			r = p
			g = q
			b = v
		elseif i == 4 then
			r = t
			g = p
			b = v
		else
			r = v
			g = p
			b = q
		end
	return {r, g, b}
end

-- Find out the current operating system platform. The platform variable should be set to either 'Windows', 'Mac', or 'Linux'.
platform = (FuPLATFORM_WINDOWS and 'Windows') or (FuPLATFORM_MAC and 'Mac') or (FuPLATFORM_LINUX and 'Linux')

-- Add the platform specific folder slash character
osSeparator = package.config:sub(1,1)

------------------------------------------------------------------------------
-- parseFilename()
--
-- this is a great function for ripping a filepath into little bits
-- returns a table with the following
--
-- FullPath	: The raw, original path sent to the function
-- Path		: The path, without filename
-- FullName	: The name of the clip w\ extension
-- Name     : The name without extension
-- CleanName: The name of the clip, without extension or sequence
-- SNum		: The original sequence string, or "" if no sequence
-- Number 	: The sequence as a numeric value, or nil if no sequence
-- Extension: The raw extension of the clip
-- Padding	: Amount of padding in the sequence, or nil if no sequence
-- UNC		: A true or false value indicating whether the path is a UNC path or not
------------------------------------------------------------------------------
function ParseFilename(filename)
	local seq = {}
	seq.FullPath = filename
	string.gsub(seq.FullPath, "^(.+[/\\])(.+)", function(path, name) seq.Path = path seq.FullName = name end)
	string.gsub(seq.FullName, "^(.+)(%..+)$", function(name, ext) seq.Name = name seq.Extension = ext end)

	if not seq.Name then -- no extension?
		seq.Name = seq.FullName
	end

	string.gsub(seq.Name,     "^(.-)(%d+)$", function(name, SNum) seq.CleanName = name seq.SNum = SNum end)

	if seq.SNum then
		seq.Number = tonumber( seq.SNum )
		seq.Padding = string.len( seq.SNum )
	else
	   seq.SNum = ""
	   seq.CleanName = seq.Name
	end

	if seq.Extension == nil then seq.Extension = "" end
	seq.UNC = ( string.sub(seq.Path, 1, 2) == [[\\]] )

	return seq
end

function csvWrite(path)
	data = UpdateTree()
	local file = assert(io.open(path, "w"))
	if file then
		file:write(data)
		file:close()
	end
	print("[Lightfielder] Exported Render Time Profiler CSV data to [" .. path .. "]")
end

function Dirname(filename)
	-- Find out the current directory from a file path
	-- Example: print(Dirname("/Volumes/Media/image.exr"))
	return filename:match('(.*' .. tostring(osSeparator) .. ')')
end

-- Open a folder window up using your desktop file browser
function OpenDirectory(mediaDirName)
	command = nil
	dir = Dirname(mediaDirName)

	-- Open a folder view using the os native command
	if platform == 'Windows' then
		-- Running on Windows
		command = 'explorer "' .. dir .. '"'

		-- print("[Launch Command] ", command)
		os.execute(command)
	elseif platform == 'Mac' then
		-- Running on Mac
		command = 'open "' .. dir .. '" &'

		-- print("[Launch Command] ", command)
		os.execute(command)
	elseif platform == 'Linux' then
		-- Running on Linux
		command = 'nautilus "' .. dir .. '" &'

		-- print("[Launch Command] ", command)
		os.execute(command)
	else
		print('[Platform] ', platform)
		print('There is an invalid platform defined in the local platform variable at the top of the code.')
	end

	print('[Opening Directory] ' .. dir)
end


function main()
	-- Check if Fusion is running
	if not fusion then
		print("[Lightfielder][Error] This is a Resolve Studio or Fusion Studio based .lua script. It should be run from within Fusion.")
	end

	toollist_rendertime = {}
	max_rendertime = 0
	min_rendertime = 0

	local ui = fu.UIManager
	local disp = bmd.UIDispatcher(ui)
	local width, height = 1280,600

	win = disp:AddWindow({
		ID = "RenderProfilerWin",
		TargetID = "RenderProfilerWin",
		WindowTitle = "Render Time Profiler",
		Geometry = {100, 170, width, height},
		Spacing = 0,

		ui:VGroup{
			ID = "root",
			ui:HGroup{
				Weight = 0.01,
				-- Add your GUI elements here:
				ui:Label{
					ID = "InfoLabel",
					Text = "Quickly view the render time for each of the nodes in your BMD Fusion Studio composite. This helps optimize your comps to be more efficient by tracking down the slowest operations in the comp that are sucking up the most clock cycles.",
					WordWrap = true,
					Alignment = {
						AlignTop = true
					},
					Font = ui:Font{
						PixelSize = 12,
					},
					MinimumSize = {600, 40},
				},
			},
			ui:Tree{
				ID = "Tree",
				SortingEnabled = true,
				Events = {
					ItemDoubleClicked = true,
					ItemClicked = true
				},
			},
			ui:HGroup{
				Weight = 0,
				-- Add your GUI elements here:
				ui:Label{
					ID = "CommentLabel",
					Text = "",
					Alignment = {
						AlignHCenter = true,
						AlignTop = true
					},
				},
			},
			ui:HGroup{
				Weight = 0,
				ui:Button{
					ID = "Cancel",
					Text = "Cancel"
				},
				ui:Button{
					ID = "Refresh",
					Text = "Refresh"
				},
				ui:Button{
					ID = "SaveCSV",
					Text = "Save CSV"
				},
			},
		},
	})

	-- The window was closed
	function win.On.RenderProfilerWin.Close(ev)
		disp:ExitLoop()
	end

	function win.On.Cancel.Clicked(ev)
		disp:ExitLoop()
	end

	function win.On.Refresh.Clicked(ev)
		UpdateTree()
	end

	-- Add your GUI element based event functions here:
	itm = win:GetItems()

	-- The Fusion "Render" command was used
	function disp.On.Comp_Render_End(ev)
		print('[Lightfielder][Update] Render Job Complete. Refreshing the view.')
		UpdateTree()
	end

	-- The Fusion Render cancelled command was used
	function disp.On.Comp_Abort(ev)
		print('[Lightfielder][Update] Render Job Cancelled. Refreshing the view.')
		UpdateTree()
	end

	-- The Fusion comp was closed
	function disp.On.Comp_Close(ev)
		print('[Lightfielder][Update] Comp Closed. Refreshing the view.')
		UpdateTree()
	end

	-- The Fusion comp was opened
	function disp.On.Comp_Open(ev)
		print('[Lightfielder][Update] Comp Opened. Refreshing the view.')
		UpdateTree()
	end

	-- The Fusion comp was opened
	function disp.On.Comp_Recent_Open(ev)
		print('[Lightfielder][Update] Comp Opened. Refreshing the view.')
		UpdateTree()
	end

	-- Copy the filepath to the clipboard when a Tree view row is clicked on
	function win.On.Tree.ItemClicked(ev)
		toolName = ev.item.Text[1]
		comp:SetActiveTool(comp:FindTool(toolName))
		-- Copy the tool name to the clipboard
		CopyToClipboard(toolName)
		-- print('[Lightfielder][Item Selected] ' .. toolName)
		-- print('\n')
	end

	function win.On.SaveCSV.Clicked(ev)
		compName = comp:GetAttrs().COMPS_FileName
		if compName == "" then
			print("[Lightfielder] Saving the comp!")
			comp:Save()
		else
			local parsed = ParseFilename(compName)
			local cleanName = parsed.CleanName
			local parent = comp:MapPath(parsed.Path)
			path = parent .. cleanName .. "_Profiler.csv"
			csvWrite(path)
			OpenDirectory(parent)
		end
	end

	-- Update the contents of the tree view
	function UpdateTree()
		comp = app:GetAttrs().FUSIONH_CurrentComp
		win.WindowTitle = "Render Time Profiler | " .. tostring(comp:GetAttrs().COMPS_Name or "")

		max_rendertime = 0
		min_rendertime = 0

		toollist = comp:GetToolList(true)
		if table.getn(toollist) == 0 then
			toollist = comp:GetToolList()
		end

		if table.getn(toollist) == 0 then
			itm.CommentLabel.Text = "[Lightfielder][Error] No tools selected and comp seems to be empty."
		end

		-- Collect max and min rendertimes
		for i, tool in ipairs(toollist) do
			attrs = tool:GetAttrs()
			if attrs ~= nil then
				last_rendertime = attrs.TOOLN_LastFrameTime
				if last_rendertime ~= nil then
					max_rendertime = math.max(max_rendertime, last_rendertime)
					min_rendertime = math.min(min_rendertime, last_rendertime)
				end
			end
		end

		itm.CommentLabel.Text = string.format("Per-node Rendertime [Min] %12.08f Seconds /  [Max] %12.08f Seconds", min_rendertime, max_rendertime)

		-- Clean out the previous entries in the Tree view
		itm.Tree:Clear()

		-- Add the Tree headers:
		hdr = itm.Tree:NewItem()
		hdr.Text[0] = "Render Time (Sec)"
		hdr.Text[1] = "Normalized Time"
		hdr.Text[2] = "Node Name"
		hdr.Text[3] = "Node Type"
		hdr.Text[4] = "Heatmap"
		itm.Tree:SetHeaderItem(hdr)

		-- Number of columns in the Tree list
		itm.Tree.ColumnCount = 5

		-- Resize the header column widths
		itm.Tree.ColumnWidth[0] = 125
		itm.Tree.ColumnWidth[1] = 116
		itm.Tree.ColumnWidth[2] = 265
		itm.Tree.ColumnWidth[3] = 223
		itm.Tree.ColumnWidth[4] = 720

		-- Color values
		hue_min = 0
		hue_max = 0.6
		hue_curve = 1
		hue_reverse = 1
		val_curve = 1
		val_min = 0.5
		val_max = 1
		val_reverse = 0
		saturation = 1

		min_normalize = min_rendertime
		max_normalize = max_rendertime

		csv = "Render Time (Sec),Normalized Time,Node Name,Node Type\n"
		for i, tool in ipairs(toollist) do
			attrs = tool:GetAttrs()
			last_rendertime = math.min(1,(attrs.TOOLN_LastFrameTime - min_normalize) / (max_normalize - min_normalize))
			last_rendertime_hue = last_rendertime
			last_rendertime_val = last_rendertime

			if hue_reverse == 1 then
				last_rendertime_hue = 1 - last_rendertime
			end

			if val_reverse == 1 then
				last_rendertime_val = 1 - last_rendertime
			end

			rgb = hsv(math.min(1, hue_min + (math.min(1, last_rendertime_hue ^ hue_curve) * (hue_max - hue_min))), saturation, (val_min + math.min(1, last_rendertime_val ^ val_curve) * (val_max - val_min)))

			-- Add an new entry to the list
			itLoader = itm.Tree:NewItem()
			itLoader.Text[0] = string.format("%012.8f", attrs.TOOLN_LastFrameTime)
			itLoader.Text[1] = string.format("%06.2f", last_rendertime * 100)
			itLoader.Text[2] = tostring(tool.Name)
			itLoader.Text[3] = tostring(tool.ID)
			itLoader.BackgroundColor[4] = {R = rgb[1], G = rgb[2], B = rgb[3], A = 1}
			csv = csv .. string.format("%s,%s,%s,%s\n", itLoader.Text[0], itLoader.Text[1], itLoader.Text[2], itLoader.Text[3])
			itm.Tree:AddTopLevelItem(itLoader)
		end

		return csv
	end

	-- Update the contents of the tree view
	UpdateTree()

	-- Track the Fusion events
	notify1 = ui:AddNotify("Comp_Abort")
	notify2 = ui:AddNotify("Comp_Render_End")
	notify3 = ui:AddNotify("Comp_Close")
	notify4 = ui:AddNotify("Comp_Open")
	notify5 = ui:AddNotify("Comp_Recent_Open")

	-- The app:AddConfig() command that will capture the "Control + W" or "Control + F4" hotkeys so they will close the window instead of closing the foreground composite.
	app:AddConfig("RenderProfilerWin", {
		Target {
			ID = "RenderProfilerWin",
		},

		Hotkeys {
			Target = "RenderProfilerWin",
			Defaults = true,

			CONTROL_W = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
			CONTROL_F4 = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
		},
	})

	win:Show()
	disp:RunLoop()
	win:Hide()

	app:RemoveConfig("RenderProfilerWin")
end

-- Run main
main()
print("[Done]")
