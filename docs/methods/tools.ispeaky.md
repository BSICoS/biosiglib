---
spec_id: tools.ispeaky
title: Classify spectral peakedness
---

# Classify spectral peakedness

## What it does

Returns whether both PKL and AKL meet their respective thresholds, including equality.

## When to use it

Use it after `peakedness` to select spectra with sufficient band concentration and relative peak height. Choose thresholds for the analysis rather than treating them as universal quality criteria.

<!-- BIOSIGLIB METHOD INTERFACE -->

## Interpretation and limitations

Both thresholds are required percentages between zero and 100. Inputs must have identical shapes; classification preserves that shape. A NaN measure produces false only at that position. With an automatic reference, AKL from a nonzero spectrum is 100, so PKL provides the discrimination.

<!-- BIOSIGLIB METHOD RESOURCES -->
