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
| `upslopes` | real_vector | vector | a.u. |
| `downslopes` | real_vector | vector | a.u. |
| `upslope_max_positions` | real_vector | vector | sample |
| `downslope_min_positions` | real_vector | vector | sample |

## Normative Definitions

| Target | Definition | Formula |
| --- | --- | --- |
| `r_wave_times` | ECG R-wave occurrence times in seconds. Values must be finite, one-dimensional, strictly increasing, without repeats, and mappable onto the derivative ECG sample grid using sampling_frequency. |  |
| `r_wave_samples` | Conceptual zero-based sample-grid positions computed as round(r_wave_times * sampling_frequency) on the derivative ECG sample grid. Each value must lie from 0 through length(decg) - 1, inclusive. Public implementations may retain native array indices in their direct APIs, but conformance values for normative position outputs must use this zero-based grid. |  |
| `analysis_windows` | Set short_window = round(sampling_frequency * 0.015) and long_window = round(sampling_frequency * 0.05). The upslope_window contains integer offsets greater than -long_window and less than or equal to short_window. The downslope_window contains integer offsets greater than or equal to -short_window and less than long_window. |  |
| `complete_beat` | A beat is complete only when both its upslope and downslope analysis windows lie entirely within the decg sample grid. Only complete beats contribute samples to upslopes or downslopes. |  |
| `extrema_selection` | For each complete beat, select the maximum decg value in the upslope window and the minimum decg value in the downslope window. If multiple samples share the selected extreme value, choose the earliest sample in the corresponding window. |  |
| `edr` | For each complete beat, compute edr as the decg value at upslope_max_positions minus the decg value at downslope_min_positions. Align edr with r_wave_times. |  |
| `upslopes` | Return a vector with the same length, zero-based sample grid, and unit as decg. Copy decg inside the union of complete-beat upslope windows and set every other sample to NaN. |  |
| `downslopes` | Return a vector with the same length, zero-based sample grid, and unit as decg. Copy decg inside the union of complete-beat downslope windows and set every other sample to NaN. |  |
| `upslope_max_positions` | Return the selected upslope maximum positions on the conceptual zero-based decg sample grid, aligned with r_wave_times. Set the position to NaN for an incomplete beat. |  |
| `downslope_min_positions` | Return the selected downslope minimum positions on the conceptual zero-based decg sample grid, aligned with r_wave_times. Set the position to NaN for an incomplete beat. |  |
| `boundary_outputs` | For an incomplete beat, preserve alignment with r_wave_times and set the corresponding edr, upslope_max_positions, and downslope_min_positions values to NaN. Do not copy either incomplete beat window into upslopes or downslopes. |  |

## Behavior

### Nan handling

NaN and infinite values in decg, r_wave_times, or sampling_frequency are invalid inputs. NaN values mark incomplete beats in edr, upslope_max_positions, and downslope_min_positions, and samples outside complete-beat analysis windows in upslopes and downslopes.

### Empty input

Empty decg and empty r_wave_times inputs are invalid.

### Input orientation

Treat decg and r_wave_times as one-dimensional vectors regardless of row or column orientation. The edr, upslope_max_positions, and downslope_min_positions outputs are one-dimensional ordered vectors aligned with r_wave_times. The upslopes and downslopes outputs are one-dimensional ordered vectors aligned with decg.

### Insufficient data

If decg is too short to support both complete windows around a beat, the aligned edr and extrema-position values are NaN and that beat contributes no samples to either signal-aligned slope vector when the corresponding r_wave_samples value is inside the signal. R-wave times that map outside the derivative ECG sample grid are invalid.

## Informative Notes

* The signal-aligned slope vectors and selected extrema positions support visual inspection of the analysis performed around each R wave.

## Conformance Cases

| Case ID | File |
| --- | --- |
| `ecg.sloperange.invalid_r_wave_time_out_of_bounds` | [conformance/ecg/sloperange/invalid_r_wave_time_out_of_bounds.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_r_wave_time_out_of_bounds.json) |
| `ecg.sloperange.invalid_r_wave_times_not_strict` | [conformance/ecg/sloperange/invalid_r_wave_times_not_strict.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/invalid_r_wave_times_not_strict.json) |
| `ecg.sloperange.synthetic_boundary_nan` | [conformance/ecg/sloperange/synthetic_boundary_nan.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/synthetic_boundary_nan.json) |
| `ecg.sloperange.synthetic_positive` | [conformance/ecg/sloperange/synthetic_positive.json](https://github.com/BSICoS/biosiglib/blob/main/conformance/ecg/sloperange/synthetic_positive.json) |
