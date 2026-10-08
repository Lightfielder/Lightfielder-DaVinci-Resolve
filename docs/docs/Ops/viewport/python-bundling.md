---
title: "Python.framework Bundling"
sidebar_label: "Python Bundling"
sidebar_position: 10
description: "How Python.framework is bundled inside the Viewport app."
---

# Lightfielder Viewport | Python.framework Bundling

This document describes how Python.framework is bundled inside the Viewport `.app` bundle for distribution.

## Overview

The Viewport app embeds a hybrid Lua + Python scripting engine via Lunatic Python. At development time, it links against the system-installed Python.framework at `/Library/Frameworks/Python.framework/` (python.org 3.11.9 or 3.12.10).

For distribution, this framework is copied into `Viewport.app/Contents/Frameworks/` so users don't need to have a copy of Python installed sepaerately.

## File Structure

| File | Role |
|------|------|
| `Extras/bundle-python.sh` | Pre-build script: copies framework, strips stdlib, fixes install name |
| `Packages/LuaPython/.../pythoninlua.c` | C init: sets `config.home` to bundled framework path |
| `project.yml` | Two build phase scripts (copy + reference fix) |

## Build Phase Scripts

### 1. Pre-build: `bundle-python.sh`

Runs every build. Copies Python.framework from `/Library/Frameworks/` into `Viewport.app/Contents/Frameworks/`:

| Step | Detail |
|------|--------|
| **Copy dylib** | 14MB universal (x86_64 + arm64) |
| **Copy Resources** | Info.plist and resource files |
| **Copy stdlib** | Full `lib/python3.11/`, **excluding** `site-packages` |
| **Copy support libs** | `libcrypto.3.dylib`, `libssl.3.dylib`, `libncursesw.5.dylib`, etc. |
| **Strip tests** | `test/`, `tests/` directories |
| **Strip GUI** | `tkinter/`, `idlelib/`, `turtledemo/`, `turtle.py` |
| **Strip dev tools** | `ensurepip/`, `distutils/`, `lib2to3/`, `venv/` |
| **Strip cache** | All `__pycache__` directories |
| **Strip top-level** | `bin/`, `include/`, `share/`, `_CodeSignature/` |
| **Fix install name** | `install_name_tool -id @rpath/...` |
| **Create symlinks** | `Python -> Versions/Current/Python`, etc. |

Result: **151MB** Viewport.app build

### 2. Post-build: Reference fix (Archive only)

Runs only during **Archive** (`runOnlyWhenInstalling: true`). 

The Post-build step changes the binary's Python.framework reference from the absolute system path to `@rpath`, then re-signs:

```bash
install_name_tool -change \
    "/Library/Frameworks/Python.framework/Versions/3.11/Python" \
    "@rpath/Python.framework/Versions/3.11/Python" \
    "$BINARY"

codesign --force --sign "$CODE_SIGN_IDENTITY" "$CODESIGNING_FOLDER_PATH"
```

During **development**, pressing the (⌘R) run hotkey in xCode takes care of the entire build process for you. The resulting binary keeps the absolute path reference and loads the Python framework from the operating system's versuon, There is no slowdown from copying or re-signing.

## Runtime Python Home Resolution

In `pythoninlua.c` (the `luaopen_python` function), `PyConfig` is configured to find the bundled stdlib:

```c
config.isolated = 1;  // ignore PYTHONHOME, PYTHONPATH

// Detect bundled framework and set home
CFBundleRef bundle = CFBundleGetMainBundle();
if (bundle) {
    // Construct: <app>/Contents/Frameworks/Python.framework/Versions/3.11
    char fw_path[PATH_MAX];
    // ... resolve from bundle URL ...
    if (access(fw_path, F_OK) == 0) {
        config.home = Py_DecodeLocale(fw_path, NULL);
    }
}
```

This is necessary because `config.isolated = 1` prevents Python from reading `PYTHONHOME`. Setting `config.home` explicitly tells Python where to find `lib/python3.11/`.

## Build Settings (`project.yml`)

```yaml
FRAMEWORK_SEARCH_PATHS: /Library/Frameworks
OTHER_LDFLAGS: -framework Python
```

These are used during linking. The `-framework Python` flag makes Python C API symbols available. At link time, the reference recorded is the framework's install name (`/Library/Frameworks/Python.framework/Versions/3.11/Python`), which is later changed to `@rpath` during Archive.

## End-to-End Validation

The full pipeline was validated using Apple Events (AppleScript) against a development build:

| Test | Script | Result |
|------|--------|--------|
| Lua execution | `test_lua.lua` writes timestamp to `/tmp` | `Hello from Lua at 17:03:18` |
| Python execution | `test_python.py` writes timestamp to `/tmp` | `Hello from Python at 17:03:19` |
| Lua→Python bridge | `python.eval('"Lua says: " + str(42)')` | `Lua says: 42` |
| Python→Lua bridge | `lua.eval('"Python says: " .. 88')` | `Python says: 88` |

**Method**: App was launched via `open`, then AppleScript clicked menu items via `System Events`:

```applescript
tell application "System Events"
    tell process "Viewport"
        click menu item "test_lua.lua" of menu "Scripts" of menu bar 1
        click menu item "test_python.py" of menu "Scripts" of menu bar 1
    end tell
end tell
```

Each script wrote a confirmation file to `/tmp/viewport_test_*.txt`. All four files were created with expected content. This confirms the full pipeline works: Script menu → `ScriptEngine.shared.runScript(at:)` → `lua_python_init()` → interpreter execution → bidirectional bridge.

## Known Limitations

- **Python version hardcoded**: The bundled path uses `Versions/3.11`. If python.org Python is upgraded to 3.12+, update:
  - `Extras/bundle-python.sh`: `FRAMEWORK_VERSION="3.11"` (line ~10)
  - `pythoninlua.c`: the path in the `CFBundleGetMainBundle` block
  - `project.yml`: the `PYTHON_REF` in the postBuildScript
- **Stdlib stripping is conservative**: Only tests, GUI toolkits, and dev tools are removed. For further size reduction, strip optional stdlib modules (`curses`, `dbm`, `mailbox`, `imghdr`, etc.)
- **Code signing**: The postBuildScript re-signs after `install_name_tool`. For official distribution, use `productbuild` or `xcodebuild -exportArchive` which handle signing properly.
