# Zero-phase filtering with NaN-aware gap handling

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `tools.nan_filtfilt` |
| Module | `tools` |
| Source JSON | [specs/tools/nan_filtfilt/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/tools/nan_filtfilt/spec.json) |

## Summary

Applies ordinary zero-phase filtering while interpolating short NaN gaps and preserving long NaN gaps.

This tool defines NaN-aware zero-phase filtering for one-dimensional vector signals. Matrix and higher-dimensional support may exist as an implementation-specific extension, but it is not required for conformance.

## Keywords

`NaN`, `missing data`, `zero-phase filter`, `gap interpolation`, `segmentation`

## Scientific References

No scientific references are listed in this specification.

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `numerator_coefficients` | real_vector | vector | 1 | false | false | minimum_length=1 |
| `denominator_coefficients` | real_vector | vector | 1 | false | false | minimum_length=1 |
| `signal` | real_vector | vector | a.u. | true | false | None |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `max_gap` | integer_scalar | 0 | sample | minimum=0 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `filtered_signal` | real_vector | vector | a.u. |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `zero_phase_filtering` | For each processed segment, apply ordinary forward-backward zero-phase filtering equivalent to filtfilt with the supplied numerator and denominator coefficients. |  |
| `boundary_nan_gap` | A contiguous run of NaN samples touching the first or last sample of the current processed signal or segment. Boundary NaN gaps are always preserved as NaN and must never be linearly extrapolated. |  |
| `internal_short_nan_gap` | A contiguous run of NaN samples fully bounded by finite samples whose length is less than or equal to max_gap. |  |
| `preserved_nan_gap` | A long internal NaN gap or any boundary NaN gap. Preserved NaN gaps remain NaN in filtered_signal and split signal into candidate finite segments. |  |
| `short_gap_interpolation` | Internal short NaN gaps are filled by linear interpolation before zero-phase filtering. |  |
| `minimum_filterable_length` | Let filter_order = max(length(numerator_coefficients) - 1, length(denominator_coefficients) - 1). A candidate finite segment is filterable only if length(segment) > 3 * filter_order, equivalently length(segment) >= 3 * filter_order + 1. |  |
| `segment_filtering` | Zero-phase filter each filterable candidate finite segment independently after internal short-gap interpolation. |  |
| `segment_too_short` | If a candidate finite segment is not longer than 3 * filter_order, set filtered_signal to NaN over that segment. |  |
| `filtered_signal` | filtered_signal is aligned sample-by-sample with signal; preserved NaN gaps and too-short candidate segments are NaN, while internal short NaN gaps in filterable segments are represented by zero-phase filtered interpolated values. |  |

## Behavior

### Nan handling

NaN samples in signal are classified as boundary gaps, internal short gaps, or preserved internal long gaps using max_gap. Boundary gaps are always preserved as NaN and never extrapolated. Internal short gaps are linearly interpolated before zero-phase filtering. Preserved gaps and too-short candidate finite segments are NaN in the output.

### Empty input

Empty signal input returns an empty filtered_signal.

### Input orientation

Row and column vectors represent the same canonical one-dimensional signal sequence. Matrix and higher-dimensional inputs are outside the normative conformance contract. filtered_signal is a one-dimensional ordered vector aligned with signal.

### Insufficient data

Candidate finite segments with length(segment) <= 3 * max(length(numerator_coefficients) - 1, length(denominator_coefficients) - 1) produce NaN output over that segment.

## Informative Notes

* The normative conformance contract is one-dimensional vector input.
* Matrix and higher-dimensional inputs are optional implementation-specific extensions and are not required for conformance.
* With no NaN samples, the output is equivalent to ordinary zero-phase filtfilt(b, a, signal).
* Only internal short gaps fully bounded by finite samples are linearly interpolated before zero-phase filtering.
* Boundary gaps and long internal gaps are preserved as NaN and split the signal into candidate finite segments.
* Candidate finite segments that are too short for MATLAB-style filtfilt produce NaN output over that segment.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.nan_filtfilt.boundary_nan_preserved` | [conformance/tools/nan_filtfilt/boundary_nan_preserved.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/boundary_nan_preserved.json) |
| `tools.nan_filtfilt.long_nan_gap_segmentation` | [conformance/tools/nan_filtfilt/long_nan_gap_segmentation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/long_nan_gap_segmentation.json) |
| `tools.nan_filtfilt.no_nan_equivalent_filtfilt` | [conformance/tools/nan_filtfilt/no_nan_equivalent_filtfilt.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/no_nan_equivalent_filtfilt.json) |
| `tools.nan_filtfilt.row_vector_orientation` | [conformance/tools/nan_filtfilt/row_vector_orientation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/row_vector_orientation.json) |
| `tools.nan_filtfilt.short_nan_gap_interpolation` | [conformance/tools/nan_filtfilt/short_nan_gap_interpolation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/short_nan_gap_interpolation.json) |
| `tools.nan_filtfilt.too_short_segments_nan` | [conformance/tools/nan_filtfilt/too_short_segments_nan.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/too_short_segments_nan.json) |
