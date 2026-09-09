"""
Lightfielder 20 Show Console.py 2026-09-02 07.10 PM (UTC -3)
By Andrew Hazelden <andrew@andrewhazelden.com>

Toggle the visibility of the Resolve Console window. This allows you to troubleshoot Lightfielder script errors if the Python scripts stop working as expected in future Resolve Studio versions.
"""

if __name__ == "__main__":
	if app:
		app.DoAction("Console_Show")
		# app.DoAction("Console_Show", {"show" : True})
