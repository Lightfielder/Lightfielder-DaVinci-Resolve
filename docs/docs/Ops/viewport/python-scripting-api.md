---
title: "Python Scripting API"
sidebar_label: "Python Scripting API"
sidebar_position: 5
description: "The lf Python scripting API for Lightfielder Viewport."
---

# Lightfielder Viewport | Python Scripting API 

The Viewport app embeds **CPython 3.11 or 3.12** through the [LuaPython](https://github.com/Lightfielder/Lua-Python) framework.  

All Viewport functionality is available by importing the `lf` module:

```python
import lf

lf.new_scene()
lf.open_scene("/path/to/file.jsonc")
```

The `lf` module is registered automatically when the LuaPython engine initialises
and is available in both the `__main__` scope and via `import lf`.

---

## Convention

Functions return `None` on success and raise `RuntimeError` on failure.

Functions that return data (like `lf.get_selected`, `lf.list_layouts`) return
a **Python object** (list or dict) parsed from JSON.

Primitive and light type names are **lowercase**:

```python
lf.create_primitive("cube")      # not "Cube"
lf.create_light("directional")   # not "Directional"
lf.set_camera_mode("orbit")      # not "Orbit"
lf.set_shading("wireframe")      # not "Wireframe"
```

Display toggles accept a **boolean** (`True` / `False`).

---

## Scene / File Operations

```python
lf.new_scene()

try:
    lf.open_scene("/Users/me/scenes/my_scene.jsonc")
except RuntimeError as e:
    print(f"Failed: {e}")

lf.save_scene()
lf.save_scene_as("/Users/me/scenes/copy.jsonc")
lf.revert_scene()
lf.import_file("/Users/me/models/car.obj")
```

---

## Creating Objects

```python
# Scene objects
lf.create_camera()
lf.create_locator()
lf.create_group()
lf.create_reference()
lf.create_audio()
lf.create_note()

# Primitives (lowercase)
lf.create_primitive("cube")
lf.create_primitive("cone")
lf.create_primitive("sphere")
lf.create_primitive("cylinder")
lf.create_primitive("pyramid")
lf.create_primitive("torus")

# Lights (lowercase)
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

```python
lf.select_all()
lf.deselect_all()
lf.select_by_name("Cube")      # partial name match
lf.select_by_id("obj_5")       # exact id match

selected = lf.get_selected()   # returns list of dicts
for obj in selected:
    print(f"{obj['name']} at {obj['position']}")
```

Example return from `get_selected()`:

```python
[
    {
        "id": "obj_3",
        "name": "Cube",
        "position": [0.0, 0.0, 0.0],
        "rotation": [0.0, 0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "type": "mesh",
    }
]
```

---

## Edit Commands

```python
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

```python
# Set transform: id, position, rotation, scale (each as list of 3 floats)
lf.set_transform("obj_3", [0, 0, 0], [0, 0, 0], [2, 2, 2])

# Get transform returns a dict
t = lf.get_transform("obj_3")
print(t["position"])  # [0.0, 0.0, 0.0]

# Reparent: child_id, parent_id
lf.set_parent("obj_3", "obj_1")

# Detach from parent (empty string)
lf.set_parent("obj_3", "")

# Rename object
lf.rename_object("obj_3", "MyCube")
```

---

## Viewport Control

```python
lf.frame_all()
lf.go_home()
lf.set_camera_mode("orbit")      # "orbit" | "fps"
lf.set_shading("shaded")         # "shaded" | "boundingBox" | "points" | "wireframe" | "none"
lf.set_interaction("selection")  # "selection" | "transform"
```

---

## Display Toggles

All take a `bool`:

```python
lf.show_grid(True)
lf.show_vertices(False)
lf.show_normals(False)
lf.show_edges(True)
lf.show_xray(False)
lf.show_hud(True)
lf.show_fps(False)
lf.show_details(False)
lf.show_distance(False)
lf.show_render(False)
lf.show_selected(False)
lf.show_camera_view(False)
lf.show_polygons(False)
lf.show_camera_locators(False)
lf.show_light_locators(False)
lf.show_locator_icons(True)
lf.show_skybox(False)
```

---

## Auxiliary Windows

```python
lf.open_outliner()          # Opens Outliner window (F6 equivalent)
lf.open_attributes()        # Opens Attributes window (F7 equivalent)
lf.open_history_stack()     # Opens History Stack (F5 equivalent)
lf.close_outliner()
lf.close_attributes()
lf.close_history_stack()
```

---

## Window Layouts

```python
lf.save_layout("my_layout")
lf.load_layout("my_layout")

layouts = lf.list_layouts()            # returns list of strings
print(layouts)                         # ["layout1", "layout2"]
```

---

## OS Tabs

```python
lf.new_tab()     # Open new scene in OS tab
lf.close_tab()   # Close current tab
```

---

## Scripts & Examples

```python
lf.run_script("/path/to/script.py")
lf.run_script("/path/to/script.lua")

scripts = lf.list_scripts()            # list of filenames
lf.open_scripts_folder()

examples = lf.list_examples()          # list of example names
lf.open_example("My Example")
lf.open_examples_folder()
```

---

## History Stack

```python
lf.clear_undo()
lf.save_undo("/Users/me/undo_snapshot.jsonc")
lf.load_undo("/Users/me/undo_snapshot.jsonc")
```

---

## Complete Example

```python
import lf

# Create a new scene
lf.new_scene()

# Add lighting and geometry
lf.create_light("directional")
lf.create_primitive("cube")
lf.create_primitive("sphere")
lf.create_camera()

# Select and inspect
lf.select_by_name("Cube")
info = lf.get_selected()
print("Selected:", info)

# Transform
lf.set_transform("obj_3", [2, 0, 0], [0, 0, 0], [1, 1, 1])
lf.rename_object("obj_3", "MyCube")

# Duplicate
lf.deselect_all()
lf.select_by_name("MyCube")
lf.duplicate_selected()

# Viewport
lf.frame_all()
lf.set_shading("wireframe")
lf.show_grid(False)

# Windows
lf.open_outliner()
lf.open_attributes()

# Save
lf.save_scene_as("/Users/me/example_scene.jsonc")
```

---

## Tips

- Run `.py` scripts from Viewport's **Scripts** menu or via `lf.run_script()`.
- The scripting engine is synchronous so long scripts will block the UI.
- Import `lf` at the top of any Python script for full Viewport control.
- All list/dict return values (from `get_selected`, `get_transform`, etc.) are
  native Python objects so no JSON parsing needed.
