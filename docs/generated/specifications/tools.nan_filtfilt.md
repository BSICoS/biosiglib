# Zero-phase filtering with NaN-aware gap handling

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `tools.nan_filtfilt` |
| Module | `tools` |
| Algorithm status | stable |
| Specification status | draft |
| Source JSON | [specs/tools/nan_filtfilt/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/tools/nan_filtfilt/spec.json) |

## Summary

Applies ordinary zero-phase filtering while interpolating short NaN gaps and preserving long NaN gaps.

This tool defines NaN-aware zero-phase filtering for one-dimensional signals. It is intended for zero-phase filtering of sampled signals that may contain missing runs marked by NaN values.

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
| `short_nan_gap` | A contiguous run of NaN samples whose length is less than or equal to max_gap. |  |
| `long_nan_gap` | A contiguous run of NaN samples whose length is greater than max_gap. |  |
| `short_gap_interpolation` | Short NaN gaps inside a valid segment are filled by linear interpolation before zero-phase filtering. |  |
| `segment_filtering` | If long NaN gaps are present, zero-phase filter each non-long-gap segment independently after short-gap interpolation. |  |
| `segment_too_short` | If a segment length is shorter than max(length(denominator_coefficients), length(numerator_coefficients)), return the linearly filled segment without applying the zero-phase filter. |  |
| `filtered_signal` | filtered_signal is aligned sample-by-sample with signal; long NaN gaps are restored to NaN and short NaN gaps are represented by zero-phase filtered interpolated values. |  |

## Behavior

### Nan handling

NaN samples in signal are classified into short and long gaps using max_gap. Short gaps are linearly interpolated and zero-phase filtered. Long gaps are restored as NaN after independent segment processing. All-NaN signal input returns all NaN with the same shape.

### Empty input

Empty signal input returns an empty filtered_signal.

### Input orientation

Row and column vectors represent the same canonical signal sequence. filtered_signal is a one-dimensional ordered vector aligned with signal.

### Insufficient data

Segments shorter than max(length(denominator_coefficients), length(numerator_coefficients)) are returned after interpolation rather than filtered. Additional filtfilt-specific minimum-length failures are pending review.

## Informative Notes

* MATLAB mapping: nanfiltfilt(b, a, x, maxgap).
* Canonical Biosigpy mapping should use tools.nan_filtfilt with numerator_coefficients, denominator_coefficients, signal, and max_gap.
* Matrix and higher-dimensional inputs are outside this draft because the current Biosiglib schema has scalar and vector shapes only.
* With no NaN samples, the output is equivalent to ordinary zero-phase filtfilt(b, a, signal).
* Short gaps are linearly interpolated before zero-phase filtering and are not restored to NaN.
* Long gaps split the signal into independently filtered segments and are restored to NaN in the output.
* filtfilt-specific minimum-length behavior beyond the shared segment_too_short rule remains pending review.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.nan_filtfilt.all_nan_input_001` | [conformance/tools/nan_filtfilt/all_nan_input_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/all_nan_input_001.json) |
| `tools.nan_filtfilt.long_nan_gap_segmentation_001` | [conformance/tools/nan_filtfilt/long_nan_gap_segmentation_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/long_nan_gap_segmentation_001.json) |
| `tools.nan_filtfilt.no_nan_equivalent_filtfilt_001` | [conformance/tools/nan_filtfilt/no_nan_equivalent_filtfilt_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/no_nan_equivalent_filtfilt_001.json) |
| `tools.nan_filtfilt.row_vector_orientation_001` | [conformance/tools/nan_filtfilt/row_vector_orientation_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/row_vector_orientation_001.json) |
| `tools.nan_filtfilt.short_nan_gap_interpolation_001` | [conformance/tools/nan_filtfilt/short_nan_gap_interpolation_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/short_nan_gap_interpolation_001.json) |
| `tools.nan_filtfilt.short_segments_unfiltered_001` | [conformance/tools/nan_filtfilt/short_segments_unfiltered_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/nan_filtfilt/short_segments_unfiltered_001.json) |
