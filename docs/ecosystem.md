# Ecosystem

Biosiglib coordinates a small ecosystem of repositories with separate responsibilities.

| Repository | Role |
| --- | --- |
| [Biosiglib](https://github.com/BSICoS/biosiglib) | Source of truth for language-independent specifications, shared fixtures, conformance cases, validation tools, and release propagation metadata. |
| [Biosigmat](https://github.com/BSICoS/biosigmat) | MATLAB implementation of the Biosiglib specifications. |
| [Biosigpy](https://github.com/BSICoS/biosigpy) | Python implementation of the Biosiglib specifications. |

Biosigmat and Biosigpy may expose idiomatic language-specific APIs. They do not need identical internal architecture, but they must preserve the normative behavior defined by Biosiglib.

## Release Propagation

Biosiglib releases are propagated downstream so each implementation can declare exactly which specification release and commit it conforms to.

The release path is:

1. Biosiglib release.
2. Biosigmat propagation pull request.
3. Biosigpy propagation pull request.

The downstream pull requests update each implementation repository's `conformance.json` file. The implementations remain independently versioned, so a Biosigmat or Biosigpy release declares its supported Biosiglib version instead of sharing the Biosiglib version number.

## Source Of Truth

When behavior is unclear, Biosiglib is the place to resolve it. Existing implementation behavior can inform a specification, especially when mature code already exists, but no implementation is automatically the authority. Disagreements should be analyzed against the Biosiglib specification, fixtures, conformance cases, and scientific references.
