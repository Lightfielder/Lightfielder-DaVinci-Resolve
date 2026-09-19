--[[--
Recurse Node Flow.lua 2026-09-18 11.54 PM (UTC -3)
Updated by Andrew Hazelden <andrew@andrewhazelden.com>

This script will recurse a comp flow by travelling from the initially selected node, "upstream" until it finds the first creator node in the branch. It works by traversing nodes using the "Main Input" background input connection as it jumps continuously backwards in the output > input node connection direction.

Typically, a user would start by selecting the final node in a comp branch to end up at the original Loader/MediaIn/FBXMesh3D/ABCMesh3D node. An example use case for this code is to help you track down the Filename of the imagery that is being rendered, without relying on the Metadata Filename tag (which is not present in Resolve Fusion-based MediaIn footage).

This is a Resolve/Fusion v17 compatible page-one rewrite of Isaac Guenard/eyeon Software's earlier "recurseExample.dfscript3" script:
http://vixen.eyeonline.com/DFReg/downloads/dfscript/recurseExample.dfscript3
http://forums.cgsociety.org/t/a-few-scripting-questions/663847/3


Loader output in Console:
[Recurse Node Flow]
[Initial Selection] Saver1
[Node Connection Traceroute]
	[1] ColorCorrector1.Output --> Saver1.Input
	[2] Merge1.Output --> ColorCorrector1.Input
	[3] BrightnessContrast1.Output --> Merge1.Background
	[4] Loader1.Output --> BrightnessContrast1.Input
[First Node] Loader1 [Type] Loader [Filename] /Users/vfx/Desktop/media.png
[Done]


MediaIn output in Console:
[Recurse Node Flow]
[Initial Selection] MediaOut1
[Node Connection Traceroute]
	[1] Saver1.Output --> MediaOut1.Input
	[2] ColorCompressor1.Output --> Saver1.Input
	[3] Merge1.Output --> ColorCompressor1.Source
	[4] BrightnessContrast1.Output --> Merge1.Background
	[5] MediaIn1.Output --> BrightnessContrast1.Input
[First Node] MediaIn1 [Type] MediaIn [Filename] /Users/vfx/Desktop/media.png
[Done]


FBXMesh3D output in Console:
[Recurse Node Flow]
[Initial Selection] Saver1
[Node Connection Traceroute]
	[1] Merge1.Output --> Saver1.Input
	[2] Renderer3D1.Output --> Merge1.Background
	[3] Merge3D1.3D Data --> Renderer3D1.SceneInput
	[4] FBXMesh3D1.3D Data --> Merge3D1.SceneInput1
[First Node] FBXMesh3D1 [Type] SurfaceFBXMesh [Filename] /Users/vfx/Reactor/Deploy/Macros/KickAss ShaderZ/Assets/kas_ShaderBall.obj
[Done]
--]]--

print('\n\n[Recurse Node Flow]')

-- Hop along the flow graph
function recurseFlow(tool)
	hopCount = hopCount + 1

	if tool then
		local toolAttrs = tool:GetAttrs()
		local inConnect = tool:FindMainInput(1)
		if inConnect then
			outConnect = inConnect:GetConnectedOutput()
			if outConnect then
				local prevTool = tool
				local tool = outConnect:GetTool()
				if tool then
					-- Print the connection details to the Console
					local inputName = tostring(tool:GetAttrs().TOOLS_Name) .. '.' .. tostring(outConnect.Name)
					local outputName = tostring(prevTool:GetAttrs().TOOLS_Name) .. '.' .. tostring(inConnect.Name)
					print('\t[' .. tostring(hopCount) .. '] ' ..  inputName .. ' --> ' .. outputName)

					-- Scan the flow backwards hopping across the next input connection point
					recurseFlow(tool)
				end
			else
				-- print('[Branch Completed] ' .. toolAttrs.TOOLS_Name .. ' primary input not connected to another node')
				finalTool = tool
				return
			end
		else
			-- print('[Flow Completed] ' .. toolAttrs.TOOLS_Name .. ' must be a creator tool')
			finalTool = tool
			return
		end
	else
		return
	end
end

-- Lookup the filename attribute for the current tool
function GetToolFilename(tool)
	if tool then
		local toolAttrs = tool:GetAttrs()

		-- Scan for the active node's filename record
		if toolAttrs.TOOLS_RegID == 'MediaIn' then
			return comp:MapPath(tool:GetData('MediaProps.MEDIA_PATH'))
		elseif toolAttrs.TOOLS_RegID == 'Loader' then
			return comp:MapPath(toolAttrs.TOOLST_Clip_Name[1])
		elseif toolAttrs.TOOLS_RegID == 'Saver' then
			return comp:MapPath(toolAttrs.TOOLST_Clip_Name[1])
		elseif toolAttrs.TOOLS_RegID == 'SurfaceFBXMesh' then
			return comp:MapPath(tool:GetInput('ImportFile'))
		elseif toolAttrs.TOOLS_RegID == 'SurfaceAlembicMesh' then
			return comp:MapPath(tool:GetInput('Filename'))
		elseif toolAttrs.TOOLS_RegID == 'ExporterFBX' then
			return comp:MapPath(tool:GetInput('Filename'))
		elseif toolAttrs.TOOLS_RegID == 'Fuse.ExternalMatteSaver' then
			return comp:MapPath(tool:GetInput('Filename'))
		elseif toolAttrs.TOOLS_RegID == 'Fuse.LifeSaver' then
			return comp:MapPath(tool:GetInput('Filename'))
		elseif toolAttrs.TOOLS_RegID == 'Fuse.PutFrame' then
			return comp:MapPath(tool:GetInput('Filename'))
		elseif toolAttrs.TOOLS_RegID == 'Fuse.GetFrame' then
			return comp:MapPath(tool:GetInput('Filename'))
		else
			return nil
		end
	end
end

-- The main function
function Main()
	hopCount = 0
	selectedNode = comp.ActiveTool

	finalTool = nil
	FilenameFinal = nil
	typeFinal = nil
	nodeNameFinal = nil
	
	if selectedNode then
		print('[Initial Selection] ', selectedNode:GetAttrs().TOOLS_Name)
		print('[Node Connection Traceroute]')
		recurseFlow(selectedNode)
		if finalTool then
			-- Lookup the filename attribute for the current node
			FilenameFinal = GetToolFilename(finalTool)
			nodeNameFinal = finalTool:GetAttrs().TOOLS_Name
			typeFinal = finalTool:GetAttrs().TOOLS_RegID
			print('[First Node] ' .. tostring(nodeNameFinal) .. ' [Type] ' .. tostring(typeFinal)  ..' [Filename] ' ..  tostring(FilenameFinal))
		end
	else
		print('[Initial Selection] Empty. Please select a node in the flow and run the script again.')
	end
end


-- Main is where the magic happens
Main()
print('[Done]')
