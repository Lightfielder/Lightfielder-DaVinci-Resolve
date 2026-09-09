# Lightfielder | Resolve Deliver Page Presets

Lightfielder media encoding workflows use pre-defined presets to specify the file naming and encoding settings for content, calibration, post-calibration, and HDRI exports.

## "Content" Export Preset

- Absolute Filepath Example: ```/Volumes/2026-08-04_Shoot_LF2200/03-footage/renders/content/ID_01336_LinearR2020/A220_B001_1030BH_001_6144x3240_Linear_R2020_29.970.000001.exr```
- Location: ```/Volumes/2026-08-04_Shoot_LF2200/03-footage/renders/content/```
- Render (x) Individual Clips

### Video Tab:

- [x] Export Video
- Format [EXR]
- Codec [RGB half]
- [x] Render at source resolution
- [x] Force sizing to highest quality
- [x] Force debayer to highest quality

### File Tab:

- Filename uses (x) Custom name
- Custom name: ```%{Source Name}_%{Render Resolution}_Linear_R2020_%{Shot Frame Rate}.```
- File subfolder: ```ID_%{Shot}_LinearR2020```
- Alternative File subfolder: ```ID_%{Shot}_PQRr2020```
- [x] Add source frame count to filename
- use [6] digits in the filename
- [x] Each clip starts at frame 1

## "HDRI" Export Preset

- Absolute Filepath Example:  
```/Volumes/2026-08-04_Shoot_LF2200/03-footage/renders/hdri/ID_01336_LinearR2020/A220_B001_1030BH_001_6144x3240_Linear_R2020_29.970.000001.exr```
- Location: ```/Volumes/2026-08-04_Shoot_LF2200/03-footage/renders/hdri/```
- Render (x) Individual Clips

### Video Tab:

- [x] Export Video
- Format [EXR]
- Codec [RGB half]
- [x] Render at source resolution
- [x] Force sizing to highest quality
- [x] Force debayer to highest quality

### File Tab:

- Filename uses (x) Custom name
- Custom name: ```%{Source Name}_%{Render Resolution}_Linear_R2020_%{Shot Frame Rate}.```
- [x] Add source frame count to filename
- File subfolder: ```ID_%{Shot}_LinearR2020```
- Alternative File subfolder: ```ID_%{Shot}_PQRr2020```
- use [6] digits in the filename
- [x] Each clip starts at frame 1


## "Calibration" Export Preset:

- Absolute Filepath Example: ```/Volumes/2026-08-04_Shoot_LF2200/03-footage/renders/calibration/01/1286_001_01_AA.000000.jpg```
- Location: ```/Volumes/2026-08-04_Shoot_LF2200/03-footage/renders/calibration/```
- Render (x) Individual Clips

### Video Tab:

- [x] Export Video
- Format [JPEG]
- [x] Render at source resolution
- Quality (x) Automatic [Best]
	- [x] Force sizing to highest quality
	- [x] Force debayer to highest quality

### File Tab:

- Filename uses (x) Custom name
- Custom name: ```%{Shot}_%{Clip #}_%{Camera Position}_%{Angle}.```
- File subfolder: ```%{Angle}```
- [x] Add source frame count to filename
- use [6] digits in the filename
- [x] Each clip starts at frame 1


## "Post-Calibration" Export Preset

- Absolute Filepath Example: ```/Volumes/2026-08-04_Shoot_LF2200/03-footage/renders/post-calibration/01/1286_001_01_AA.000000.jpg```
- Location: ```/Volumes/2026-08-04_Shoot_LF2200/03-footage/renders/post-calibration/```
- Render (x) Individual Clips

### Video Tab:

- [x] Export Video
- Format [JPEG]
- [x] Render at source resolution
- Quality (x) Automatic [Best]
	- [x] Force sizing to highest quality
	- [x] Force debayer to highest quality

### File Tab:

- Filename uses (x) Custom name
- Custom name: ```%{Shot}_%{Clip #}_%{Camera Position}_%{Angle}.```
- File subfolder: ```%{Angle}```
- [x] Add source frame count to filename
- use [6] digits in the filename
- [x] Each clip starts at frame 1

--------------------------------------------------
