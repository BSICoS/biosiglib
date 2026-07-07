# Causal filtering with NaN-aware gap handling

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `tools.nan_filter` |
| Module | `tools` |
| Source JSON | [specs/tools/nan_filter/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/tools/nan_filter/spec.json) |

## Summary

Applies ordinary causal filtering while interpolating short NaN gaps and preserving long NaN gaps.

This tool defines NaN-aware causal filtering for one-dimensional vector signals. Matrix and higher-dimensional support may exist as an implementation-specific extension, but it is not required for conformance.

## Keywords

`NaN`, `missing data`, `causal filter`, `gap interpolation`, `segmentation`

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
| `boundary_nan_gap` | A contiguous run of NaN samples touching the first or last sample of the current processed signal or segment. Boundary NaN gaps are always preserved as NaN and must never be linearly extrapolated. |  |
| `internal_short_nan_gap` | A contiguous run of NaN samples fully bounded by finite samples whose length is less than or equal to max_gap. |  |
| `preserved_nan_gap` | A long internal NaN gap or any boundary NaN gap. Preserved NaN gaps remain NaN in filtered_signal and split signal into candidate finite segments. |  |
| `short_gap_interpolation` | Internal short NaN gaps are filled by linear interpolation before causal filtering. |  |
| `minimum_filterable_length` | A candidate finite segment is filterable only if length(segment) is at least max(length(numerator_coefficients), length(denominator_coefficients)). |  |
| `segment_filtering` | Filter each filterable candidate finite segment independently with ordinary causal filter semantics after internal short-gap interpolation. |  |
| `segment_too_short` | If a candidate finite segment is shorter than minimum_filterable_length, set filtered_signal to NaN over that segment. |  |
| `filtered_signal` | filtered_signal is aligned sample-by-sample with signal; preserved NaN gaps and too-short candidate segments are NaN, while internal short NaN gaps in filterable segments are represented by filtered interpolated values. |  |

## Behavior

### Nan handling

NaN samples in signal are classified as boundary gaps, internal short gaps, or preserved internal long gaps using max_gap. Boundary gaps are always preserved as NaN and never extrapolated. Internal short gaps are linearly interpolated before filtering. Preserved gaps and too-short candidate finite segments are NaN in the output.

### Empty input

Empty signal input returns an empty filtered_signal.

### Input orientation

Row and column vectors represent the same canonical one-dimensional signal sequence. Matrix and higher-dimensional inputs are outside the normative conformance contract. filtered_signal is a one-dimensional ordered vector aligned with signal.

### Insufficient data

Candidate finite segments shorter than max(length(numerator_coefficients), length(denominator_coefficients)) produce NaN output over that segment.

## Informative Notes

* The normative conformance contract is one-dimensional vector input.
* Matrix and higher-dimensional inputs are optional implementation-specific extensions and are not required for conformance.
* With no NaN samples, the output is equivalent to ordinary causal filter(b, a, signal).
* Only internal short gaps fully bounded by finite samples are linearly interpolated before filtering.
* Boundary gaps and long internal gaps are preserved as NaN and split the signal into candidate finite segments.
* Candidate finite segments that are too short for causal filtering produce NaN output over that segment.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.nan_filter.boundary_nan_preserved` | [conformance/tools/nan_filter/boundary_nan_preserved.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/boundary_nan_preserved.json) |
| `tools.nan_filter.long_nan_gap_segmentation` | [conformance/tools/nan_filter/long_nan_gap_segmentation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/long_nan_gap_segmentation.json) |
| `tools.nan_filter.no_nan_equivalent_filter` | [conformance/tools/nan_filter/no_nan_equivalent_filter.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/no_nan_equivalent_filter.json) |
| `tools.nan_filter.row_vector_orientation` | [conformance/tools/nan_filter/row_vector_orientation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/row_vector_orientation.json) |
| `tools.nan_filter.short_nan_gap_interpolation` | [conformance/tools/nan_filter/short_nan_gap_interpolation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/short_nan_gap_interpolation.json) |
| `tools.nan_filter.too_short_segments_nan` | [conformance/tools/nan_filter/too_short_segments_nan.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/too_short_segments_nan.json) |
