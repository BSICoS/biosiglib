---
spec_id: tools.interpgap
title: Interpolate short NaN gaps
---

# Interpolate short NaN gaps

## What it does

This utility estimates missing samples in short internal gaps while preserving signal length and sample alignment.

## When to use it

Use it to reconstruct limited losses of samples before further analysis, independently of filtering or spectral estimation. The maximum gap is measured in missing samples on a regular sampling grid.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Long gaps separate independent segments. Within each segment, interpolation uses the original finite samples and their positions. Linear interpolation joins neighboring values; nearest interpolation selects a measured value. PCHIP preserves local shape, while the spline provides a smooth cubic interpolation through the available support.

## Interpretation and limitations

Reconstructed values are estimates. Choose the maximum gap and method for the signal and intended analysis. Cubic interpolation needs neighboring measurements to establish shape; with only two available values it reduces to a straight line. Boundary gaps remain missing because the method does not extrapolate. Spline interpolation may overshoot between measured values.

<!-- BIOSIGLIB METHOD RESOURCES -->
