# Median-filtered adaptive threshold

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `tools.medfilt_threshold` |
| Module | `tools` |
| Algorithm status | stable |
| Specification status | draft |
| Source JSON | [specs/tools/medfilt_threshold/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/tools/medfilt_threshold/spec.json) |

## Summary

Computes a capped adaptive threshold from a one-dimensional signal using Biosigmat-compatible median filtering.

The threshold is intended for detecting unusually large samples relative to a local median baseline. The current draft captures the public Biosigmat medfiltThreshold behavior needed by Biosigpy examples while leaving NaN-specific behavior pending maintainer review.

## Keywords

`median filter`, `adaptive threshold`, `outlier detection`, `Biosigmat`

## Scientific References

No scientific references are listed in this specification.

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `x` | real_vector | vector | a.u. | true | false | minimum_length=1 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `window` | integer_scalar |  | sample | exclusive_minimum=0 |
| `factor` | real_scalar |  | 1 | exclusive_minimum=0 |
| `max_threshold` | real_scalar |  | a.u. | exclusive_minimum=0 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `threshold` | real_vector | vector | a.u. |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `x` | x is the ordered one-dimensional signal or interval sequence from which a local adaptive threshold is computed. |  |
| `effective_window` | If window is larger than the length of x, use length(x) as the effective window. Otherwise use the supplied positive integer window. |  |
| `boundary_padding` | Let half_window = floor(effective_window / 2). Pad x by prepending the first half_window samples in reverse order and appending the last half_window samples in reverse order. |  |
| `median_filtered_baseline` | Apply a median filter with length effective_window - 1 to the padded sequence, then remove the half_window padded samples from each end to recover an output aligned with x. |  |
| `threshold` | threshold is factor times the median_filtered_baseline, with any value greater than max_threshold replaced by max_threshold. |  |

## Behavior

### Nan handling

NaN values in x are accepted by the current Biosigmat input parser, but shared NaN semantics are unspecified in this draft and require maintainer review before conformance cases are added. Inf and -Inf values are invalid.

### Empty input

Empty x input is invalid.

### Input orientation

Row and column vectors represent the same canonical x sequence. The threshold output is a one-dimensional ordered vector aligned sample-by-sample with x.

### Insufficient data

If window is larger than the signal length, the effective window is shortened to length(x). The window = 1 edge currently produces all-NaN thresholds in Biosigmat and is pending review.

## Informative Notes

* MATLAB mapping: medfiltThreshold(x, window, factor, maxthreshold).
* Canonical Biosigpy mapping should use tools.medfilt_threshold and snake_case parameter names.
* Biosigmat converts row and column vectors to a column vector before processing.
* Biosigmat currently calls medfilt1 with window - 1 after boundary padding; this makes requested even and odd window values observable and is covered by conformance cases.
* NaN input behavior is not yet specified by shared conformance and remains pending review.
* The window = 1 edge currently returns all-NaN thresholds in Biosigmat and remains pending maintainer review.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.medfilt_threshold.even_window_behavior_001` | [conformance/tools/medfilt_threshold/even_window_behavior_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/medfilt_threshold/even_window_behavior_001.json) |
| `tools.medfilt_threshold.max_threshold_cap_001` | [conformance/tools/medfilt_threshold/max_threshold_cap_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/medfilt_threshold/max_threshold_cap_001.json) |
| `tools.medfilt_threshold.normal_outlier_001` | [conformance/tools/medfilt_threshold/normal_outlier_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/medfilt_threshold/normal_outlier_001.json) |
| `tools.medfilt_threshold.odd_window_behavior_001` | [conformance/tools/medfilt_threshold/odd_window_behavior_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/medfilt_threshold/odd_window_behavior_001.json) |
| `tools.medfilt_threshold.row_vector_orientation_001` | [conformance/tools/medfilt_threshold/row_vector_orientation_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/medfilt_threshold/row_vector_orientation_001.json) |
| `tools.medfilt_threshold.window_larger_than_signal_001` | [conformance/tools/medfilt_threshold/window_larger_than_signal_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/medfilt_threshold/window_larger_than_signal_001.json) |
