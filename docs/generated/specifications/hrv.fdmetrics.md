# Frequency-domain HRV metrics

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `hrv.fdmetrics` |
| Module | `hrv` |
| Source JSON | [specs/hrv/fdmetrics/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/hrv/fdmetrics/spec.json) |

## Summary

Integrates conventional LF and HF powers or respiration-separated OSP powers on an authoritative frequency grid.

The shared contract preserves the two mature Biosigmat fdmetrics call forms while making band selection, warning aggregation, missing-data behavior, and the robust respiration-separated ratio reproducible across languages.

## Keywords

`heart rate variability`, `frequency domain`, `low frequency`, `high frequency`, `orthogonal subspace projection`, `cardiorespiratory interaction`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `task_force_hrv_1996` | metric_definition | Provides the conventional LF and HF frequency bands and normalized frequency-domain HRV measures. |
| `varon_unconstrained_hrv_osp_2019` | method_extension | Supports frequency-domain analysis after separating respiration-related and unrelated HRV modulation with OSP. |
| `liu_robust_cardiorespiratory_index_2019` | metric_definition | Defines the robust normalization of respiration-unrelated LF power by total respiration-related and unrelated power. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `pxx` | real_vector | vector | caller-defined power/Hz | true | false | minimum=0, minimum_length=1 |
| `related_pxx` | real_vector | vector | 1/Hz | true | false | minimum=0, minimum_length=1 |
| `unrelated_pxx` | real_vector | vector | 1/Hz | true | false | minimum=0, minimum_length=1 |
| `f` | real_vector | vector | Hz | false | false | minimum=0, minimum_length=1 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `limit_hf` | boolean | true |  | None |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `hf` | real_scalar | scalar | caller-defined power |
| `lf` | real_scalar | scalar | caller-defined power |
| `lfn` | real_scalar | scalar | 1 |
| `lfhf` | real_scalar | scalar | 1 |
| `urlf` | real_scalar | scalar | 1 |
| `re` | real_scalar | scalar | 1 |
| `r` | real_scalar | scalar | 1 |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `canonical_api` | One public operation has two mutually exclusive call forms. Single-spectrum mode takes pxx and f, with optional boolean limit_hf defaulting to true, and returns hf, lf, lfn, and lfhf. Separated OSP mode takes related_pxx, unrelated_pxx, and f and returns urlf, re, and r. The second mode has no limit_hf option. Implementations must reject missing, mixed, or ambiguous mode-specific input sets. Language bindings may preserve mature positional overloads: a third logical scalar selects the single-spectrum option, while a third numeric frequency vector selects separated mode. |  |
| `frequency_grid` | f is authoritative and must be a nonempty real vector of finite, nonnegative, strictly increasing frequencies. Do not resample, interpolate, or insert samples at 0.04, 0.15, or 0.4 Hz. Every selected PSD must have exactly the same number of samples as f. |  |
| `psd_validation` | Every selected PSD must be a nonempty real vector. Negative and infinite values are invalid. A PSD containing any NaN follows the mode-wide NaN return instead of raising an error. In single-spectrum mode the input unit is deliberately caller-defined, for example ms^2/Hz or 1/Hz. In separated mode related_pxx and unrelated_pxx are PSDs of the dimensionless respiration-related and respiration-unrelated modulation components and have unit 1/Hz. |  |
| `trapezoidal_integration` | For inclusive zero-based indices a through b, integrate only the original selected samples as sum from i = a to b - 1 of (f[i+1] - f[i]) * (p[i] + p[i+1]) / 2. A selection containing exactly one sample therefore integrates to zero. |  |
| `band_indices` | Let i_lf_start be the first index with f >= 0.04 and i_lf_end be the first index with f >= 0.15. The LF selection includes both indices. The HF selection starts at i_lf_end. When limit_hf is true and at least one sample has f >= 0.4, its end is the first such index; when no sample reaches 0.4, its end is the final index. When limit_hf is false, its end is always the final index. The boundary sample at i_lf_end belongs to both LF and HF trapezoidal selections, but no finite interval is counted twice. |  |
| `single_powers` | In single-spectrum mode, lf is the trapezoidal integral of pxx from i_lf_start through i_lf_end and hf is the integral from i_lf_end through the selected HF end. The powers inherit the integrated caller unit. There is no magnitude rejection for lf or hf; in particular, powers greater than 15000 remain valid. |  |
| `single_ratios` | When both required powers are strictly positive, lfn = lf / (lf + hf) and lfhf = lf / hf. Both ratios are dimensionless. |  |
| `separated_powers` | In separated OSP mode, urlf is the LF-band trapezoidal integral of unrelated_pxx from i_lf_start through i_lf_end. re is the trapezoidal integral of related_pxx over the complete supplied frequency grid, independent of LF/HF coverage. Apply the retained empirical re rejection only to re: if its finite raw value is greater than 0.05, return re as NaN. Apply the retained empirical urlf rejection only to urlf: if its finite raw value is greater than 0.003, return urlf as NaN. Either rejected component makes r NaN but does not change the other component. |  |
| `robust_ratio` | When the unrejected raw urlf is strictly positive and re is nonnegative, r = urlf / (re + urlf). Exact re = 0 is valid and gives r = 1. The ratio is dimensionless and bounded from 0 through 1 for valid powers. |  |
| `vlf_diagnostic` | Evaluate the VLF diagnostic independently for pxx in single-spectrum mode and for related_pxx and unrelated_pxx in separated mode. If f has no sample below 0.04 Hz, emit no VLF warning. Otherwise, when a boundary index i_vlf equal to the first f >= 0.04 exists, integrate P_vlf from the first sample through i_vlf and P_rest from i_vlf through the final sample. Emit excessive_vlf_power for a spectrum when P_vlf / P_rest > 0.05. If P_rest = 0 and P_vlf > 0, the condition is true; if both are zero, it is false. If no i_vlf exists, the diagnostic is not evaluable and emits no warning. |  |
| `warning_aggregation` | Emit at most one warning per warning id and call. excessive_vlf_power aggregates every offending selected PSD using affected input ids pxx, related_pxx, or unrelated_pxx. zero_required_power aggregates every exactly zero required band power using affected output ids lf and hf in single-spectrum mode or urlf in separated mode. A call may emit both warning ids because they represent distinct conditions. Warning ordering and message text are not normative; the canonical id and complete affected-id set are normative. |  |
| `nan_mode_return` | If any selected PSD contains NaN, return NaN for every output of the selected mode and emit neither excessive_vlf_power nor zero_required_power. The unselected mode's outputs are not part of the call. |  |
| `insufficient_band_return` | If the required LF or HF index selection does not exist, return NaN for every output of the selected mode without a zero-power warning. Partial nominal coverage is otherwise valid: the default HF selection may end below 0.4 at the last supplied sample. |  |
| `zero_power_return` | After successful selection and integration, exact zero lf or hf makes all four single-spectrum outputs NaN and emits zero_required_power identifying every zero band. Exact zero urlf makes all three separated outputs NaN and emits zero_required_power identifying urlf. This includes a one-sample band whose trapezoidal integral is zero. Exact zero re is not an error and does not emit a warning when urlf is positive. The VLF diagnostic remains independent and may also warn on the same call. |  |
| `comparison` | Each conformance case defines its absolute tolerance and uses zero relative tolerance; ordinary subunit powers and ratios use 1e-12, while large caller-unit powers use a scale-appropriate absolute tolerance. NaN outputs compare equal only when the conformance case enables nan_equal. Expected warnings compare as an unordered set of canonical warning ids, and each affected_ids value compares as an unordered complete set. Absence of expected_warnings means that no warning is expected. |  |
| `error_categories` | Use invalid_type for non-numeric PSD or frequency inputs and for a non-boolean limit_hf; invalid_shape for non-vector PSD/f inputs or a non-scalar option; and invalid_value for empty, infinite, or negative PSD values, empty, NaN, infinite, negative, or non-increasing frequencies, unequal PSD/f lengths, or invalid combinations of mode-specific inputs. Language-specific exception classes, warning classes, and message text are not normative. |  |

## Warnings

| id | condition | effect | aggregation |
| --- | --- | --- | --- |
| `excessive_vlf_power` | At least one selected PSD satisfies the normative VLF-to-rest power condition. | Diagnostic only; returned values and validation behavior are unchanged. | Emit once and identify the complete set of offending PSD input ids. |
| `zero_required_power` | At least one successfully selected required band power is exactly zero. | Return NaN for every output of the selected mode. | Emit once and identify the complete set of zero required power output ids. |

## Behavior

### Nan handling

NaN is permitted only as a PSD missing-data marker. If any selected PSD contains NaN, all outputs of that mode are NaN and no warning is emitted. NaN in f is invalid.

### Empty input

Every selected PSD and f must be nonempty; empty vectors are invalid rather than missing-data returns.

### Input orientation

MATLAB row and column input vectors represent the same canonical sequences. Python accepts one-dimensional vectors. Every returned metric is scalar.

### Insufficient data

Missing required band indices produce a mode-wide NaN return. A present one-sample required band is instead an exact zero power, produces the zero_required_power warning, and also causes the mode-wide NaN return. Partial HF coverage below 0.4 Hz remains processable.

## Informative Notes

* Conventional LF and HF labels describe frequency bands and do not by themselves identify unique autonomic mechanisms.
* Band edges are selected from the supplied frequency samples without interpolation, so coarse or irregular grids can materially affect the result.
* The VLF diagnostic and the retained OSP rejection thresholds are empirical compatibility rules rather than universal physiological validity criteria.
* The former single-spectrum 15000 power rejection is intentionally absent because its meaning depended on caller units.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `hrv.fdmetrics.default_bands_irregular_grid` | [conformance/hrv/fdmetrics/default_bands_irregular_grid.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/default_bands_irregular_grid.json) |
| `hrv.fdmetrics.insufficient_band_all_nan` | [conformance/hrv/fdmetrics/insufficient_band_all_nan.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/insufficient_band_all_nan.json) |
| `hrv.fdmetrics.large_single_spectrum_retained` | [conformance/hrv/fdmetrics/large_single_spectrum_retained.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/large_single_spectrum_retained.json) |
| `hrv.fdmetrics.nan_separated_all_nan_no_warning` | [conformance/hrv/fdmetrics/nan_separated_all_nan_no_warning.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/nan_separated_all_nan_no_warning.json) |
| `hrv.fdmetrics.one_sample_hf_zero` | [conformance/hrv/fdmetrics/one_sample_hf_zero.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/one_sample_hf_zero.json) |
| `hrv.fdmetrics.partial_default_hf_coverage` | [conformance/hrv/fdmetrics/partial_default_hf_coverage.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/partial_default_hf_coverage.json) |
| `hrv.fdmetrics.related_power_threshold_rejection` | [conformance/hrv/fdmetrics/related_power_threshold_rejection.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/related_power_threshold_rejection.json) |
| `hrv.fdmetrics.separated_vlf_warning` | [conformance/hrv/fdmetrics/separated_vlf_warning.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/separated_vlf_warning.json) |
| `hrv.fdmetrics.single_vlf_warning_preserves_metrics` | [conformance/hrv/fdmetrics/single_vlf_warning_preserves_metrics.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/single_vlf_warning_preserves_metrics.json) |
| `hrv.fdmetrics.unlimited_hf_irregular_grid` | [conformance/hrv/fdmetrics/unlimited_hf_irregular_grid.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/unlimited_hf_irregular_grid.json) |
| `hrv.fdmetrics.unrelated_power_threshold_rejection` | [conformance/hrv/fdmetrics/unrelated_power_threshold_rejection.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/unrelated_power_threshold_rejection.json) |
| `hrv.fdmetrics.vlf_and_zero_warnings` | [conformance/hrv/fdmetrics/vlf_and_zero_warnings.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/vlf_and_zero_warnings.json) |
| `hrv.fdmetrics.zero_related_power_robust_ratio` | [conformance/hrv/fdmetrics/zero_related_power_robust_ratio.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/zero_related_power_robust_ratio.json) |
| `hrv.fdmetrics.zero_single_powers_aggregated` | [conformance/hrv/fdmetrics/zero_single_powers_aggregated.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/zero_single_powers_aggregated.json) |
| `hrv.fdmetrics.zero_urlf_atomic` | [conformance/hrv/fdmetrics/zero_urlf_atomic.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/hrv/fdmetrics/zero_urlf_atomic.json) |
