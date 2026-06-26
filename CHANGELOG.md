# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

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
- Normative `ecg_filtered`, `decg`, and `decg_envelope` outputs for `ecg.pantompkins`.
- Expected-error conformance cases with language-independent error categories and literal inputs.
- Initial invalid-type, invalid-shape, and invalid-value cases for both pilot specifications.
