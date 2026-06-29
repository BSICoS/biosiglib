# Pan-Tompkins-style ECG R-wave detection

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `ecg.pantompkins` |
| Module | `ecg` |
| Algorithm status | stable |
| Specification status | draft |
| Source JSON | [specs/ecg/pantompkins/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/ecg/pantompkins/spec.json) |

## Summary

Detects ordered R-wave occurrence times from a sampled ECG signal and exposes intermediate processing signals for plotting and debugging.

This Pan-Tompkins-style detector is implemented in Biosigmat using bandpass filtering, derivative filtering, squaring, moving-window integration, peak detection, and peak refinement. The current implementation follows the Pan-Tompkins processing style but is not a byte-for-byte reproduction of the original paper.

## Keywords

`ECG`, `Pan-Tompkins`, `QRS detection`, `R waves`, `debugging`, `intermediate signals`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `pan_tompkins_1985` | original_method | Algorithm origin for the Pan-Tompkins-style processing chain. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `ecg` | real_vector | vector | a.u. | true | false | None |
| `sampling_frequency` | real_scalar | scalar | Hz | false | false | exclusive_minimum=0 |

## Parameters

| id | data_type | default | unit | constraints |
| --- | --- | --- | --- | --- |
| `bandpass_frequency` | real_vector | [5, 12] | Hz | minimum_length=2 |
| `integration_window_size` | real_scalar | 0.15 | s | exclusive_minimum=0 |
| `minimum_peak_distance` | real_scalar | 0.5 | s | exclusive_minimum=0 |
| `snap_to_peak_window_size` | real_scalar | 20 | sample | exclusive_minimum=0 |

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `r_wave_times` | real_vector | vector | s |
| `ecg_filtered` | real_vector | vector | a.u. |
| `decg` | real_vector | vector | a.u. |
| `decg_envelope` | real_vector | vector | a.u.^2 |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `detection_chain` | Apply bandpass filtering, derivative filtering, squaring, moving-window integration, peak detection, and peak refinement to the ECG signal. |  |
| `r_wave_times` | Detected ECG R-wave occurrence times in seconds, sorted in ascending order. |  |
| `ecg_filtered` | Bandpass-filtered ECG signal, represented as a one-dimensional vector with the same canonical sample order and length as the input ECG. |  |
| `decg` | Derivative-filtered ECG signal, represented as a one-dimensional vector with the same canonical sample order and length as the input ECG. |  |
| `decg_envelope` | Squared and moving-window integrated detection envelope, represented as a one-dimensional vector with the same canonical sample order and length as the input ECG. |  |

## Behavior

### Nan handling

NaN samples in the ECG signal are preserved through filtering as the implementation permits. Detections should not be produced inside NaN-corrupted regions in a future shared NaN case; the case in this draft contains no NaN samples.

### Empty input

Empty ECG input is invalid; the exact failure mechanism is implementation-specific.

### Input orientation

Treat ECG input as a one-dimensional vector regardless of row or column orientation. All vector outputs are conceptually one-dimensional ordered vectors.

### Insufficient data

Unspecified in this draft.

## Informative Notes

* The primary detection target is the ECG R wave.
* Intermediate outputs are part of the public contract because they are used for plotting and debugging detections.
* Exact cross-language numerical equality of intermediate signals is not required by the first positive conformance case.
* Python should expose r_wave_times, ecg_filtered, decg, and decg_envelope using the canonical names.
* Insufficient-data behavior remains unspecified in this draft.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `ecg.pantompkins.invalid_ecg_matrix` | [conformance/ecg/pantompkins/invalid_ecg_matrix.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/pantompkins/invalid_ecg_matrix.json) |
| `ecg.pantompkins.invalid_ecg_non_numeric` | [conformance/ecg/pantompkins/invalid_ecg_non_numeric.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/pantompkins/invalid_ecg_non_numeric.json) |
| `ecg.pantompkins.invalid_sampling_frequency_non_numeric` | [conformance/ecg/pantompkins/invalid_sampling_frequency_non_numeric.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/pantompkins/invalid_sampling_frequency_non_numeric.json) |
| `ecg.pantompkins.invalid_sampling_frequency_non_positive` | [conformance/ecg/pantompkins/invalid_sampling_frequency_non_positive.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/pantompkins/invalid_sampling_frequency_non_positive.json) |
| `ecg.pantompkins.invalid_sampling_frequency_vector` | [conformance/ecg/pantompkins/invalid_sampling_frequency_vector.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/pantompkins/invalid_sampling_frequency_vector.json) |
| `ecg.pantompkins.medicom_mtd_r_wave_times` | [conformance/ecg/pantompkins/medicom_mtd_r_wave_times.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/pantompkins/medicom_mtd_r_wave_times.json) |
