---
spec_id: tools.trimnans
title: Trim boundary NaN samples
---

# Trim boundary NaN samples

## What it does

This utility removes missing samples at the beginning and end of a signal while preserving missing samples inside the retained span.

## When to use it

Use it to remove boundary padding before processing a signal whose internal gaps must remain explicit.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The method locates the first and last finite samples and copies the inclusive span between them. It performs no interpolation and changes no retained amplitudes.

## Interpretation and limitations

Trimming changes the signal length and discards its original starting offset. Preserve the corresponding time origin separately when aligning the result with other recordings.

<!-- BIOSIGLIB METHOD RESOURCES -->
