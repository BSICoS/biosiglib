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

## Current Pilot Specifications

The current MVP pilots are:

| Specification | Module | Summary |
| --- | --- | --- |
| [`hrv.tdmetrics`](generated/specifications/hrv.tdmetrics.md) | HRV | Time-domain HRV metrics from cleaned beat-to-beat or pulse-to-pulse intervals. |
| [`ecg.pantompkins`](generated/specifications/ecg.pantompkins.md) | ECG | Pan-Tompkins-style ECG R-peak detection with public intermediate signals. |

These pilots are not the final Biosiglib scope. They establish the specification format, validation rules, fixtures, conformance cases, documentation structure, and release propagation pattern that later specifications will reuse.

## Generated Pages

The algorithm-specific pages are generated from the JSON specifications and committed under `docs/generated/specifications/`. They should not be edited manually. Update the JSON source and run `python tools/generate_docs.py` instead.

## JSON Remains Normative

The human-readable pages summarize the JSON specifications. They are generated views of the JSON files, not separate normative copies.
