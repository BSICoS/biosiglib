# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]

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
- Adopted direct use of the Biosigmat ECG timing fixture `dtk` column for `hrv.tdmetrics`.
- Preserved the leading `NaN` in the ECG timing fixture to verify missing-value handling.
- Recalculated full-precision expected outputs for the `hrv.tdmetrics` ECG timing conformance case.
