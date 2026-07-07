# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## Unreleased

### Breaking changes

- Removed `algorithm_status` and `specification_status` from algorithm specification metadata and from the algorithm-spec schema.
- Renamed existing shared conformance case files and IDs to remove unnecessary `_001` suffixes.

### Added

- Draft tool specifications for `tools.medfilt_threshold`, `tools.lpd_filter`, `tools.nan_filter`, `tools.nan_filtfilt`, and `tools.snap_to_peak`.
- Shared tool fixtures and conformance cases covering reference outputs, meaningful edge behavior, orientation handling, invalid values, and NaN-aware filtering semantics.

### Changed

- Regenerated specification documentation for the updated schemas, renamed conformance cases, and new tool specifications.
- Clarified insufficient-data behavior for ECG signal specifications.
- Documented agent policy to avoid trivial all-NaN or empty fixtures and to avoid serial suffixes in descriptive conformance case names.
- Removed implementation-specific MATLAB and Python mapping notes from tool specifications so Biosiglib remains the normative source of truth.

### Removed

- Trivial tool conformance fixtures for empty outputs and all-NaN inputs where the behavior is fully specified in text.
- Biosigmat-derived wording from tool specifications while retaining fixture/reference provenance where applicable.

## v0.4.0 - 2026-07-07

### Changed

- Renamed the normative `ecg.pantompkins` intermediate output from `decg` to `decg_squared` to reflect that it is the squared derivative signal.

## v0.3.0 - 2026-06-30

### Added

- Draft `ecg.sloperange` specification for slope-range ECG-derived respiration.
- Kontaxis et al. 2020 and Varon et al. 2020 references for ECG-derived respiration.
- Scientific note for `ecg.sloperange`.
- Focused shared `ecg.sloperange` conformance cases covering positive synthetic EDR output, boundary `NaN` alignment, R-wave time outside the derivative ECG sample grid, and non-strict or repeated `r_wave_times`.
- Fixture metadata and derived-parent provenance for the R-wave timing table.
- Validation for snake_case structured IDs and forbidden `r_peak` identifiers in specifications, conformance mappings, fixture IDs, file roles, and channel IDs.
- Naming and conformance-case policy in `AGENTS.md`.

### Changed

- Renamed ECG timing contract identifiers from `r_peak_*` to `r_wave_*`.
- Clarified `ecg.sloperange` timing semantics using `r_wave_times` and conceptual `r_wave_samples`.
- Kept `hrv.tdmetrics` modality-generic with `dtk`.
- Renamed Medicom MTD fixtures and CSV columns to canonical names.

## v0.2.1 - 2026-06-26

### Fixed

- Corrected the expected outputs for `hrv.tdmetrics.valid_dtk_with_nan_001` so the case matches omit-missing-value semantics on the fixture `dtk` column.
- Restored equivalence between the fixture `dtk` column after omitting its leading missing-value marker and the interval sequence obtained from the corresponding `tk` differences.

## v0.2.0 - 2026-06-26

### Breaking changes

- Corrected the canonical `hrv.tdmetrics` input from event times `tk` to interval series `dtk`.
- Updated `hrv.tdmetrics` so `NaN` values in `dtk` are allowed as missing or invalid interval markers and omitted from all metric calculations.
- Replaced `tk`-based `hrv.tdmetrics` conformance cases with `dtk`-based cases.
- Updated successive-difference metric definitions to operate on the cleaned valid interval sequence after omitting `NaN` markers.

### Added

- Missing-data and preprocessing guidance reference: Cajal et al. 2022, “Effects of Missing Data on Heart Rate Variability Metrics”.
- `hrv.tdmetrics` conformance coverage for clean `dtk`, `dtk` with `NaN` markers, non-numeric input, matrix-shaped input, negative intervals, zero intervals, and infinite intervals.
- Optional `article_number` support in the reference catalog schema.
- `preprocessing_guidance` as a controlled provenance relation for algorithm specifications.

### Changed

- Regenerated the `hrv.tdmetrics` documentation page from the corrected JSON specification.
- Updated fixture catalog notes to describe `dtk` missing-value handling.
- Removed stale documentation and agent guidance that described `tk` as the canonical `hrv.tdmetrics` input.

## v0.1.1 - 2026-06-26

### Added

- Automatic Biosigmat propagation after Biosiglib releases through `repository_dispatch`.
- Automatic Biosigpy propagation after Biosiglib releases through `repository_dispatch`.
- Multi-implementation release path from Biosiglib releases to downstream implementation pull requests.
- Biosigpy conformance manifest integration for the pilot `hrv.tdmetrics` and `ecg.pantompkins` specifications.

### Changed

- Documented release propagation secrets and target-repository permissions for Biosigmat and Biosigpy.
- Updated Biosigpy CI to read the pinned Biosiglib commit from `conformance.json` instead of duplicating the commit in the workflow.

## v0.1.0 - 2026-06-24

### Added

- Initial repository structure for language-independent specifications, shared fixtures, conformance cases, references, tools, and documentation.
- Persistent AI agent guidance in AGENTS.md.
- Initial algorithm specification schema.
- Initial reference catalog schema.
- Initial scientific reference catalog.
- Task Force HRV 1996 reference.
- Draft `hrv.tdmetrics` specification.
- Local validator.
- Cross-validation between specs and references.
- Repository-local `.venv` for Python development tooling.
- Windows and POSIX environment setup documentation.
- Virtual-environment and Python-cache exclusions in `.gitignore`.
- Fixture catalog schema.
- Conformance case schema.
- First synthetic HRV interval fixture.
- First `hrv.tdmetrics` conformance case.
- Cross-validation of specs, references, fixture files, inputs, parameters, and outputs.
- Implementation conformance manifest schema.
- Version-pinning policy requiring implementation manifests to reference an exact Biosiglib commit.
- Implementation manifest specification support now uses an object keyed by canonical specification ID, guaranteeing identifier uniqueness and simplifying lookup by implementations.
- External implementation-manifest validation with current Biosiglib commit matching.
- Replaced the small synthetic `tdmetrics` fixture with the existing Biosigmat ECG timing fixture.
- Adopted the Biosigmat ECG timing fixture `tk` column for `hrv.tdmetrics`.
- Defined `dtk` as the successive differences derived from canonical event times `tk`.
- Recalculated full-precision expected outputs for the `hrv.tdmetrics` ECG timing conformance case.
- Pan-Tompkins 1985 reference entry.
- Draft `ecg.pantompkins` specification.
- Fixture-column references for ordered vector expected outputs in conformance cases.
- ECG signal fixture copied from the existing Biosigmat regression data.
- First `ecg.pantompkins` conformance case.
- Normative `ecg_filtered`, `decg_squared`, and `decg_envelope` outputs for `ecg.pantompkins`.
- Expected-error conformance cases with language-independent error categories and literal inputs.
- Initial invalid-type, invalid-shape, and invalid-value cases for both pilot specifications.
