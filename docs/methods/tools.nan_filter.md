---
spec_id: tools.nan_filter
title: NaN-aware causal filtering
---

# NaN-aware causal filtering

## What it does

This utility applies an ordinary causal digital filter while interpolating short internal NaN gaps and preserving long missing spans.

## When to use it

Use it when filtering must remain causal and short missing gaps may be bridged without joining independent signal segments across longer gaps.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Short internal gaps are interpolated before filtering. Long gaps split the signal into independent finite segments, and missing boundary samples remain missing.

## Interpretation and limitations

Interpolated samples are estimates. `max_gap` should reflect the sampling frequency and the longest absence that can reasonably be bridged for the intended analysis.

<!-- BIOSIGLIB METHOD RESOURCES -->
