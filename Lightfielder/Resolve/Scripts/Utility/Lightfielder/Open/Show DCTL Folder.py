"""
Lightfielder Show DCTL Folder 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Shows the DCTL folder in a new folder browsing window.

"""

import platform
import sys, os

# Load the Lightfielder shared utility module
lightfielder_path = os.path.dirname(app.MapPath("Scripts:/Support/lightfielder.py"))
if lightfielder_path not in sys.path:
	sys.path.append(lightfielder_path)
	# print(sys.path)
	from lightfielder import *

if __name__ == "__main__":
	print("[Lightfielder][Open Folder][PathMap] DCTL Folder")

	currentOS = GetPlatform()
	if currentOS == "Mac":
		ShowFolderFromFilepath("/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/")
	elif currentOS == "Windows":
		ShowFolderFromFilepath("C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/LUT/")
	elif currentOS == "Linux":
		ShowFolderFromFilepath("/opt/resolve/LUT/")
		# ShowFolderFromFilepath("/home/resolve/LUT/")
