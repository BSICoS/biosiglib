# Biosiglib

**Language-independent specifications and shared validation resources for reproducible biomedical signal processing.**

Biosiglib defines the expected scientific and computational behavior of public algorithms implemented by the BSICoS biomedical signal-processing libraries. It is not an executable signal-processing package; it contains specifications, scientific provenance, shared fixtures, conformance cases, and documentation-generation tooling.

## Ecosystem

- [Biosigmat](https://github.com/BSICoS/biosigmat): MATLAB implementation.
- [Biosigpy](https://github.com/BSICoS/biosigpy): Python implementation.

## What is in this repository

- Machine-readable JSON specifications for public algorithms.
- JSON Schemas used to validate specifications and implementation manifests.
- Scientific references associated with each method.
- Shared fixtures and conformance cases.
- Tools for validation and generated documentation.

The current pilot specifications are:

- `hrv.tdmetrics`
- `ecg.pantompkins`
- `ecg.sloperange`

Additional specifications will be incorporated progressively from the current Biosigmat public API.

## Documentation

The generated documentation site is available at [https://bsicos.github.io/biosiglib/](https://bsicos.github.io/biosiglib/).

The website is generated from the JSON specifications. The JSON files remain the normative source of truth for algorithm behavior, inputs, outputs, units, defaults, missing-value handling, edge cases, tolerances, and conformance status.

## Local validation

Create a repository-local virtual environment and run the validator from that environment.

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe tools\validate_specs.py
```

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/validate_specs.py
```

Implementation repositories can validate their conformance manifests with:

```bash
.venv/bin/python tools/validate_specs.py --manifest ../biosigmat/conformance.json
```

Use the equivalent `.venv\Scripts\python.exe` command on Windows.

## Releases

Biosiglib, Biosigmat, and Biosigpy use independent semantic versioning. A language-specific implementation declares which Biosiglib release and commit it conforms to instead of sharing the same version number.

To create a Biosiglib release:

1. Ensure the `Validate Biosiglib` workflow passes on `main`.
2. Update `CHANGELOG.md` manually.
3. Run the `Release Biosiglib` workflow from `main`.
4. Enter a version such as `v0.1.0`.

The release workflow validates the repository, creates the matching Git tag and GitHub Release, and dispatches propagation to Biosigmat and Biosigpy.

## Project status

Biosiglib is under active development. The first development phase establishes the specification format, validation tooling, generated documentation, shared fixtures, conformance cases, and integration with Biosigmat and Biosigpy.

## License

Biosiglib is distributed under the GNU General Public License version 3. See [LICENSE](LICENSE) for the complete license text.
