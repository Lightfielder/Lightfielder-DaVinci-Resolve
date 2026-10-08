---
title: "Compiling the Rust App"
sidebar_label: "Compiling (Rust)"
sidebar_position: 9
description: "Build the cross-platform Rust Viewport app with Cargo."
---

# Lightfielder Viewport | Compiling the Russ App

## macOS

```bash
# Install Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

```bash
# Build from source
cd $HOME/Documents/Git/LightfielderVulkanViewport/Viewport
cargo build
cargo run
```

## Ubuntu Linux 

```bash
# Install Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

```bash
# Add libraries
sudo apt install libxkbcommon-dev libxkbcommon-x11-dev
```

```bash
# Build from source
cd /opt/Lightfielder/Viewport/Sources/
cargo build
cargo run
```
