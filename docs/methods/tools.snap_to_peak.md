---
spec_id: tools.snap_to_peak
title: Detection refinement to local ECG peaks
---

# Detection refinement to local ECG peaks

## What it does

This utility moves each candidate detection to the maximum ECG sample inside a local search window.

## When to use it

Use it to refine approximate ECG detections after a detector has identified the correct neighborhood but not the exact local peak sample.

<!-- BIOSIGLIB METHOD INTERFACE -->

## Interpretation and limitations

The method assumes the desired fiducial is the local maximum. Wide windows can jump to a neighboring wave, while narrow windows may not reach the intended peak. Missing samples inside the search region are ignored according to the defined NaN behavior.

<!-- BIOSIGLIB METHOD RESOURCES -->
