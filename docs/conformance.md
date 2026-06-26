# Conformance

Conformance describes how a language-specific implementation declares and validates its relationship to Biosiglib.

Each implementation repository maintains a machine-readable implementation manifest, conventionally named `conformance.json`. The manifest records the implementation identity, implementation version, pinned Biosiglib release and commit, and the support status for each Biosiglib specification.

## Statuses

Implementation manifests use the following statuses:

| Status | Meaning |
| --- | --- |
| `conformant` | The implementation supports the specification and all applicable conformance cases pass for the pinned Biosiglib release and commit. |
| `implemented` | The implementation has behavior for the specification, but full conformance has not yet been established or declared. |
| `planned` | Support is intended, but implementation work is not complete. |
| `unsupported` | The implementation does not support the specification and does not currently plan to expose it. |

`conformant` should only be used after validation has passed for the exact Biosiglib version and commit recorded in the manifest.

## Exact Pinning

A downstream manifest must pin an exact Biosiglib commit. A semantic version alone is not enough because conformance must be reproducible against the precise specifications, schemas, fixtures, and conformance cases used during validation.

The pinned release communicates the public release relationship. The pinned commit makes the validation target exact.

## Validation Across Implementations

Biosigmat and Biosigpy validate their manifests and behavior against Biosiglib resources. Each implementation can keep its own public API style, internal architecture, error classes, and plotting tools, but its normative outputs and edge-case behavior must match the Biosiglib contracts within the declared tolerances.

The shared Biosiglib validator checks repository specifications and can validate implementation manifests with:

```bash
python tools/validate_specs.py --manifest path/to/conformance.json
```

Cross-language conformance is built from shared specifications, shared fixtures, and shared expected results rather than from one implementation copying the other.
