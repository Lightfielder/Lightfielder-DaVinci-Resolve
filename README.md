# Lightfielder v26.09.18 B3 for DaVinci Resolve

Created by: [Andrew Hazelden](mailto:andrew@andrewhazelden.com)

## Public Beta 3 Release

This initial documentation is aimed at a professional audience already working in the 3D graphics and immersive media sector.

## Overview

Lightfielder is an LGPL-licensed open-source hybrid computer-vision IDE and digital content creation (DCC) toolset developed by Andrew Hazelden. Designed to unify volumetric video content creation and XR post-production.

Lightfielder for Resolve is a multi-view workflow automation toolset that streamlines the creation of volumetric experiences inside tools like BMD DaVinci Resolve Studio. It is designed to help video editors and colourists be more productive as they work with planar and polar grid array filmed multi-view content.

The Python-scripted tools help automate common tasks that can be tedious and time-consuming to carry out manually. This makes creative tasks run smoothly when processing stacks of footage from large camera arrays.

![Toolbar](Lightfielder/Docs/images/toolbar_about.png)

Note: Lightfielder is also available as a separate standalone app. This self-hosted version is called [Lightfielder Ops](https://github.com/Lightfielder/LightfielderOperators). The Ops (Operators) software is now entering its initial private beta testing phase.

## Am I Lightfielder?

You might be. Are you a tech artist, photographer, or filmmaker working with multi-view content in the [plenoptic imaging](https://en.wikipedia.org/wiki/Light_field_camera) domain? Do you frequently capture or process lightfield data? If YES, then you can easily use the colloquial term "Lightfielder" to describe your craft.

## What is a Lightfield Capture of a Scene?

Lightfield recordings of a real-world or virtual scene provide a unique experience compared to traditional legacy VR/XR media types (like 360VR, 180VR, Fulldome, 3DTV, or Spatial Media).

When digitized, a lightfield based 3D scene-graph stores the captured content using a data structure that holds the individual samples of light rays. Each ray has a unique light intensity property and a light ray direction property that indicates the angle that the light beam is travelling along. 

This allows the observer of a lightfield scene asset to experience free-view motion (aka 6DoF navigation) when viewing the digital environment. The observer is able to interactively re-adjust the synthetic camera properties such as aperture, exposure, colour temperature, and shutter angle to sculpt the final cinematic result. A lightfield photography/filmmaking approach can be used to display a still representation of a scene (freezing a single moment in time), or a full motion version of the scene which supports narrative storytelling goals.

## GitHub Downloads

Go to the GitHub [Releases page](https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve/releases) to access the latest build of Lightfielder.

## Free Open-Source License Terms

Lightfielder is cross-platform compatible and works across Linux, macOS, and Windows. The software is released under a permissive free open-source LPGPL/GPL license. Attribution is required and must be maintained on forks of the Lightfielder project's codebase and scripts. 

Note: The bundled sound effects were acquired with a license specifically for the Lightfielder/Kartaverse project so are not open-source/public domain licensed content.

## Software Requirements

- If you are running Lightfielder with Resolve Studio, it is suggested to have either Resolve Studio v20.x or 21.1.x installed.
- If you are running Lightfielder with Resolve (Free), it is suggested to have either Resolve (Free) v18.6.6 or v19.0.3 installed. Using v19.0.3 is the highest version number possible with a free copy of Resolve for the reasons listed below:
	- Note: BMD removed access to the Resolve API's UI Manager (GUI) user interface library at Resolve (Free) v19.1.
	- Note: BMD removed access to the Resolve API's entire Python scripting functionality at Resolve (Free) v21.1.0.

**Resolve (Free) Volumetric Beginner Tip:**

If you are a hobbyist, indie filmmaker, or educator, and your volumetric camera array uses 4K UHD resolution video cameras, you can still use a majority of the Lightfielder features with DaVinci Resolve (Free).

This approach certainly gives an accessible and affordable route to enter volumetric research and learning. If you enjoy the process, you can easily upgrade to Resolve Studio at any time, when you wish to unlock access to higher-resolution editing timelines, or the extra features BMD offers in their paid products.

## Example Projects

Additional learning content and example project files are being prepared for Lightfielder this month.

- [Pikachu Still Frame 50 View (A1-E5) ZIP Archive (300 MB)](https://we.tl/t-STJrEEaqnLC4tVGK)

## Accessing Lightfielder inside Resolve

The Lightfielder workflow automation scripts are accessed using the "Workspace \> Scripts \> Lightfielder \> " menu system, or the Lightfielder toolbar with the (Command + F11) hotkey.

## Documentation

The Lightfielder docs during the initial public beta phase are located on-disk at: [Lightfielder:/Docs/README.md](Lightfielder/Docs/README.md)  
