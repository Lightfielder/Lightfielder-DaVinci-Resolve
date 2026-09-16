# Lightfielder v26.09.15 B2 for DaVinci Resolve

Created by: [Andrew Hazelden](mailto:andrew@andrewhazelden.com)

## Public Beta 2 Release

This initial documentation is aimed at a professional audience already working in the 3D graphics and immersive media sector.

## Overview

Lightfielder is an LGPL-licensed open-source hybrid computer-vision IDE and digital content creation (DCC) toolset developed by Andrew Hazelden. Designed to unify volumetric video content creation and XR post-production.

Lightfielder for Resolve is a multi-view workflow automation toolset that streamlines the creation of volumetric experiences inside tools like BMD DaVinci Resolve Studio. It is designed to help video editors and colourists be more productive as they work with planar and polar grid array-filmed multi-view content.

The Python-scripted tools help automate common tasks that can be tedious and time-consuming to carry out manually. This makes creative tasks run smoothly when processing stacks of footage from large camera arrays.

![Toolbar](images/toolbar_about.png)

Note: Lightfielder also comes as a separate standalone app, and as a thin client. This self-hosted version is called [Lightfielder Ops](https://github.com/Lightfielder/LightfielderOperators). The Ops (Operators) software is now entering its initial private beta testing phase.

## Am I Lightfielder?

You might be. Are you tech-artist, photographer, or filmmaker working with multi-view content in the [plenoptic imaging](https://en.wikipedia.org/wiki/Light_field_camera) domain? Do you frequently capture or process lightfield data? If YES, then you can easily use the colloquial term "Lightfielder" to describe your craft.

## What is a Lightfield Capture of a Scene?

Lightfield recordings of a real-world or virtual scene provide a unique experience compared to traditional legacy VR/XR media types (like 360VR, 180VR, Fulldome, 3DTV, or Spatial Media).

When digitized, a lightfield based 3D scene-graph stores the captured content using a data structure that holds the individual samples of light rays. Each ray has a unique light intensity property and a light ray direction property that indicates the angle that the light beam is travelling along. 

This allows the observer of a lightfield scene asset to experience free-view motion (aka 6DoF navigation) when viewing the digital environment. The observer is able to interactively re-adjust the synthetic camera properties such as aperture, exposure, colour temperature, and shutter angle to sculpt the final cinematic result. A lightfield photography/filmmaking approach can be used to display a still representation of a scene (freezing a single moment in time), or a full motion version of the scene which supports narrative storytelling goals.

## GitHub Downloads

Go to the GitHub [Releases page](https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve/releases) to access the latest build of Lightfielder.

## Free Open-Source License Terms

Lightfielder is cross-platform compatible and works across Linux, macOS, and Windows. The software is released under a permissive free open-source LPGPL/GPL license. Attribution is required and must be maintained on forks of the Lightfielder project's codebase and scripts. 

Note: The bundled sound effects were acquired with a license specifically for the Lightfielder/Kartaverse project so are not open-source/public domain licensed content.

## Example Projects

Additional learning content and example project files are being prepared for Lightfielder this month.

- [Pikachu Still Frame 50 View (A1-E5) ZIP Archive (300 MB)](https://we.tl/t-STJrEEaqnLC4tVGK)

## Accessing Lightfielder inside Resolve

The Lightfielder workflow automation scripts are accessed using the "Workspace \> Scripts \> Lightfielder \> " menu system, or the Lightfielder toolbar with the (Command + F11) hotkey.

## Table of Contents

- [ReadMe (You are here)](README.md)
- [ChangeLog](ChangeLog.md)
- [Known Issues](Known_Issues.md)
- [PunchList](PunchList.md)
- Deployment
 	- [Install Python](Install_Python.md)
	- [Install Lightfielder](Install_Lightfielder.md)
 	- [Uninstalling Lightfielder](Uninstall_Lightfielder.md)
- Usage
	- [Toolbar Scripts](Toolbar.md)
		- [00 Toolbar](Scripts_00_Toolbar.md)
		- [01 Preferences](Scripts_01_Preferences.md)
		- [02 Bin Templates](Scripts_02_Bin_Templates.md)
		- [03 Shotlog Pre-Flight](Scripts_03_Shotlog_PreFlight.md)
		- [04 Import Footage](Scripts_04_Import_Footage.md)
		- [05 Metadata Sync](Scripts_05_Metadata_Sync.md)
		- [06 Still Frames Export](Scripts_06_Still_Frames_Export.md)
		- [07 Create EDLs](Scripts_07_Create_EDLs.md)
		- [08 Batch Trim](Scripts_08_Batch_Trim.md)
		- [09 EDL Stack Swizzle](Scripts_11_EDL_Stack_Swizzle.md)
		- [10 EDL Checker](Scripts_09_EDL_Checker.md)
		- [11 Log Viewer](Scripts_10_Log_Viewer.md)
		- [12 Video Track Solo](Scripts_12_Video_Track_Solo.md)
		- [13 Camera Contact Sheet](Scripts_13_Camera_Contact_Sheet.md)
		- [14 Grade Automation](Scripts_14_Grade_Automation.md)
		- [15 EDL Export](Scripts_15_EDL_Export.md)
		- [16 Extensions](Scripts_16_Extensions.md)
		- [17 Edit Jupyter Link](Scripts_17_Jupyter_Link.md)
		- [18 Open Lightfielder Folder](Scripts_18_Open_Lightfielder_Folder.md)
		- [19 Show Console](Scripts_19_Show_Console.md)
		- [20 Documentation](Scripts_20_Documentation.md)
		- [21 Edit Python Module](Scripts_21_Edit_Python_Module.md)
		- [22 About Lightfielder](Scripts_22_About_Lightfielder.md)
	- [Metadata Tags](Metadata_Tags.md)
	- [Shotlog Format](Shotlog.md)
	- [Deliver Page Presets](Deliver_Page_Presets.md)
	- [Unit Tests](Unit_Tests.md)

## Workflow Guides

- [Lightfielder Live Grade Video Flowchart](Workflow_Guides/Lightfielder_Live_Grade_Flowchart.md)
- [Lightfielder HDR Image Based Rendering](Workflow_Guides/Lightfielder_HDR_Image_Based_Rendering.md)
- [Volumetric Color Decision Lists](Workflow_Guides/Volumetric_Color_Decision_Lists.md)
- [PBR-GS Physically Based Rendering of Gaussian Splats](Workflow_Guides/Physically_Based_Rendering_of_Gaussian_Splats.md)

## Blog Content

- [Exploring the Puerto Rico Caveverse Project](https://medium.com/@andrewhazelden/kartaverse-journeys-f5a115840fa1)
- [Is this the right time to do Lightfield & 6DoF Virtual Production?](https://medium.com/@andrewhazelden/is-this-the-right-time-to-do-lightfield-6dof-virtual-production-ee0841bb500c)
- [6DoF VP (Virtual Production) Learning Resources for the Rest of Us](https://medium.com/@andrewhazelden/kartaverse-journeys-e482c15756b0)
- [XR & VP Asset Management](https://medium.com/@andrewhazelden/xr-vp-asset-management-c01a6e50fd8b)
- [Raytraced Volumetric Video Stitching](https://medium.com/@andrewhazelden/raytraced-volumetric-video-stitching-d907678d61f4)
- [Applying MAGI High Frame Rate Capture ideas to 4D Volumetric Scanning](https://medium.com/@andrewhazelden/applying-magi-high-frame-rate-capture-ideas-to-4d-volumetric-scanning-48c87e61f7d7)
- [Parametric Genome Driven Digital Human Modeling and Rendering Workflows 🧬](https://medium.com/@andrewhazelden/parametric-genome-driven-digital-human-modeling-and-rendering-workflows-ad71424b7088)

