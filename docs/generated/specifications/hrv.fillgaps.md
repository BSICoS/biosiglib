# Missing-event gap filling

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `hrv.fillgaps` |
| Module | `hrv` |
| Source JSON | [specs/hrv/fillgaps/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/hrv/fillgaps/spec.json) |

## Summary

Reconstructs missing event timestamps by iteratively interpolating intervals inside locally detected gaps.

The method preserves every original event timestamp and attempts progressively larger insertion counts in unresolved long intervals. Each reconstruction uses PCHIP interpolation from nearby valid intervals, is rescaled to the exact gap duration, and is accepted or rolled back according to local interval bounds.

## Keywords

`event times`, `missing events`, `HRV preprocessing`, `PCHIP interpolation`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `cajal_missing_data_hrv_2022` | preprocessing_guidance | Documents the missing-data problem in HRV analysis and the original empirical gap-detection and correction factors; the canonical defaults include later Biosigmat refinements recorded by this contract. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `tk` | real_vector | vector | s | false | false | minimum_length=1 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `gap_detection_factor` | real_scalar | 1.5 | 1 | exclusive_minimum=0 |
| `correction_upper_factor` | real_scalar | 1.15 | 1 | exclusive_minimum=0 |
| `correction_lower_factor` | real_scalar | 0.75 | 1 | exclusive_minimum=0 |
| `minimum_interval` | real_scalar | 0.5 | s | minimum=0 |
| `max_gap_duration` | real_scalar | 10 | s | exclusive_minimum=0 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `tn` | real_vector | vector | s |
| `dtn` | real_vector | vector | s |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `tk` | tk is a non-empty ordered vector of finite event timestamps expressed in seconds. The time origin is unrestricted, so negative timestamps are valid. tk is assumed to have already undergone any desired false-positive removal; fillgaps must not invoke hrv.removefp internally. |  |
| `event_order` | Event timestamps must be strictly increasing: every timestamp must be greater than the preceding timestamp. Unsorted timestamps and duplicate timestamps are invalid, and implementations must not sort tk implicitly. |  |
| `parameter_relationships` | All five parameters must be finite. The three factors must satisfy 0 < correction_lower_factor < correction_upper_factor <= gap_detection_factor. minimum_interval must be greater than or equal to 0 s, and max_gap_duration must be strictly positive. |  |
| `adaptive_baseline` | For a series with at least three events, compute its successive intervals and apply tools.medfilt_threshold with window = 30 samples, factor = 1, and max_threshold = 1.5 s. Recompute this aligned baseline after every complete insertion-count pass. |  |
| `gap_detection` | An interval is a gap only when it is strictly greater than both gap_detection_factor times its aligned adaptive baseline and minimum_interval. Equality to either boundary is not a gap. A detected gap whose duration exceeds max_gap_duration is uncorrectable. |  |
| `segment_wide_iteration` | Start with one inserted event for every unresolved correctable gap in the complete series. Finish that pass for every such gap before attempting two insertions in any still-unresolved gap, then continue with three and higher insertion counts without an arbitrary maximum. Attempts within a pass use the interval series, baseline, and unresolved-gap set at the start of that pass; accepted results are applied together after the pass, followed by interval, baseline, and gap recomputation. |  |
| `interpolation_support` | For a gap attempt with N inserted events, select the two nearest valid intervals before the gap and the two nearest valid intervals after it. Intervals belonging to every other unresolved gap are excluded while searching outward. The search distance is unbounded, but no extrapolation or lower-order interpolation is allowed; a gap without two valid intervals on each side is uncorrectable. |  |
| `pchip_reconstruction` | Place the four support-interval values at compressed coordinates [-1, 0, N + 2, N + 3] in chronological order. Evaluate shape-preserving piecewise cubic Hermite interpolation at integer coordinates 1 through N + 1. Rescale all N + 1 reconstructed intervals by one common factor so their sum equals the original gap duration exactly, then insert N events at their cumulative offsets from the original event before the gap. |  |
| `sufficient_reconstruction` | A reconstruction is sufficient only when every one of its N + 1 intervals is strictly less than correction_upper_factor times the baseline aligned with the original gap at the start of the current pass. If sufficient, accept it and finalize that gap. |  |
| `over_insertion` | A reconstruction is over-inserted only when every one of its N + 1 intervals is strictly less than max(correction_lower_factor times the baseline aligned with the original gap at the start of the current pass, minimum_interval). If an attempt is over-inserted, finalize the gap using the preceding insertion-count reconstruction, even when that preceding reconstruction did not satisfy the upper bound. Because iteration starts at N = 1, an over-inserted N = 1 attempt leaves the gap unresolved with no inserted events. |  |
| `original_events` | tn contains every original timestamp from tk unchanged and in its original order. Reconstruction can only add timestamps strictly inside a gap; it must never remove or displace original events. |  |
| `unresolved_gap_output` | If a gap is uncorrectable or remains unresolved, preserve both original timestamps spanning it and insert no event in that span. Compute dtn as diff(tn), then replace the single dtn element spanning every unresolved gap with NaN. This rule also applies when no gap can be attempted and the algorithm returns early. |  |
| `dtn` | dtn is the successive-difference vector of tn, with length max(length(tn) - 1, 0), except that intervals spanning unresolved gaps are represented by NaN as defined above. |  |

## Behavior

### Nan handling

NaN, Inf, and -Inf timestamps are invalid. NaN does not represent a missing event in tk; a missed event is represented by the resulting abnormally long finite interval. NaN is used only in dtn to mark an unresolved gap span.

### Empty input

Empty tk input is invalid.

### Input orientation

Row and column vectors represent the same canonical event-time sequence. Output orientation is implementation-specific and is not part of the language-independent contract.

### Insufficient data

A single event is valid and returns tn equal to tk with empty dtn. A two-event series is valid; without enough baseline and two-sided interpolation support, its timestamps are preserved and any detected unresolved gap would be represented by NaN in dtn. Small valid inputs must not fail merely because reconstruction support is unavailable.

## Informative Notes

* Input event times must already be strictly increasing; implementations must not sort them implicitly.
* fillgaps receives an already cleaned event series and must not call hrv.removefp internally. The recommended preprocessing order is hrv.removefp followed by hrv.fillgaps.
* The default factors are empirical algorithm settings and are not clinically validated thresholds.
* Original event timestamps are never displaced or removed, including when a gap cannot be reconstructed.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `hrv.fillgaps.insufficient_support_unresolved` | [conformance/hrv/fillgaps/insufficient_support_unresolved.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fillgaps/insufficient_support_unresolved.json) |
| `hrv.fillgaps.over_insertion_fallback` | [conformance/hrv/fillgaps/over_insertion_fallback.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fillgaps/over_insertion_fallback.json) |
| `hrv.fillgaps.over_maximum_duration_unresolved` | [conformance/hrv/fillgaps/over_maximum_duration_unresolved.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fillgaps/over_maximum_duration_unresolved.json) |
| `hrv.fillgaps.pchip_single_insertion` | [conformance/hrv/fillgaps/pchip_single_insertion.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fillgaps/pchip_single_insertion.json) |
| `hrv.fillgaps.regular_series_unchanged` | [conformance/hrv/fillgaps/regular_series_unchanged.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fillgaps/regular_series_unchanged.json) |
| `hrv.fillgaps.segment_wide_iteration` | [conformance/hrv/fillgaps/segment_wide_iteration.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fillgaps/segment_wide_iteration.json) |
| `hrv.fillgaps.single_event` | [conformance/hrv/fillgaps/single_event.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fillgaps/single_event.json) |
