---
spec_id: hrv.fillgaps
title: Missing-event gap filling
status: draft
---

# Missing-event gap filling

## Purpose

Missing-event gap filling reconstructs plausible event timestamps inside abnormally long intervals before interval-based HRV analysis. It operates on event times that have already undergone any desired false-positive removal.

## Scientific rationale

A missed beat or pulse detection merges several physiological intervals into one long observed interval. Nearby valid intervals provide local timing context from which a smooth sequence can be reconstructed, while exact duration rescaling preserves the original events on both sides of the gap.

## Method summary

The method detects locally long intervals with a median-filtered adaptive baseline. It tries progressively larger insertion counts across the whole series. For each gap it uses shape-preserving cubic interpolation from nearby valid intervals, accepts a reconstruction that falls below the local upper bound, and stops before an additional insertion would make all reconstructed intervals too short.

## Key assumptions

Input events are finite, correctly ordered, and already cleaned of false-positive detections. The surrounding valid intervals are assumed to represent the local rhythm well enough to guide interpolation. A gap needs interval support on both sides; the method does not extrapolate from only one side.

## Interpretation and limitations

Inserted timestamps are deterministic reconstructions, not observed physiological events. They can reduce the impact of missed detections on interval statistics, but they cannot recover true beat timing when local rhythm changes abruptly or when too much context is missing. Unresolved spans remain explicit as NaN intervals in the interval output. The threshold factors are empirical algorithm settings rather than clinical decision thresholds.

## References

The missing-data motivation and original empirical factors are described by Cajal et al., *Effects of Missing Data on Heart Rate Variability Metrics* (2022). The canonical defaults include later refinements recorded in the normative contract.

## Specification

The normative contract is the generated [`hrv.fillgaps` specification](../generated/specifications/hrv.fillgaps.md).
