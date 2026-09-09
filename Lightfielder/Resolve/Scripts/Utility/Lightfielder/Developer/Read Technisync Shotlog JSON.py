"""
Lightfielder Read Technisync Shotlog JSON 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

A script to extract and parse shotlog data from the Technisync Lightfielder camera array. The output is dumped to the terminal with indented JSON formatting to make it easier to read.

Each log file entry is formatted as:
YYYY-MM-DD HH:MM:SS.SSSSSS {JSON}

A single line of data from the shotlog file holds a JSON encoded blob of information with keys for:

- appConfig
- camConfig
- sysConfig


# Script Usage

1. Run the "Workspace > Scripts > Lightfielder > Development > Read Technisync Shotlog JSON.py" file.
1. Select a Technsync shotlog .json file using the file browser dialog that appears.
2. Open the Console window to see the results.


# Script Controls:

The script has two variables named "records" and "display" that you can toggle in the "__main__" section at the bottom of the code:

# Do you want to see the first record, or all of the data?
records = "single"
#records = "all"

# Do you want a top-level summary, or a direct dump of the JSON records?
display = "summary"
#display = "dump"

The Display "summary" mode shows:
[ShotLog] [File] /Users/vfx/Desktop/ID_0001/technisync_sample_log-shot.log
	[Production] Test
	[Timecode] 05:05:55
	[Frame Limit] 15 (frames)
	[Shot] 1
	[Reel] 1
	[Take] 1
	[Roll Number] 1
	[Technical]
		[Camera Brand] RED
		[Camera Type] KOMODO
		[FPS] 29.97 FPS
		[ISO] ISO 800
		[White Balance] 5000K
		[Focal Length] 35mm
		[Aperture] f/8
		[Camera Count] 50


The Display "dump" mode shows:
[ShotLog] [File] /Users/vfx/Desktop/ID_0001/technisync_sample_log-shot.log
{
	"appConfig": {
		"peakingColor": 16711680,
		"frameRateMenuItem": 3,
		"camRows": 10,
		"sdiZoom": false,
		"isoMenu": [
			"MULT",
			"ISO 250",
			"ISO 320",
			"ISO 400",
			"ISO 500",
			"ISO 640",
			"ISO 800",
			"ISO 1000",
			"ISO 1280",
			"ISO 1600",
			"ISO 2000",
			"ISO 2500",
			"ISO 3200",
			"ISO 4000",
			"ISO 5000",
			"ISO 6400",
			"ISO 12800"
		],
		"slate": "A",
		"peakingEnabled": false,
		"tcStatus": "green",
		"shotLogIdx": -1,
		"selectedClipIdx": 11,
		"shot": 1,
		"reel": 1,
		"rollNumber": 1,
		"preRecordEnabled": false,
		"tempCal": "green",
		"genStatus": "green",
		...

"""

import re
import os
import json

def ParseLine(log_line):
	# Parse the date/time stamp and json blob

	jsonDict = []
	pattern = r"""
^                                     # Start of line
(?P<year>[0-9][0-9][0-9][0-9])        # Year 2023
([-])                                 # Dash separator
(?P<month>[0-9][0-9])                 # Month 04
([-])                                 # Dash separator
(?P<day>[0-9][0-9])                   # Day 03
([ ])                                 # Space separator
(?P<hour>[0-9][0-9])                  # Hour 14
([:])                                 # Colon separator
(?P<minute>[0-9][0-9])                # Minute 33
([:])                                 # Colon separator
(?P<second>[0-9][0-9][.]\d+)          # Second 01.161435
\s                                    # Whitespace - Tab or Space
(?P<json>.*)                          # JSON blob of data
$                                     # End of line
"""

	# Process a regular expression based named group
	pat = re.compile(pattern, re.VERBOSE)
	mat = pat.match(log_line)
	result = None
	if mat:
		m = mat.groupdict()
		#print("\t[RegEx Parsing]")
		#print(m)
		if m:
			if "json" in m:
				jsonDict = json.loads(m["json"])

	return jsonDict

def ExtractData(j, displayMode):
	# Format the data for terminal output
	if displayMode == "dump":
		# Add indentations to the json data to make it easier to read
		print(json.dumps(j, ensure_ascii = True, indent = "\t"))
	elif displayMode == "summary":
		# Display a short summary of the info
		if "appConfig" in j:
			print("\t[Production] " + str(j["appConfig"]["production"]))
			print("\t[Timecode] " + str(j["appConfig"]["timecode"]))
			print("\t[Frame Limit] " + str(j["appConfig"]["frameLimitFrames"]) + " (frames)")
			print("\t[Shot] " + str(j["appConfig"]["shot"]))
			print("\t[Reel] " + str(j["appConfig"]["reel"]))
			print("\t[Take] " + str(j["appConfig"]["take"]))
			print("\t[Roll Number] " + str(j["appConfig"]["rollNumber"]))

			print("\t[Technical]")

		if ("sysConfig" in j) and ("cameras" in j["sysConfig"]):
			try:
				firstCamera = next(iter(j["sysConfig"]["cameras"].values()))

				print("\t\t[Camera Brand] " + str(firstCamera["brand"]))
				print("\t\t[Camera Type] " + str(firstCamera["type"]))
			except StopIteration:
				pass

		if "appConfig" in j:
			print("\t\t[FPS] " + str(j["appConfig"]["fpsStr"]))
			print("\t\t[ISO] " + str(j["appConfig"]["isoStr"]))
			print("\t\t[White Balance] " + str(j["appConfig"]["wbStr"]))

		if "camConfig" in j:
			try:
				firstCamera = next(iter(j["camConfig"].values()))
				if "LENS_FOCAL_LENGTH" in firstCamera:
					print("\t\t[Focal Length] " + str(firstCamera["LENS_FOCAL_LENGTH"]))
				if "APERTURE" in firstCamera:
					print("\t\t[Aperture] " + str(firstCamera["APERTURE"]))
			except StopIteration:
				pass

		if "appConfig" in j:
			print("\t\t[Camera Count] " + str(j["appConfig"]["numCameras"]))
			#print("\t[Cameras] " + str(j["appConfig"]["cameraNames"]))


def OpenJSON(file, recordAccess, displayMode):
	# Open the JSON log file and read it line by line

	print("[Lightfielder][ShotLog] [File] " + str(file))
	with open(file) as f:
		if recordAccess == "single":
			# Read the first line from the log file
			line = f.readline()

			# Use regular expressions to pull out the json blob
			j = ParseLine(line)

			# Format the data for terminal output
			ExtractData(j, displayMode)
		elif recordAccess == "all":
			count = 1
			# Read all the lines in the log file
			for line in f:
				print("[" +  str(count) + "]")

				# Use regular expressions to pull out the json blob
				j = ParseLine(line)

				# Format the data for terminal output
				ExtractData(j, displayMode)

				# Line number
				count += 1


if __name__ == "__main__":
	# JSON log filepath
	# shotlogFile = "/Users/vfx/Desktop/ID_0001/technisync_sample_log-shot.json"
	shotlogFile = str(app.MapPath(fu.RequestFile()))
	if shotlogFile:
		if os.path.isfile(shotlogFile):
			# Do you want to see the first record, or all of the data?
			records = "single"
			#records = "all"

			# Do you want a top-level summary, or a direct dump of the JSON records?
			display = "summary"
			#display = "dump"

			# Open the JSON log file and read it line by line
			OpenJSON(shotlogFile, records, display)
		else:
			print("[Lightfielder][Preferences] A JSON File does not exist at this filepath.")
