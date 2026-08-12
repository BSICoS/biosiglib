# Contributing to Biosiglib

## Local setup

Create a repository-local virtual environment and install the development dependencies:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## Validation

Run these checks before submitting a change:

```powershell
.venv\Scripts\python.exe -m compileall tools
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe tools\validate_specs.py
.venv\Scripts\python.exe -m mkdocs build --strict
git diff --check
```

## Method changes

The JSON specification and shared validation cases define behavior. A method page explains its purpose, expected data, scientific rationale, interpretation, and limitations. Repeated interface tables, references, and technical links are inserted from machine-readable sources during the documentation build.

When adding or changing a method:

1. update its specification and meaningful validation cases;
2. update the corresponding page and field descriptions under `docs/methods/`;
3. keep scientific references in `references/references.json`;
4. run the full validation set above.

Do not include implementation history, compatibility commentary, release planning, or contributor workflow in public method pages. Link to source code or technical artifacts when their contents do not need to be restated for a user.
