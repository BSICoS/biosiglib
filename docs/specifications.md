# Specifications

Biosiglib specifications are machine-readable JSON files validated against the repository schemas. They define the behavior that implementations must preserve across languages.

A specification can describe:

* canonical inputs and outputs;
* units, shapes, and data types;
* parameters and default values;
* mathematical and computational definitions;
* missing-value and edge-case behavior;
* numerical comparison requirements;
* scientific provenance;
* associated fixtures and conformance cases.

Specification fields are separated into normative behavior and informative documentation. Normative fields affect conformance. Informative fields help explain the algorithm without creating a separate source of truth.

## Current Specifications

The current specifications are:

| Specification | Module | Summary |
| --- | --- | --- |
| [`hrv.tdmetrics`](generated/specifications/hrv.tdmetrics.md) | HRV | Time-domain HRV metrics from cleaned beat-to-beat or pulse-to-pulse intervals. |
| [`hrv.fillgaps`](generated/specifications/hrv.fillgaps.md) | HRV | Iterative PCHIP reconstruction of missing events in locally detected gaps. |
| [`hrv.ipfm`](generated/specifications/hrv.ipfm.md) | HRV | Sampled instantaneous-rate reconstruction and optional TVIPFM modulation from event times. |
| [`hrv.removefp`](generated/specifications/hrv.removefp.md) | HRV | Deterministic false-positive event removal using an adaptive interval baseline. |
| [`ecg.pantompkins`](generated/specifications/ecg.pantompkins.md) | ECG | Pan-Tompkins-style ECG R-wave detection with public intermediate signals. |
| [`ecg.sloperange`](generated/specifications/ecg.sloperange.md) | ECG | Slope-range ECG-derived respiration from derivative ECG morphology around R waves. |
| [`tools.lpd_filter`](generated/specifications/tools.lpd_filter.md) | Tools | Low-pass differentiating FIR filter design with linear-phase delay. |
| [`tools.medfilt_threshold`](generated/specifications/tools.medfilt_threshold.md) | Tools | Median-filtered adaptive threshold with a configurable cap. |
| [`tools.nan_filter`](generated/specifications/tools.nan_filter.md) | Tools | Causal filtering with NaN-aware gap handling. |
| [`tools.nan_filtfilt`](generated/specifications/tools.nan_filtfilt.md) | Tools | Zero-phase filtering with NaN-aware gap handling. |
| [`tools.snap_to_peak`](generated/specifications/tools.snap_to_peak.md) | Tools | NaN-aware local-maximum refinement of detection positions. |

These specifications are not the final Biosiglib scope. The initial pilots established the specification format, validation rules, fixtures, conformance cases, documentation structure, and release propagation pattern that later specifications reuse.

## Generated Pages

The algorithm-specific pages are generated from the JSON specifications and committed under `docs/generated/specifications/`. They should not be edited manually. Update the JSON source and run `python tools/generate_docs.py` instead.

## JSON Remains Normative

The human-readable pages summarize the JSON specifications. They are generated views of the JSON files, not separate normative copies.
