# Ecosystem

Biosiglib coordinates a small ecosystem of repositories with separate responsibilities.

| Repository | Role |
| --- | --- |
| [Biosiglib](https://github.com/BSICoS/biosiglib) | Source of truth for language-independent specifications, shared fixtures, conformance cases, validation tools, and coordinated release policy. |
| [Biosigmat](https://github.com/BSICoS/biosigmat) | MATLAB implementation of the Biosiglib specifications. |
| [Biosigpy](https://github.com/BSICoS/biosigpy) | Python implementation of the Biosiglib specifications. |

Biosigmat and Biosigpy may expose idiomatic language-specific APIs. They do not need identical internal architecture, but they must preserve the normative behavior defined by Biosiglib.

## Conformance and Releases

Each implementation declares conformance with one exact Biosiglib commit. The declaration covers every specification in that commit; support is not selected algorithm by algorithm.

The release path is:

1. Prepare and validate the Biosiglib contract commit.
2. Adapt Biosigmat and Biosigpy to that exact commit and merge both implementations after their complete suites pass.
3. Release Biosiglib only after both downstream manifests pin the release target commit.

The implementations remain independently versioned. Their one-line `biosiglib.lock` files record the reproducible commit relationship instead of mirroring the Biosiglib version number.

## Source Of Truth

When behavior is unclear, Biosiglib is the place to resolve it. Existing implementation behavior can inform a specification, especially when mature code already exists, but no implementation is automatically the authority. Disagreements should be analyzed against the Biosiglib specification, fixtures, conformance cases, and scientific references.
