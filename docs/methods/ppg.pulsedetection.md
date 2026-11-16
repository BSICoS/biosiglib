---
spec_id: ppg.pulsedetection
title: Detect pulse maximum upslopes
---

# Detect pulse maximum upslopes

## What it does

Detects maximum upslopes in an already filtered PPG derivative and returns their quadratically refined times in seconds, together with the adaptive threshold.

## When to use it

Use it after baseline removal and low-pass differentiation when maximum-upslopes are the desired pulse fiducials. Preprocessing and any filter-delay compensation belong to the caller.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The initial threshold uses nonnegative samples in the first ten seconds of available signal and an initial rate estimate of 80 beats/minute. A complete excursion above and back below the threshold supplies a local maximum. Detected amplitudes and pulse intervals update the refractory hold and subsequent linear decay. After sufficient history, median estimates reduce the influence of unusually large pulses.

State continues through the entire input. Internal search blocks do not restart adaptation. The exact initialization window endpoints, rounding, history lengths and threshold updates are defined in the specification.

## Interpretation and limitations

Times start at zero for the first input sample. The detector is based on the adaptive method of Lázaro et al.; this variant defines its own initialization and amplitude adaptation and measures the decay after the refractory period.

Missing samples cannot satisfy threshold crossings. They do not automatically split crossing regions or clear history, and intervals can span a missing stretch. Refinement uses the original neighboring samples and drops undefined times.

The optional `reset_after` feature restarts adaptation after a chosen duration without a raw detection, including missing time. This can help when a device changes gain and its signal returns at a lower amplitude. It is disabled by default; the appropriate duration depends on the application. A restart keeps previous detections and discards the earlier adaptive history.

<!-- BIOSIGLIB METHOD RESOURCES -->
