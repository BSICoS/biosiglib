---
spec_id: ecg.sloperange
title: Slope-range ECG-derived respiration
---

# Slope-range ECG-derived respiration

## What it does

Slope-range ECG-derived respiration estimates a beat-to-beat respiratory modulation signal from derivative ECG morphology around detected R waves.

## When to use it

Use it when a respiratory signal is unavailable but reliable R-wave timing and a derivative ECG are available. It provides a relative respiration surrogate, not a measurement in physical respiratory units.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

For each R wave, the method compares the strongest local upslope with the strongest local downslope. Their difference forms the EDR amplitude. Signal-aligned slope traces and selected extrema positions are returned for visual inspection.

## Interpretation and limitations

Interpret trends rather than absolute amplitudes. Incorrect R-wave detections, unstable QRS morphology, noise, or incomplete boundary windows can make the surrogate unreliable.

<!-- BIOSIGLIB METHOD RESOURCES -->
