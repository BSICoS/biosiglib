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

## Documentation

The generated documentation site is available at [https://bsicos.github.io/biosiglib/](https://bsicos.github.io/biosiglib/).

The website is generated from the JSON specifications. The JSON files remain the normative source of truth for algorithm behavior, inputs, outputs, units, defaults, missing-value handling, edge cases, tolerances, and conformance status.

## Local validation

See [docs/development.md](docs/development.md) for local setup and validation commands.

## Releases

See [docs/releases.md](docs/releases.md) for release semantics and propagation details.

## Project status

Biosiglib is under active development. The first development phase establishes the specification format, validation tooling, generated documentation, shared fixtures, conformance cases, and integration with Biosigmat and Biosigpy.

## License

Biosiglib is distributed under the GNU General Public License version 3. See [LICENSE](LICENSE) for the complete license text.
