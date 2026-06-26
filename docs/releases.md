# Releases

Biosiglib uses independent semantic versioning with `MAJOR.MINOR.PATCH`. Biosigmat and Biosigpy also use their own independent versions. A downstream implementation release declares which Biosiglib release and commit it conforms to.

## Release Semantics

A Biosiglib release captures the current language-independent source of truth:

* JSON specifications;
* schemas;
* fixture catalogs and fixture files;
* conformance cases and expected outputs;
* validation tooling;
* release propagation metadata.

Changes to normative specification behavior may require implementation updates and an appropriate semantic-version increment. Informative documentation changes can usually be released without changing implementation behavior.

## Propagation

The expected propagation path is:

1. Biosiglib release.
2. Automated Biosigmat propagation pull request.
3. Automated Biosigpy propagation pull request.

The downstream propagation pull requests update `conformance.json` in the implementation repositories. Those pull requests make the new Biosiglib release visible to implementation maintainers and provide a review point before implementation repositories declare support for the new source of truth.

## Documentation Publication

The documentation workflow builds the MkDocs site on pull requests. On pushes to `main`, it uploads the built site for GitHub Pages deployment. Repository settings may still need GitHub Pages enabled with "GitHub Actions" selected as the build and deployment source before the first publication succeeds.
