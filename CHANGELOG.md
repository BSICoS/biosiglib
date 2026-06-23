# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## v0.1.0 - 2026-06-23

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
