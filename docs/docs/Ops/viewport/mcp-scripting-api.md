---
title: "MCP Server"
sidebar_label: "MCP Server"
sidebar_position: 6
description: "Expose the Viewport scripting API as a Model Context Protocol server."
---

# Lightfielder Viewport | MCP Server

The Viewport app exposes its full scripting API as a **Model Context Protocol (MCP) server**,
allowing AI coding assistants and other MCP clients to control the Viewport programmatically.

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    Viewport App                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ScriptingServer (TCP JSON-RPC, port 9876)           │   │
│  │ Routes lf.* commands to the active scene             │   │
│  └─────────────────────┬───────────────────────────────┘   │
└────────────────────────┼──────────────────────────────────┘
                         │ TCP 127.0.0.1:9876
┌────────────────────────▼──────────────────────────────────┐
│  Extras/mcp_server.py  (Python MCP server)                 │
│  Translates MCP tool calls → JSON-RPC to Viewport app      │
│  stdio transport for opencode / Claude Desktop etc.        │
└────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Launch the Viewport App

The app automatically starts the JSON-RPC server on port **9876**.
```
MCP Server: listening on port 9876
```
Visible in the app's console output.

### 2. Install Dependencies

```bash
pip install mcp
```

### 3. Connect with MCP

#### Using opencode

Add to your `opencode.json`:

```json
{
  "mcpServers": {
    "viewport": {
      "command": "python3",
      "args": ["/path/to/Viewport/Extras/mcp_server.py"]
    }
  }
}
```

#### Using Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "viewport": {
      "command": "python3",
      "args": ["/path/to/Viewport/Extras/mcp_server.py"]
    }
  }
}
```

#### Using any MCP client

```bash
python3 /path/to/Viewport/Extras/mcp_server.py
```

### 4. Interactive Test Mode

If the `mcp` library is not installed, `mcp_server.py` falls back to a
**direct TCP test mode** where you can send JSON-RPC commands manually:

```bash
$ python3 Extras/mcp_server.py
MCP library not installed. Running in test mode.
Connected to Viewport app at 127.0.0.1:9876

> {"method":"new_scene","params":[],"id":1}
{
  "jsonrpc": "2.0",
  "result": true,
  "id": 1
}
> {"method":"create_primitive","params":["cube"],"id":2}
{
  "jsonrpc": "2.0",
  "result": true,
  "id": 2
}
```

---

## Available MCP Tools

### Scene / File

| Tool | Description | Parameters |
|------|-------------|------------|
| `new_scene` | Create an empty scene | *(none)* |
| `open_scene` | Open a scene file | `path`: string |
| `save_scene` | Save current scene | *(none)* |
| `save_scene_as` | Save to new path | `path`: string |
| `revert_scene` | Revert to saved | *(none)* |
| `import_file` | Import a reference file | `path`: string |

### Create Objects

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_camera` | Add a camera | *(none)* |
| `create_locator` | Add a locator | *(none)* |
| `create_group` | Add an empty group | *(none)* |
| `create_reference` | Add a reference container | *(none)* |
| `create_audio` | Add an audio container | *(none)* |
| `create_note` | Add a note | *(none)* |
| `create_primitive` | Add a mesh primitive | `type`: `cube \| cone \| sphere \| cylinder \| pyramid \| torus` |
| `create_light` | Add a light | `type`: `ambient \| area \| directional \| dome \| point \| spot \| sphere \| tube` |

### Selection

| Tool | Description | Parameters |
|------|-------------|------------|
| `select_all` | Select everything | *(none)* |
| `deselect_all` | Clear selection | *(none)* |
| `select_by_name` | Select by partial name match | `name`: string |
| `select_by_id` | Select by exact ID | `id`: string |
| `get_selected` | Get details of selected objects | *(none)* |

### Edit

| Tool | Description | Parameters |
|------|-------------|------------|
| `undo` | Undo last action | *(none)* |
| `redo` | Redo last undone action | *(none)* |
| `cut` | Cut selected | *(none)* |
| `copy` | Copy selected | *(none)* |
| `paste` | Paste from clipboard | *(none)* |
| `delete_selected` | Delete selected objects | *(none)* |
| `duplicate_selected` | Duplicate selected objects | *(none)* |
| `group_selected` | Group selected | *(none)* |
| `ungroup_selected` | Ungroup selected group | *(none)* |

### Transform

| Tool | Description | Parameters |
|------|-------------|------------|
| `set_transform` | Set object transform | `id`, `position[3]`, `rotation[3]`, `scale[3]` |
| `get_transform` | Get object transform as JSON | `id`: string |
| `set_parent` | Reparent an object | `child_id`, `parent_id` (empty to detach) |
| `rename_object` | Rename an object | `id`, `name` |

### Viewport

| Tool | Description | Parameters |
|------|-------------|------------|
| `frame_all` | Frame all objects | *(none)* |
| `go_home` | Reset camera to home | *(none)* |
| `set_camera_mode` | Switch camera mode | `mode`: `orbit \| fps` |
| `set_shading` | Set shading mode | `mode`: `shaded \| boundingBox \| points \| wireframe \| none` |
| `set_interaction` | Set interaction mode | `mode`: `selection \| transform` |

### Display Toggles

| Tool | Description |
|------|-------------|
| `show_grid` | Toggle grid |
| `show_vertices` | Toggle vertex display |
| `show_normals` | Toggle normal display |
| `show_edges` | Toggle edge wireframe |
| `show_xray` | Toggle X-Ray |
| `show_hud` | Toggle HUD overlay |
| `show_fps` | Toggle FPS counter |
| `show_details` | Toggle detail info |
| `show_distance` | Toggle distance display |
| `show_render` | Toggle render info |
| `show_selected` | Toggle selected info |
| `show_camera_view` | Toggle camera view info |
| `show_polygons` | Toggle polygon count |
| `show_camera_locators` | Toggle camera icons |
| `show_light_locators` | Toggle light icons |
| `show_locator_icons` | Toggle locator icons |
| `show_skybox` | Toggle skybox |

Each takes a single parameter `on`: boolean.

### Windows

| Tool | Description |
|------|-------------|
| `open_outliner` | Open Outliner window |
| `open_attributes` | Open Attributes window |
| `open_history_stack` | Open History Stack |
| `close_outliner` | Close Outliner |
| `close_attributes` | Close Attributes |
| `close_history_stack` | Close History Stack |

### Layouts

| Tool | Description | Parameters |
|------|-------------|------------|
| `save_layout` | Save window layout | `name`: string |
| `load_layout` | Load window layout | `name`: string |
| `list_layouts` | List saved layouts | *(none)* |

### Tabs

| Tool | Description |
|------|-------------|
| `new_tab` | Open new scene in OS tab |
| `close_tab` | Close current tab |

### Scripts & Examples

| Tool | Description | Parameters |
|------|-------------|------------|
| `run_script` | Run a script file | `path`: string |
| `list_scripts` | List available scripts | *(none)* |
| `open_scripts_folder` | Open Scripts folder | *(none)* |
| `open_example` | Open an example scene | `name`: string |
| `list_examples` | List available examples | *(none)* |
| `open_examples_folder` | Open Examples folder | *(none)* |

### History

| Tool | Description | Parameters |
|------|-------------|------------|
| `clear_undo` | Clear undo history | *(none)* |
| `save_undo` | Save undo events to file | `path`: string |
| `load_undo` | Load undo events from file | `path`: string |

---

## Example Usage (openocode / MCP Client)

### Basic Scene Setup

```
Tool: new_scene
Tool: create_light       type="directional"
Tool: create_primitive   type="cube"
Tool: frame_all
```

### Building and Exporting

```
Tool: new_scene
Tool: create_light       type="directional"
Tool: create_primitive   type="cube"
Tool: get_selected       → [{"id":"obj_3","name":"Cube",...}]
Tool: set_transform      id="obj_3", position=[2,0,0], rotation=[0,0,0], scale=[1,1,1]
Tool: save_scene_as      path="/Users/me/output.jsonc"
```

### Scene Inspection

```
Tool: open_scene         path="/Users/me/scene.jsonc"
Tool: get_selected       → [...]
Tool: select_by_name     name="Camera"
Tool: get_selected       → [{"type":"camera",...}]
Tool: get_transform      id="obj_1"  → {"position":[0,2,6],...}
```

### Duplicating and Grouping

```
Tool: select_all
Tool: duplicate_selected
Tool: group_selected
```

### Layout Management

```
Tool: save_layout        name="my_workspace"
Tool: close_attributes
Tool: close_outliner
Tool: load_layout        name="my_workspace"
```

---

## Configuration

### Changing the Port

Set the port via environment variable or `UserDefaults`:

```bash
# Environment variable (Python MCP server)
VIEWPORT_MCP_PORT=9877 python3 Extras/mcp_server.py

# UserDefaults (Viewport app)
defaults write com.Lightfielder.Viewport MCPPort 9877
```

### Network

- The TCP server binds to **127.0.0.1** only (localhost).
- Firewall-friendly with no incoming connections from the network.
- Transport: raw TCP with **newline-delimited JSON**.  

### JSON-RPC Wire Format

**Request:**
```json
{"jsonrpc":"2.0","method":"frame_all","params":[],"id":1}
```

**Success response:**
```json
{"jsonrpc":"2.0","result":true,"id":1}
```

**Error response:**
```json
{"jsonrpc":"2.0","error":{"code":-1,"message":"Object not found"},"id":1}
```

**Data response:**
```json
{"jsonrpc":"2.0","result":[{"id":"obj_3","name":"Cube"}],"id":1}
```

---

## Troubleshooting

**"Cannot connect to Viewport app"**
- Ensure the Viewport app is running.
- Check the port: `lsof -i :9876`
- Verify no firewall is blocking localhost connections.

**"Method not found"**
- Check the tool name matches exactly (case-sensitive, snake_case).
- Update `mcp_server.py` if the app has been updated with new functions.

**"Operation failed"**
- The action could not be completed so check the Viewport app's console output for details.
- Common causes: no active scene, no object selected, invalid object ID.
