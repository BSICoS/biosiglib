---
spec_id: tools.localmax
title: Find the highest local maximum
---

# Find the highest local maximum

## What it does

Returns the value and position of the highest interior peak in a signal. For matrix input, it analyzes each row or column independently along the selected axis.

## When to use it

Use it to select one peak within a known search region, or one peak per window in a matrix. A high value at the edge of the region does not count as a local maximum.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Peaks must be bounded by strictly lower neighbors after ignoring NaNs. A flat peak is represented by its middle sample, choosing the earlier middle sample for even lengths. The highest candidate wins, and ties choose the first candidate.

## Interpretation and limitations

An omitted axis selects the first non-singleton axis. Use MATLAB dimension `2` or Python `axis=1` to search each row. Sample positions refer to the original input and start at 1 in MATLAB and 0 in Python. If no peak exists, both the value and position are NaN. The method returns one peak per signal and does not measure prominence or separation.

<!-- BIOSIGLIB METHOD RESOURCES -->
