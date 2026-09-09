"""
Lightfielder Open Toolbar File 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Edits the "00 Toolbar.py" file using the script editor defined in Fusion's preferences.

This feature requires the "xdg-open" package to be installed on Linux.
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
	print("[Lightfielder][Edit] Toolbar File")
	# This feature requires the "xdg-open" package to be installed on Linux.
	ExternalEditor("Scripts:/Utility/Lightfielder/00 Toolbar.py")
