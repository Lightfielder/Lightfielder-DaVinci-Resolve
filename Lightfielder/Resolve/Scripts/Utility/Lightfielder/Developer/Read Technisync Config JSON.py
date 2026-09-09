"""
Lightfielder Read Technisync Config JSON.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

A script to parse camera array data from the "activeTechnisyncConfig.json" file.

# Script Usage

1. Run the "Workspace > Scripts > Lightfielder > Development > Read Technisync Config JSON.py" file.
1. Select a Technsync config .json file using the file browser dialog that appears.
2. Open the Console window to see the results.

Sample Console Window Output:
[ShotLog] [File] /Users/vfx/Desktop/ID_0001/activeTechnisyncConfig.json
[Cameras] 50
	 ['A130'] 1
	 ['A150'] 2
	 ['A220'] 3
	 ['A240'] 4
	 ['A260'] 5
	 ['A330'] 6
	 ['A350'] 7
	 ['A420'] 8
	 ['A440'] 9
	 ['A460'] 10
	 ['A530'] 11
	 ['A550'] 12
	 ['B120'] 13
	 ['B140'] 14
	 ['B160'] 15
	 ['B230'] 16
	 ['B250'] 17
	 ['B320'] 18
	 ['B340'] 19
	 ['B360'] 20
	 ['B430'] 21
	 ['B450'] 22
	 ['B520'] 23
	 ['B540'] 24
	 ['B560'] 25
	 ['C120'] 26
	 ['C140'] 27
	 ['C160'] 28
	 ['C230'] 29
	 ['C250'] 30
	 ['C320'] 31
	 ['C340'] 32
	 ['C360'] 33
	 ['C430'] 34
	 ['C450'] 35
	 ['C520'] 36
	 ['C540'] 37
	 ['C560'] 38
	 ['D130'] 39
	 ['D150'] 40
	 ['D220'] 41
	 ['D240'] 42
	 ['D260'] 43
	 ['D330'] 44
	 ['D350'] 45
	 ['D420'] 46
	 ['D440'] 47
	 ['D460'] 48
	 ['D530'] 49
	 ['D550'] 50

[Camera Lookup] D550 [Index]  50

"""

import re
import os
import json

def ExtractData(j, displayMode):
	cameraItems = []

	# Format the data for terminal output
	if displayMode == "dump":
		# Add indentations to the json data to make it easier to read
		print(json.dumps(j, ensure_ascii = True, indent = "\t"))
	elif displayMode == "records":
		# Display a short summary of the info
		if "controlBoxes" in j:
			controllerCount = len(j["controlBoxes"])
			#print("\t[Controllers] " + str(controllerCount))
			if controllerCount != None:
				for c in j["controlBoxes"]:
					if "ports" in c:
						portCount = len(c["ports"])
						# print("\t\t[Ports] ", portCount)
						for p in c["ports"]:
							try:
								## A1 - J5
								cameras = str(c["cameras"][p-1])

								# AA - DE
								cameraAlias = str(c["cameraAlias"][p-1])

								# 0, 210 - 650
								cameraPosition = str(c["cameraPosition"][p-1]).zfill(3)

								# A210
								# Note: Trimmed the camera alias by removing the 2nd character, then appended the camera position
								cameraLabel = str(cameraAlias[:-1]) + str(cameraPosition)
								if cameras != None and cameras != "--":
									cameraItems.append([cameraLabel])
							except StopIteration:
								pass
	cameraItems.sort()

	return cameraItems

def OpenJSON(file, displayMode):
	# Open the JSON log file and read it line by line
	print("[Lightfielder][ShotLog] [File] " + str(file))
	try:
		with open(file, "r") as f:
			j =  json.load(f)
			cams = ExtractData(j, displayMode)

			print("[Cameras]", len(cams))
			if cams != None:
				for c in cams:
					print("\t", c, cams.index(c) + 1)

				findCam = "A110"
				try:
					print("\n\n[Camera Lookup]", findCam, "[Index] ", cams.index([findCam]) + 1)
				except ValueError:
					print("[Index] not found for:", findCam)
					pass
	except OSError as error:
		print("\t[Lightfielder][Exception][JSON Get Error]", error)

if __name__ == "__main__":
	# JSON log filepath
	# configFile = "/Users/vfx/Desktop/ID_0001/TechnisyncConfig.json"
	configFile = str(app.MapPath(fu.RequestFile()))
	if configFile:
		if os.path.isfile(configFile):
			# Do you want a top-level summary, or a direct dump of the JSON records?
			display = "records"
			#display = "dump"

			# Open the JSON log file and read it line by line
			OpenJSON(configFile, display)
