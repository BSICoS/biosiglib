# Time-domain beat or pulse variability metrics

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `hrv.tdmetrics` |
| Module | `hrv` |
| Algorithm status | stable |
| Specification status | draft |
| Source JSON | [specs/hrv/tdmetrics/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/hrv/tdmetrics/spec.json) |

## Summary

Computes standard time-domain HRV metrics from cleaned beat-to-beat or pulse-to-pulse intervals.

The input dtk is the interval series, in seconds, after beat or pulse detection, interval construction, and preprocessing for artifacts, missed beats, false detections, ectopic beats, outliers, and missing data. Invalid intervals may be removed before calling this algorithm, or retained as NaN markers that are omitted from metric calculations.

## Keywords

`dtk`, `HRV`, `time-domain`, `missing data`, `artifact handling`, `wearable`, `omitnan`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `task_force_hrv_1996` | metric_definition | Supports the conventional definitions and units of time-domain variability metrics; Biosiglib generalizes the timing input beyond ECG-only R-wave timing. |
| `cajal_missing_data_hrv_2022` | preprocessing_guidance | Supports robust handling of missing or invalid intervals when computing HRV metrics from wearable or artifact-affected interval series. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `dtk` | real_vector | vector | s | true | false | exclusive_minimum=0 |

## Parameters

No parameters.

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `mhr` | real_scalar | scalar | beats/min |
| `sdnn` | real_scalar | scalar | ms |
| `sdsd` | real_scalar | scalar | ms |
| `rmssd` | real_scalar | scalar | ms |
| `pnn50` | real_scalar | scalar | % |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `dtk` | dtk is the ordered vector of beat-to-beat or pulse-to-pulse intervals, expressed in seconds, after preprocessing for artifacts, missed beats, false detections, ectopic beats, outliers, and missing data. |  |
| `valid_interval` | A valid interval is a finite, strictly positive, non-infinite, non-NaN element of dtk expressed in seconds. |  |
| `missing_interval_marker` | NaN is an allowed missing or invalid interval marker in dtk and is omitted from all metric calculations. |  |
| `mhr` | Mean heart or pulse rate is 60 / mean(valid dtk), where valid dtk is the sequence remaining after omitting NaN markers. | \mathrm{MHR} = \frac{60}{\operatorname{mean}(dTK)} |
| `sdnn` | SDNN is the sample standard deviation of valid dtk intervals after omitting NaN markers, using denominator N - 1, converted from seconds to milliseconds. |  |
| `successive_interval_differences` | Successive interval differences are calculated between adjacent entries of the cleaned valid interval sequence after omitting NaN markers from dtk. NaN is not treated as zero and is not interpolated inside tdmetrics. |  |
| `rmssd` | RMSSD is the square root of the mean squared successive interval differences from the cleaned valid interval sequence, converted from seconds to milliseconds. |  |
| `sdsd` | SDSD is the sample standard deviation of successive interval differences from the cleaned valid interval sequence, using denominator N - 1, converted from seconds to milliseconds. |  |
| `pnn50` | pNN50 is 100 * count(abs(successive interval differences) > 0.05 s) / number of successive interval differences in the cleaned valid interval sequence. The threshold is strictly greater than 50 ms. |  |

## Behavior

### Nan handling

NaN values in dtk are allowed and omitted from all metric calculations. Inf and -Inf intervals are invalid. Zero or negative finite intervals are invalid. tdmetrics must not silently interpolate, gap-fill, or treat invalid intervals as physiological variability.

### Empty input

Empty dtk input is invalid; the exact failure mechanism is implementation-specific until an expected-error case is added.

### Input orientation

Row and column vectors represent the same canonical dtk sequence and must produce scientifically equivalent outputs.

### Insufficient data

Unspecified for too few valid intervals to calculate mean, sample standard deviations, or successive-difference metrics after omitting NaN markers.

## Informative Notes

* The canonical input is dtk, the cleaned beat-to-beat or pulse-to-pulse interval sequence.
* Intervals affected by artifacts, missed beats, false detections, ectopic beats, or outlier behavior should be detected and removed, corrected, or marked as NaN before calling the algorithm.
* NaN intervals are explicit missing or invalid interval markers and are ignored in all metric calculations, equivalent to omit-NaN behavior.
* The function must not silently treat invalid intervals as physiological variability.
* Removing invalid intervals or marking them as NaN can both be correct choices for time-domain statistics over valid intervals.
* tdmetrics does not interpolate NaN values, gap-fill intervals, or reconstruct event times internally.
* Canonical output IDs map directly in Python. In Biosigmat, pnn50 maps to pNN50 and the other output IDs map directly.
* Unresolved behavior: empty input.
* Unresolved behavior: one valid interval.
* Unresolved behavior: no valid successive intervals.
* Unresolved behavior: only one valid successive interval when sample standard deviation is requested.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `hrv.tdmetrics.invalid_dtk_inf` | [conformance/hrv/tdmetrics/invalid_dtk_inf.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_dtk_inf.json) |
| `hrv.tdmetrics.invalid_dtk_matrix` | [conformance/hrv/tdmetrics/invalid_dtk_matrix.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_dtk_matrix.json) |
| `hrv.tdmetrics.invalid_dtk_negative` | [conformance/hrv/tdmetrics/invalid_dtk_negative.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_dtk_negative.json) |
| `hrv.tdmetrics.invalid_dtk_non_numeric` | [conformance/hrv/tdmetrics/invalid_dtk_non_numeric.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_dtk_non_numeric.json) |
| `hrv.tdmetrics.invalid_dtk_zero` | [conformance/hrv/tdmetrics/invalid_dtk_zero.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_dtk_zero.json) |
| `hrv.tdmetrics.valid_dtk_001` | [conformance/hrv/tdmetrics/valid_dtk_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/valid_dtk_001.json) |
| `hrv.tdmetrics.valid_dtk_with_nan_001` | [conformance/hrv/tdmetrics/valid_dtk_with_nan_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/valid_dtk_with_nan_001.json) |
