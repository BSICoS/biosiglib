---
spec_id: ecg.pantompkins
title: Pan-Tompkins-style ECG R-wave detection
---

# Pan-Tompkins-style ECG R-wave detection

## What it does

This detector locates ordered R-wave occurrence times in a sampled ECG signal. It can also return the filtered ECG, squared derivative, and integrated envelope used to inspect detections.

## When to use it

Use it for conventional QRS-oriented R-wave detection when the ECG sampling frequency is known. The intermediate signals are useful for checking why a beat was accepted or missed.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Finite ECG segments pass through band-pass filtering, derivative filtering, squaring, moving-window integration, peak detection, and local peak refinement. NaN samples separate independent finite segments so filtering and detection never cross a missing-data gap.

## Interpretation and limitations

The detector follows the Pan-Tompkins processing approach but is not an exact reproduction of the original real-time algorithm. Noise, atypical QRS morphology, poor parameter choices, or records shorter than the required processing context can reduce detection reliability.

<!-- BIOSIGLIB METHOD RESOURCES -->
