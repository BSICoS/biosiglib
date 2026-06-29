# Development

Development in Biosiglib should keep the machine-readable sources and the human-readable documentation aligned.

## Local Validation

Use the repository-local `.venv` for local Python tooling. After creating and installing the development environment, the core validation commands are:

```bash
python tools/generate_docs.py
python tools/generate_docs.py --check
python tools/validate_specs.py
python -m compileall tools
mkdocs build --strict
```

On Windows PowerShell, explicit `.venv` invocations look like:

```powershell
.venv\Scripts\python.exe tools\generate_docs.py
.venv\Scripts\python.exe tools\generate_docs.py --check
.venv\Scripts\python.exe tools\validate_specs.py
.venv\Scripts\python.exe -m compileall tools
.venv\Scripts\python.exe -m mkdocs build --strict
```

`mkdocs build --strict` treats warnings as build failures, which keeps broken links and configuration drift visible during review.

## Documentation Workflow

The documentation site is built on pull requests. On pushes to `main`, the workflow also prepares a GitHub Pages deployment artifact and runs the Pages deployment action.

If the repository has not yet enabled Pages publication, maintainers may need to configure GitHub Pages in repository settings and select "GitHub Actions" as the source.

## Generated Documentation

Specification pages under `docs/generated/specifications/` are generated from the JSON specifications. Generated files must be committed and kept in sync with the JSON source.

Run `python tools/generate_docs.py` after changing any file under `specs/*/*/spec.json` or conformance cases linked from a specification page. CI runs `python tools/generate_docs.py --check` and fails when generated pages are missing or stale.

## Scientific Notes

Scientific notes under `docs/scientific/` are short explanatory pages for researchers. They describe why a method is useful, the scientific rationale behind it, key assumptions, and interpretation limits.

They are not normative. JSON specifications and conformance cases remain the source of truth for inputs, outputs, units, parameters, defaults, numerical definitions, edge-case behavior, tolerances, and implementation conformance.

Scientific notes must declare `spec_id` in Markdown front matter and link to the corresponding generated specification page. They should summarize the method in readable language without duplicating the full input, parameter, output, tolerance, or edge-case definitions from the JSON specification.

## Spec And Note Review Checklist

For pull requests touching `specs/`, `conformance/`, or `docs/scientific/`, reviewers should check:

* JSON specs and conformance cases still define the normative contract;
* scientific notes remain explanatory and do not introduce independent requirements;
* note `spec_id` values point to existing specifications;
* notes are discoverable from the scientific documentation section or MkDocs navigation;
* related specs, notes, generated docs, references, fixtures, and conformance cases remain consistent;
* validation and documentation build commands are reported with their results.
