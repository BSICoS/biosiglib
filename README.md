# Biosiglib

**Language-independent specifications and shared resources for reproducible biomedical signal processing.**

Biosiglib is the central repository of the Biosiglib ecosystem. It defines the expected scientific and computational behavior of the public algorithms implemented by language-specific libraries.

The current implementations are:

* [biosigmat](../biosigmat): MATLAB implementation.
* [biosigpy](../biosigpy): Python implementation.

Biosiglib is not an executable signal-processing library. It contains the specifications, scientific provenance, shared fixtures, conformance cases, and common usage scenarios used by the implementations.

## Goals

Biosiglib aims to provide:

* Reproducible biomedical signal-processing methods.
* Consistent behavior across programming languages.
* Explicit separation between algorithm specifications and implementations.
* Traceability between algorithms and their scientific publications.
* Shared validation resources for ECG, PPG, respiration, HRV, and other biomedical signal modalities.
* Machine-readable specifications with automatically generated human-readable documentation.

## Design principles

### Specifications are the source of truth

The scientific and computational behavior of each public algorithm is defined in Biosiglib.

Language-specific implementations must conform to these specifications, but they may use different internal architectures and idiomatic APIs.

An implementation is not considered the source of truth solely because it was developed first.

### Independent implementations

Biosigmat and Biosigpy are independent implementations of the same specifications.

The Python implementation is not intended to be a line-by-line translation of the MATLAB implementation. Both implementations must reproduce the behavior defined by Biosiglib within the established numerical tolerances.

### Canonical names across implementations

Biosiglib uses canonical `snake_case` IDs as the conceptual source of truth. Python APIs should generally use those names directly. MATLAB APIs may use idiomatic camelCase or name-value spelling, but each different spelling must map explicitly to the same canonical concept. Implementations should not introduce unrelated names unless the underlying signal semantics differ.

### Scientific provenance and software attribution are separate

The scientific authorship of an algorithm is recognised by citing the publications that introduce or extend the method.

The authorship of Biosiglib and its implementations corresponds to the people responsible for the software project, including its architecture, implementation, validation, documentation, and maintenance.

Using an algorithm through Biosiglib does not replace the citation of the original scientific publication.

### Minimal necessary infrastructure

New abstractions and automation mechanisms are introduced only when they solve a concrete project requirement.

The project avoids infrastructure that makes the specifications or implementations harder to understand and maintain.

## Repository contents

Biosiglib will contain:

* JSON specifications for public algorithms.
* JSON Schema definitions used to validate every specification.
* Scientific references associated with the algorithms.
* Shared fixtures and their machine-readable metadata.
* Conformance cases and expected outputs.
* Language-independent descriptions of common examples and workflows.
* Tools for validation and documentation generation.
* A generated documentation website.

The initial pilot specifications are:

* `hrv.tdmetrics`
* `ecg.pantompkins`

Additional specifications will be incorporated progressively from the current Biosigmat public API.

## Specifications

Each public algorithm is described using a standard JSON template validated with JSON Schema.

Specifications define aspects such as:

* Inputs and outputs.
* Units.
* Parameters and default values.
* Mathematical or computational behavior.
* Missing-value behavior.
* Edge cases.
* Numerical comparison requirements.
* Scientific provenance.
* Associated conformance cases.

Specification fields are classified as either normative or informative.

### Normative fields

Normative fields affect implementation conformance. Examples include:

* Input and output definitions.
* Units.
* Default parameter values.
* Mathematical definitions.
* Missing-value behavior.
* Edge-case behavior.

Changes to normative fields may require updates to the implementations and an appropriate semantic-version increment.

### Informative fields

Informative fields improve explanation and documentation without changing the required behavior. Examples include:

* Summaries.
* Explanatory notes.
* Background information.
* Documentation-oriented descriptions.

Informative changes do not invalidate a conforming implementation unless they correct an ambiguity in normative behavior.

## Fixtures and conformance cases

Shared fixtures are stored in open formats:

* JSON for metadata and small structured values.
* CSV for signals, annotations, and tabular numerical data.

The fixture catalog records the information required by tests and examples, including:

* Modality.
* Device and acquisition source.
* Sampling frequency.
* Units.
* Duration.
* Processing already applied to the signal.
* Available annotations.

Conformance cases associate:

* A specification.
* One or more fixtures.
* Input parameters.
* Expected outputs.
* Absolute numerical tolerances.
* Expected handling of `NaN` values.
* Language-independent expected-error categories for scientifically mandatory invalid inputs.
* The origin of the reference result.

Reference results may originate from analytical calculations, external annotations, published values, manual review, or a previously validated implementation.

## Shared examples and workflows

Examples and workflows teach users how to apply the ecosystem to complete signal-processing tasks.

A common workflow may define steps such as:

1. Load a signal.
2. Inspect its metadata.
3. Apply preprocessing.
4. Detect or delineate physiological events.
5. Compute derived measurements.
6. Visualise the signal and results.

Each language-specific repository provides executable code using its own syntax and plotting tools. However, corresponding examples should preserve the same conceptual sequence, parameters, input data, and scientific interpretation whenever possible.

Examples and workflows are not part of the public API contract unless a specification explicitly references their behavior.

## Conformance

Each implementation maintains a machine-readable conformance manifest.

The manifest identifies:

* The implementation and its version.
* The Biosiglib release and commit used for validation.
* The specifications implemented.
* Their current conformance status.

Continuous integration verifies the declared relationship by running the relevant conformance cases against the referenced Biosiglib version.

Implementation repositories declare their relationship to Biosiglib with a machine-readable implementation manifest. The manifest identifies the implementation, pins the exact Biosiglib commit used for validation, and records specification support in an object keyed by canonical Biosiglib specification ID. Each value contains the implementation status and optional implementation-specific metadata; object keys guarantee one entry per specification ID.

## Local validation

Create a repository-local virtual environment, install the development requirements, and run the validator through that environment's Python executable. The local validator checks specifications, references, fixture metadata, fixture files, and conformance cases.

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe tools\validate_specs.py
```

Activation is optional for interactive development:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/validate_specs.py
```

Activation is optional for interactive development:

```bash
source .venv/bin/activate
```

Explicitly invoking the environment interpreter is preferred for automation and AI agents because it avoids ambiguity about which Python installation is being used.

## Implementation manifest validation

Implementation repositories can validate their conformance manifest from a Biosiglib checkout. Validation uses the current Biosiglib checkout, requires the manifest's pinned commit to match that checkout, and checks manifest structure and specification identifiers without executing the implementation.

Windows PowerShell:

```powershell
.venv\Scripts\python.exe tools\validate_specs.py --manifest ..\biosigmat\conformance.json
```

Linux/macOS:

```bash
.venv/bin/python tools/validate_specs.py --manifest ../biosigmat/conformance.json
```

## Versioning

Biosiglib and each language-specific implementation use independent semantic versioning:

```text
MAJOR.MINOR.PATCH
```

A Biosigmat or Biosigpy release therefore declares which Biosiglib version it conforms to instead of sharing the same version number.

Specification changes are recorded in the Biosiglib changelog. Changes that affect implementations are propagated automatically to their repositories.

## Documentation

The human-readable documentation is generated from the machine-readable specifications.

The generated website will include:

* Algorithm descriptions.
* Inputs, outputs, and units.
* Parameters and defaults.
* Scientific references.
* Edge-case behavior.
* Available fixtures and conformance cases.
* Implementation support status.
* Shared examples and workflows.

The generated documentation is a view of the JSON source and is not maintained as a separate normative copy.

## Project status

Biosiglib is currently under active development.

The first development phase will establish:

* The JSON Schema templates.
* The `tdmetrics` pilot specification.
* The `pantompkins` pilot specification.
* The initial fixture catalog.
* Shared conformance cases.
* Validation and documentation-generation tooling.
* Integration with Biosigmat and Biosigpy.

## License

Biosiglib is distributed under the GNU General Public License version 3.

See `LICENSE` for the complete license text.
