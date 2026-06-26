# Development

Development in Biosiglib should keep the machine-readable sources and the human-readable documentation aligned.

## Local Validation

Use the repository-local `.venv` for local Python tooling. After creating and installing the development environment, the core validation commands are:

```bash
python tools/validate_specs.py
python -m compileall tools
mkdocs build --strict
```

On Windows PowerShell, explicit `.venv` invocations look like:

```powershell
.venv\Scripts\python.exe tools\validate_specs.py
.venv\Scripts\python.exe -m compileall tools
.venv\Scripts\python.exe -m mkdocs build --strict
```

`mkdocs build --strict` treats warnings as build failures, which keeps broken links and configuration drift visible during review.

## Documentation Workflow

The documentation site is built on pull requests. On pushes to `main`, the workflow also prepares a GitHub Pages deployment artifact and runs the Pages deployment action.

If the repository has not yet enabled Pages publication, maintainers may need to configure GitHub Pages in repository settings and select "GitHub Actions" as the source.

## Generated Documentation

The current specification pages are manually written summaries. Generated pages from the JSON specifications are planned as future work so algorithm pages can be derived directly from the normative machine-readable source.
