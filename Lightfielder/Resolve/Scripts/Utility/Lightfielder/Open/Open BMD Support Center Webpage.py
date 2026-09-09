"""
Lightfielder Open BMD Support Center Webpage.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Open the Blackmagic Design Support Centre website in the default web browser. This webpage is where new Resolve Studio releases are downloaded from.

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
	ShowWebpage("https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion")
