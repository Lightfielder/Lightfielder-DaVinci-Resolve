"""
Lightfielder 17 Show Extensions Folder.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Open the Lightfielder Extensions folder:
$HOME/Lightfielder/Resolve/Scripts/Support/Lightfielder_Extensions/

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
	print("[Lightfielder][Open Folder][PathMap] \"Lightfielder Extensions\" \t[Absolute Path] \"" + str(app.MapPath("Lightfielder:/Resolve/Scripts/Support/Lightfielder_Extensions/")) + "\"")
	ShowFolderFromFilepath("Lightfielder:/Resolve/Scripts/Support/Lightfielder_Extensions/")
