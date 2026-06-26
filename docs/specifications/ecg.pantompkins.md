# ecg.pantompkins

`ecg.pantompkins` defines a Pan-Tompkins-style ECG R-peak detector and its public intermediate processing signals.

!!! note
    This page is a manually written summary of the pilot JSON specification. Generated pages from JSON specifications will be introduced in a follow-up issue.

## Purpose

The specification describes R-wave detection from a sampled ECG signal. The current pilot follows the Pan-Tompkins processing style through bandpass filtering, derivative filtering, squaring, moving-window integration, peak detection, and peak refinement.

It is not intended to be a byte-for-byte reproduction of the original paper. The contract is the behavior captured by Biosiglib's JSON specification and conformance cases.

## Canonical Inputs

| Input | Unit | Meaning |
| --- | --- | --- |
| `ecg` | a.u. | One-dimensional ECG signal. |
| `sampling_frequency` | Hz | Positive sampling frequency for the ECG signal. |

NaN samples are allowed in `ecg` in the draft schema, while infinite values are not. The sampling frequency must be finite, non-NaN, and strictly positive.

## Parameters

| Parameter | Default | Unit | Summary |
| --- | --- | --- | --- |
| `bandpass_frequency` | `[5, 12]` | Hz | Bandpass range for the detector preprocessing. |
| `integration_window_size` | `0.15` | s | Moving-window integration duration. |
| `minimum_peak_distance` | `0.5` | s | Minimum distance between detected peaks. |
| `snap_to_peak_window_size` | `20` | sample | Local refinement window used to snap detections to signal peaks. |

## Outputs

| Output | Unit | Summary |
| --- | --- | --- |
| `r_peak_times` | s | Detected R-wave occurrence times in ascending order. |
| `ecg_filtered` | a.u. | Bandpass-filtered ECG signal. |
| `decg` | a.u. | Derivative-filtered ECG signal. |
| `decg_envelope` | a.u.^2 | Squared and moving-window integrated detection envelope. |

The intermediate signals are part of the public contract because implementations use them for plotting and debugging detections.

## Draft Behavior Notes

Row and column ECG vectors represent the same canonical ordered signal. Empty input and insufficient-data behavior remain unspecified in this draft pilot.

The first positive conformance case focuses on the detected R-peak times. Exact cross-language numerical equality of intermediate signals is not required by that case.

## Conformance Resources

The pilot conformance cases include one positive `edr_signals_001` case and invalid-input cases for non-numeric ECG values, matrix-shaped ECG values, and invalid sampling-frequency values.

The JSON specification remains the normative source:

* [`specs/ecg/pantompkins/spec.json`](https://github.com/BSICoS/biosiglib/blob/main/specs/ecg/pantompkins/spec.json)
