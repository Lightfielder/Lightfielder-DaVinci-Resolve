# **The OBJ-GS Guide**

Hi. Welcome to the initial draft version of the "Wavefront OBJ | Gaussian Splatting" guide. An up-to-date version of this same content can be found on the [Lightfielder PBR-GS GitHub Repo](https://github.com/Lightfielder/PBR-GS/edit/master/OBJ-GS.md).

This document describes a novel approach to convert the frozen (static) Alias | Wavefront .obj file format into something that continues forward, into an extended living file format. This extension to the established spec has transparent backwards compatibility that gracefully works with legacy 1996-2024 era OBJ file parser code. 

This guide adds several new parameters to the .mtl and .obj files, and ships with several suggestions for asset packaging conventions with the primary goal to keep this foundational 3D file format relevant for new and evolving workflows.

A precedent for this type of aftermarket evolution to an existing format has already been set when [Ben from Exocortex](https://ben3d.ca/blog/extended-wavefront-obj-mtl-for-pbr) added PBR attributes to Wavefront MTL files that Blender and other DCC tools now support. 

Also, the whole 3DGS ecosystem did not bat-an-eye for a moment when the old-school "[Stanford Bunny](https://en.wikipedia.org/wiki/Stanford_bunny)" and "[Utah Teapot](https://en.wikipedia.org/wiki/Utah_teapot)" centric .ply format from ages ago, had spherical harmonics shading information appended. This .ply wrapper for splatting data is now the baseline standard for Gaussian Splatting data interchange, not an odd-ball anomaly. 

# Who am I?

I'm Andrew Hazelden, a compositing technical director (aka a comp TD) based out of Nova Scotia, Canada. I run Dover Studios, Inc. with my brother Rusty Hazelden (a Pixar RenderMan Certified Trainer).

My personal background, for the last 20 years+ is to build new immersive workflows for media projects I am directly attached to as an external consultant. This means in 2026 that my primary objective is to streamline multi-view "lightfield" based post-production efforts, and smooth things out with customized workflow automation tech. 

After time off from January to September, this autumn I'm officially back into the "XR production" fray, again. I'm actively toying with the need to deploy solutions that simplify cross-vendor asset handoff, and multi-shot content delivery needs. 

The focus is to accelerate the creation of multi-view centric intermediate assets. This means handling content pushed between multiple artists and teams, that are spread across the divide of a larger all-encompassing hybrid VFX/ML/3D Scanning/Volumetric video post workflow. 

This OBJ-GS paper's initial proving-ground test will be through the usage on my next R\&D project which is called "[Lightfielder Operators (Ops)](https://github.com/Lightfielder/LightfielderOperators)". The node-based "Ops" software was built as an experimental multi-view "test-bed" IDE (Integrated Development Environment) during my down time, at the start of the year. Ops runs as a standalone desktop / tablet based companion app. 

Lightfielder Ops is intended to be used primarily as a rapid on-set previz/tech-viz toolset that exists in the same connected ecosystem of tools, alongside the newly open-sourced "[Lightfielder for DaVinci Resolve](https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve)" release that shipped at IBC 2026 as a free LGPL licensed public beta this month.

# **Wavefront OBJ Format Extensions for VFX**

Date Created: Sept 28, 2026 at 02:07 PM (UTC \-3)  
Date Updated: Oct 1, 2026 at 11:31 PM (UTC \-3)  
Docs Written By: [Andrew Hazelden](mailto:andrew@andrewhazelden.com)  
OBJ-GS Project Title Named By: [Didier Muanza](mailto:didier.muanza@gmail.com)

Edition: Draft Zero of the core idea:

* Support a per-model .gz or .zip compressed folder based project hierarchy  
  * The data is archived as a "store compressed" asset similar to an OpenUSD file .usdz zipped container  
  * Zip/GZIP compression is fast to decode. They allow the scene data to be live-read by cross-platform compatible frameworks like the [z-lib library](https://en.wikipedia.org/wiki/Zlib), on-the-fly, without the need to pre-extract the files to disk first.  
  * It should be mentioned in a \~2018-2020ish timescale that SketchFab allowed volumetric sequences of approx 120 frame duration to be sourced from zipped OBJ meshes and texture sequences   
* With OBJ folder compressed assets, we can store any of the following sidecar elements inside the OBJ project folder's hierarchy:  
  * Setup.json automates loading the scene hierarchy and any user defined data records into a generic [Python dict](https://www.w3schools.com/python/python_dictionaries.asp) or [Lua Table](https://www.lua.org/pil/2.5.html) structure. The [JSON](https://www.json.org/json-en.html) file can act as a scene loading template to rapidly bootstrap the scene assembly processes. OR  
  * Scene.csv CSV ([Comma Separated Value](https://en.wikipedia.org/wiki/Comma-separated_values)) spreadsheet based asset instancing and referencing can work for a simplistic scene assembly approach with per-asset level model variations  
  * Readme.md guide provides a VFX vendor handoff document that explains how to translate the customized OBJ extension attributes and channel mappings when compared to the existing FBX/Alembic/OpenUSD file format specifications  
  * Wavefront .obj meshes  
    * OBJ file header has a comment with the [Timecode](https://en.wikipedia.org/wiki/Timecode) value  
    * [Pixar OpenSubD](https://www.opensubdiv.org/docs/intro.html) Crease support added to the OBJ file  
    * Wavefront MTL file referenced from OBJ mesh holds PBR attributes, as well as external [MaterialX](https://materialx.org/) .mtlx material and [PTEX](https://ptex.us/overview.html) resource file names  
    * Support SPH ([Spherical Harmonics](https://en.wikipedia.org/wiki/Spherical_harmonics)) data storage between MTL files and as per-point sample/per-vertex color records in the OBJ file. This data is encoded with the same attribute names present in 3DGS based .ply files. It is hoped that [PBR-GS](https://github.com/Kartaverse/PBR-GS) approaches and the concepts shared by the earlier [Kartaverse for Houdini COPs demos](https://kartaverse.github.io/Kartaverse-for-Houdini/#/pbr/pbr) would be useful to help support interactive asset relighting.  
  * Wavefront .mtl materials  
    * Add [OpenPBR](https://github.com/AcademySoftwareFoundation/OpenPBR) shading model support with a goal of handling [Substance Painter](https://www.adobe.com/products/substance3d/apps/painter.html) PBR Metal Roughness based texture maps. ([Exocortex lead a PBR effort so that concept pre-exists](https://ben3d.ca/blog/extended-wavefront-obj-mtl-for-pbr))  
    * [MaterialX](https://materialx.org/) file with relative path reference support added in .mtl file for shader attributes  
    * [PTEX](https://ptex.us/overview.html) file with relative path reference support added in .mtl file for shader attributes. This allows texturing 3D models without the need for UV layouts via per-polygon face mapped textures.  
    * Flexible image and image sequence based media handling, and time-based frame controls, with relative path reference support added in the .mtl file for shader attributes that can be packaged as a zipped OBJ asset  
    * [OGraf](https://ograf.ebu.io/), [Lottie](https://lottie.github.io/), and [SVG](https://en.wikipedia.org/wiki/SVG) files as textures, with relative path reference support added in the .mtl file for shader attributes  
    * Movie files with relative path reference support added in the .mtl file for shader attributes  
  * Optional extras for more complex workflow needs:  
    * Cameras.txt files hold SfM ([Structure from Motion](https://en.wikipedia.org/wiki/Structure_from_motion)) style [COLMAP](https://colmap.github.io/) camera poses for 3D scanning, and multi-plane DMP (Digital [Matte Painting](https://en.wikipedia.org/wiki/Matte_painting)) camera texture projection needs  
    * [Open-Pose JSON](https://cmu-perceptual-computing-lab.github.io/openpose/web/html/doc/md_doc_02_output.html) for character rigs, and for ComfyUI \+ NVIDIA DLSS like style transfer, and paint-over workflows  
    * Audio clips for lip synced dialog, soundtracks, room tone, or sound effects  
    * Subtitle.srt adds [subtitles](https://en.wikipedia.org/wiki/SubRip) for multi-shot EDLs, multi-lingual lipsync dialog assistance, and animation timing work  
    * Lens.json for defining the settings used in Lens-space [STMAP](https://docs.google.com/document/d/1lQ-wc9ucLJqj-HL7iKMNWA71klV5O1fk2-JicRB6gDY/edit?tab=t.0#heading=h.abzdtec4alet) lens distort maps, Brown Conrady / [OpenCV](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html) / Nuke K1-K3+ [lens distortion](https://en.wikipedia.org/wiki/Distortion_\(optics\)), or [OpenTrackIO](https://ris-pub.smpte.org/ris-osvp-metadata-camdkit/) / [OpenLensIO](https://ris-pub.smpte.org/ris-osvp-metadata-camdkit/res/OpenLensIO_v1-0-1.pdf)  
    * [Cooke Optics /i Technology](https://cookeoptics.com/product/i-technlogy/) lens metadata with per-frame support from cinema lenses  
    * [CDL](https://en.wikipedia.org/wiki/ASC_CDL)/[LUT](https://en.wikipedia.org/wiki/3D_lookup_table)/[OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) EDLs for post-production to apply multi-shot [volumetric grading](https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve/blob/main/Lightfielder/Docs/Workflow_Guides/Volumetric_Color_Decision_Lists.md), and editing/timeline based [clip sequencing](https://github.com/Lightfielder/LightfielderOperators/blob/main/Ops/Docs/Sequencer.md)  
    * [Apache Parquet](https://parquet.apache.org/) for extended data tables for the scene data. Can scale massively and supports data driven visuals.

# What do I want data conversion and asset archiving tech to do?

I want to work with 3D scanner and LIDAR focused software like:  
Metashape Python Module / Meshroom / RealityScan / COLMAP / Leica Cyclone / FARO scene / InstantNGP / nerfstudio / CloudCompare / MeshLab / etc

And use the updated scene-assembly focused OBJ extension approach with other pipeline tools written in Python, LuaJIT, Javascript/NodeJS, Rust, C++, etc..

I also want to more easily exchange 3D scan data data between DCC apps like: Houdini, Unreal Blueprints/Metahumans/Twin-motion, Reallusion, Marvelous Designer, OpenPose, ComfyUI, and 3D Coat. 

The Python, and general purpose scripting support for OBJ-GS should also be made to work inside of LightWave3D, Blender, Maya, 3DS Max, C4D, Katana, Omniverse, Unity3D, Godot, Cascadeur, Rumba/Guerilla Render, JangaFX apps, Adobe AE, NukeX/Nuke Studio, Flame, Resolve/Fusion, and OTOY Studio.

# Why should we do something different like this, right now?

This XKCD comic storyline explains how new standards proliferate all over the place:  
[https://xkcd.com/927/](https://xkcd.com/927/)

The one word answer is "Lightfielder" needs this if it wants a generic container format to support archiving 3D scan data. One can't realistically demand a small team adopt and use HoudiniFX with SOLARIS as the only deliverable option for this field. 

A base fallback container format is needed for Lightfielder’s pipeline stack. This will allow the effort to dip its toes into a concept called "Renderless Compositing" that facilitates an in-memory way to bridge multi-view data. The core idea with a renderless composition task, is to avoid filling disk arrays with intermediate temp files, and proxies for all of the XPU (CPU \+ GPU) live-rendered imagery that your DCC apps output to support multi-pass rendering/comp, and volumetric color grading. Metadata drives the process fully.

On the independent production side of things you are likely to have a core team size of \~1- 10 artists. At this level of budget and complexity, OpenUSD technology is too high of an entry barrier for the full range of pipeline tools and scripts one might adopt across 100% of the performance capture, and 3D scanning, content creation, and realtime playback side.

The generic pipeline/comp technical director's reply to this OBJ Extension suggestion is likely an initial puzzled look. Then a little while later, that same person is voted most likely to mention several of the talking points listed below, if you chat with them long enough to understand their struggles:

* [FBX](https://www.autodesk.com/products/fbx/overview) is typically a pain to modify: Autodesk's FBX container format is typically used as an opaque binary file format for exchanging textured 3D models with lighting & cameras. It started out as the format for working with motion captured characters and skeletal rigs from the program Motion Builder (Kaydara Filmbox). If you change a single element inside a 750 MB FBX formatted 3D model, each revision becomes an ever growing backup problem as iterations occur. Make 10 revisions and you have 10 x 750MB of data on hand to store.  
* [GLTF](https://www.khronos.org/gltf/) is optimized as a single-asset per file based document format. This is very similar to FBX files in their lack of a strong scene assembly and external asset referencing feature set.   
* [Alembic](https://www.alembic.io/) dropped the ball on many aspects, and took so long to evolve that OpenUSD came to the forefront and tried to do better. There is little evolution planned for Alembic.  
* Pixar's OpenUSD format is frequently too complex for easily re-packing "baked" assets with in-place editing of the file and resaving the 3D model back to disk. This means if you want to use an OpenUSD file inside a scene assembly task you don't have a lot of options outside of Houdini SOLARIS or the Foundry's Katana.  
* The [Stanford PLY](https://en.wikipedia.org/wiki/PLY_\(file_format\)) format is often more of a pain to rely on if you need consistent support in DCC apps, when compared to Wavefront OBJ meshes. But you can easily convert the data as needed between PLY and OBJ.

All DCC apps seem to have a minimal Wavefront OBJ I/O option. And they have scripting access, too. So you could apply native to the host DCC APP extra metadata to the scene-graph data on import, and push it out again afterwards to disk. 

So this skunkworks project is more of an OBJ overlay/extension than a full replacement of the Alias | Wavefront OBJ 3D file format specification. A nice, comfortable saftey net exists with this approach, since you always have the base fallback spec of a classic .obj mesh and .mtl file solution that works identically to the "old ways" of working since even the \~1996-1998 era of SGIs and the Alias | Wavefront Power Animator software can still read the asset.

Using an "OBJ zipped folder" project wrapper approach also makes single file uploads work mlre effectively with "Web app" hosted SaaS like content running in a web browser session called a ([PWA](https://web.dev/learn/pwa/progressive-web-apps/)) Progressive Web App. 

Additionally, the single-file archived OBJ project hiearchy idea allows compact portable assets to be displayed using [WebXR](https://immersive-web.github.io/), [WebGPU](https://webgpu.org/), [BabylonJS](.), and [ThreeJS](https://threejs.org/) like webpage embeds. This "OBJ \+ more" concept makes it feasible to push single-file assets to LAN based air-gapped local web browser sessions, or for indies to use online hosted javascript powered simple SaaS platforms that could interact with the scene exchange focused containerized assets on a mobile phone or tablet device.

Yeah, OpenUSD does much of what the OBJ extension wants to do, but [USDZ](https://openusd.org/release/spec_usdz.html) is failing in many places to be **fully interoperable** without severe issues, across all DCC apps and key utilities that are essential to a project's completion. 

In my view of things, increasing the overall pipeline R\&D cost, and allocated budget spend level to play with OpenUSD assets, at the same level of depth and capability as Houdini, Katana, Multiverse, or Clarisse (EOL) provide for scene assembly tasks, is very often understated at the start of a project. And it is not miscalculated by a small margin, but infact by a whole a lot of 💸💸💸.

My intuition normally attributes this large disparity gap in implementation cost vs overall benifit, as something reducable to a mix of key factors, including naive optimism, and the very real excitement to be playing with innovative tech on the cutting edge. At the end of a long, drawn out project, even the most ardent 
OpenUSD supporters seem to recalibrate their sentiment with hindsite informed from personal experience.

Often, the technical debt issues with deploying a pure end-to-end USD workflow are too high, to receive the full architectural upsides promised "on the side of the tin", when you initially played along with your in-house experts and agreed to adopt it, system wide, just to make a named specific staff member happy. 🙂

The idea for this OBJ-GS paper is built primarily from these prior efforts:

* [https://github.com/Kartaverse/PBR-GS](https://github.com/Kartaverse/PBR-GS)  
* [https://ben3d.ca/blog/extended-wavefront-obj-mtl-for-pbr](https://ben3d.ca/blog/extended-wavefront-obj-mtl-for-pbr)  
* [https://projects.blender.org/blender/blender/commit/a99a62231e04](https://projects.blender.org/blender/blender/commit/a99a62231e04)  
* [https://lebrov.com/octane-pipeline](https://lebrov.com/octane-pipeline)

# Why can't you just accept OpenUSD as the one true post-production format for all? Are you just trying to be difficult?

The real world is constructed from shades of grey, that extends in every direction and in all of the varying world / scene scales you look at. So there is no black & white like simplicity, to any complex decision remaining unsolved on your longterm todo list. 

This is an important factual realization for a new pipeline developer, or standards pusher to findout IRL and accept. Its quite similar to "Murphy's Law" or rapidly discovering the existence of actual physically bound Karma (which is often classed as a "FAFO" decision making event, in our part of the media sector). 

So Yes… OpenUSD, Alembic, and FBX files are going to be scattered everywhere in an XR pipeline once you go past the first staff person doing everything by themself. That format war, is pretty much unavoidable, when linking many staff people, with many tools, where they need to be used together, to make a larger creative project happen. 

If a 3D scanned mesh needs to go through a manual rebuilding of the mesh topology or UV layout, then you will often send the model out to a 3rd party sculpting tool, or a voxel based app that works with OpenVDB or Wavefront OBJs. 

A lot of the advertised elegance, just got lost in that singular data cleanup operation, from your pie-in-the sky beautiful pipeline of modernness. Let's go over this a bit more so there are no missed subtleties for the people at the back of the room eating 🍩 donuts.

The moment you hit the big export button, to save your data into another 3D file format, that is the point your "high concept" OpenUSD nested, externally referenced, scene graph doesn't account for much. It honestly showed we still aren't there yet and the USD grand vision from Late 2013-ish, that I signed up for and made one of the [first externally produced OpenUSD syntax highlighters for](https://github.com/Lightfielder/PIXAR-USD-Syntax-Highlighter), has not finished being constructed. It's incomplete. It's not fully done after, what for me is now \~13 years later.

And truthfully, if you weren't using OpenUSD but were an Autodesk FBX user for data handoffs, your bloated, ugly, and now randomly triangulated FBX mesh export. Has a lot of issues hiding under the surface. Maybe it's the flipped normals from your 3D printer focused STL file. Or it's that your FBX file is 750 MB and it has texture maps pushed along for the ride, and all instances like nuts and bolts on a vehicle had their instanced relationship destroyed. Likely, all of the renderer proprietary attributes were so tampered with you have to rebuild all materials if you aren't a Lambert, Blinn, or Phong shading model user from the times of Autodesk Maya 8.5 or Motion Builder. 

Your latest Alembic exports just trashed your beautiful rectangular area lights and dome lights, and turfed out your shading networks, and the rigging data (blend shapes, weight maps, clusters, spline deformers, lattice deformers, etc) is not the same fidelity as you started with. And the list of asset shredding continues. Instances are not so much preserved as Alembic has the largest data compression scheme ever running behind the curtain to hide the data bloat. You still shutter at the failed promises of Ogawa vs HDF5 era Alembic data interoperability, that went poof 💨once a new team of pipeline devs arrived, and tinkered with your makefiles to optimize things.

Maybe you have tamed the beast and avoided all this mess. In the 'I have achieved enlightenment' world, of a pure USD scene graph, one often needs a more primitive way to pack assets and archive them.

If you are in film & TV production, all of this data translation effort still happens before the project you are working on is sent off to the final render farm as PRMan .rib/ Arnold .ass/ or V-Ray .vrscene like renderer specific standalone files.

# Closing Thoughts

It's a big world, and there is likely room for a few more ways to do things. The specs "PBR-GS" and "OBJ-GS" are helping to reshape and improve the "indie self-funded" end of XR production and post.

With the right nudge of accessible tooling, and efficient tech, it's possible you might just land on a few grey-hair saving QoL (Quality of Life) improvements that can help save your bacon 🥓, improve your sleep schedule, and maintain your teams sanity.

There is no award issued for "working yourself to death" 🪦in the multi-view field: Think smarter, and focus on implementing processes that help the filmmaking and story craft aspects thrive. 

Also, don't be "blinded by the tech" as a long time friend and London based VFX supervisor reminded me, in the early VP stage rollout era.

Regards,  
Andrew Hazelden  
[Lightfielder Developer](https://github.com/Lightfielder/)  
Dover Studios, Inc.  
West Dover, Nova Scotia, Canada
