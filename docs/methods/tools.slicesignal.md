---
spec_id: tools.slicesignal
title: Slice a signal into windows
---

# Slice a signal into windows

## What it does

Extracts fixed-length windows from a sampled signal, with overlap specified in samples.

## When to use it

Use it to prepare windows for spectral analysis or other operations that process successive parts of a signal independently.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The first window begins at the first sample. Later windows advance by the window length minus the overlap. By default only complete windows are returned. Enable the last-window option to include an uncovered tail with right-side NaN padding, or to pad a nonempty signal shorter than one window.

## Interpretation and limitations

MATLAB stores windows as columns and Python stores them as rows. The sample contents and window order are the same. If you provide the sampling frequency, you can obtain the time centers. These refer to the nominal window grid, including any padding, and use the first input sample as time zero. Existing missing samples are preserved.

<!-- BIOSIGLIB METHOD RESOURCES -->
