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

This tool defines NaN-aware causal filtering for one-dimensional signals. It is intended for filtering sampled signals that may contain missing runs marked by NaN values.

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
| `short_nan_gap` | A contiguous run of NaN samples whose length is less than or equal to max_gap. |  |
| `long_nan_gap` | A contiguous run of NaN samples whose length is greater than max_gap. |  |
| `short_gap_interpolation` | Short NaN gaps inside a valid segment are filled by linear interpolation before causal filtering. |  |
| `segment_filtering` | If long NaN gaps are present, filter each non-long-gap segment independently with ordinary causal filter semantics after short-gap interpolation. |  |
| `segment_too_short` | If a segment length is shorter than max(length(denominator_coefficients), length(numerator_coefficients)), return the linearly filled segment without applying the filter. |  |
| `filtered_signal` | filtered_signal is aligned sample-by-sample with signal; long NaN gaps are restored to NaN and short NaN gaps are represented by filtered interpolated values. |  |

## Behavior

### Nan handling

NaN samples in signal are classified into short and long gaps using max_gap. Short gaps are linearly interpolated and filtered. Long gaps are restored as NaN after independent segment processing. All-NaN signal input returns all NaN with the same shape.

### Empty input

Empty signal input returns an empty filtered_signal.

### Input orientation

Row and column vectors represent the same canonical signal sequence. filtered_signal is a one-dimensional ordered vector aligned with signal.

### Insufficient data

Segments shorter than max(length(denominator_coefficients), length(numerator_coefficients)) are returned after interpolation rather than filtered.

## Informative Notes

* Matrix and higher-dimensional inputs are outside this draft because the current Biosiglib schema has scalar and vector shapes only.
* With no NaN samples, the output is equivalent to ordinary causal filter(b, a, signal).
* Short gaps are linearly interpolated before filtering and are not restored to NaN.
* Long gaps split the signal into independently filtered segments and are restored to NaN in the output.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.nan_filter.long_nan_gap_segmentation` | [conformance/tools/nan_filter/long_nan_gap_segmentation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/long_nan_gap_segmentation.json) |
| `tools.nan_filter.no_nan_equivalent_filter` | [conformance/tools/nan_filter/no_nan_equivalent_filter.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/no_nan_equivalent_filter.json) |
| `tools.nan_filter.row_vector_orientation` | [conformance/tools/nan_filter/row_vector_orientation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/row_vector_orientation.json) |
| `tools.nan_filter.short_nan_gap_interpolation` | [conformance/tools/nan_filter/short_nan_gap_interpolation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/short_nan_gap_interpolation.json) |
| `tools.nan_filter.short_segments_unfiltered` | [conformance/tools/nan_filter/short_segments_unfiltered.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filter/short_segments_unfiltered.json) |
