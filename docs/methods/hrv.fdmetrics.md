---
spec_id: hrv.fdmetrics
title: Frequency-domain HRV metrics
---

# Frequency-domain HRV metrics

## What it does

This method integrates conventional LF and HF powers or, alternatively, respiration-related and respiration-unrelated spectra obtained after orthogonal subspace projection.

## When to use it

Use conventional mode to summarize an HRV spectrum in standard frequency bands. Use respiration-separated mode only when the supplied spectra represent the related and residual components of a compatible OSP analysis.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Band samples are selected directly from the supplied frequency grid and integrated without interpolating new spectral points. The represented grid therefore determines the effective band coverage. Respiration-separated mode reports unrelated LF power, related power, and a bounded normalized index.

## Interpretation and limitations

LF and HF powers are descriptive and should not be treated as pure sympathetic or parasympathetic measures. Spectral estimation, detrending, record length, stationarity, artifacts, and respiratory conditions can dominate interpretation. Partial frequency coverage should be reported explicitly.

<!-- BIOSIGLIB METHOD RESOURCES -->
