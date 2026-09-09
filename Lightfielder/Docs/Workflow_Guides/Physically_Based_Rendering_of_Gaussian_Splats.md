# PBR-GS

Physically Based Rendering of Gaussian Splats

## PBR GS PLY File Format Spec V1

Prepared 2025-07-29  
Last Updated 2026-08-01  
Written By: [Andrew Hazelden](mailto:andrew@andrewhazelden.com)  
Developed in collaboration with [Eric Paré](mailto:eric@xangle.team) and [Didier Muanza](mailto:didier.muanza@gmail.com)  

### Overview

The Kartaverse development team has explored various workflows available to extend the existing 3DGS PLY container format. The primary goal is to add PBR shading attributes to support interactive relighting while preserving backwards compatibility with existing 3D Gaussian Splatting training / rendering workflows and tools.

The most promising idea comes from Ben Houston's paper "[PBR extensions to Wavefront OBJ/MTL](https://benhouston3d.com/blog/extended-wavefront-obj-mtl-for-pbr)". We reached out to talk with Ben on 2025-07-29 and got his approval for this PBR GS concept to be scaffolded on-top of his core concepts and naming conventions. Thanks!

### Further Reading Materials

The Library of Congress has a document about the [Wavefront MTL file format](https://www.loc.gov/preservation/digital/formats/fdd/fdd000508.shtml). Check out Wikipedia for insights into the core specifications of the [ply file format](https://en.wikipedia.org/wiki/PLY_(file_format)). Also look at the PDF version of Greg Turk's [The PLY Polygon File Format](https://gamma.cs.unc.edu/POWERPLANT/papers/ply.pdf) document.

### Timecode Addition

To allow sidecar files like audio tracks to sync up with 4DGS sequences, it is useful to add an SMPTE formatted timecode ("00:00:00:00") attribute to the PLY file. One could also include a frame number element if it is useful.

```
property char timecode[11]
```

### Motion Blur Addition

We can render 4DGS sequences with accurate 3D motion blur with the addition of a per-point sample "velocity vector" property to the PLY file.

```
property float vx
property float vy
property float vz
```

Realistic motion blur is computed based on the point-sample's movement between the current and previous PLY frame in the sequence. The correct level of blur to apply to a point is determined using the velocity vector combined with the time step value (sourced from the timecode property).

The "vx/vy/vz" PLY channels hold the velocity data. When imported into a DCC package or renderer, the 3D vector information is typcially converted into a `Vec3f` array of 32-bit floating-point numbers. VFX industry file formats like Alembic treat this array as a `V3fArrayProperty`.

### Temporal Consistency Point ID Addition

Adding a unique pointIds property to each point sample in a .ply file provides the functionality of a classic "per-particle ID" capability to 3D gaussian splat video workflows. When generating a new 3DGS/4DGS file sequence, the individual pointIds values are tracked and matched over time. This optimization results in smooth and reliable motion consistency, as well as efficient data storage through point sample de-duplication. At the per-frame level, a .ply file sequence can vary the amount of point-samples present but at a global sequence level the pointIds are linked temporally.

This new property gives us a way to track an individual point-sample's "particle lifespan" over a longer 4DGS clip:

```
property float pointIds
```

This approach avoids common pitfalls in simplistic 3DGS-based file sequences where constant per-splat flickering and other artifacts would appear due to a lack of temporal coherence in the dataset.

The biggest advantage of temporally stable 3DGS/4DGS sequences is that you can make better use of computed optical-flow based motion vector velocity data. Since the individual pointIds properties are merged for common point samples across the sequence, each of your motion blur samples becomes temporally consistent. You can even render motion details like circular motion blur on radially moving objects, because you can walk forwards and backwards by several frames at a time when computing cross-frame motion trajectories. 

This enables more advanced workflows, such as optical flow-retiming of volumetric captures to support high-speed or slow-motion (bullet-time like) interpolated effects, where the motion blur length and motion characteristics maintain their natural cinematic look. The end result is the visually realistic retiming of splats without the traditional abrupt "stepping" or notched look that comes from naïve .ply file sequences being frame‑held.

Through the use of retiming with synthetic motion sub‑steps and "3D motion vector concatenation" approaches, we are able to match various delivery requirements for framerates such as 120, 90, 60, 48, 30, or 24 FPS, without introducing unnatural judder or picket‑fence motion artifacts in the final output. The motion vector data allows the simulation of real-world shutter angles for 4DGS rendered content such as a 180-degree shutter angle which is common with a standard film camera, or a 360-degree angle shutter angle which represents a full frame of blur.

In many ways, this [provides the 4D volumetric scanning equivalent](https://medium.com/@andrewhazelden/applying-magi-high-frame-rate-capture-ideas-to-4d-volumetric-scanning-48c87e61f7d7) of Douglas Trumbull's earlier HFR (High-Frame Rate) [MAGI 120 FPS stereo 3D process](https://www.youtube.com/watch?v=-Am2CbRLOPI) that was used in the pioneering [UFOTOG project](https://www.youtube.com/watch?v=wd6_oz7KBWk).

### PBR Additions

If we add the following PBR pass channels to the PLY file specification we can support fully interactive volumetric relighting of 3DGS assets and scenes:

```
aniso = Anisotropy
anisor = Anisotropy rotation
Ke = Emissive
Pc = Clearcoat thickness
Pcr = Clearcoat roughness
Pm = Metallic
Pr = Roughness
Ps = Sheen
```

It would be feasible to also store the ambient occlusion data that is used in a directX style "rmo" attribute as well.

The standard "f_dc" PLY channels hold the RGB image data on each point-sample:

```
f_dc_0 = red color
f_dc_1 = green color
f_dc_2 = blue color
```

The standard "nx/ny/nz" PLY channels hold the "norm" Normal map (RGB components) on each point sample:

```
nx = norm map red channel
ny = norm map green channel
nz = norm map blue channel
```

### PBR PLY Properties

When these PBR extension for 3DGS ideas are applied, it results in a PBR compatible 3DGS PLY file with the following header properties:

```
ply
format binary_little_endian 1.0
property char timecode[11]
element vertex 3000000
property float pointIds
property float x
property float y
property float z
property float nx
property float ny
property float nz
property float vx
property float vy
property float vz
property float aniso
property float anisor
property float ke
property float pc
property float pcr
property float pm
property float pr
property float ps
property float f_dc_0
property float f_dc_1
property float f_dc_2
property float f_rest_0
property float f_rest_1
property float f_rest_2
property float f_rest_3
property float f_rest_4
property float f_rest_5
property float f_rest_6
property float f_rest_7
property float f_rest_8
property float f_rest_9
property float f_rest_10
property float f_rest_11
property float f_rest_12
property float f_rest_13
property float f_rest_14
property float f_rest_15
property float f_rest_16
property float f_rest_17
property float f_rest_18
property float f_rest_19
property float f_rest_20
property float f_rest_21
property float f_rest_22
property float f_rest_23
property float f_rest_24
property float f_rest_25
property float f_rest_26
property float f_rest_27
property float f_rest_28
property float f_rest_29
property float f_rest_30
property float f_rest_31
property float f_rest_32
property float f_rest_33
property float f_rest_34
property float f_rest_35
property float f_rest_36
property float f_rest_37
property float f_rest_38
property float f_rest_39
property float f_rest_40
property float f_rest_41
property float f_rest_42
property float f_rest_43
property float f_rest_44
property float opacity
property float scale_0
property float scale_1
property float scale_2
property float rot_0
property float rot_1
property float rot_2
property float rot_3
end_header
```
