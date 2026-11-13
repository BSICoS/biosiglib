---
spec_id: tools.hjorth
title: Compute Hjorth descriptors
---

# Compute Hjorth descriptors

## What it does

Summarizes a sampled signal by its mean-square power, mobility, and frequency spread estimated from consecutive differences.

## When to use it

Use it to compare signal windows, for example when looking for changes in power or waveform variation. Remove the baseline before calling the method if its power should not contribute to the descriptors.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The activity is the mean of the squared samples. Mobility and complexity use ratios of the sums of squares of the signal and its first and second differences. The sampling frequency scales both difference-based descriptors. The method does not center the signal or pad the differences.

## Interpretation and limitations

Activity includes any residual mean in the window. Mobility and complexity use a frequency scale in Hz, but the finite differences only approximate time derivatives. Complexity uses the absolute difference of the two ratios and is not an exact spectral bandwidth or a dimensionless mobility ratio. A window containing any NaN has undefined descriptors. Short or constant windows may have undefined mobility or complexity even when activity is available.

<!-- BIOSIGLIB METHOD RESOURCES -->
