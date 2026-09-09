"""
Lightfielder Show OpenFX Plugins Folder 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Shows the OpenFX plugins folder in a new folder browsing window.

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
	print("[Lightfielder][Open Folder] OpenFX Plugins")

	currentOS = GetPlatform()
	if currentOS == "Mac":
		ShowFolderFromFilepath("/Library/OFX/Plugins/")
	elif currentOS == "Windows":
		ShowFolderFromFilepath("C:/Program Files/Common Files/OFX/Plugins/")
	elif currentOS == "Linux":
		ShowFolderFromFilepath("/usr/OFX/Plugins/")
