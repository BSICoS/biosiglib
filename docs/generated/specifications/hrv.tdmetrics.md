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

Computes standard time-domain variability metrics from ordered beat or pulse event times.

The input tk contains occurrence times, in seconds, of beat or pulse event k. Events may come from ECG R waves, PPG fiducial points such as maximum upstroke slope, or another validated beat or pulse timing source. Abnormal detections, missed detections, false detections, and artifacts must be corrected or removed before calling this algorithm.

## Keywords

`HRV`, `time-domain`, `beat timing`, `pulse timing`, `tk`, `dtk`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `task_force_hrv_1996` | metric_definition | Supports the conventional definitions and units of time-domain variability metrics; Biosiglib generalizes the timing input beyond ECG-only R-wave timing. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `tk` | real_vector | vector | s | false | false | minimum=0 |

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
| `tk` | tk is the ordered sequence of finite, non-negative occurrence times of beat or pulse event k, expressed in seconds. |  |
| `valid_tk_sequence` | A valid tk sequence is a one-dimensional real vector containing finite, non-NaN values that are strictly increasing. |  |
| `dtk` | dtk is the successive interval sequence derived from adjacent entries of tk: dtk[i] = tk[i+1] - tk[i]. |  |
| `valid_interval` | A valid interval is a finite, positive element of dtk expressed in seconds. |  |
| `mhr` | Mean heart or pulse rate is 60 / mean(valid intervals), where the mean is calculated over valid dtk intervals. | \mathrm{MHR} = \frac{60}{\operatorname{mean}(dTK)} |
| `sdnn` | SDNN is the sample standard deviation of valid dtk intervals using denominator N - 1, converted from seconds to milliseconds. |  |
| `successive_interval_differences` | Successive interval differences are calculated between adjacent entries in the dtk interval vector derived from tk. A difference is valid only when both adjacent intervals are valid. |  |
| `rmssd` | RMSSD is the square root of the mean squared valid successive interval differences, converted from seconds to milliseconds. |  |
| `sdsd` | SDSD is the sample standard deviation of valid successive interval differences using denominator N - 1, converted from seconds to milliseconds. |  |
| `pnn50` | pNN50 is 100 * count(abs(valid successive interval differences) > 0.05 s) / number of valid successive interval differences. The threshold is strictly greater than 50 ms. |  |

## Behavior

### Nan handling

NaN values in tk are invalid. Missing or abnormal events must be corrected or removed before calling the algorithm.

### Empty input

Empty tk input is invalid; the exact failure mechanism is implementation-specific until an expected-error case is added.

### Input orientation

Row and column vectors represent the same canonical tk sequence and must produce scientifically equivalent outputs.

### Insufficient data

Unspecified for fewer than two valid event times or for too few valid intervals to calculate sample standard deviations.

## Informative Notes

* The canonical input is tk, not an ECG-only RR/NN interval series.
* The interval series dtk is derived as successive differences of adjacent tk values.
* Python should expose the canonical input as tk.
* Biosigmat currently accepts the derived interval vector dtk; a conformance adapter derives dtk = diff(tk) until the MATLAB public API is aligned with the canonical input.
* Canonical output IDs map directly in Python. In Biosigmat, pnn50 maps to pNN50 and the other output IDs map directly.
* Unresolved behavior: empty input.
* Unresolved behavior: one valid event time.
* Unresolved behavior: no valid successive intervals.
* Unresolved behavior: only one valid successive interval when sample standard deviation is requested.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `hrv.tdmetrics.ecg_tk_001` | [conformance/hrv/tdmetrics/ecg_tk_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/ecg_tk_001.json) |
| `hrv.tdmetrics.invalid_tk_matrix` | [conformance/hrv/tdmetrics/invalid_tk_matrix.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_tk_matrix.json) |
| `hrv.tdmetrics.invalid_tk_negative` | [conformance/hrv/tdmetrics/invalid_tk_negative.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_tk_negative.json) |
| `hrv.tdmetrics.invalid_tk_non_monotonic` | [conformance/hrv/tdmetrics/invalid_tk_non_monotonic.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_tk_non_monotonic.json) |
| `hrv.tdmetrics.invalid_tk_non_numeric` | [conformance/hrv/tdmetrics/invalid_tk_non_numeric.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_tk_non_numeric.json) |
| `hrv.tdmetrics.invalid_tk_repeated` | [conformance/hrv/tdmetrics/invalid_tk_repeated.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/tdmetrics/invalid_tk_repeated.json) |
