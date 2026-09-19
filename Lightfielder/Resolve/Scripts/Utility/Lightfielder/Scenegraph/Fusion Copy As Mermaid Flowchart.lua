--[[
Lightfielder Fusion Copy As Mermaid Flowchart 2026-09-19 12.35 AM (UTC -3)
By Andrew Hazelden

This script copies the currently selected nodes in a Fusion composite to the copy/paste clipboard buffer as a Mermaid flowchart.

Mermaid is an open-source graphing format that allows you to create vector charts that can be saved to a Markdown format and rendered inline in a webpage.

https://mermaid.ai/open-source/syntax/flowchart.html

The WSL forum supports Mermaid graphs embedded in a pair of BBCode tags:
[mermaid][/mermaid]

GitHub Flavoured Markdown supports Mermaid graphs embedded in a pair of code tags:
```mermaid
```

Known Issues:
- GroupOperator and MacroOperator items are not handled correctly.

Tip: The internal nodes are used to generate the flowchart when you run this script with nothing selected in the node graph. If the Group node is selected, the input and output connections are not added to the Mermaid graph.

--]]

-- ----------------------
--  Customization Options
-- -----------------------

-- Mermaid Output Wrapper - Should BBCode tags or Markdown tags be used?
-- local outputWrapper = "BBCode"
local outputWrapper = "Markdown"

-- Should the graph be rendered using a left/right or top/bottom orientation?
-- local flowShape = "LR"
local flowShape = "TB"

-- ----------------------
-- ----------------------

-- ------------------
--  Mermaid elements
-- ------------------
local mermaidContent = ""

-- Colors
local classDef = ""

-- Node Connections
local connections = ""

-- Node Names
local class = ""

-- Check if nodes are selected
local tools = comp:GetToolList(true)

-- Fusion Registry Listing
reg_map = fusion:GetRegList()

-- ------------------

function Color(tbl)
	-- RGB to HEX Color Conversions
	local hexString = "B9B097"
	if tbl and tbl.TileColor then
		local r, g, b = tbl.TileColor.R, tbl.TileColor.G, tbl.TileColor.B
		hexString = string.format("%02X%02X%02X",
			math.floor(r * 255),
			math.floor(g * 255),
			math.floor(b * 255)
		)
	end

	return hexString
end

-- Fallback to use all nodes since nothing was selected
if #tools > 0 then
	print("[Lightfielder][Copy As Mermaid] Selected Nodes")
	-- dump(tools)
else
	print("[Lightfielder][Copy As Mermaid] Nothing Selected - Using all nodes in comp")
	tools = comp:GetToolList(false)
	-- dump(tools)
end

print("[Lightfielder][Node List]")
if comp and comp.CurrentFrame and comp.CurrentFrame.FlowView then
	local flow = comp.CurrentFrame.FlowView
	for i, tool in ipairs(tools) do
		-- Get the node location in the flow
		local x, y = flow:GetPos(tool)

		if x == nil then
			x = 0
		end
		if y == nil then
			y = 0
		end

		-- Translate to Mermaid
		print(string.format("\t[#] %3d [Node Name] %20s [Reg ID] %20s [Pos XY] %f, %f", tonumber(i), tostring(tool:GetAttrs().TOOLS_Name), tostring(tool.ID), x, y))
	end
end

print("\n[Lightfielder][Copy As Mermaid][Graph Output]")
if comp and comp.CurrentFrame and comp.CurrentFrame.FlowView then
	print("[[Lightfielder]Status] Generating output... This might take a few moments.\n\n")
	local flow = comp.CurrentFrame.FlowView
	-- Traverse the nodes
	for i, tool in ipairs(tools) do
		local toolAttrs = tool:GetAttrs()
		-- Scan the input connections
		inpNum = 1
		while true do
			-- local inConnect = tool:FindMainInput(1)
			local inConnect = tool:FindMainInput(inpNum)
			inpNum = inpNum + 1
			if inConnect then
				outConnect = inConnect:GetConnectedOutput()
				if outConnect then
					local prevTool = tool
					local t = outConnect:GetTool()
					if t then
						local inputName = tostring(t:GetAttrs().TOOLS_Name) .. '.' .. tostring(outConnect.Name)
						local outputName = tostring(prevTool:GetAttrs().TOOLS_Name) .. '.' .. tostring(inConnect.Name)

						-- Node Colors
						-- RGB to HEX Color Conversions
						local hexTileString = Color(tool)
						local classDefItem = string.format("\tclassDef %s fill:#%s,stroke:#333,color:#fff\n", tostring(tool:GetAttrs().TOOLS_Name), hexTileString)
						classDef = classDef .. tostring(classDefItem)

						-- Node Connections
						local inputNum = i
						local outputNum = nil

						-- Look up the output connection node number in the tools table
						for iT, outputT in ipairs(tools) do
							if tostring(t:GetAttrs().TOOLS_Name) == tostring(outputT.Name) then
								outputNum = iT
								break
							end
						end

						local inputOp = ""
						local outputOp = ""
						for _iR, reg in ipairs(reg_map) do
							if reg.ID == tool:GetAttrs().TOOLS_RegID then
								inputOp = " (" .. tostring(reg:GetAttrs().REGS_OpIconString) .. ")"
								-- dump(reg.ID, tool:GetAttrs().TOOLS_RegID)
								break
							end
						end

						-- inputOp = " (" .. tostring(prevTool:GetAttrs().TOOLS_RegID) .. ")"
						local inputLabel = tostring(prevTool:GetAttrs().TOOLS_Name) .. tostring(inputOp)

						if outputNum ~= nil then
							for _iR, reg in ipairs(reg_map) do
								if reg.ID == t:GetAttrs().TOOLS_RegID then
									outputOp = " (" .. tostring(reg:GetAttrs().REGS_OpIconString) .. ")"
									-- dump(reg.ID, t:GetAttrs().TOOLS_RegID)
									break
								end
							end
						end

						-- outputOp = " (" .. tostring(t:GetAttrs().TOOLS_RegID) .. ")"
						local outputLabel = tostring(t:GetAttrs().TOOLS_Name) .. tostring(outputOp)

						if outputNum ~= nil and outputLabel ~= nil and inputNum ~= nil and inputLabel  ~= nil then
							local connectionsItem = string.format('\tN%d(["%s"]) --> N%d(["%s"])\n', tonumber(outputNum), tostring(outputLabel), tonumber(inputNum), tostring(inputLabel))
							connections = tostring(connections) .. tostring(connectionsItem)
						end

						-- Node Names
						local classItem = string.format("\tclass N%d %s\n", tonumber(i), tostring(tool:GetAttrs().TOOLS_Name))
						class = class .. tostring(classItem)
					end
				else
					-- print('[Lightfielder][Branch Completed] ' .. toolAttrs.TOOLS_Name .. ' primary input not connected to another node')

					-- Node Colors
					-- RGB to HEX Color Conversions
					local hexTileString = Color(tool)
					local classDefItem = string.format("\tclassDef %s fill:#%s,stroke:#333,color:#fff\n", tostring(tool:GetAttrs().TOOLS_Name), hexTileString)
					classDef = classDef .. tostring(classDefItem)

					-- Node Names
					local classItem = string.format("\tclass N%d %s\n", tonumber(i),  tostring(tool:GetAttrs().TOOLS_Name))
					class = class .. tostring(classItem)

					break
				end
			else
				-- print('[Lightfielder][Flow Completed] ' .. toolAttrs.TOOLS_Name .. ' must be a creator tool')
				finalTool = tool

				-- Node Colors
				-- RGB to HEX Color Conversions
				local hexTileString = Color(tool)
				local classDefItem = string.format("\tclassDef %s fill:#%s,stroke:#333,color:#fff\n", tostring(tool:GetAttrs().TOOLS_Name), hexTileString)
				classDef = classDef .. tostring(classDefItem)

				-- Node Names
				local classItem = string.format("\tclass N%d %s\n", tonumber(i), tostring(tool:GetAttrs().TOOLS_Name))
				class = class .. tostring(classItem)

				break
			end
		end
	end

	-- Append all the Mermaid elements into a single output:
	local mermaidOpen = ""
	local mermaidClose = ""

	-- Header and Footer tags
	if outputWrapper == "BBCode" then
		-- WSL PHP BBCode format
		mermaidOpen = "[mermaid]"
		mermaidClose = "[/mermaid]"
	else
		-- GitHub Flavoured Markdown format
		mermaidOpen = "```mermaid"
		mermaidClose = "```"
	end

	-- Mermaid graph LR/TB
	local mermaidHeader = "graph "
	mermaidHeader = mermaidHeader .. tostring(flowShape)

	-- Link wireline color
	local mermaidLinkStyle = "\tlinkStyle default stroke:#ffffff,stroke-width:2px;"

	-- Combined Document
	mermaidContent = tostring(mermaidOpen) .. "\n" .. tostring(mermaidHeader) .. "\n" .. tostring(classDef) .. "\n" .. tostring(connections) ..  "\n" .. tostring(class) .. "\n" .. tostring(mermaidLinkStyle) .. "\n" .. tostring(mermaidClose)
	print(mermaidContent)

	-- Copy the Mermaid document into the copy/paste clipboard buffer
	bmd.setclipboard(mermaidContent)
else
	print("[Lightfielder][Copy As Mermaid][Error] Cannot Find FlowView window. The node graph might be detached on a 2nd monitor.")
end
