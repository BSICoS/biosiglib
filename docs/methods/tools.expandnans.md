---
spec_id: tools.expandnans
title: Expand NaN gaps
---

# Expand NaN gaps

## What it does

This utility marks samples near missing spans as NaN without changing signal length or time alignment.

## When to use it

Use it when a missing or invalid span also makes nearby samples unsuitable for analysis, for example when excluding a temporal margin around an artifact.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The duration is converted to a symmetric sample radius. The method expands the original missing mask once, clips at the signal boundaries, and unites overlapping spans.

## Interpretation and limitations

The duration applies on each side, so an isolated missing sample can exclude samples both before and after it. This operation deliberately discards nearby measurements and does not estimate missing values. Choose the margin to match the source of invalid data and the intended analysis.

<!-- BIOSIGLIB METHOD RESOURCES -->
