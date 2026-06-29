# Scientific Notes

Scientific notes give researchers a short, human-friendly explanation of an algorithm's purpose, rationale, assumptions, interpretation, and limitations.

They are explanatory documentation. They do not replace, override, or extend the normative JSON specification or its conformance cases.

## Authority

The Biosiglib contract is interpreted in this order:

1. JSON specifications and conformance cases are normative.
2. Scientific notes explain the method and must not contradict the corresponding specification.
3. Implementations conform to the specification and conformance cases.

When a scientific note and a JSON specification disagree, the JSON specification and conformance cases remain the source of truth. The disagreement should be fixed by updating the incorrect explanatory text or, when the specification itself is wrong, by changing the specification and reviewing the downstream impact.

## Writing Rules

Each scientific note must:

* declare the corresponding `spec_id` in Markdown front matter;
* link to the generated normative specification page;
* explain the scientific or signal-processing idea in accessible language;
* keep assumptions and limitations focused on scientific interpretation;
* avoid duplicating full input, parameter, output, tolerance, or edge-case definitions from the JSON specification.

Scientific notes may summarize the algorithm at a high level, but detailed contracts belong in `specs/*/*/spec.json` and `conformance/*/*/*.json`.

## Review Expectations

Changes touching specifications or scientific notes require a consistency review. Reviewers should check that:

* the note's `spec_id` points to an existing specification;
* the note is listed from this documentation section or the MkDocs navigation;
* the note does not introduce normative behavior absent from the JSON specification;
* specification changes are reflected in related notes when the scientific explanation changes;
* note changes do not contradict inputs, outputs, units, assumptions, behavior, references, or conformance cases.

## Current Notes

No scientific notes are currently published.

Use the [scientific-note template](template.md) when adding one.
