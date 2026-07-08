# Low-pass differentiator filter design

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `tools.lpd_filter` |
| Module | `tools` |
| Source JSON | [specs/tools/lpd_filter/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/tools/lpd_filter/spec.json) |

## Summary

Designs a low-pass differentiating FIR filter and reports its linear-phase delay.

This tool defines low-pass differentiator FIR filter design used in ECG and pulse-processing pipelines. Explicit-order behavior is required for conformance. Automatic-order behavior is preferred when an implementation has a reliable FIR order estimator, but implementations without one may reject omitted order with an unsupported-configuration error while still conforming to the explicit-order profile.

## Keywords

`FIR`, `differentiator`, `low-pass`, `filter design`, `linear phase`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `lazaro_prv_sleep_apnea_ppg_2014` | original_method | Method provenance for the low-pass differentiator filter used in pulse-rate variability processing. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `sampling_frequency` | real_scalar | scalar | Hz | false | false | exclusive_minimum=0 |
| `stop_frequency` | real_scalar | scalar | Hz | false | false | exclusive_minimum=0 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `pass_frequency` | real_scalar | "stop_frequency - 0.2" | Hz | exclusive_minimum=0 |
| `order` | integer_scalar | "automatic" | sample | exclusive_minimum=0 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `filter_coefficients` | real_vector | vector | 1/s |
| `delay` | real_scalar | scalar | sample |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `pass_frequency` | If pass_frequency is omitted, set pass_frequency = stop_frequency - 0.2 Hz. |  |
| `frequency_constraints` | pass_frequency must be strictly less than stop_frequency, and stop_frequency must be strictly less than sampling_frequency / 2. |  |
| `normalized_frequencies` | Let wPass = pass_frequency / (sampling_frequency / 2) and wStop = stop_frequency / (sampling_frequency / 2). |  |
| `explicit_effective_order` | For explicit order, use effective_order = order + mod(order, 2), so odd explicit orders are rounded upward to the next even order. |  |
| `automatic_effective_order` | For omitted order, automatic-order implementations estimate estimated_order using firpmord([wPass, wStop], [1, 0], [0.01, 0.1]), then use effective_order = estimated_order + mod(estimated_order, 2). Implementations without a reliable automatic FIR order estimator may reject omitted order as an unsupported configuration. |  |
| `filter_coefficients` | filter_coefficients are the numerator coefficients of the canonical linear-phase low-pass differentiating FIR design equivalent to MATLAB fdesign.differentiator('n,fp,fst', effective_order, wPass, wStop) followed by design(..., 'firls'), scaled by sampling_frequency / (2*pi). |  |
| `delay` | delay is effective_order / 2 samples. |  |

## Behavior

### Nan handling

NaN, Inf, and -Inf scalar frequencies are invalid.

### Empty input

Empty scalar frequency inputs are invalid.

### Input orientation

All inputs are scalars. filter_coefficients is a one-dimensional ordered vector.

### Insufficient data

Explicit-order behavior is required for conformance. Omitted-order automatic behavior is preferred when a reliable FIR order estimator is available; otherwise omitted order may be rejected with an unsupported-configuration error.

## Informative Notes

* When pass_frequency is omitted, use stop_frequency - 0.2 Hz.
* Explicit-order behavior is required for conformance; automatic-order behavior is preferred when supported.
* When order is supplied, round it upward to the next even integer before design.
* When order is omitted, implementations may either estimate the automatic order as specified here or reject the configuration as unsupported.
* The filter is a linear-phase low-pass differentiator; delay is one half of the effective even order.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.lpd_filter.explicit_pass_frequency_order4_coefficients` | [conformance/tools/lpd_filter/explicit_pass_frequency_order4_coefficients.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/lpd_filter/explicit_pass_frequency_order4_coefficients.json) |
| `tools.lpd_filter.fs256_stop12_order4_coefficients` | [conformance/tools/lpd_filter/fs256_stop12_order4_coefficients.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/lpd_filter/fs256_stop12_order4_coefficients.json) |
| `tools.lpd_filter.invalid_pass_frequency_not_less_than_stop` | [conformance/tools/lpd_filter/invalid_pass_frequency_not_less_than_stop.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/lpd_filter/invalid_pass_frequency_not_less_than_stop.json) |
| `tools.lpd_filter.invalid_stop_frequency_at_nyquist` | [conformance/tools/lpd_filter/invalid_stop_frequency_at_nyquist.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/lpd_filter/invalid_stop_frequency_at_nyquist.json) |
