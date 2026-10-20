#!/bin/zsh
set -u
echo "Restart DaVinci Resolve"

APP_PATH="/Applications/DaVinci Resolve/DaVinci Resolve.app"
APP_NAME="DaVinci Resolve"
MATCH_PATTERN="DaVinci Resolve.app/Contents/MacOS/Resolve|/MacOS/Resolve"
if [[ ! -d "$APP_PATH" ]]; then
	FOUND_APP="$(mdfind "kMDItemCFBundleIdentifier == 'com.blackmagic-design.DaVinciResolve'" 2>/dev/null | head -n 1)"
	if [[ -n "${FOUND_APP:-}" && -d "$FOUND_APP" ]]; then
		APP_PATH="$FOUND_APP"
	fi
fi

if pgrep -f "$MATCH_PATTERN" >/dev/null 2>&1; then
	echo "Stopping DaVinci Resolve..."
	osascript -e 'tell application "DaVinci Resolve" to quit' >/dev/null 2>&1 || true
	for _ in {1..10}; do
		pgrep -f "$MATCH_PATTERN" >/dev/null 2>&1 || break
		sleep 1
	done
	if pgrep -f "$MATCH_PATTERN" >/dev/null 2>&1; then
		echo "DaVinci Resolve did not quit; forcing it to close..."
		pkill -f "$MATCH_PATTERN" 2>/dev/null || true
		sleep 2
		pkill -9 -f "$MATCH_PATTERN" 2>/dev/null || true
	fi
	echo "Waiting 5 seconds..."
	sleep 5
else
	echo "DaVinci Resolve is not currently running"
fi

echo "Launching DaVinci Resolve..."
if [[ -d "$APP_PATH" ]]; then
	open "$APP_PATH"
else
	open -a "$APP_NAME"
fi
if [[ -t 0 ]]; then
	echo
	read -r "?Press Return to close this window..."
fi
