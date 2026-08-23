# Changelog

All notable changes to this pack are documented here. The format follows
[keep a changelog](https://keepachangelog.com/en/1.1.0/), and this pack uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

What is under semantic versioning here: the record types and their fields, the
recipe names and shapes, the label coverage a recipe promises, and the byte-level
output for a fixed seed. A change that alters emitted bytes for a fixed seed is a
major version event even when no field moved, because it breaks the
reproducibility of every published manifest.

The pack version is one of the six inputs every generation stream is derived
from, so raising the version is itself such a change. Version and content
correspond exactly, which is the point. The pack digest is a separate record of
which declarations produced a dataset and seeds nothing.

## 0.2.0 - 2026-08-23

### Security

- Require the audited Mintmark 0.3.1 core, whose manifest budget verifies the
  pack's 72,000 payroll rows; allow only the safe identifier policy,
  and bind the vendored wheel to an immutable source commit and checksum.
- Remove ignored recipe controls, classify address and employer entity lexicons,
  and make every declared lexicon reachable from generation.
- Remove the byte-identical `anomaly-mix` recipe, whose name falsely implied it
  could alter anomaly rates fixed by the payroll declaration.
- Pin CI actions, keep secrets away from pull-request code, and make the canary
  scanner fail closed on links, nested archives, gzip, and resource exhaustion.
- Scan decoded templates and every rendered reference document family against
  clinical and accusatory language controls, including Unicode obfuscations.

## 0.1.1 - 2026-08-22

### Added

- Dataset terms travel with the data. `pack.yaml` declares `dataset_license` and
  the engine writes it into every manifest along with a credit line, so a
  downloaded dataset says under what terms it may be used instead of leaving that
  to a README nobody downloads.
- Turkish mirrors of every community document: contributing, conduct,
  governance, security, and support. A README mirror alone left a Turkish
  contributor reading the project's own rules in a second language.
- `docs/kvkk.md` and its Turkish mirror: what this pack produces and what it does
  not claim under law 6698, including a table mapping the special-category
  labels to the categories the law enumerates and naming the three it does not
  cover.
- `CITATION.cff`, issue and pull request templates, `CODEOWNERS`, and grouped
  monthly dependency updates.

### Changed

- The dataset license moved from CC0-1.0 to CC-BY-4.0. CC0 would have let a
  published dataset be resold with the provenance removed and no credit given
  anywhere. Attribution keeps the enterprise path open, because the intended
  reader of this pack is a commercial one, while making the source impossible to
  strip silently.
- Birth dates are drawn from an age window of eighteen to sixty five, rather
  than from the recipe window. Employment gives the window a floor and a ceiling
  the other packs do not have.

### Notes

Nothing has been released. Beyond the usual checkpoints, this pack carries one
the others do not: the baseline special rate and the full special-category
template subset need a recorded governance sign-off before any public launch
surface exists.

### About this version number

This is the first published release and it is not 0.1.0. The pack version is one
of the six inputs every generation stream is derived from, so the declaration
change that added the dataset license moved the version with it. Version 0.1.0
existed in this repository and was never published; nothing reproduces from it.
