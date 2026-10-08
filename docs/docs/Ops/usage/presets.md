---
title: "Export Presets"
sidebar_label: "Export Presets"
sidebar_position: 3
description: "Content, HDRI, calibration, and post-calibration media encoding presets."
---

# Lightfielder Operators | Presets

Ops media encoding workflows use pre-defined presets to specify the file naming and encoding settings for content, calibration, post-calibration, and HDRI exports.

## "Content" Export Preset

- Format: [EXR RGB 16-bit]
- Custom name: ```%{Source Name}_%{Render Resolution}_Linear_R2020_%{Shot Frame Rate}.```
- File subfolder: ```ID_%{Shot}_LinearR2020```
- Alternative File subfolder: ```ID_%{Shot}_PQRr2020```
- [x] Render As Clips
- [x] Clips start at frame 1

## "HDRI" Export Preset

- Format: [EXR RGB 32-bit]
- Custom name: ```%{Source Name}_%{Render Resolution}_Linear_R2020_%{Shot Frame Rate}.```
- File subfolder: ```ID_%{Shot}_LinearR2020```
- Alternative File subfolder: ```ID_%{Shot}_PQRr2020```
- [x] Render As Clips
- [x] Clips start at frame 1


## "Calibration" Export Preset:

- Format: [JPEG Best]
- Custom name: ```%{Shot}_%{Clip #}_%{Camera Position}_%{Angle}.```
- File subfolder: ```%{Angle}```
- [x] Render As Clips
- [x] Clips start at frame 1

## "Post-Calibration" Export Preset

- Format: [JPEG Best]
- Filename uses (x) Custom name
- Custom name: ```%{Shot}_%{Clip #}_%{Camera Position}_%{Angle}.```
- File subfolder: ```%{Angle}```
- [x] Render As Clips
- [x] Clips start at frame 1

