# Respiration-related HRV decomposition by orthogonal subspace projection

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `hrv.osp` |
| Module | `hrv` |
| Source JSON | [specs/hrv/osp/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/hrv/osp/spec.json) |

## Summary

Separates a uniformly sampled HRV modulating signal into a component linearly related to respiration and an orthogonal residual.

The canonical contract preserves the mature Biosigmat OSP workflow: it estimates a dominant respiratory frequency from a supplied spectrum, uses approximately two respiratory cycles to set an adaptive delayed-respiration model order, and projects the aligned HRV modulation onto that subspace.

## Keywords

`heart rate variability`, `respiration`, `orthogonal subspace projection`, `cardiorespiratory interaction`, `linear decomposition`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `varon_respiratory_hrv_osp_2017` | method_extension | Applies OSP to separate respiration-related and residual HRV dynamics and compares delayed-respiration and wavelet respiratory subspaces. |
| `varon_unconstrained_hrv_osp_2019` | original_method | Defines and validates the HRV analysis approach based on removing linear respiratory influences with OSP. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `m` | real_vector | vector | 1 | true | false | None |
| `resp` | real_vector | vector | a.u. | true | false | None |
| `resp_pxx` | real_vector | vector | a.u.^2/Hz | false | false | minimum_length=2 |
| `f` | real_vector | vector | Hz | false | false | minimum_length=2 |
| `fs` | real_scalar | scalar | Hz | false | false | exclusive_minimum=0 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `min_resp_frequency` | real_scalar | 0.1 | Hz | exclusive_minimum=0 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `m_resp` | real_vector | vector | 1 |
| `m_unrelated` | real_vector | vector | 1 |
| `delay` | integer_scalar | scalar | sample |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `canonical_api` | The language-independent API requires aligned HRV modulation m, respiration resp, respiratory PSD resp_pxx, its frequency vector f, and sampling frequency fs. It returns the respiration-related component m_resp, residual m_unrelated, and adaptive model order delay. Spectrum estimation itself is outside this contract. |  |
| `aligned_signals` | m and resp are real sample sequences on the same uniform fs grid and with the same time origin. After the approved empty and NaN early returns, they must have equal lengths. Implementations must not resample, shift, detrend, normalize, or otherwise preprocess either sequence implicitly. |  |
| `respiratory_spectrum` | resp_pxx and f must have the same length L >= 2. Every resp_pxx value must be nonnegative. f must be strictly increasing, but the contract does not require a zero first frequency, uniform spacing, or a particular relation between its last value and fs. |  |
| `occupied_power_integration` | Reproduce the current 90% occupied-power calculation in double precision. Let delta_bar = (f[L-1] - f[0]) / (L - 1). If f[0] = 0, use rectangle widths w[i] = f[i+1] - f[i] for i = 0, ..., L-2 and w[L-1] = delta_bar. Otherwise use w[0] = delta_bar and w[i] = f[i] - f[i-1] for i = 1, ..., L-1. Let power[i] = resp_pxx[i] * w[i], cumulative powers c[0] = 0 and c[i+1] = c[i] + power[i], and cumulative-frequency locations b[0] = f[0], b[i] = (f[i-1] + f[i]) / 2 for i = 1, ..., L-1, and b[L] = f[L-1]. For each threshold T equal to 5% or 95% of c[L], select the first cumulative index j for which T <= c[j], replacing j = 0 by j = 1, and linearly interpolate frequency between (c[j-1], b[j-1]) and (c[j], b[j]). If total power is zero, this interpolation divides zero by zero and both limits are NaN. |  |
| `occupied_band_samples` | Select every spectral sample whose frequency is greater than or equal to the interpolated lower occupied limit and less than or equal to the upper limit. Both boundaries are inclusive. If no spectral sample is selected, including when zero total power produced NaN limits, fall back to the complete resp_pxx and f vectors. |  |
| `candidate_peaks` | If the selected spectrum has fewer than three samples, skip peak detection and choose its first maximum. Otherwise detect local maxima in frequency order. The first and last selected samples are not peaks. A flat peak contributes only its lowest-index sample on the rising edge. If no peak is found, choose the first maximum of the selected spectrum. With one to three peaks, choose the peak with greatest power; equal-power ties select the first, lowest-frequency peak. With more than three peaks, choose the lowest-frequency peak regardless of power. |  |
| `dominant_frequency` | Let the frequency selected by the peak-dependent rule be f_selected. Set dominant_frequency = max(f_selected, min_resp_frequency). The entire selection rule and the default 0.1 Hz floor are empirical Biosigmat heuristics and must not be replaced by a simpler global maximum or attributed to the cited OSP literature. |  |
| `delay` | Compute delay = max(round_half_away_from_zero(2 * fs / dominant_frequency), 1). All operands are positive, so an exact fractional tie ending in .5 rounds upward. delay is both the number of delayed-respiration regressors and the first one-based sample index represented by the returned components. | q = \max\left(\operatorname{round}_{\mathrm{half\ away}}\left(\frac{2 f_s}{f_{resp}}\right), 1\right) |
| `alignment` | For N >= delay, discard the first delay - 1 samples. Both returned components correspond to m[delay-1:N] with zero-based indexing, equivalently m(delay:end) in MATLAB, and have length N - delay + 1. |  |
| `respiratory_subspace` | For q = delay and N >= q, construct V with N - q + 1 rows and q columns using V[r,c] = resp[r+c] for zero-based r = 0, ..., N-q and c = 0, ..., q-1. Thus each row is one q-sample sliding respiration window and the first row spans resp[0:q]. |  |
| `gram_pseudoinverse` | Form G = transpose(V) * V and compute its singular-value decomposition G = U * diag(s) * transpose(W), with singular values in descending order. Let sigma_max = s[0] and tol = max(rows(G), columns(G)) * eps(sigma_max), where eps(x) is the distance from finite IEEE 754 binary64 x to the next larger representable value. Define s_plus[i] = 1 / s[i] only when s[i] is strictly greater than tol and zero otherwise, then G_plus = W * diag(s_plus) * transpose(U). Apply this threshold to G, not to V, and do not use a language-specific default pseudoinverse threshold. Rank-deficient finite subspaces are valid. |  |
| `decomposition` | Form P = V * G_plus * transpose(V), delayed_m = m[delay-1:N], m_resp = P * delayed_m, and m_unrelated = delayed_m - m_resp. This separates the part represented by the delayed-respiration subspace from the remaining dynamics. | m_{resp} = V(V^\mathsf{T}V)^+V^\mathsf{T}m_{delayed}, \qquad m_{unrelated} = m_{delayed} - m_{resp} |
| `reconstruction` | For every finite processed case, m_resp + m_unrelated reconstructs delayed_m. Shared numerical comparisons of either component and of reconstruction use absolute tolerance 1e-10 and zero relative tolerance. delay is compared exactly. |  |
| `residual_orthogonality` | On the analytical orthogonality case, verify norm(transpose(V) * m_unrelated) / max(norm(transpose(V) * delayed_m), eps) < 1e-8 using the Euclidean norm and eps = 2.220446049250313e-16. This external check is deliberately distinct from the internal Gram pseudoinverse tolerance because forming transpose(V) * V squares the subspace condition number. |  |
| `early_return_order` | After validating the common argument types, shapes, spectrum, fs, and parameter, return all three outputs empty if either m or resp is empty. Next, return all three outputs empty if either signal contains any NaN. These two returns occur before the m/resp length-equality check. After them, reject any infinite signal value explicitly and require equal signal lengths. |  |
| `error_categories` | Use invalid_type for non-numeric inputs, invalid_shape for non-vector signals or spectra and non-scalar fs/min_resp_frequency, and invalid_value for infinite m/resp values, negative or non-finite resp_pxx, non-finite or non-increasing f, unequal spectrum lengths, non-positive fs/min_resp_frequency, or unequal non-empty finite signal lengths. Language-specific exception classes and message text are not normative. |  |

## Behavior

### Nan handling

NaN is permitted only in m and resp as a compatibility marker: if either signal contains NaN, all three outputs are empty. NaN in resp_pxx, f, fs, or min_resp_frequency is invalid. Inf and -Inf are invalid in every input and parameter; in particular, infinite m or resp values raise invalid_value instead of entering spectral or linear-algebra processing.

### Empty input

If either m or resp is empty, return empty m_resp, empty m_unrelated, and empty delay, even when the other signal is non-empty. resp_pxx, f, fs, and min_resp_frequency must still satisfy their common argument constraints.

### Input orientation

MATLAB row and column input vectors represent the same canonical sequences, and its processed vector outputs are columns. Python accepts and returns one-dimensional arrays. Empty-output orientation is implementation-specific.

### Insufficient data

If non-empty, NaN-free, finite, equal-length signals have N < delay, return scalar NaN for m_resp and m_unrelated while preserving the computed integer delay. Do not replace these scalar NaNs with empty vectors. N >= delay, including equality, is processable.

## Informative Notes

* Orthogonal subspace projection supports separating linear respiratory influences from the remaining HRV dynamics; nonlinear respiratory influences may remain in the residual.
* The peak-count-dependent dominant-frequency rule, the 90% occupied-power band, and the default 0.1 Hz floor are empirical heuristics inherited from Biosigmat. The cited OSP publications do not establish them as optimal or generally required.
* The public delay output is retained for compatibility, although it is primarily the adaptive number of respiratory regressors and also fixes output alignment.
* The explicit Gram-matrix pseudoinverse threshold is a cross-language numerical compatibility rule, not a physiological tolerance.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `hrv.osp.analytical_decomposition_orthogonality` | [conformance/hrv/osp/analytical_decomposition_orthogonality.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/analytical_decomposition_orthogonality.json) |
| `hrv.osp.empty_signal_early_return` | [conformance/hrv/osp/empty_signal_early_return.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/empty_signal_early_return.json) |
| `hrv.osp.greatest_peak_tie` | [conformance/hrv/osp/greatest_peak_tie.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/greatest_peak_tie.json) |
| `hrv.osp.halfway_rounding_alignment` | [conformance/hrv/osp/halfway_rounding_alignment.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/halfway_rounding_alignment.json) |
| `hrv.osp.infinite_signal_error` | [conformance/hrv/osp/infinite_signal_error.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/infinite_signal_error.json) |
| `hrv.osp.minimum_frequency_override` | [conformance/hrv/osp/minimum_frequency_override.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/minimum_frequency_override.json) |
| `hrv.osp.more_than_three_peaks_lowest_frequency` | [conformance/hrv/osp/more_than_three_peaks_lowest_frequency.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/more_than_three_peaks_lowest_frequency.json) |
| `hrv.osp.nan_signal_early_return` | [conformance/hrv/osp/nan_signal_early_return.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/nan_signal_early_return.json) |
| `hrv.osp.near_rank_pseudoinverse_threshold` | [conformance/hrv/osp/near_rank_pseudoinverse_threshold.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/near_rank_pseudoinverse_threshold.json) |
| `hrv.osp.occupied_band_boundary_inclusive` | [conformance/hrv/osp/occupied_band_boundary_inclusive.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/occupied_band_boundary_inclusive.json) |
| `hrv.osp.short_signal_scalar_nan` | [conformance/hrv/osp/short_signal_scalar_nan.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/short_signal_scalar_nan.json) |
| `hrv.osp.zero_spectrum_no_peak_fallback` | [conformance/hrv/osp/zero_spectrum_no_peak_fallback.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/osp/zero_spectrum_no_peak_fallback.json) |
