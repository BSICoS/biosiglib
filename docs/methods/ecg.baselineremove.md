---
spec_id: ecg.baselineremove
title: ECG baseline removal from fiducial isoelectric samples
---

# ECG baseline removal from fiducial isoelectric samples

## What it does

This method estimates slow ECG baseline drift from supplied fiducial positions expected to represent the local isoelectric level. It subtracts a smooth interpolation of those levels and also returns the estimated baseline.

## When to use it

Use it when suitable isoelectric fiducials are already available and low-frequency baseline motion is obscuring ECG morphology or amplitude measurements. It is not a fiducial detector and does not verify that the supplied positions are physiologically appropriate.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Each fiducial is shifted by `offset`, normalized to the sample grid, and represented by the mean ECG level in a short local window. Two or more valid levels define a smooth baseline over the complete signal: linear with two levels, quadratic with three, and not-a-knot cubic with four or more.

The offset, averaging window, and boundary behavior are empirical algorithm choices rather than constants established by the original spline-baseline literature.

## Interpretation and limitations

Poorly placed fiducials can remove genuine ECG morphology or create misleading extrapolation near the signal boundaries. Fiducials should cover the analyzed segment and should be reviewed in the context of the downstream measurement.

<!-- BIOSIGLIB METHOD RESOURCES -->
