# False-positive event removal

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `hrv.removefp` |
| Module | `hrv` |
| Source JSON | [specs/hrv/removefp/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/hrv/removefp/spec.json) |

## Summary

Removes detections that follow abnormally short event-to-event intervals using a fixed adaptive-baseline rule.

The method is a deterministic preprocessing operation for event-time series. It identifies intervals that are short relative to a local median-filtered baseline and removes the second event of every flagged pair in one simultaneous pass.

## Keywords

`event times`, `false positives`, `HRV preprocessing`, `adaptive baseline`

## Scientific References

No scientific references are listed in this specification.

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `tk` | real_vector | vector | s | false | false | minimum_length=1 |

## Parameters

No parameters.

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `tn` | real_vector | vector | s |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `tk` | tk is a non-empty ordered vector of finite event timestamps expressed in seconds. The time origin is unrestricted, so negative timestamps are valid. |  |
| `event_order` | Event timestamps must be strictly increasing: every timestamp must be greater than the preceding timestamp. Unsorted timestamps and duplicate timestamps are invalid, and implementations must not sort tk implicitly. |  |
| `original_intervals` | For an input containing at least three events, compute dtk as every successive difference of the original tk sequence before any removal. |  |
| `adaptive_baseline` | Compute the adaptive baseline by applying tools.medfilt_threshold to the original dtk sequence with window = 30 samples, factor = 1, and max_threshold = 1.5 s. |  |
| `false_positive_interval` | Flag an original interval only when dtk is strictly less than 0.7 times its aligned adaptive baseline. An interval equal to 0.7 times the baseline is retained. |  |
| `tn` | Retain the first input event. For every flagged original interval, remove the second event of that interval; retain every other input event without modifying its timestamp. |  |
| `single_pass_removal` | Compute the baseline and all interval flags on the complete original event series, then apply all removals simultaneously in one pass. Do not recompute the baseline or iterate after removal. |  |
| `adjacent_false_positive_intervals` | When flagged intervals are adjacent, remove the second event of every flagged interval. This can remove multiple consecutive events while always retaining the first event of the first flagged pair. |  |
| `empirical_algorithm_constants` | The baseline window of 30 samples, baseline factor of 1, 1.5 s baseline cap, and 0.7 false-positive multiplier are fixed empirical algorithm constants. They are not population-independent or clinically validated thresholds. |  |

## Behavior

### Nan handling

NaN, Inf, and -Inf timestamps are invalid. NaN does not represent a missing event in tk; a missed event is represented by the resulting abnormally long finite interval.

### Empty input

Empty tk input is invalid.

### Input orientation

Row and column vectors represent the same canonical event-time sequence. Output orientation is implementation-specific and is not part of the language-independent contract.

### Insufficient data

One- and two-event inputs are valid and are returned unchanged because there is insufficient interval context for false-positive detection.

## Informative Notes

* Input event times must already be strictly increasing; implementations must not sort them implicitly.
* The recommended HRV preprocessing sequence applies false-positive removal before missing-event gap filling.
* The median-filter settings and the 0.7 multiplier are empirical algorithm constants inherited from Biosigmat, not clinically validated thresholds.
* Timestamp-only processing cannot always distinguish a false detection from a nearby true event; the contract preserves the deterministic historical selection rule.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `hrv.removefp.consecutive_flagged_intervals` | [conformance/hrv/removefp/consecutive_flagged_intervals.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/removefp/consecutive_flagged_intervals.json) |
| `hrv.removefp.inserted_close_detection` | [conformance/hrv/removefp/inserted_close_detection.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/removefp/inserted_close_detection.json) |
| `hrv.removefp.regular_series_unchanged` | [conformance/hrv/removefp/regular_series_unchanged.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/removefp/regular_series_unchanged.json) |
| `hrv.removefp.strict_equality_retained` | [conformance/hrv/removefp/strict_equality_retained.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/removefp/strict_equality_retained.json) |
