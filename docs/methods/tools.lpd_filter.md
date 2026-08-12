---
spec_id: tools.lpd_filter
title: Low-pass differentiating FIR filter design
---

# Low-pass differentiating FIR filter design

## What it does

This utility designs a linear-phase FIR filter that differentiates low-frequency signal content while attenuating higher frequencies.

## When to use it

Use it when a processing chain requires a reproducible low-pass differentiator with an explicit constant delay.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The requested sampling, pass, and stop frequencies define an even-order antisymmetric FIR response. The returned delay can be used to align the filtered signal with the original samples.

## Interpretation and limitations

The coefficients are tied to the requested sampling frequency and should be redesigned when it changes. The delay must be handled explicitly in causal processing chains.

<!-- BIOSIGLIB METHOD RESOURCES -->
