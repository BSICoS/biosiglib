---
spec_id: hrv.tdmetrics
title: Time-domain HRV metrics
---

# Time-domain HRV metrics

## What it does

This method computes standard time-domain variability metrics from cleaned beat-to-beat or pulse-to-pulse intervals.

## When to use it

Use it after event detection and interval cleaning. The input may contain NaN markers for intervals that should be omitted, but valid intervals must be positive and expressed in seconds.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Mean rate and SDNN use all valid intervals. SDSD, RMSSD, and pNN50 use successive differences only when both adjacent intervals are valid. The sample standard-deviation convention is used where applicable.

## Interpretation and limitations

Results depend strongly on recording duration, preprocessing, missing data, activity, posture, and physiological context. Metrics from different protocols should not be compared without accounting for those factors.

<!-- BIOSIGLIB METHOD RESOURCES -->
