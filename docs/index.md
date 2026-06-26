# Biosiglib

Biosiglib is the language-independent source of truth for the Biosiglib ecosystem. It is not an executable signal-processing library, and it does not provide user-facing MATLAB or Python functions.

Instead, Biosiglib defines the shared contract that implementations use:

* machine-readable JSON specifications for public algorithm behavior;
* shared fixtures and metadata;
* conformance cases and expected outputs;
* validation resources for specifications, fixtures, references, and implementation manifests.

The language-specific libraries implement those contracts:

* [Biosigmat](https://github.com/BSICoS/biosigmat) is the MATLAB implementation.
* [Biosigpy](https://github.com/BSICoS/biosigpy) is the Python implementation.

## What Lives Here

Biosiglib describes scientific and computational behavior that should remain consistent across programming languages. It records canonical inputs, outputs, units, parameters, defaults, edge-case behavior, numerical comparison rules, fixtures, conformance cases, and scientific provenance.

The repository is designed so humans can read the behavior while tools can validate it. The JSON files are the normative source. This website is the readable view.

## Current Scope

The current documentation covers the initial MVP pilots:

* [`hrv.tdmetrics`](generated/specifications/hrv.tdmetrics.md) - time-domain beat or pulse variability metrics.
* [`ecg.pantompkins`](generated/specifications/ecg.pantompkins.md) - Pan-Tompkins-style ECG R-peak detection.

These pilots establish the specification, fixture, conformance, and release patterns before the full Biosiglib scope expands across ECG, PPG, respiration, HRV, and other biomedical signal-processing tools.
