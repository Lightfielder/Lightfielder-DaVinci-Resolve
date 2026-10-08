---
title: "Unit Tests"
sidebar_label: "Unit Tests"
sidebar_position: 4
description: "Validate Ops scripts with synthetic camera array data and symlinked media."
---

# Lightfielder Operators | Unit Tests

A collection of new "unit tests" are being developed for the Ops repo. They allow the Ops script functionality to be validate with synthetic camera array data. This avoids the need to interact with client NDA covered media assets when developing and debugging the core scripts.

These assets are located in the GitHub repo at:  
`Ops/Extras/Unit Tests/`

## What is a Symlink?

A [Symlink](https://en.wikipedia.org/wiki/Symbolic_link) (which is also known as a "Symbolic Link") is a UNIX centric idea of a shortcut like file reference that points to the original file. This approach allows you to have synthetic R3D file names generated for each camera view, without the disk burden of storing hundreds of GBs of data. A Symlink is usually only a few KBs in size.

You can manually delete a symlink file if you would like to remove it. The original file will remain on disk.
