---
spec_id: hrv.removefp
title: False-positive event removal
---

# False-positive event removal

## What it does

This method removes event detections that follow abnormally short event-to-event intervals.

## When to use it

Use it before gap filling or interval-based variability analysis when an event detector may have inserted extra beats or pulses. It is intended for strictly ordered event times.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Each interval is compared with a local median-based baseline. A detection after a sufficiently short interval is removed, and the surrounding interval structure is reevaluated deterministically.

## Interpretation and limitations

The threshold is an empirical preprocessing rule, not a clinical classifier. Genuine short intervals may be removed when the local rhythm changes abruptly or contains arrhythmia.

<!-- BIOSIGLIB METHOD RESOURCES -->
