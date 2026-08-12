---
spec_id: tools.medfilt_threshold
title: Median-filter adaptive threshold
---

# Median-filter adaptive threshold

## What it does

This utility produces a sample-aligned adaptive threshold from a one-dimensional signal using a local median baseline, a multiplier, and an upper cap.

## When to use it

Use it when a detector needs a robust local threshold that follows slow baseline changes without being dominated by isolated large samples.

<!-- BIOSIGLIB METHOD INTERFACE -->

## Interpretation and limitations

The result depends on window length and boundary handling. The factor and cap are algorithm settings rather than universal physiological thresholds.

<!-- BIOSIGLIB METHOD RESOURCES -->
