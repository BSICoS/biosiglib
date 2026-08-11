---
spec_id: ecg.baselineremove
title: ECG baseline removal from fiducial isoelectric samples
status: draft
---

# ECG baseline removal from fiducial isoelectric samples

## Purpose

Slow baseline drift can obscure ECG morphology and distort amplitude measurements without behaving like the cardiac activity of interest. This method estimates that drift from supplied fiducial positions expected to represent the local isoelectric level, then subtracts the resulting smooth baseline from the ECG.

## Scientific rationale

Meyer and Keiser describe estimating baseline noise from samples in the PR segment and reconstructing a continuous baseline with cubic splines. The approach uses physiologically selected locations rather than assuming that a generic frequency cutoff can always separate baseline motion from diagnostically relevant ECG content.

The fiducial positions remain an external input to this contract. Biosiglib does not define how they are detected or guarantee that they fall in a genuinely isoelectric interval. Poor fiducials can therefore produce a numerically conformant but scientifically misleading correction.

## Local level estimation

Biosiglib preserves the mature Biosigmat behavior of shifting each position by a caller-supplied sample offset and averaging ECG values in a short symmetric neighborhood. That offset, the default window, expansion of an even requested window to an odd span, and truncation at signal boundaries are empirical compatibility choices. They are not constants or boundary rules established by Meyer and Keiser.

Unordered, repeated, and fractional fiducial positions are normalized before local levels are calculated. These rules make the numerical result reproducible across languages while keeping the public API free to use its native array representation.

## Baseline interpolation

With enough local levels, the baseline is evaluated over the complete ECG sample grid. Four or more points use the not-a-knot cubic spline behavior of the established MATLAB implementation. Two and three points use its linear and quadratic reduced-degree behavior. Evaluation outside the first and last valid fiducials continues the corresponding end polynomial rather than clamping the baseline.

This extrapolation can grow rapidly when endpoint fiducials poorly constrain the polynomial. Supplying fiducials that cover the analyzed segment is therefore preferable even though the contract defines outlying samples for compatibility.

## Assumptions and limitations

The ECG must be finite and real, and the supplied fiducials must use the expected sample grid. Baseline removal changes amplitudes and can remove genuine low-frequency morphology when fiducials are misplaced or when the ECG does not have a stable local isoelectric reference.

The method is a deterministic preprocessing operation, not a detector, quality measure, or physiological interpretation. Its output should be reviewed in the context of the fiducial source and intended downstream analysis.

## References

The use of PR-segment baseline estimates and cubic-spline reconstruction is described by Meyer and Keiser (1977). The exact normalization, local averaging, fallback, and boundary rules are Biosigmat compatibility behavior defined by the normative contract.

## Specification

The normative contract is the generated [`ecg.baselineremove` specification](../generated/specifications/ecg.baselineremove.md).
