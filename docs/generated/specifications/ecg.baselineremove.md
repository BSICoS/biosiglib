# ECG baseline removal from fiducial isoelectric samples

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `ecg.baselineremove` |
| Module | `ecg` |
| Source JSON | [specs/ecg/baselineremove/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/ecg/baselineremove/spec.json) |

## Summary

Estimates a slowly varying ECG baseline from local means around fiducial positions and subtracts its spline interpolation.

The method samples an isoelectric ECG level around supplied fiducial positions, interpolates those levels across the complete signal, and returns both the detrended ECG and estimated baseline.

## Keywords

`ECG`, `baseline wander`, `isoelectric level`, `fiducial positions`, `spline interpolation`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `meyer_keiser_ecg_baseline_spline_1977` | original_method | Supports estimating ECG baseline noise from PR-segment samples and interpolating those estimates with cubic splines; the exact compatibility rules in this specification are not attributed to the paper. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `ecg` | real_vector | vector | a.u. | false | false | minimum_length=1 |
| `fiducial_positions` | real_vector | vector | sample | false | false | exclusive_minimum=0, minimum_length=1 |
| `offset` | integer_scalar | scalar | sample | false | false | minimum=0 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `window_size` | integer_scalar | 5 | sample | exclusive_minimum=0 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `ecg_detrended` | real_vector | vector | a.u. |
| `baseline` | real_vector | vector | a.u. |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `canonical_sample_grid` | Interpret ecg on the one-based integer sample grid 1 through N, where N = length(ecg). Public APIs may accept native indices only if they convert them to this grid before applying the remaining rules. |  |
| `adjusted_positions` | Subtract offset from every fiducial_positions value, then round each result to the nearest integer with exact half-way values rounded away from zero. Sort the rounded results, remove duplicates, and discard values outside the inclusive canonical range 1 through N, in that order. The remaining values are the valid fiducial positions. |  |
| `fiducial_ordering` | Raw fiducial_positions may be unordered, repeated, and fractional. Their order and multiplicity do not affect the result after adjusted-position sorting and deduplication. |  |
| `local_window` | Set radius = floor(window_size / 2). For each valid fiducial position p, use every ECG sample from max(1, p - radius) through min(N, p + radius), inclusive. The nominal span is therefore 2 * radius + 1: an odd window_size uses exactly window_size samples away from boundaries, while an even window_size uses window_size + 1 samples. Truncate the span at signal boundaries without padding. |  |
| `fiducial_levels` | At each valid fiducial position, compute the arithmetic mean of all ECG samples in its local_window. Pair the resulting finite level with that valid one-based position. |  |
| `spline_interpolation` | Interpolate the fiducial levels over every integer position 1 through N using the same polynomial piecewise model as MATLAB spline with same-size position and value vectors: two valid positions define a linear polynomial, three define a quadratic polynomial, and four or more define a cubic not-a-knot spline. Evaluate outside the first and last valid positions by polynomial extrapolation from the corresponding end piece. |  |
| `baseline` | Return the interpolated or extrapolated fiducial-level model evaluated at every canonical ECG sample position. baseline has length N and is aligned with ecg. |  |
| `ecg_detrended` | Return ecg - baseline element by element. ecg_detrended has length N and is aligned with ecg. |  |
| `comparison` | Each conformance output defines an absolute tolerance and uses zero relative tolerance. Absence of expected_warnings means that no warning is expected. |  |
| `error_categories` | Use invalid_type for non-real or non-numeric inputs, invalid_shape for non-vector ECG or fiducial inputs and non-scalar offset or window_size, invalid_value for empty or nonfinite vectors, nonpositive raw fiducial positions, negative or non-integer offset, or nonpositive or non-integer window_size, and insufficient_data when exactly one valid fiducial position remains. Language-specific exception and warning classes and message text are not normative. |  |

## Warnings

| id | condition | effect | aggregation |
| --- | --- | --- | --- |
| `no_valid_fiducial_positions` | No fiducial position remains after offset subtraction, half-away-from-zero rounding, sorting, deduplication, and range filtering. | Return ecg unchanged as ecg_detrended and an all-zero baseline of the same length. | Emit exactly once per call and identify fiducial_positions as the complete affected-id set. |

## Behavior

### Nan handling

NaN, positive infinity, negative infinity, and complex values in ecg or fiducial_positions are invalid. Successful outputs are finite for finite inputs.

### Empty input

Empty ecg and empty fiducial_positions inputs are invalid.

### Input orientation

Treat ecg and fiducial_positions as one-dimensional vectors regardless of MATLAB row or column orientation. Both outputs are one-dimensional ordered vectors aligned with ecg; a language may preserve the ECG vector orientation in its direct API.

### Insufficient data

If no valid fiducial position remains, emit no_valid_fiducial_positions and return the defined identity result. If exactly one valid position remains, raise insufficient_data because a spline baseline cannot be defined. Two or more valid positions are sufficient.

## Informative Notes

* Using PR-segment fiducials and cubic-spline interpolation is literature-backed; offset, local-window, boundary, and fallback details are empirical Biosigmat compatibility choices.
* The canonical sample-position grid is one-based even when a public implementation exposes native zero-based indices.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `ecg.baselineremove.boundary_truncated_local_means` | [conformance/ecg/baselineremove/boundary_truncated_local_means.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/baselineremove/boundary_truncated_local_means.json) |
| `ecg.baselineremove.even_window_linear_extrapolation` | [conformance/ecg/baselineremove/even_window_linear_extrapolation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/baselineremove/even_window_linear_extrapolation.json) |
| `ecg.baselineremove.fractional_positions_quadratic_extrapolation` | [conformance/ecg/baselineremove/fractional_positions_quadratic_extrapolation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/baselineremove/fractional_positions_quadratic_extrapolation.json) |
| `ecg.baselineremove.no_valid_fiducials_identity_warning` | [conformance/ecg/baselineremove/no_valid_fiducials_identity_warning.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/baselineremove/no_valid_fiducials_identity_warning.json) |
| `ecg.baselineremove.nonfinite_ecg_error` | [conformance/ecg/baselineremove/nonfinite_ecg_error.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/baselineremove/nonfinite_ecg_error.json) |
| `ecg.baselineremove.nonfinite_fiducial_error` | [conformance/ecg/baselineremove/nonfinite_fiducial_error.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/baselineremove/nonfinite_fiducial_error.json) |
| `ecg.baselineremove.not_a_knot_cubic_extrapolation` | [conformance/ecg/baselineremove/not_a_knot_cubic_extrapolation.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/baselineremove/not_a_knot_cubic_extrapolation.json) |
| `ecg.baselineremove.single_valid_fiducial_error` | [conformance/ecg/baselineremove/single_valid_fiducial_error.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/baselineremove/single_valid_fiducial_error.json) |
