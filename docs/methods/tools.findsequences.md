---
spec_id: tools.findsequences
title: Find repeated adjacent values
---

# Find repeated adjacent values

## What it does

Finds maximal spans containing at least two identical consecutive samples and returns each value, inclusive boundaries, and length.

## When to use it

Use it to locate repeated codes, constant signal spans, or consecutive missing samples. Isolated samples are omitted, so detecting every invalid span also requires handling isolated invalid samples.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Equality is exact, with consecutive NaNs treated as equal. Results retain the established category order: nonzero finite values, zero, NaN, positive infinity, and negative infinity. Runs within each category follow their position in the input.

## Interpretation and limitations

Positions use the implementation's native index origin: one in MATLAB and zero in Python. Both endpoints are included. Lengths count samples and do not depend on the index origin. Convert a Python row into a slice with `signal[start:end + 1]`.

Nearby floating-point values do not form a run unless exactly equal. Positive and negative infinity are accepted and remain separate categories. The output is grouped by category rather than globally sorted by occurrence.

<!-- BIOSIGLIB METHOD RESOURCES -->
