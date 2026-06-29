## Summary


## Validation

- [ ] `python tools/generate_docs.py --check`
- [ ] `python tools/validate_specs.py`
- [ ] `python -m compileall tools`
- [ ] `mkdocs build --strict`

## Reviewer Checklist

- [ ] JSON specifications and conformance cases remain the normative source of truth.
- [ ] Scientific notes, if changed, are explanatory and do not duplicate full input/output or parameter definitions.
- [ ] Specification and scientific-note changes were reviewed for consistency.
- [ ] No implementation repository changes are included unless this PR explicitly targets one.
