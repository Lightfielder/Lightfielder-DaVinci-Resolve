"""
Lightfielder Show Deliver Page Presets Folder 2026-09-18 11.54 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Shows the Lightfielder "Deliver Page Presets" folder in a new folder browsing window.

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
	print("[Lightfielder][Open Folder][PathMap] Unit Tests Folder")

	ShowFolderFromFilepath("Lightfielder:/Extras/Deliver Page Presets/")
