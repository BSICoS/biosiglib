# Conformance

Conformance describes how a language-specific implementation declares and validates its relationship to Biosiglib.

Each implementation repository maintains a machine-readable implementation manifest, conventionally named `conformance.json`. The manifest identifies the implementation and pins the exact Biosiglib commit used for conformance.

The declaration is total: the implementation conforms to every specification in the pinned commit and must execute every shared conformance case. Partial support, roadmaps, and work in progress belong in issues and pull requests rather than in the conformance manifest.

Passing the shared cases is executable evidence for the declaration. It does not make the cases a substitute for the complete normative JSON contracts.

## Exact Pinning

A downstream manifest pins one exact Biosiglib commit. A semantic version alone is not enough because conformance must be reproducible against the precise specifications, schemas, fixtures, and conformance cases used during validation.

The `$schema` URL is derived from the same commit so editors can load the matching schema. Biosiglib's validator rejects a schema URL whose commit differs from `biosiglib.commit`; contributors therefore maintain one normative pin.

Implementation and Biosiglib release versions remain visible in their respective repositories and release notes. They are not duplicated in the conformance manifest.

## Validation Across Implementations

Biosigmat and Biosigpy validate their manifests and behavior against Biosiglib resources. Each implementation can keep its own public API style, internal architecture, error classes, and plotting tools, but its normative outputs and edge-case behavior must match every contract in the pinned commit within the declared tolerances.

The shared Biosiglib validator checks repository specifications and can validate implementation manifests with:

```bash
python tools/validate_specs.py --manifest path/to/conformance.json
```

Cross-language conformance is built from shared specifications, shared fixtures, and shared expected results rather than from one implementation copying the other.

When behavior depends on requesting an optional output, a conformance case uses `requested_outputs` to declare the return profile that must be exercised. This is especially important for expected-error cases, where there are no expected-output mappings from which to infer the request.

Successful cases may also use `expected_warnings` to require observable, non-fatal diagnostics. Warning identifiers are defined by the corresponding specification. Each expected warning lists the complete `affected_ids` set that must be aggregated into that single warning. Warning and affected-id ordering is not significant. If `expected_warnings` is absent, the call must not emit a normative warning. Expected-error cases cannot also declare warnings because the operation does not complete successfully.
