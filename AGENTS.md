# AGENTS

Persistent project rules for coding agents working in Biosiglib:

1. Biosiglib is the language-independent contract for public methods implemented independently by Biosigpy and Biosigmat. JSON specifications and shared conformance cases are normative.
2. A downstream `biosiglib.lock` declares total conformance with one exact commit. Partial support belongs in issues or pull requests, not repository metadata.
3. Preserve normative scientific behavior across languages while allowing idiomatic APIs, internal structures, exceptions, indexing, and plotting.
4. Do not change formulas, filtering direction or phase, units, defaults, NaN behavior, physiological meaning, edge cases, or reference results without explicit maintainer review.
5. Canonical structured IDs use `snake_case`. ECG timing uses `r_wave_*`, not `r_peak_*`. Keep generic interval methods modality-neutral unless their contract says otherwise.
6. Add shared cases for meaningful numerical behavior, cross-language ambiguity, and regressions. Do not multiply cases for trivial validation already stated unambiguously in a specification.
7. Use JSON for structured metadata and small values, and CSV for signals, annotations, and tabular numerical data. Conformance comparisons use absolute tolerances and explicit NaN comparison.
8. Every public method has one page under `docs/methods/`. It should help a user choose, call, and interpret the method. Keep implementation history and development-process commentary out of public documentation.
9. Method interfaces, references, and technical links are injected during the MkDocs build. Do not commit derived Markdown or duplicate the normative contract in prose.
10. Keep specifications, method pages, field descriptions, references, and cases consistent. Scientific authorship is recognised through original publications; software authorship belongs to the project maintainers.
11. Use English for filenames, code, comments, structured fields, and technical documentation. All repositories use GPL-3.0 and independent semantic versioning.
12. Use the repository-local `.venv` and the commands in `CONTRIBUTING.md`. Do not commit virtual environments or caches.
13. Avoid new generators, resource APIs, databases, cross-language runners, or repositories unless they solve a demonstrated problem.
