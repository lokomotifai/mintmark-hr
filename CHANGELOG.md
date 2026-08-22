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

A security and conformance review of this pack and its two siblings found one
defect repeated across them: a field declared here, validated by the schema,
asserted by a test in this suite, and read by nothing. Every item below closes one
of those. The release moves emitted bytes for a fixed seed, which is a major
version event under this pack's own rule, so the samples and the reference seeds
produce different data than 0.1.x did. Datasets already attached to the previous
release stay valid and reproduce with the core and pack versions their own
manifests record.

### Fixed

- **The pack allowed the validator identifier policy.** Every recipe declared
  `identifier_policy: safe` and a test asserted it, and the engine read neither:
  the effective policy came from the command line, gated only by
  `allowed_identifier_policies` here, which listed `validator`. So a recipe pinned
  to `safe` minted checksum-valid identifiers whenever a caller passed the flag.
  The allowlist is now `[safe]`, and core 0.2.0 treats a recipe pin as binding.
  This matters most for TCKN and VKN: an IBAN from this family carries a bank code
  no institution holds and a PAN begins with a major industry identifier no card
  network uses, but a national identity number has no unassignable range, so a
  checksum-valid one cannot be distinguished from an issued one.

- **The evaluation set measured memorization.** Every `*_eval` template was the
  same carrier sentence with a different pair of special categories on the end,
  and the evaluation recipe runs its special rate at one, so every optional was
  always present. Three thousand documents came out of twenty-four distinct
  shapes, with each entity at a fixed offset behind a fixed cue word. A word list
  and six regular expressions scored near perfectly on that, which says nothing
  about how a detector behaves on real text. The evaluation templates now vary
  their openings, their cue words, which blocks appear, and their closings, and a
  test fails the build if the shape count collapses again.

- **The denylist scan ran against the wrong list.** The core list is the payment
  systems participant register, so it holds banks and nothing else. This pack
  scans its lexicons, its templates, and its minted output against the pack
  extension instead, and the extension is now one list across the family: the
  core's banks, every real insurer, and every real holding and industrial company
  a fictional name in any of these packs could land on.

- **Lexicons that reached no generator.** `employers_fictional` and `departments_tr` were shipped,
  source-noted, denylist-tested, guarded by their own tests, and absent from every
  byte this pack emitted, because a pack lexicon is only reachable through a field
  generator and nothing named them. They are wired now, through the new
  `entity_lexicons` map in `pack.yaml` and the new `{lex:...}` template slot, and
  core 0.2.0 refuses to load a pack that ships an unreachable one.

- **The private-corpus canary failed every external pull request.** GitHub does
  not give repository secrets to a workflow triggered from a fork, so the required
  check went red on every outside contribution, and the shape that would have
  fixed it hands the secret to code the fork controls. The scan now runs on the
  push to main, where the secret exists and where it is the last gate before
  anything is published. A pull request proves the tripwire is still armed instead:
  the scanner has to refuse a wrong canary and a missing one.

- **The core pin workflow compared nothing.** It printed instructions, declared
  `issues: write`, and opened no issue, so a green run read as evidence about an
  artifact nobody outside this repository had ever seen. It now fetches the digest
  PyPI publishes for the vendored version and compares, and opens one issue per
  version on a mismatch.

### Changed

- **The core moves from 0.1.3 to 0.2.0**, which honours template weights, lets a
  pack contribute entity surfaces, composes person names from the core name pools
  rather than listing twelve, widens the special-category surface lists, always
  runs the checksum sweep in `verify`, and fails verification on a coverage target
  the mint did not meet. `requires_core` follows to `>=0.2,<0.3`.

- **The README states what a document does not tell you about its record.** An
  identifier in a document body is a fresh draw, so a document linked to a record
  names somebody else. The spans are still right; what is ruled out is any test
  that needs the two sides to agree. A test holds the disclosure in both languages.

### Removed

- **The `anomaly-mix` recipe.** In all three packs it was the baseline recipe with
  a different `name` and nothing else: the same counts, the same window, the same
  document mix, the same special rate. The anomaly rates it appeared to control
  live in field declarations, which a recipe cannot reach, so the name promised
  something the engine cannot deliver. The anomaly fields and their stated
  limitation stay on the baseline recipe, where they always were.

- **`doc_mix` from every recipe.** It restated what the record counts already fix,
  and core 0.2.0 no longer defines it.

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
