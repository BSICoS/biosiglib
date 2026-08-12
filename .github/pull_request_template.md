## Summary


## Validation

- [ ] `python -m unittest discover -s tests -v`
- [ ] `python tools/validate_specs.py`
- [ ] `python -m compileall tools`
- [ ] `mkdocs build --strict`

## Reviewer Checklist

- [ ] JSON specifications and conformance cases remain the normative source of truth.
- [ ] Method pages help users call and interpret a function without duplicating the normative contract.
- [ ] Specification, method-page, field-description, reference, and case changes were reviewed for consistency.
- [ ] No implementation repository changes are included unless this PR explicitly targets one.
