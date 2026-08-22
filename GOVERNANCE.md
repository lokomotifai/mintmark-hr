# Governance

This file describes how decisions are made in this repository today, not how we
would like them to be made eventually.

## Current state, stated plainly

Founder-led, one maintainer. Independent maintainer review is not currently
possible. That is a real limitation, recorded here rather than disguised by a
review process with one participant.

## What this repository decides, and what it does not

A sector pack is downstream of two things it does not control: the core engine's
contract, and the family charter. Most of what looks like a decision here was
made elsewhere.

| Class | Examples | Who decides |
| --- | --- | --- |
| Pack content | A lexicon entry, a template's wording, a distribution parameter | Maintainer merge |
| Pack shape | A record type, a recipe, a coverage target | Maintainer decision recorded in the changelog |
| Contract | Field types, generator kinds, the label taxonomy, identifier policy semantics | Not decided here. These belong to the core engine |
| Settled family decision | Topology, sector order, licensing, the no-model rule | Not decided here. These come from the family charter |
| External authority | Repository creation, releases, the reference datasets, any sentence referencing a regulation | Not a maintainer decision. Requires the owner's recorded approval |

## Founder-led merge rule, and the control that replaces it

While there is one maintainer, that maintainer may merge their own changes. The
compensating control is that no merge passes without required CI green, and CI
includes the conformance run, the denylist scan, and the coverage feasibility
check. The checks stand between a defect and the main branch, not the reviewer.

When a second maintainer joins, this rule is removed and two-party review applies
to anything beyond pack content.

## Releases

A release carries reference datasets, which are the thing consumers actually
take. It is cut by a maintainer, is immutable once published, and sits behind the
owner's recorded approval. A release may not be tagged while `packcheck` fails.

## Continuity

If the sole maintainer becomes unavailable, this repository is archived rather
than transferred silently. Datasets already published stay verifiable, because
verification needs only the artifacts and a core in the pinned range.
