# Scientific-Note Template

Use this concise structure for new scientific notes. Replace the placeholder `spec_id`, title, and section text, then add the note to `docs/scientific/index.md` or `mkdocs.yml`.

Do not duplicate the full normative input, parameter, output, tolerance, or edge-case definitions from the JSON specification.

```markdown
---
spec_id: ecg.example
title: Human-readable method title
status: draft
---

# Human-readable method title

## Purpose

Briefly state what the method estimates or detects and when it is useful.

## Scientific rationale

Explain the physiological or signal-processing idea behind the method.

## Method summary

Summarize the algorithm in readable language. Do not duplicate the full normative input/output contract.

## Key assumptions

List only assumptions that matter scientifically or methodologically.

## Interpretation and limitations

Explain how to interpret the result and when the method may be unreliable.

## References

List or link the main methodological references.

## Specification

Link to the corresponding normative specification.
```
