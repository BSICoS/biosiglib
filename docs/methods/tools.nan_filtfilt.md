---
spec_id: tools.nan_filtfilt
title: NaN-aware zero-phase filtering
---

# NaN-aware zero-phase filtering

## What it does

This utility applies forward-backward zero-phase filtering while interpolating short internal NaN gaps and preserving long missing spans.

## When to use it

Use it for offline processing when phase preservation matters and short missing gaps may be bridged. It is not suitable for real-time causal processing.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Short internal gaps are interpolated before filtering. Long gaps split the signal into independent finite segments. Each sufficiently long segment is filtered forward and backward without using samples across a missing span.

## Interpretation and limitations

Short segments may be impossible to filter with the requested coefficients. Interpolation and forward-backward edge handling can affect samples near gaps and segment boundaries.

<!-- BIOSIGLIB METHOD RESOURCES -->
