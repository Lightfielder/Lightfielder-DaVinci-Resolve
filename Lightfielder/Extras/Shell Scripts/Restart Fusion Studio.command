#!/bin/zsh
set -u
echo "Restart Fusion Studio"

APP_PATH="'/Applications/Blackmagic Fusion 21/Fusion.app"
APP_NAME="Fusion"
MATCH_PATTERN="Fusion.app/Contents/MacOS/Fusion"
if [[ ! -d "$APP_PATH" ]]; then
	FOUND_APP="$(mdfind "kMDItemCFBundleIdentifier == 'com.blackmagic-design.fusion'" 2>/dev/null | head -n 1)"
	if [[ -n "${FOUND_APP:-}" && -d "$FOUND_APP" ]]; then
		APP_PATH="$FOUND_APP"
	fi
fi

if pgrep -f "$MATCH_PATTERN" >/dev/null 2>&1; then
	echo "Stopping Fusion Studio..."
	osascript -e 'tell application "Fusion Studio" to quit' >/dev/null 2>&1 || true
	for _ in {1..10}; do
		pgrep -f "$MATCH_PATTERN" >/dev/null 2>&1 || break
		sleep 1
	done
	if pgrep -f "$MATCH_PATTERN" >/dev/null 2>&1; then
		echo "Fusion Studio did not quit; forcing it to close..."
		pkill -f "$MATCH_PATTERN" 2>/dev/null || true
		sleep 2
		pkill -9 -f "$MATCH_PATTERN" 2>/dev/null || true
	fi
	echo "Waiting 5 seconds..."
	sleep 5
else
	echo "Fusion Studio is not currently running"
fi

echo "Launching Fusion Studio..."
if [[ -d "$APP_PATH" ]]; then
	open "$APP_PATH"
else
	open -a "$APP_NAME"
fi
if [[ -t 0 ]]; then
	echo
	read -r "?Press Return to close this window..."
fi
