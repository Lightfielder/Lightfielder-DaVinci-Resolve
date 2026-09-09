# Lightfielder | PunchList

## Short-term Dev Tasks

### Enable "01 Preference.py" Backend Code and Script UI Controls

Add and test the backend code required to support the following script preference options:

- Drop Frame Timecode (DF)
- Toolbar Preset
	- Toolbar Settings
	- Toolbar Grid Layout "X Wide by Y Tall"
- Minimal Timecode Sync
- Use Current Folder Hierarchy
- Create One Timeline
- Preserve Gap
- Assign Angle to Track Name
- Remove Empty Tracks
- OTIO

Scripts to Update:

- Shotlog Pre-Flight.py
- EDL Export.py
- Camera Contact Sheet Polar.py
- Extensions.py
- Batch Trim "Validate" and "Apply" Modes
- Swizzle with trimmed clip ranges

### Accelerate the Import Footage and Metadata Sync Tasks

Accelerate the speed of automated R3D media data-heavy tasks in Resolve. This centers around the media pool clip importing, and applying metadata stages.

### Create One Timeline

> Windows = Stack Swizzle and Create EDLs

- The "05 Still Frames Export" script has a checkbox control named "Create One Timeline". When this control is active alongside the Track Layout: "To Vertical Stack" control being selected, multiple vertical stacks of video clips are created.

This packs all the videos from many capture sessions into a unified dense grid. This mode would be useful to add to the Stack Swizzle and Create EDLs dialogs to allow multi-take clips, in a horizontal stack, to be pushed to a common vertical stack dense grid layout.

### Video Track Naming via Angle 

> Windows = Still Frames Export & Create EDLs

- When creating "Vertical Stack" timelines add an option to the script for renaming each video track from V1, V2 so the 50 or so tracks are displayed with the active "Angle" metadata record from a multi-view video clip like "E5" or "Z977".

### Update Polar Camera Contact Sheet

- Finish adding a Polar layout option to the Camera Contact Sheet window.

## Longterm Dev Tasks

### Multi-lingual Localization Support

- Move all of the Lightfielder user interface text strings and toolip messages into an external resource so it is possible to manage sevral different localized translations of the toolset. Validate UTF8 multi-byte character handling support. This  makes it possible to support more languages than purely English. The Resolve/Fusion native language preferences could help drive the selection of the active Lightfielder language parameters by default, too.

### Stereo Pair Footage Matching

When left and right eye views are imported from a multi-view Stereo 3D SfM camera rig, the native Resolve media pool attributes for stereo pairing of the clips could be used. This would allow for native Stereo 3D based review of the media in the Edit and Color pages. It would also help to better manage the Deliver page exports.

### Add a new Plugin Interface

- Build out a modular Python based plugin interface spec to support user defined arbitrary camera rigs, media ingest, metadata tagging, etc.

### More Camera Array Geometry Options

- Add support for Python script extensions for defining new arrays
- Add support for a wider range of camera rig data interchange formats including:
	- [Agisoft Metashape (XML)](https://github.com/agisoft-llc/metashape-scripts)
	- [Alembic (ABC)](https://www.alembic.io/)
	- [COLMAP Text and Binary (TXT, BIN)](https://colmap.github.io/format.html)
	- [Comma Separated Values (CSV)](https://en.wikipedia.org/wiki/Comma-separated_values)
	- [Filmbox (FBX)](https://www.autodesk.com/products/fbx/overview)
	- [Image File List (IFL)](https://help.autodesk.com/view/3DSMAX/2024/ENU/?guid=GUID-CA63616D-9E87-42FC-8E84-D67E1990EE71)
	- [OpenUSD (USD, USDA, USDC, USDZ)](https://openusd.org/release/api/class_usd_geom_camera.html)
	- [Open Photogrammetry Format (OPF)](https://pix4d.github.io/opf-spec/)
	- [Reality Capture/RealityScan (XMP)](https://rshelp.capturingreality.com/en-US/tools/xmpalign.htm)

### EDL Export

- Improve spatial audio and OTIO focused EDL export automation options.
- Provide a way to quickly place scaled versions of multiple camera view angles onto the same final video frame so you can see them at the same time. Add a few text based title elements as well for labelling what is being shown. The Individual clip export mode would likely be disabled when this format of deliverable is rendered if a movie file is wanted in addition to the still photo.
