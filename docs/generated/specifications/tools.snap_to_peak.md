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

Refines detection sample positions by moving each detection to the maximum signal sample in a NaN-aware local search window.

This tool defines local-maximum snapping used by ECG detection pipelines to refine approximate detections onto nearby R-wave maxima while treating NaN ECG samples as signal gaps.

## Keywords

`peak refinement`, `sample position`, `ECG`, `R wave`, `local maximum`

## Scientific References

No scientific references are listed in this specification.

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `ecg` | real_vector | vector | a.u. | true | false | minimum_length=2 |
| `detections` | real_vector | vector | sample | true | false | exclusive_minimum=0 |

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
| `effective_window_size` | window_size is rounded to the nearest integer number of samples before constructing search windows. |  |
| `finite_ecg_segment` | A finite ECG segment is a maximal contiguous run of ecg samples that are neither NaN nor infinite. NaN samples are hard boundaries between finite ECG segments; Inf and -Inf samples are invalid inputs. |  |
| `search_window` | For each finite valid detection d that falls on a finite ECG sample, search from max(1, segment_start, d - effective_window_size) through min(length(ecg), segment_end, d + effective_window_size), inclusive on the one-based sample grid, where segment_start and segment_end are the boundaries of the finite_ecg_segment containing d. |  |
| `refined_detection` | The refined detection is the one-based sample position of the first maximum-valued ECG sample inside the clipped finite search_window for that detection. If the corresponding detection is NaN, or if a finite detection falls on a NaN ECG sample, the refined detection is NaN. |  |

## Behavior

### Nan handling

NaN values in ecg are allowed and act as hard segment boundaries. Snapping for a finite valid detection must search only inside the contiguous finite ECG segment containing that detection and must not omit NaNs in a way that crosses gaps. NaN values in detections are allowed missing detection markers and produce NaN in the corresponding refined_detections element. If a finite detection falls on a NaN ECG sample, the corresponding refined_detections element is NaN. Inf and -Inf values in either ecg or detections are invalid.

### Empty input

Empty ecg input is invalid. Empty detections input returns an empty refined_detections vector.

### Input orientation

Row and column vectors represent the same canonical ecg and detections sequences. refined_detections is a one-dimensional ordered vector aligned with detections.

### Insufficient data

Finite detection positions less than 1 or greater than length(ecg) are invalid. Search windows near signal boundaries or NaN ECG gaps are clipped to valid finite ECG sample positions.

## Informative Notes

* Canonical detection positions are one-based sample positions, matching existing Biosiglib r_wave_samples fixtures and the public sample-coordinate convention.
* NaN values are accepted in ecg as hard signal-gap boundaries and in detections as missing detection markers.
* Inf and -Inf values in ecg or detections are invalid.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.snap_to_peak.boundary_clipping` | [conformance/tools/snap_to_peak/boundary_clipping.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/boundary_clipping.json) |
| `tools.snap_to_peak.configurable_window_large` | [conformance/tools/snap_to_peak/configurable_window_large.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/configurable_window_large.json) |
| `tools.snap_to_peak.configurable_window_small` | [conformance/tools/snap_to_peak/configurable_window_small.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/configurable_window_small.json) |
| `tools.snap_to_peak.detection_nan_returns_nan` | [conformance/tools/snap_to_peak/detection_nan_returns_nan.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/detection_nan_returns_nan.json) |
| `tools.snap_to_peak.detection_on_nan_ecg_returns_nan` | [conformance/tools/snap_to_peak/detection_on_nan_ecg_returns_nan.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/detection_on_nan_ecg_returns_nan.json) |
| `tools.snap_to_peak.ecg_nan_segment_boundary` | [conformance/tools/snap_to_peak/ecg_nan_segment_boundary.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/ecg_nan_segment_boundary.json) |
| `tools.snap_to_peak.invalid_detection_out_of_bounds` | [conformance/tools/snap_to_peak/invalid_detection_out_of_bounds.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/invalid_detection_out_of_bounds.json) |
| `tools.snap_to_peak.local_maxima` | [conformance/tools/snap_to_peak/local_maxima.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/snap_to_peak/local_maxima.json) |
