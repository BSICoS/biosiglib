# Releases

Biosiglib uses independent semantic versioning with `MAJOR.MINOR.PATCH`. Biosigmat and Biosigpy also use their own independent versions. Implementation versions do not mirror the Biosiglib version: each implementation declares conformance with one exact Biosiglib commit.

## Release Semantics

A Biosiglib release captures the current language-independent source of truth:

* JSON specifications;
* schemas;
* fixture catalogs and fixture files;
* conformance cases and expected outputs;
* validation tooling;
* coordinated conformance metadata.

Classify the complete change set since the latest release. When several changes have different impacts, use the highest required increment.

## Classification Checklist

| Increment | Use when | Typical downstream impact |
| --- | --- | --- |
| **MAJOR** | A released normative contract changes incompatibly. This includes required input or output changes, removals or renames, formulas, units, defaults, validation, `NaN` handling, edge cases, output semantics, or incompatible schema and validator changes. It also includes a correction that deliberately replaces released normative behavior. | Previously conformant implementations must adapt before the Biosiglib release is published. |
| **MINOR** | The source of truth gains a compatible capability: a new specification, fixture, conformance case, optional schema field, or compatible validator rule. A new case may expose a latent implementation defect even when the normative behavior itself is unchanged. | Existing public behavior remains valid, but both implementations must pass the expanded complete suite before release. |
| **PATCH** | Normative behavior is unchanged. Examples include informative-only documentation and tooling corrections, provenance metadata corrections, and expected-value corrections that restore an already unambiguous released definition. | No intentional public algorithm change. Downstream metadata or tests may still need a small update. |

Apply these checks before choosing an increment:

1. List every specification, fixture, case, schema, validator, scientific-provenance, tooling, and documentation change since the latest tag.
2. Identify whether each change affects normative behavior, compatible conformance coverage, or informative material only.
3. Check whether any previously conformant implementation or valid machine-readable artifact would become non-conformant.
4. Check corrections to released expected values against the normative definition and scientific provenance. Use PATCH only when the correction restores an unambiguous existing contract; use MAJOR if the contract itself changes.
5. Route ambiguous scientific changes to explicit maintainer review. Do not infer a release class automatically when formulas, signal-processing direction, phase, units, physiological meaning, missing-value behavior, or provenance leave more than one defensible interpretation.
6. Record the selected increment and reasoning in the pull request and changelog.

## Examples From Project History

* **Compatible new specification — MINOR:** v0.3.0 added the new `ecg.sloperange` specification and its first shared cases without replacing an existing released contract.
* **Conformance case exposes an implementation defect — classify the contract, not the failure:** the v0.6.0 `hrv.tdmetrics` single-interval cases exposed defects tracked by [Biosigpy #37](https://github.com/BSICoS/biosigpy/issues/37) and [Biosigmat #48](https://github.com/BSICoS/biosigmat/issues/48). A new case against unchanged released behavior is MINOR, but those cases accompanied a normative minimum-data change, so an equivalent future Biosiglib release would use the higher MAJOR classification. Each downstream fix remains independently versioned.
* **Normative correction requiring downstream changes — MAJOR:** issue #59 made four previously informative `ecg.sloperange` diagnostics required outputs and defined their indexing, boundary, and tie semantics. Downstream implementations must adapt before claiming conformance.
* **Released expected-value correction — PATCH:** v0.5.4 corrected the `tools.nan_filtfilt` long-gap fixture to match independent filtering and the already defined segment semantics.
* **Informative-only correction — PATCH:** an isolated correction to generated-document navigation, explanatory prose, or a citation that does not change normative JSON is a patch.

## Release Readiness Checklist

Before tagging a Biosiglib release:

1. Replace the changelog's `Unreleased` heading with the selected version and release date, and describe breaking or adaptation-requiring changes explicitly.
2. Regenerate specification pages and pass documentation checks, specification and fixture validation, validator tests, compile checks, strict MkDocs build, and `git diff --check`.
3. Confirm the release is created from the intended commit on the default branch and that the version tag resolves to that exact commit.
4. Verify Biosigmat and Biosigpy have merged their adaptations and complete conformance suites for the release target commit.
5. Verify both downstream manifests pin that exact commit. The release workflow enforces this invariant before tagging.
6. Prepare release notes that state the classification, normative impact, exact commit, and downstream readiness.

## Coordinated Conformance

The expected path is:

1. Merge the reviewed Biosiglib contract commit without releasing it yet.
2. Update Biosigmat and Biosigpy to that commit, include any required implementation work, and pass their complete suites.
3. Merge both downstream conformance declarations.
4. Release the exact Biosiglib commit after the automated downstream-pin gate passes.

For changes that require no implementation adaptation, each downstream repository provides an `Update Biosiglib Pin` workflow that validates the full suite before opening a ready-for-review pull request. Changes requiring implementation work use an ordinary feature or fix pull request that updates the pin together with the code.

A pin update is a total conformance declaration, not a roadmap entry. It cannot merge while any specification or shared case in the pinned commit remains unsupported.

## Documentation Publication

The documentation workflow builds the MkDocs site on pull requests. On pushes to `main`, it uploads the built site for GitHub Pages deployment. Repository settings may still need GitHub Pages enabled with "GitHub Actions" selected as the build and deployment source before the first publication succeeds.
