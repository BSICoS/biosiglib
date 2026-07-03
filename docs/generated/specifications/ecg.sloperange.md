# Slope-range ECG-derived respiration

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `ecg.sloperange` |
| Module | `ecg` |
| Source JSON | [specs/ecg/sloperange/spec.json](https://github.com/BSICoS/biosiglib/blob/main/specs/ecg/sloperange/spec.json) |

## Summary

Estimates an ECG-derived respiration amplitude series from derivative ECG morphology around detected R waves.

The slope-range method summarizes beat-to-beat respiratory modulation by comparing the maximum upslope and minimum downslope of a derivative ECG signal in short windows around each R wave.

## Keywords

`ECG`, `ECG-derived respiration`, `EDR`, `slope range`, `respiratory modulation`

## Scientific References

| ID | Relation | Note |
| --- | --- | --- |
| `kontaxis_edr_af_2020` | original_method | Primary method and provenance reference for slope-range ECG-derived respiration. |
| `varon_comparative_edr_2020` | validation | Comparative EDR context and validation evidence for single-lead ambulatory ECG. |

## Inputs

| id | data_type | shape | unit | allow_nan | allow_inf | constraints |
| --- | --- | --- | --- | --- | --- | --- |
| `decg` | real_vector | vector | a.u. | false | false | minimum_length=2 |
| `r_wave_times` | real_vector | vector | s | false | false | minimum_length=1 |
| `sampling_frequency` | real_scalar | scalar | Hz | false | false | exclusive_minimum=0 |

## Parameters

No parameters.

## Outputs

| id | data_type | shape | unit |
| --- | --- | --- | --- |
| `edr` | real_vector | vector | a.u. |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `r_wave_times` | ECG R-wave occurrence times in seconds. Values must be finite, one-dimensional, strictly increasing, without repeats, and mappable onto the derivative ECG sample grid using sampling_frequency. |  |
| `r_wave_samples` | Conceptual sample-grid positions derived from r_wave_times and sampling_frequency on the derivative ECG sample grid. Each value must lie within the decg sample grid. The contract does not specify implementation-specific array indexing conventions. |  |
| `analysis_windows` | Set short_window = round(sampling_frequency * 0.015) and long_window = round(sampling_frequency * 0.05). The upslope_window contains integer offsets greater than -long_window and less than or equal to short_window. The downslope_window contains integer offsets greater than or equal to -short_window and less than long_window. |  |
| `edr` | For each R wave with complete analysis windows, compute edr as max(decg over the upslope window) minus min(decg over the downslope window). |  |
| `boundary_edr` | For an R wave whose analysis windows extend outside the derivative ECG signal, preserve output alignment with r_wave_times and set the corresponding edr value to NaN. |  |

## Behavior

### Nan handling

NaN and infinite values in decg, r_wave_times, or sampling_frequency are invalid inputs. NaN values may appear in edr only to mark R waves whose analysis windows are incomplete at signal boundaries.

### Empty input

Empty decg and empty r_wave_times inputs are invalid.

### Input orientation

Treat decg and r_wave_times as one-dimensional vectors regardless of row or column orientation. The edr output is a one-dimensional ordered vector aligned with r_wave_times.

### Insufficient data

If decg is too short to support complete windows around a beat, the affected boundary edr value is NaN when the corresponding r_wave_samples value is inside the signal. R-wave times that map outside the derivative ECG sample grid are invalid.

## Informative Notes

* This first Biosiglib contract makes edr the only normative output.
* Diagnostic arrays exposed by implementations, including upslopes, downslopes, upslope_max_position, and downslope_min_position, are informative implementation details at this stage.
* Implementation-specific array indexing conventions are not part of the Biosiglib contract.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `ecg.sloperange.invalid_r_wave_time_out_of_bounds` | [conformance/ecg/sloperange/invalid_r_wave_time_out_of_bounds.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_r_wave_time_out_of_bounds.json) |
| `ecg.sloperange.invalid_r_wave_times_not_strict` | [conformance/ecg/sloperange/invalid_r_wave_times_not_strict.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_r_wave_times_not_strict.json) |
| `ecg.sloperange.synthetic_boundary_nan` | [conformance/ecg/sloperange/synthetic_boundary_nan.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/synthetic_boundary_nan.json) |
| `ecg.sloperange.synthetic_positive` | [conformance/ecg/sloperange/synthetic_positive.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/synthetic_positive.json) |
