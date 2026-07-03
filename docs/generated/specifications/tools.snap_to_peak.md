# Snap detections to local maxima

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `tools.snap_to_peak` |
| Module | `tools` |
| Source JSON | [specs/tools/snap_to_peak/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/tools/snap_to_peak/spec.json) |

## Summary

Refines detection sample positions by moving each detection to the maximum signal sample in a local search window.

This tool defines local-maximum snapping used by ECG detection pipelines to refine approximate detections onto nearby R-wave maxima.

## Keywords

`peak refinement`, `sample position`, `ECG`, `R wave`, `local maximum`

## Scientific References

No scientific references are listed in this specification.

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `ecg` | real_vector | vector | a.u. | false | false | minimum_length=2 |
| `detections` | real_vector | vector | sample | false | false | exclusive_minimum=0 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `window_size` | real_scalar | 20 | sample | exclusive_minimum=0 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `refined_detections` | real_vector | vector | sample |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `one_based_sample_position` | A sample position is expressed on a one-based sample grid: the first ECG sample has position 1 and the last sample has position length(ecg). |  |
| `effective_window_size` | window_size is rounded to the nearest integer number of samples before constructing search windows. |  |
| `search_window` | For each detection d, search from max(1, d - effective_window_size) through min(length(ecg), d + effective_window_size), inclusive on the one-based sample grid. |  |
| `refined_detection` | The refined detection is the one-based sample position of the first maximum-valued ECG sample inside the search_window for that detection. |  |
| `refined_detections` | refined_detections is aligned one-for-one with detections and preserves the input detection order. |  |

## Behavior

### Nan handling

NaN, Inf, and -Inf values in ecg or detections are invalid in this draft.

### Empty input

Empty ecg input is invalid. Empty detections input returns an empty refined_detections vector.

### Input orientation

Row and column vectors represent the same canonical ecg and detections sequences. refined_detections is a one-dimensional ordered vector aligned with detections.

### Insufficient data

Detection positions less than 1 or greater than length(ecg) are invalid. Search windows near signal boundaries are clipped to valid ECG sample positions.

## Informative Notes

* MATLAB mapping: snaptopeak(ecg, detections, 'WindowSize', window_size).
* Canonical Biosigpy mapping should use tools.snap_to_peak with ecg, detections, and window_size.
* Canonical detection positions are one-based sample positions, matching existing Biosiglib r_wave_samples fixtures and the public sample-coordinate convention.
* Python implementations may convert to zero-based internal indexes, but public inputs and outputs for this specification use the one-based sample grid.
* NaN samples in ecg are outside this draft contract pending maintainer review.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.snap_to_peak.boundary_clipping` | [conformance/tools/snap_to_peak/boundary_clipping.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/boundary_clipping.json) |
| `tools.snap_to_peak.configurable_window_large` | [conformance/tools/snap_to_peak/configurable_window_large.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/configurable_window_large.json) |
| `tools.snap_to_peak.configurable_window_small` | [conformance/tools/snap_to_peak/configurable_window_small.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/configurable_window_small.json) |
| `tools.snap_to_peak.invalid_detection_out_of_bounds` | [conformance/tools/snap_to_peak/invalid_detection_out_of_bounds.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/invalid_detection_out_of_bounds.json) |
| `tools.snap_to_peak.local_maxima` | [conformance/tools/snap_to_peak/local_maxima.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/local_maxima.json) |
