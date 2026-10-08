---
title: "Lua Scripting API"
sidebar_label: "Lua Scripting API"
sidebar_position: 4
description: "The lf Lua scripting API for Lightfielder Viewport."
---

# Lightfielder Viewport | Lua Scripting API

The Viewport app embeds a **Lua 5.1** compatible runtime through the LuaPython framework.  

All Viewport functionality is exposed under the global `lf` table.  

```lua
-- Enable from any Lua script:
lf.new_scene()
local ok, err = lf.open_scene("/path/to/file.jsonc")
```

---

## Convention

Every function returns two values:

| Return | Meaning |
|--------|---------|
| `true` | Success |
| `nil, "error message"` | Failure |

Functions that return data (like `get_selected`, `list_layouts`) return a **JSON string** on success, or `nil, "error"` on failure.

Primitive and light type names are **lowercase**:

```lua
lf.create_primitive("cube")      -- not "Cube"
lf.create_light("directional")   -- not "Directional"
lf.set_camera_mode("orbit")      -- not "Orbit"
lf.set_shading("wireframe")      -- not "Wireframe"
```

---

## Scene / File Operations

```lua
-- New empty scene
lf.new_scene()                     -- true

-- Open a .jsonc scene file
local ok, err = lf.open_scene("/Users/me/scenes/my_scene.jsonc")

-- Save current scene (must already have a file path)
lf.save_scene()

-- Save As
lf.save_scene_as("/Users/me/scenes/copy.jsonc")

-- Revert to last saved version
lf.revert_scene()

-- Import a file as a reference
lf.import_file("/Users/me/models/car.obj")
```

---

## Creating Objects

```lua
-- Scene objects
lf.create_camera()
lf.create_locator()
lf.create_group()
lf.create_reference()
lf.create_audio()
lf.create_note()

-- Primitives (lowercase)
lf.create_primitive("cube")
lf.create_primitive("cone")
lf.create_primitive("sphere")
lf.create_primitive("cylinder")
lf.create_primitive("pyramid")
lf.create_primitive("torus")

-- Lights (lowercase)
lf.create_light("ambient")
lf.create_light("area")
lf.create_light("directional")
lf.create_light("dome")
lf.create_light("point")
lf.create_light("spot")
lf.create_light("sphere")
lf.create_light("tube")
```

---

## Selection

```lua
lf.select_all()
lf.deselect_all()
lf.select_by_name("Cube")        -- partial name match
lf.select_by_id("obj_5")         -- exact id match

local selected_json = lf.get_selected()  -- returns JSON string
```

Example `get_selected()` return:

```json
[
  {
    "id": "obj_3",
    "name": "Cube",
    "position": [0, 0, 0],
    "rotation": [0, 0, 0],
    "scale": [1, 1, 1],
    "type": "mesh"
  }
]
```

---

## Edit Commands

```lua
lf.undo()
lf.redo()
lf.cut()
lf.copy()
lf.paste()
lf.delete_selected()
lf.duplicate_selected()
lf.group_selected()
lf.ungroup_selected()
```

---

## Transform

```lua
-- Set transform: id, position(x3), rotation(x3), scale(x3)
lf.set_transform("obj_3", 0, 0, 0, 0, 0, 0, 2, 2, 2)

-- Get transform returns JSON string
local t = lf.get_transform("obj_3")
-- t = '{"id":"obj_3","name":"Cube","position":[0,0,0],...}'

-- Reparent: child_id, parent_id
lf.set_parent("obj_3", "obj_1")

-- Detach from parent (empty string)
lf.set_parent("obj_3", "")

-- Rename object
lf.rename_object("obj_3", "MyCube")
```

---

## Viewport Control

```lua
lf.frame_all()
lf.go_home()
lf.set_camera_mode("orbit")   -- "orbit" | "fps"
lf.set_shading("shaded")      -- "shaded" | "boundingBox" | "points" | "wireframe" | "none"
lf.set_interaction("selection") -- "selection" | "transform"
```

---

## Display Toggles

All take a boolean-like value (`true`/`false` or `1`/`0`):

```lua
lf.show_grid(true)
lf.show_vertices(false)
lf.show_normals(false)
lf.show_edges(true)
lf.show_xray(false)
lf.show_hud(true)
lf.show_fps(false)
lf.show_details(false)
lf.show_distance(false)
lf.show_render(false)
lf.show_selected(false)
lf.show_camera_view(false)
lf.show_polygons(false)
lf.show_camera_locators(false)
lf.show_light_locators(false)
lf.show_locator_icons(true)
lf.show_skybox(false)
```

---

## Auxiliary Windows

```lua
lf.open_outliner()         -- Opens Outliner window (F6 equivalent)
lf.open_attributes()       -- Opens Attributes window (F7 equivalent)
lf.open_history_stack()    -- Opens History Stack (F5 equivalent)
lf.close_outliner()
lf.close_attributes()
lf.close_history_stack()
```

---

## Window Layouts

```lua
lf.save_layout("my_layout")       -- Saved to Layouts/ folder
lf.load_layout("my_layout")

local layouts = lf.list_layouts() -- Returns JSON array ["layout1", "layout2"]
```

---

## OS Tabs

```lua
lf.new_tab()    -- Open new scene in OS tab
lf.close_tab()  -- Close current tab
```

---

## Scripts & Examples

```lua
lf.run_script("/path/to/script.py")
lf.run_script("/path/to/script.lua")

local scripts = lf.list_scripts()    -- Returns JSON array of filenames
lf.open_scripts_folder()             -- Opens Scripts folder in Finder

local examples = lf.list_examples()  -- Returns JSON array of example names
lf.open_example("My Example")
lf.open_examples_folder()
```

---

## History Stack

```lua
lf.clear_undo()
lf.save_undo("/Users/me/undo_snapshot.jsonc")
lf.load_undo("/Users/me/undo_snapshot.jsonc")
```

---

## Complete Example

```lua
-- Full workflow example in Lua
lf.new_scene()
lf.create_light("directional")
lf.create_primitive("cube")
lf.create_primitive("sphere")
lf.create_camera()

lf.select_by_name("Cube")
local info = lf.get_selected()
print("Selected: " .. info)

lf.set_transform("obj_3", 2, 0, 0, 0, 0, 0, 1, 1, 1)
lf.rename_object("obj_3", "MyCube")

lf.deselect_all()
lf.select_by_name("MyCube")
lf.duplicate_selected()

lf.frame_all()
lf.set_shading("wireframe")
lf.show_grid(false)

lf.open_outliner()
lf.open_attributes()

lf.save_scene_as("/Users/me/example_scene.jsonc")
```

---

## Notes

- All scripting runs on the **main thread** so long operations block the UI.
- JSON strings returned by API functions can be parsed with any Lua JSON library (e.g., `dkjson`, `lunajson`).
- The `lf` table is registered automatically when the LuaPython engine initialises on first script execution.
- Errors follow the Lua convention of returning `nil, message`.
