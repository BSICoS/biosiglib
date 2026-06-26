# hrv.tdmetrics

`hrv.tdmetrics` defines standard time-domain variability metrics from ordered beat or pulse event times.

!!! note
    This page is a manually written summary of the pilot JSON specification. Generated pages from JSON specifications will be introduced in a follow-up issue.

## Purpose

The specification describes how to compute conventional time-domain variability metrics from a canonical input named `tk`. The input is an ordered sequence of beat or pulse event occurrence times in seconds.

Events may come from ECG R waves, PPG fiducial points, or another validated beat or pulse timing source. Abnormal detections, missed detections, false detections, and artifacts should be corrected or removed before calling an implementation.

## Canonical Input

| Input | Unit | Meaning |
| --- | --- | --- |
| `tk` | s | Ordered finite, non-negative event occurrence times. |

A valid `tk` sequence is one-dimensional, finite, non-NaN, non-negative, and strictly increasing. The interval sequence `dtk` is derived internally as successive differences between adjacent event times.

## Outputs

| Output | Unit | Summary |
| --- | --- | --- |
| `mhr` | beats/min | Mean heart or pulse rate, defined as `60 / mean(dtk)`. |
| `sdnn` | ms | Sample standard deviation of valid intervals. |
| `sdsd` | ms | Sample standard deviation of successive interval differences. |
| `rmssd` | ms | Root mean square of successive interval differences. |
| `pnn50` | % | Percentage of successive interval differences strictly greater than 50 ms. |

## Draft Behavior Notes

NaN values in `tk` are invalid. Row and column vectors represent the same canonical event sequence and should produce scientifically equivalent outputs.

Some insufficient-data behavior remains intentionally unresolved in the draft pilot, including empty input, a single valid event time, no valid successive intervals, and a single successive interval when sample standard deviation is requested.

## Conformance Resources

The pilot conformance cases include one positive `ecg_tk_001` case and invalid-input cases for non-numeric, negative, non-monotonic, repeated, and matrix-shaped `tk` values.

The JSON specification remains the normative source:

* [`specs/hrv/tdmetrics/spec.json`](https://github.com/BSICoS/biosiglib/blob/main/specs/hrv/tdmetrics/spec.json)
