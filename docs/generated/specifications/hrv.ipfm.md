# Integral pulse frequency modulation heart-timing reconstruction

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `hrv.ipfm` |
| Module | `hrv` |
| Source JSON | [specs/hrv/ipfm/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/hrv/ipfm/spec.json) |

## Summary

Estimates uniformly sampled instantaneous heart rate and an optional TVIPFM autonomic modulating signal from event times.

The canonical contract reconstructs cumulative beat count with an edge-stabilized high-order B-spline, differentiates it to obtain instantaneous heart rate, and optionally applies the time-varying-threshold IPFM correction. It covers sampled numerical outputs only; language-specific unevaluated spline objects are outside shared conformance.

## Keywords

`heart timing signal`, `instantaneous heart rate`, `IPFM`, `TVIPFM`, `B-spline interpolation`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `mateo_laguna_ipfm_2000` | original_method | Original heart-timing/IPFM formulation and explicit analysis of fourteenth-order spline interpolation. The paper does not prescribe the canonical 10/8 edge constants. |
| `mateo_laguna_ectopic_ht_2003` | validation | Validates heart-timing analysis in the presence of ectopic beats and uses fourteenth-order spline interpolation after incorrect values are removed. |
| `bailon_tvipfm_2011` | original_method | Defines TVIPFM Approach A, including the time-varying mean-rate correction and the 0.03 Hz separation used here. |
| `bailon_tvipfm_2011` | validation | Validates the TVIPFM correction during exercise stress testing; it does not prescribe Biosigmat's exact fourth-order Butterworth and forward-backward realization. |
| `sornmo_bailon_laguna_hrv_review_2024` | scientific_context | Provides the later derivation and review context for the TVIPFM correction under a time-varying mean heart rate. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `tn` | real_vector | vector | s | false | false | minimum_length=2 |
| `fs` | real_scalar | scalar | Hz | false | false | exclusive_minimum=0 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `spline_order` | integer_scalar | 14 | 1 | minimum=2 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `ihr` | real_vector | vector | Hz |
| `m` | real_vector | vector | 1 |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `canonical_api` | The language-independent API requires tn and fs and returns numerical values evaluated on the canonical uniform grid. ihr is always available. m is an optional output computed only when requested. Returning an unevaluated spline representation, including the MATLAB ipfm(tn) convenience mode, is outside this contract. |  |
| `tn` | tn is a finite real event-time vector containing at least two timestamps in seconds. It must be strictly increasing, and implementations must not sort or deduplicate it implicitly. |  |
| `boundary_extension` | Let d = diff(tn) and q = min(8, length(d)). Prepend 10 virtual events separated by median(d[0:q]) and append 10 virtual events separated by median(d[length(d)-q:length(d)]). The resulting extended event sequence tau remains strictly increasing and contains N = length(tn) + 20 sites. The virtual events stabilize interpolation but do not enlarge the valid output domain. |  |
| `spline_order` | spline_order is an integer satisfying 2 <= spline_order <= N, where N is the number of extended event sites. The default is 14. Order k means polynomial degree k - 1; an implementation must reject an order above N instead of silently reducing it. |  |
| `aptknt_knot_sequence` | For spline order k and strictly increasing extended sites tau_1 through tau_N, form interior knots xi_i = mean(tau_{i+1}, ..., tau_{i+k-1}) for i = 1, ..., N - k. The complete knot vector is tau_1 repeated k times, followed by xi_1 through xi_{N-k}, followed by tau_N repeated k times. This is the MATLAB aptknt construction for these sites and must be used instead of a language-specific default knot placement. |  |
| `heart_timing_spline` | Construct the unique order-k B-spline on the canonical knot vector that interpolates cumulative beat indices 1 through N at tau_1 through tau_N. Differentiate this spline once with respect to time. The derivative is instantaneous rate because the interpolated dependent variable is cumulative beat count and event time is measured in seconds. |  |
| `sampling_grid` | The output grid contains t_j = tn[0] + j / fs for every non-negative integer j satisfying t_j <= tn[-1]. Construct it from integer indices and remove any floating-point overshoot beyond tn[-1]. Do not append an irregular endpoint or alter fs to force tn[-1] onto the grid. Never evaluate outside the original interval [tn[0], tn[-1]], and disable spline extrapolation where the implementation API permits it. |  |
| `ihr` | Evaluate the differentiated heart-timing spline at every canonical grid point. ihr is the resulting unfiltered instantaneous heart-rate vector in hertz and has the same length as the grid. Every value must be finite and strictly positive. |  |
| `tvipfm_filter` | When m is requested, design a fourth-order digital Butterworth low-pass filter with cutoff 0.03 Hz, equivalently normalized cutoff 0.06 / fs relative to Nyquist. Apply it forward and backward to ihr for zero phase. Filter family, order, cutoff, and zero-phase application are fixed and are not public parameters. |  |
| `forward_backward_filter_convention` | Reproduce the MATLAB filtfilt padding convention for the five-coefficient Butterworth numerator and denominator: extend each end by exactly 12 samples, use odd-symmetry linear reflection about each endpoint, and use steady-state initial conditions scaled by the endpoint of the extended signal on each pass. SciPy implementations must use method = pad, padtype = odd, and padlen = 12 explicitly. |  |
| `m` | Let mean_ihr be the forward-backward low-pass result and hrv = ihr - mean_ihr. The TVIPFM Approach A modulating signal is m = hrv / mean_ihr. m is dimensionless and has the same length as ihr. The division corrects the scaling caused by a time-varying threshold or mean heart rate; it must not be described as generic detrending alone. | m(t) = \frac{ihr(t) - mean\_ihr(t)}{mean\_ihr(t)} |
| `numerical_validity` | Do not clamp ihr or mean_ihr, take absolute values, or replace a non-positive denominator with an epsilon. If spline evaluation produces any non-finite or non-positive ihr, or filtering produces any non-finite or non-positive mean_ihr, raise invalid_numerical_result. |  |
| `error_categories` | Use invalid_type for non-numeric inputs, invalid_shape for non-vector tn or non-scalar fs/spline_order, invalid_value for non-finite values, non-increasing tn, fs outside the requested-output domain, or spline_order outside its valid range, insufficient_data when tn has fewer than two events or requested m has fewer than 13 grid samples, and invalid_numerical_result for the defensive numerical failures defined above. Language-specific exception classes and message text are not normative. |  |

## Behavior

### Nan handling

NaN, Inf, and -Inf are invalid in tn and fs. NaN and infinite output values are never conformant numerical results and raise invalid_numerical_result.

### Empty input

Empty tn is insufficient_data. An omitted fs is outside the canonical sampled API.

### Input orientation

MATLAB row and column tn inputs represent the same sequence, and canonical MATLAB numerical outputs are column vectors. Python accepts and returns one-dimensional arrays.

### Insufficient data

At least two event times are required. Computing only ihr requires fs > 0 and does not invoke the TVIPFM filter, so 12 or fewer grid samples remain valid. Requesting m additionally requires fs > 0.06 Hz and at least 13 canonical grid samples; 12 or fewer grid samples raise insufficient_data.

## Informative Notes

* The default order-14 spline is supported by the Mateo-Laguna heart-timing literature.
* The 10 virtual events per side and the use of up to 8 boundary intervals are empirical stabilization constants inherited from Biosigmat, not physiological or clinically validated parameters.
* The 0.03 Hz TVIPFM separation is literature-backed, while the exact fourth-order Butterworth realization and forward-backward edge convention are fixed numerical compatibility choices inherited from Biosigmat.
* Implementations must not expose the virtual-event count, boundary-median width, trend cutoff, filter order, filter family, or forward-backward padding length as canonical public parameters.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `hrv.ipfm.constant_rate` | [conformance/hrv/ipfm/constant_rate.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/ipfm/constant_rate.json) |
| `hrv.ipfm.insufficient_modulating_signal_samples` | [conformance/hrv/ipfm/insufficient_modulating_signal_samples.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/ipfm/insufficient_modulating_signal_samples.json) |
| `hrv.ipfm.invalid_numerical_rate` | [conformance/hrv/ipfm/invalid_numerical_rate.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/ipfm/invalid_numerical_rate.json) |
| `hrv.ipfm.medicom_mtd_tvipfm` | [conformance/hrv/ipfm/medicom_mtd_tvipfm.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/ipfm/medicom_mtd_tvipfm.json) |
| `hrv.ipfm.non_aligned_sampling_grid` | [conformance/hrv/ipfm/non_aligned_sampling_grid.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/ipfm/non_aligned_sampling_grid.json) |
| `hrv.ipfm.spline_order_exceeds_sites` | [conformance/hrv/ipfm/spline_order_exceeds_sites.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/ipfm/spline_order_exceeds_sites.json) |
