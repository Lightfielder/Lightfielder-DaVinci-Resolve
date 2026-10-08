---
title: "REPL Interactive Scripting"
sidebar_label: "Interactive REPL"
sidebar_position: 7
description: "Interactive Lua and Python REPL for Lightfielder Viewport."
---

# Lightfielder Viewport | REPL Interactive Scripting

The Viewport app includes an **interactive REPL** (Read–Eval–Print–Loop) for both Lua and Python. It runs from the terminal with no GUI, providing an inline-editable command line with history, cursor movement, and the full `lf.*` scripting API.

---

## Starting the REPL

```
./Viewport.app/Contents/MacOS/Viewport -i lua
./Viewport.app/Contents/MacOS/Viewport -i python
```

On first run the engine initialises the Lua 5.4 runtime and the Lunatic Python bridge, then registers the Viewport `lf` API.

```
Lightfielder Viewport  REPL [lua]
Commands: $lua, $python for switching the language  |  exit() for quitting
lua>
```

---

## Switching Languages Mid-Session

The REPL can switch between Lua and Python at any time without restarting:

| Command | Action |
|---------|--------|
| `$lua` | Switch to Lua mode |
| `$python` or `$py` | Switch to Python mode |

The prompt updates to reflect the current mode (`lua>` or `py>`) and a confirmation message is printed. The language switch is a no-op if already in the requested mode.

```
lua> $python
switched to Python
py> print(2 + 2)
4
py> $lua
switched to Lua
lua> == math.pi
3.1415926535898
```

---

## Key Bindings

### Cursor Movement

| Key | Action |
|-----|--------|
| `←` / `→` | Move cursor left / right one character |
| `Home` / `End` | Jump to beginning / end of line |
| `Ctrl+A` | Beginning of line |
| `Ctrl+E` | End of line |

### Editing

| Key | Action |
|-----|--------|
| `Backspace` | Delete character before cursor |
| `Delete` (fn+Backspace) | Delete character at cursor |
| `Ctrl+U` | Clear entire line |
| `Ctrl+K` | Delete from cursor to end of line |
| `Ctrl+C` | Cancel current line (does not exit) |

### History

| Key | Action |
|-----|--------|
| `↑` | Recall previous command |
| `↓` | Recall next command (back to pending line) |

History is preserved for the duration of the REPL session. Empty lines and duplicate consecutive commands are not added to history.

### Exit

| Command / Key | Action |
|---------------|--------|
| `exit()` | Quit the REPL |
| `Ctrl+D` on empty line | EOF, quit the REPL |

---

## Input Editing Behaviour

The REPL switches the terminal to **raw mode** (`tcsetattr` with `ECHO`, `ICANON`, `IEXTEN`, `ISIG` disabled) so it can read individual keystrokes. When stdin is not a TTY (e.g. piping a script), the REPL falls back to plain `readLine()` with no inline editing.

### How It Works

- A `buffer` (the entered text) and a `cursor` (character offset within the buffer) are tracked
- ANSI escape codes (`\e[D`, `\e[C`, `\e[H`, `\e[F`, `\e[K`, etc.) redraw the line as the cursor moves or text changes
- History navigation saves the current "pending" line when the user first presses Up, then restores it when pressing Down back to the new-line slot

---

## Command Execution

Every line is processed in two phases:

1. **Eval**  
	Tries to evaluate the code as an expression (with an implicit `return`). If successful, prints the result.
2. **Execute**  
	If the eval fails it will run the code as a statement (function call, assignment, etc.). If that also fails, the error message is printed.

### The `==` Shortcut (Lua only)

`==` at the start of a line is expanded to `dump(...)`, which pretty-prints any Lua value:

```
> == math.pi
3.1415926535898
> == lf
{
  "active_tool" : "function: 0x...",
  "new_scene" : "function: 0x...",
  ...
}
```

This is equivalent to typing `dump(math.pi)` or `dump(lf)`.

---

## Lua Environment

| Item | Details |
|------|---------|
| Version | Lua 5.4 (embedded C source via the LuaPython package) |
| Global API | `lf.*` For all Viewport scripting functions (scene, camera, geometry, lights, shading, etc.) |
| Utility | `dump()` Will pretty print any Lua value to stdout |
| Module paths | Lua modules are loaded from `~/Library/Application Support/com.Lightfielder.Viewport/Modules/Lua/` |
| Demo | `Preferences/Scripts/Hello LuaJIT World.lua` |

---

## Python Environment

| Item | Details |
|------|---------|
| Engine | CPython bridging via the Lunatic Python bridge |
| Global API | `lf.*` Uses the same Viewport scripting functions as Lua |
| Module paths | Python modules are loaded from `~/Library/Application Support/com.Lightfielder.Viewport/Modules/Python/` |
| Demo | `Preferences/Scripts/Hello CPython World.py` |

---

## Example Session

```
$ /Applications/Viewport.app/Contents/MacOS/Viewport -i lua
Lightfielder Viewport  REPL [lua]
Type 'exit()' to quit

> lf.new_scene()
true
> lf.create_primitive("cube")
true
> == lf.get_selected()
[ "Cube_1" ]
> lf.set_transform("Cube_1", 0, 5, 0)
true
> lf.save_scene_as("/tmp/test.jsonc")
true
> exit()
```

---

## Shell Launcher

A convenience shell script is available at:

```
Viewport/Extras/Viewport CLI.command
```

It launches the Viewport binary with `-i lua` for a quick REPL session.
