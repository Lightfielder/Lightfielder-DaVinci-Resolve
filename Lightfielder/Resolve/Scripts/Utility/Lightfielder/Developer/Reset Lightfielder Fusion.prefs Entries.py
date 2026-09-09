"""
Reset Lightfielder Fusion.prefs Entries.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Quickly reset the location of the Lightfielder script windows and their settings by zeroing out the Lightfielder entries in the Fusion.prefs file.

"""

if __name__ == "__main__":
	print("[Lightfielder][Reset Preferences and Window Positions]")

	# Clear all preferences
	app.SetData("Lightfielder", None)

	# Write the preferences to disk
	app.SavePrefs()

	print("[Lightfielder][Done]")
