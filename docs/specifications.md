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

<!-- BEGIN GENERATED SPECIFICATION TABLE -->
| Specification | Module | Summary |
| --- | --- | --- |
| [`ecg.baselineremove`](generated/specifications/ecg.baselineremove.md) | ECG | Estimates a slowly varying ECG baseline from local means around fiducial positions and subtracts its spline interpolation. |
| [`ecg.pantompkins`](generated/specifications/ecg.pantompkins.md) | ECG | Detects ordered R-wave occurrence times from a sampled ECG signal and exposes intermediate processing signals for plotting and debugging. |
| [`ecg.sloperange`](generated/specifications/ecg.sloperange.md) | ECG | Estimates an ECG-derived respiration amplitude series from derivative ECG morphology around detected R waves. |
| [`hrv.fdmetrics`](generated/specifications/hrv.fdmetrics.md) | HRV | Integrates conventional LF and HF powers or respiration-separated OSP powers on an authoritative frequency grid. |
| [`hrv.fillgaps`](generated/specifications/hrv.fillgaps.md) | HRV | Reconstructs missing event timestamps by iteratively interpolating intervals inside locally detected gaps. |
| [`hrv.ipfm`](generated/specifications/hrv.ipfm.md) | HRV | Estimates uniformly sampled instantaneous heart rate and an optional TVIPFM autonomic modulating signal from event times. |
| [`hrv.osp`](generated/specifications/hrv.osp.md) | HRV | Separates a uniformly sampled HRV modulating signal into a component linearly related to respiration and an orthogonal residual. |
| [`hrv.removefp`](generated/specifications/hrv.removefp.md) | HRV | Removes detections that follow abnormally short event-to-event intervals using a fixed adaptive-baseline rule. |
| [`hrv.tdmetrics`](generated/specifications/hrv.tdmetrics.md) | HRV | Computes standard time-domain HRV metrics from cleaned beat-to-beat or pulse-to-pulse intervals. |
| [`tools.lpd_filter`](generated/specifications/tools.lpd_filter.md) | Tools | Designs a low-pass differentiating FIR filter and reports its linear-phase delay. |
| [`tools.medfilt_threshold`](generated/specifications/tools.medfilt_threshold.md) | Tools | Computes a capped adaptive threshold from a one-dimensional signal using median-filter-based local baseline estimation. |
| [`tools.nan_filter`](generated/specifications/tools.nan_filter.md) | Tools | Applies ordinary causal filtering while interpolating short NaN gaps and preserving long NaN gaps. |
| [`tools.nan_filtfilt`](generated/specifications/tools.nan_filtfilt.md) | Tools | Applies ordinary zero-phase filtering while interpolating short NaN gaps and preserving long NaN gaps. |
| [`tools.snap_to_peak`](generated/specifications/tools.snap_to_peak.md) | Tools | Refines detection sample positions by moving each detection to the maximum signal sample in a NaN-aware local search window. |
<!-- END GENERATED SPECIFICATION TABLE -->

These specifications are not the final Biosiglib scope. The generated catalog expands as new contracts and their complete cross-language conformance work become ready together.

## Generated Pages

The algorithm-specific pages are generated from the JSON specifications and committed under `docs/generated/specifications/`. The specification table above and its MkDocs navigation entries are generated at the same time. Do not edit the delimited generated blocks manually; update the JSON source and run `python tools/generate_docs.py` instead.

## JSON Remains Normative

The human-readable pages summarize the JSON specifications. They are generated views of the JSON files, not separate normative copies.
