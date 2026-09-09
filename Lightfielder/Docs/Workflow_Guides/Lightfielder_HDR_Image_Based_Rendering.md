# Lightfielder HDR Image Based Rendering

Prepared by: Andrew Hazelden <andrew@andrewhazelden.com>  
Date Created: 2026-05-19

## HDR Overview

This document describes the current options that exist for HDR (High Dynamic Range) compatible volumetric reconstruction tools. Most Gaussian Splatting implementations used today are based around the use of LDR (Low Dynamic Range) 8-bit per channel source imagery, or Tonemapped imagery that is fit within a 0-1 floating point color range.

Tools like [Jawset Postshot](https://www.jawset.com/) list in their documentation that they can import HDR imagery. If you save the output from Postshot to a standard .ply container format the values will be limited. Most implementations of gaussian splatting store color and spherical harmonic (SH) coefficients as 32-bit floats (float32), but they are optimized for the typical range of LDR 0-1 floating point color range values.

## Modern HDR Options

- [PhysHDR-GS](https://github.com/ZeldaM1/PhysHDR-GS) 2026
- [InstantHDR](https://arxiv.org/pdf/2603.11298) 2026
- [LCD-GS](https://arxiv.org/html/2511.12895v2) 2026
- [GaussHDR](https://github.com/LiuJF1226/GaussHDR) 2025
- [HDR-GS](https://arxiv.org/abs/2405.15125) 2024

## Legacy HDR Options

The earlier NeRF and Plenoxels rendering pipelines had HDR options:

- [HDR-Plenoxels](https://github.com/kaist-ami/HDR-Plenoxels) 2022
- [HDR-NeRF](https://github.com/xhuangcv/hdr-nerf) 2022
  - HDR-NeRF was built ontop of [NeRF-PyTorch](https://github.com/yenchenlin/nerf-pytorch/)
