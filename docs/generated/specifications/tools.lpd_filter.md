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

This tool defines low-pass differentiator filter design used in ECG processing pipelines. The draft specifies scalar frequency validation, the default pass-band frequency, explicit-order filter design, and returned delay. Automatic order selection remains pending shared review because it depends on filter-design tooling that may vary across implementations.

## Keywords

`FIR`, `differentiator`, `low-pass`, `filter design`, `linear phase`

## Scientific References

No scientific references are listed in this specification.

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
| `effective_order` | For explicit order, use order + mod(order, 2), so odd explicit orders are rounded upward to the next even order. |  |
| `filter_coefficients` | filter_coefficients are the numerator coefficients of the canonical low-pass differentiating FIR design for the normalized pass and stop frequencies. |  |
| `delay` | delay is effective_order / 2 samples. |  |

## Behavior

### Nan handling

NaN, Inf, and -Inf scalar frequencies are invalid. NaN or Inf behavior inside automatic filter-design internals is outside this draft.

### Empty input

Empty scalar frequency inputs are invalid.

### Input orientation

All inputs are scalars. filter_coefficients is a one-dimensional ordered vector.

### Insufficient data

Automatic order selection is pending review for shared conformance. Explicit-order behavior is specified for positive scalar order values.

## Informative Notes

* MATLAB mapping: lpdfilter(fs, stopFreq, 'PassFreq', pass_frequency, 'Order', order).
* Canonical Biosigpy mapping should use tools.lpd_filter with sampling_frequency, stop_frequency, pass_frequency, and order.
* When pass_frequency is omitted, use stop_frequency - 0.2 Hz.
* When order is supplied, round it upward to the next even integer before design.
* Automatic order selection is not covered by a shared conformance case in this draft.
* The filter is a linear-phase differentiator; delay is one half of the effective even order.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `tools.lpd_filter.explicit_pass_frequency_order4_coefficients` | [conformance/tools/lpd_filter/explicit_pass_frequency_order4_coefficients.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/lpd_filter/explicit_pass_frequency_order4_coefficients.json) |
| `tools.lpd_filter.fs256_stop12_order4_coefficients` | [conformance/tools/lpd_filter/fs256_stop12_order4_coefficients.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/lpd_filter/fs256_stop12_order4_coefficients.json) |
| `tools.lpd_filter.invalid_pass_frequency_not_less_than_stop` | [conformance/tools/lpd_filter/invalid_pass_frequency_not_less_than_stop.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/lpd_filter/invalid_pass_frequency_not_less_than_stop.json) |
| `tools.lpd_filter.invalid_stop_frequency_at_nyquist` | [conformance/tools/lpd_filter/invalid_stop_frequency_at_nyquist.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/tools/lpd_filter/invalid_stop_frequency_at_nyquist.json) |
