# Slope-range ECG-derived respiration

!!! warning "Generated page"
    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.

## Metadata

| Field | Value |
| --- | --- |
| Canonical specification ID | `ecg.sloperange` |
| Module | `ecg` |
| Algorithm status | stable |
| Specification status | draft |
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
| `r_peak_times` | real_vector | vector | s | false | false | minimum_length=1 |
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
| `r_wave_sample_indices` | Convert each R-wave time in seconds to a one-based sample index using round(r_peak_times * sampling_frequency) + 1. |  |
| `analysis_windows` | Set shortWindow = round(sampling_frequency * 0.015), longWindow = round(sampling_frequency * 0.05), upslopeWindow = -longWindow + 1 through shortWindow, and downslopeWindow = -shortWindow through longWindow - 1. |  |
| `edr` | For each R wave with complete analysis windows, compute edr as max(decg over the upslope window) minus min(decg over the downslope window). |  |
| `boundary_edr` | For an R wave whose analysis windows extend outside the derivative ECG signal, preserve output alignment with r_peak_times and set the corresponding edr value to NaN. |  |

## Behavior

### Nan handling

NaN and infinite values in decg, r_peak_times, or sampling_frequency are invalid inputs. NaN values may appear in edr only to mark R waves whose analysis windows are incomplete at signal boundaries.

### Empty input

Empty decg and empty r_peak_times inputs are invalid.

### Input orientation

Treat decg and r_peak_times as one-dimensional vectors regardless of row or column orientation. The edr output is a one-dimensional ordered vector aligned with r_peak_times.

### Insufficient data

If decg is too short to support complete windows around a beat, the affected boundary edr value is NaN when the R-wave sample index is inside the signal. R-wave times that map outside the signal are invalid.

## Informative Notes

* This first Biosiglib contract makes edr the only normative output.
* Diagnostic arrays exposed by Biosigmat, including upslopes, downslopes, upslope_max_position, and downslope_min_position, are informative implementation details at this stage.
* Biosigmat maps r_peak_times to its input currently named tk and sampling_frequency to fs.
* R-wave sample indices follow the existing Biosigmat convention round(r_peak_times * sampling_frequency) + 1.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `ecg.sloperange.invalid_decg_inf` | [conformance/ecg/sloperange/invalid_decg_inf.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_decg_inf.json) |
| `ecg.sloperange.invalid_decg_matrix` | [conformance/ecg/sloperange/invalid_decg_matrix.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_decg_matrix.json) |
| `ecg.sloperange.invalid_decg_non_numeric` | [conformance/ecg/sloperange/invalid_decg_non_numeric.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_decg_non_numeric.json) |
| `ecg.sloperange.invalid_r_peak_time_out_of_bounds` | [conformance/ecg/sloperange/invalid_r_peak_time_out_of_bounds.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_r_peak_time_out_of_bounds.json) |
| `ecg.sloperange.invalid_sampling_frequency_non_numeric` | [conformance/ecg/sloperange/invalid_sampling_frequency_non_numeric.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_sampling_frequency_non_numeric.json) |
| `ecg.sloperange.invalid_sampling_frequency_non_positive` | [conformance/ecg/sloperange/invalid_sampling_frequency_non_positive.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_sampling_frequency_non_positive.json) |
| `ecg.sloperange.synthetic_boundary_nan_001` | [conformance/ecg/sloperange/synthetic_boundary_nan_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/synthetic_boundary_nan_001.json) |
| `ecg.sloperange.synthetic_positive_001` | [conformance/ecg/sloperange/synthetic_positive_001.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/synthetic_positive_001.json) |
