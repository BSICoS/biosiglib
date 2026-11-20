---
spec_id: resp.tidalvolume
title: Estimate respiratory amplitude per cycle
---

# Estimate respiratory amplitude per cycle

## What it does

Estimates the peak-to-valley amplitude of each complete respiratory cycle and returns an interpolated amplitude trajectory alongside the upper and lower envelopes.

## When to use it

Use a uniformly sampled respiration signal with slow baseline drift already removed. Amplitudes retain the units of the input. A recording in arbitrary units can track changes in breathing depth; volume in litres requires an appropriate volume calibration.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Following linear detrending, zero crossings delimit the search for peaks and valleys. Set `mindist` in seconds to suppress closely spaced crossings. Each peak pairs with the next valley in the same observed segment. Their amplitude difference is placed halfway between the two extrema in time. Each output is interpolated from its own points using PCHIP.

## Interpretation and limitations

Missing samples interrupt respiratory-cycle detection. Set `max_gap` to limit interpolation across time without valid points. With a limit of 15 s, two consecutive cycle midpoints 14 s apart can support interpolation, while midpoints exactly 15 s apart belong to different groups. The envelopes can have different support because peaks and valleys occur at different times.

<!-- BIOSIGLIB METHOD RESOURCES -->
