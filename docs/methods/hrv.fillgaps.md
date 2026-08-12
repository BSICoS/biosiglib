---
spec_id: hrv.fillgaps
title: Missing-event gap filling
---

# Missing-event gap filling

## What it does

This method reconstructs plausible event timestamps inside abnormally long intervals before interval-based HRV or pulse-rate variability analysis.

## When to use it

Use it after false-positive detections have been removed and when missed beats or pulses have merged several physiological intervals into one long observed interval.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Locally long intervals are detected against a median-based adaptive baseline. The method tries increasing insertion counts and uses shape-preserving interpolation from surrounding valid intervals. Reconstructions must remain inside local acceptance bounds and preserve the duration between observed events.

## Interpretation and limitations

Inserted timestamps are deterministic estimates, not observed events. Abrupt rhythm changes, insufficient context, or long missing spans may remain unresolved; those spans stay explicit in the interval output.

<!-- BIOSIGLIB METHOD RESOURCES -->
