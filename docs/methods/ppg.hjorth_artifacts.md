---
spec_id: ppg.hjorth_artifacts
title: Detect artifacts using Hjorth descriptors
---

# Detect artifacts using Hjorth descriptors

## What it does

Marks sample intervals whose windowed power, mobility or frequency spread differs from adaptive median baselines. Windows containing missing samples are also excluded.

## When to use it

Use it on a preprocessed physiological signal when deviations in local power or waveform variation identify unsuitable segments. Margins depend on signal scaling and must match the intended analysis.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The signal is centered globally and analyzed in complete windows. Each descriptor is compared with a truncated, NaN-omitting median baseline plus or minus its absolute margins. The lower activity threshold is floored to 0.0001 when nonpositive. Detected windows become sample intervals, and overlap or contiguity is always merged. A positive separation also joins uncovered gaps strictly shorter than that duration.

## Interpretation and limitations

A zero mask value means no artifact was marked there; it does not certify signal quality, particularly in an unexamined tail or between spaced windows. The default separation is zero seconds. Interval endpoints identify included samples, and the first sample is at time zero. Negative mode inverts the threshold decision, but windows containing NaN remain excluded. Plotting, if offered by an implementation, does not alter detections.

<!-- BIOSIGLIB METHOD RESOURCES -->
