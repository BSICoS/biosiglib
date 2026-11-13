---
spec_id: tools.nanpwelch
title: Estimate PSD across NaN gaps
---

# Estimate PSD across NaN gaps

## What it does

Computes a one-sided power spectral density from complete analysis windows without crossing preserved gaps. Each window contributes equally to the final average.

## When to use it

Use it when a regularly sampled signal contains missing spans and you want a spectrum based on valid stretches, optionally reconstructing short gaps first.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Boundary NaNs are trimmed. Eligible internal gaps may be linearly interpolated; all remaining gaps separate independent stretches. The window grid restarts in each stretch. Only complete windows contribute to the mean PSD. A scalar window chooses rectangular weights; a vector supplies the actual weights. No detrending is performed, so a constant signal retains its DC power.

## Interpretation and limitations

PSD units are squared signal amplitude per Hz. Longer stretches contribute more if they provide more complete windows. Per-window spectra expose those contributions. Matrices keep channels in columns, including NaN PSD columns when a channel has no estimate. An FFT shorter than the window folds weighted samples modulo the FFT length rather than truncating them. Interpolation changes the analyzed signal and should be chosen for the intended analysis.

<!-- BIOSIGLIB METHOD RESOURCES -->
