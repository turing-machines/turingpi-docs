---
title: "Intro & Specs"
description: "This series of articles will guide you through the process of preparing the Nvidia Jetson modules to work on the Turing Pi 2 board. These instructions are…"
head:
  - tag: title
    content: "Intro and Specs | Nvidia Jetson Orin / Nano NX | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## Introduction

This series of articles will guide you through the process of preparing the Nvidia Jetson modules to work on the Turing Pi 2 board. These instructions are based on the Nvidia documentation for the modules. The whole installation process might not be quick but should be pretty straightforward. In the future, we hope to make it much easier. The article series will be updated with the Nvidia Jetson Nano (the original one) soon.

## Specs

### Jetson Orin NX 16GB

| Specification     | Value                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------- |
| AI Performance    | 100 TOPS                                                                               |
| GPU               | 1024-core NVIDIA Ampere architecture GPU with 32 Tensor Cores                          |
| GPU Max Frequency | 930 MHz                                                                                |
| CPU               | 8-core NVIDIA Arm® Cortex A78AE v8.2 64-bit CPU  2MB L2 + 4MB L3                       |
| CPU Max Frequency | 2.2 GHz                                                                                |
| DL Accelerator    | 1x NVDLA v2.0                                                                          |
| DL Max Frequency  | 1.4 Ghz                                                                                |
| Memory            | 16GB 128-bit LPDDR5 102.4GB/s                                                          |
| Storage           | 16GB eMMC 5.1                                                                          |
| Video Encode      | 1x 4K60 (H.265) 3x 4K30 (H.265) 7x 1080p60 (H.265) 15x 1080p30 (H.265)                 |
| Video Decode      | 1x 8K30 (H.265) 3x 4K60 (H.265) 7x 4K30 (H.265 11x 1080p60 (H.265) 23x 1080p30 (H.265) |

### Jetson Orin NX 8GB

| Specification     | Value                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------- |
| AI Performance    | 70 TOPS                                                                                |
| GPU               | 512-core NVIDIA Ampere architecture GPU with 16 Tensor Cores                           |
| GPU Max Frequency | 765 MHz                                                                                |
| CPU               | 6-core NVIDIA Arm® Cortex A78AE v8.2 64-bit CPU  1.5MB L2 + 4MB L3                     |
| CPU Max Frequency | 2.0 GHz                                                                                |
| DL Accelerator    | 1x NVDLA v2.0                                                                          |
| DL Max Frequency  | 1.2 Ghz                                                                                |
| Memory            | 8GB 128-bit LPDDR5 102.4GB/s                                                           |
| Storage           | 16GB eMMC 5.1                                                                          |
| Video Encode      | 1x 4K60 (H.265) 3x 4K30 (H.265) 6x 1080p60 (H.265) 12x 1080p30 (H.265)                 |
| Video Decode      | 1x 8K30 (H.265) 2x 4K60 (H.265) 4x 4K30 (H.265) 9x 1080p60 (H.265) 18x 1080p30 (H.265) |

### Jetson Orin Nano 8GB

| Specification     | Value                                                        |
| ----------------- | ------------------------------------------------------------ |
| AI Performance    | 40 TOPs                                                      |
| GPU               | 512-core NVIDIA Ampere architecture GPU with 16 Tensor Cores |
| GPU Max Frequency | 765 MHz                                                      |
| CPU               | 6-core Arm® Cortex®-A78AE v8.2 64-bit CPU 1.5MB L2 + 4MB L3  |
| CPU Max Frequency | 1.5 GHz                                                      |
| Memory            | 8GB 128-bit LPDDR5 68 GB/s                                   |
| Storage           | 16GB eMMC 5.1                                                |
| Video Encode      | 1080p30 supported by 1-2 CPU cores                           |
| Video Decode      | 1x 4K60 (H.265) 2x                                           |

### Jetson Orin Nano 4GB

| Specification     | Value                                                                                |
| ----------------- | ------------------------------------------------------------------------------------ |
| AI Performance    | 20 TOPs                                                                              |
| GPU               | 256-core NVIDIA Pascal™ architecture GPU                                             |
| GPU Max Frequency | 1.12GHz                                                                              |
| CPU               | Dual-Core NVIDIA Denver 2 64-Bit CPU and Quad-Core Arm® Cortex®-A57 MPCore processor |
| CPU Max Frequency | Denver2: 1.95 GHz Cortex-A57: 1.92 GHz                                               |
| DL Accelerator    | —                                                                                    |
| DL Max Frequency  | —                                                                                    |
| Memory            | 4GB 64-bit LPDDR4  34 GB/s                                                           |
| Storage           | 16GB eMMC 5.1                                                                        |
| Video Encode      | 1x 4K30 (H.265) 2x 1080p60 (H.265)                                                   |
| Video Decode      | 1x 4K60 (H.265) 2x 4K30 (H.265) 4x 1080p60 (H.265) 8x 1080p30 (H.265)                |
