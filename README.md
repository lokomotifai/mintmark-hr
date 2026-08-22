<p align="center">
  <img src="assets/brand/mintmark-logo.svg" width="112" height="112" alt="Mintmark">
</p>

<h1 align="center">Mintmark human resources</h1>

<p align="center"><strong>Turkish workforce and payroll data, including the two surfaces most people would rather not model.</strong></p>

<p align="center">
  Employees with their position history, leave and payroll,<br>
  and the free text where health and criminal record mentions actually appear.
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark-hr/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/lokomotifai/mintmark-hr/ci.yml?branch=main&amp;style=flat-square&amp;label=CI"></a>
  <img alt="Zero engine code" src="https://img.shields.io/badge/engine%20code-none-3C873A?style=flat-square">
  <img alt="18 of 18 coverage targets met" src="https://img.shields.io/badge/coverage%20targets-18%2F18-3C873A?style=flat-square">
  <img alt="No release published" src="https://img.shields.io/badge/release-not%20published-3B3F46?style=flat-square">
  <a href="LICENSE"><img alt="Apache-2.0 license" src="https://img.shields.io/badge/license-Apache--2.0-3B3F46?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark"><img alt="Requires the Mintmark core" src="https://img.shields.io/badge/core-%3E%3D0.1%2C%3C0.2-17191F?style=flat-square"></a>
  <img alt="Seven record types" src="https://img.shields.io/badge/record%20types-7-17191F?style=flat-square">
  <img alt="Three document families" src="https://img.shields.io/badge/document%20families-3-17191F?style=flat-square">
  <img alt="26 fictional employer names" src="https://img.shields.io/badge/fictional%20employers-26-D11F26?style=flat-square">
  <img alt="Two sensitive boundaries" src="https://img.shields.io/badge/boundaries-health%20%2B%20accusatory-C98A2B?style=flat-square">
  <a href="README.tr.md"><img alt="Türkçe" src="https://img.shields.io/badge/belgeler-Türkçe-D11F26?style=flat-square"></a>
</p>

<p align="center">
  <a href="#mint-it-yourself"><strong>Mint it yourself</strong></a>
  ·
  <a href="#the-two-boundaries-this-pack-holds"><strong>The two boundaries</strong></a>
  ·
  <a href="#three-things-the-contract-decided-for-us"><strong>What the contract decided</strong></a>
  ·
  <a href="README.tr.md"><strong>Türkçe</strong></a>
</p>

---

> **This repository contains no engine code.** It is declarations and data. The
> engine that reads them lives in
> [mintmark](https://github.com/lokomotifai/mintmark) and is pinned here by a
> version range with a closed upper bound.

Every Turkish company holds employee data, and almost none of it can move into a
test environment. Payroll carries bank details. Leave records carry sick days.
Recruiting carries criminal record checks. This pack declares that data, and the
engine mints it: deterministic, span-labeled, and sealed by a manifest.

**Version 0.1, pre-release. No release has been published and no reference
dataset exists yet to download.** What is true today: `packcheck` passes against
the pinned core, the test suite passes, and the evaluation recipe meets every one
of its eighteen coverage targets.

> [!IMPORTANT]
> **What this pack is not.** It is not anonymization of your HR system; it ingests
> none. It is not a compliance guarantee and not a legal safe harbor. It is **not
> clinical data**: health stays at category granularity by design. It **makes no
> accusation about anybody**, synthetic or otherwise: the criminal record surface
> records that a document was requested, never what it contained. Payroll amounts
> model no tax code and no minimum wage. Generated phone numbers can coincide with
> assigned ones, because the Turkish numbering plan reserves no fictional range.
> This data is for testing systems. It is never for contacting anyone.
> What this
> does and does not mean under Turkish data protection law is set out in
> [docs/kvkk.md](docs/kvkk.md).

## What is in here, and what is not

![Diagram of the human resources pack's record types: employee with a national identity number, a birth date drawn from an eighteen to sixty five age window and a manager name that is a draw rather than a reference; position history; leave record whose type column carries no label at all; and payroll entry with a labeled anomaly kind. Three document types below in red, performance note, recruiter note and hr request, each producing a label sidecar, with the recruiter note deliberately pointing at no parent. Two bands across the bottom state the health boundary and the accusatory boundary](assets/readme/record-map.png)

<p align="center"><sub><a href="assets/readme/record-map.svg">View the accessible SVG source</a></sub></p>

| In here | Not in here |
| --- | --- |
| Seven record types, three of which are free text | Any engine code. The only Python is under `tests/` and `tools/` |
| Payroll with gross, net, an IBAN and a labeled anomaly kind | Any tax calculation. Net is a draw, not a deduction |
| A criminal record surface, reached through reference checks | Any statement about what a record contains. See below |
| 26 invented employer names, scanned against a real-company list | Any real company. The scan runs on every mint in CI |

## The two boundaries this pack holds

Most packs in this family hold one sensitive surface. This one holds two, and both
are held by a control rather than by review, because review gets tired and a list
does not.

### Health stays at category granularity

Health reaches HR text in two ordinary ways: a leave request that gives a reason,
and a performance conversation that mentions a working arrangement. Both are in
here. A condition class and nothing more: no diagnosis, no clinical finding, no
treatment, no medication, no prognosis.

Every health span draws from the core's curated condition-class descriptors, and
`lexicons/clinical_denied_tr.txt` lists the vocabulary this pack refuses. A test
scans every rendered document against it. The failure mode is silent, which is
why the control exists: a template that drifts into clinical detail still renders,
still labels, and still passes every other check.

### The criminal record surface stays procedural

A reference check is a process. This pack's documents record that a criminal
record document was **requested**, **received**, or is **pending**. They never
record what it contains.

Text asserting that a person committed an offence, was convicted, or is under
investigation is an accusation about a person, and a synthetic person is still a
person-shaped claim. A model trained on text that convicts synthetic people learns
to produce that text about real ones. So
`lexicons/accusatory_denied_tr.txt` lists 43 phrases this pack refuses,
covering conviction, allegation, named offence classes, and workplace conduct
framed as an accusation. Every rendered document is scanned against it, and a test
plants a denied phrase to prove the list still catches one.

## Three things the contract decided for us

None of these is an oversight, and all three are the kind of thing a reader will
otherwise assume is a bug.

**A leave type carries no label, including the sick-leave code.** `leave_record.type`
is a structured enum, and the last of its values is `raporlu`. Labeling it HEALTH
would teach a detector that a seven-character enum value in a database column is a
health disclosure, and every evaluation run against the dataset would then be
scoring detectors on whether they flag codes. The health signal worth detecting
lives in the document bodies, where a condition class appears in running Turkish
text and a span points at it.

**A recruiter note points at no employee.** Its subject is a candidate, and a
candidate is by definition not yet an employee. A parent reference here would
encode the opposite claim into every dataset the pack produces. The type is an
orphan in the record graph, which is the honest shape of the data.

**The manager name corresponds to no employee record.** The pack contract has no
self-reference, so `employee.manager_name` is a surname lexicon draw. That is a
real modeling loss for anyone testing org-chart traversal, and it is stated here
rather than discovered after ingest.

## Mint it yourself

```bash
uv tool install mintmark
git clone https://github.com/lokomotifai/mintmark-hr
cd mintmark-hr

mintmark packcheck .
mintmark mint --pack . --recipe workforce-baseline --seed 20261101 --out ./run
mintmark verify ./run
```

One recruiter note, as emitted:

```
Aday degerlendirme notu. Aday Mehmet Demir, basvurdugu pozisyon
icin teknik_degerlendirme asamasinda degerlendirildi. Iletisim +90
575 131 44 23, eposta kullanici4843.7421@example.net. Onceki
isvereni Anka Lojistik. Teknik yetkinlik beklentiyi karsiliyor
olarak notlandi. Surec sonraki asamaya gecti.
```

That is the first record in [`samples/recruiter_note.jsonl`](samples/recruiter_note.jsonl),
not an illustration written for the README. A test compares the two.

## The evaluation set

`pii-eval` declares a coverage target for every label and meets all eighteen.

| Label group | Target | Achieved |
| --- | --- | --- |
| PERSON, ADDRESS, ORG, DOB | 300 each | 3000 each |
| The eight special categories | 300 each | 726 to 773 |
| TCKN, VKN, IBAN, PAN, PHONE, EMAIL | 500 each | 3000 each |

Eight special-category labels at 300 spans each is 2400 injections. The baseline
recipe runs its special rate at 0.06, which across baseline document volume
produces nowhere near that, and raising the baseline rate to reach the target
would misrepresent how often special categories actually appear in HR text. So the
evaluation twins are separate record types with their own template family at rate
one, two special slots each, spread evenly across the labels. Three document
families rather than the insurance pack's two makes the arithmetic comfortable
here.

## The three recipes

| Recipe | Shape | For |
| --- | --- | --- |
| **workforce-baseline** | 6 000 employees, 11 000 position rows, 24 000 leave records, 72 000 payroll entries, and 11 000 documents | Filling a test environment with something that behaves like a workforce |
| **pii-eval** | 3 000 documents, every label above its target | Measuring a detector on Turkish HR text |
| **anomaly-mix** | The baseline plus a labeled anomaly field on every payroll entry | Scoring a monitoring system against ground truth |

### A limitation of anomaly-mix, stated plainly

Every payroll entry carries `anomaly_kind` and `is_anomaly`, and the two never
disagree. But the kinds are **per-row labels drawn at declared rates, not genuine
temporal or cross-record structures**. A real payroll anomaly is a month that
breaks a pattern across an employee's other months; here it is a label on one row.

That is a limit of the pack contract rather than an oversight: each field is drawn
from an independent stream, so a pack cannot declare a pattern that correlates
rows. Use this recipe to check that your pipeline carries labels through
correctly. Do not use it to measure whether a detector finds real patterns.

## A denylist that fired on our own people

Worth telling, because it is what a control is for and because the fix changed the
rule rather than the symptom.

This pack invents employer names, and neither the core's bank list nor the
insurance pack's insurer list was built to catch a collision with an industrial
holding. So a compilation of 51 widely known Turkish corporates went into the pack
denylist, each name reduced to its distinctive part.

That reduction turned **Dogan Holding** into `dogan` and **Yildiz Holding** into
`yildiz`. Both are among the most common surnames in Turkey, and both are drawn by
the core's own surname lexicon. The list fired four times on a single baseline
mint, every hit a synthetic employee rather than a real company.

A denylist that flags the pack's own data is a denylist somebody switches off, so
the rule changed: a one-word core is now checked against the core's given-name,
surname, province, and street lexicons, and a name whose distinctive part is an
ordinary Turkish word keeps the whole company name. The same rule is why
`Toros Tarim` is listed as two words, so an invented `Toros Lojistik` does not
collide while the real fertilizer producer is still covered.

One limitation is worth stating: the exchange publishes the authoritative listing
of traded companies and it was not available as a machine-readable public endpoint
from here, so the list used is a compilation rather than the register. A manual
read of the exchange's own list belongs in the release checklist. The full record
is in [docs/normative-verification.md](docs/normative-verification.md).

## Repository map

```
pack.yaml           identity, the core pin, the allowed identifier policies
fields/             one file per record type, in generation order
recipes/            workforce-baseline, pii-eval, anomaly-mix
templates/          baseline sets, and the separate evaluation sets
lexicons/           invented employers, titles and departments, the denylist,
                    and the clinical and accusatory vocabularies this pack refuses
samples/            fifty records per type, regenerated from a fixed seed
vendor/             the core wheel required CI runs against, recorded by checksum
tests/              the conformance suite, including both boundary checks
docs/               the reference dataset record, the verification record, and
                    what this pack does and does not claim under KVKK
```

## Develop the repository

```bash
uv sync
uv run mintmark packcheck .
uv run pytest
uv run python tools/mdlint.py .
```

All of it runs offline against the vendored core wheel.

## Project status

Version 0.1, pre-release. No release, no published dataset. The reference datasets
are declared in [docs/reference-datasets.json](docs/reference-datasets.json) with
their settled seeds.

This pack carries one governance checkpoint the other packs do not: the baseline
special rate and the full special-category template subset need a recorded
sign-off before any public launch surface exists. Publishing the reference
datasets and confirming the dataset license are the usual external checkpoints on
top of that.

## Community contract

Contributions under the Developer Certificate of Origin 1.1, no contributor
license agreement. See [CONTRIBUTING.md](CONTRIBUTING.md),
[GOVERNANCE.md](GOVERNANCE.md), and [SECURITY.md](SECURITY.md).

`README.md` is canonical and [README.tr.md](README.tr.md) is a full mirror.

## License and trademark

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). The license grants no
right to the Mintmark name or logo; see [TRADEMARKS.md](TRADEMARKS.md).

Reference datasets are licensed **CC BY 4.0**: use them for anything, including
commercially, and credit the source. Every dataset carries its own credit line in
`MINTMARK.json` and `mintmark verify` prints it, so nothing has to be assembled by
hand. See [LICENSE-DATASETS.md](LICENSE-DATASETS.md). Pending legal confirmation;
nothing here states it as settled.

<p align="center"><sub>Part of the Mintmark family: <a href="https://github.com/lokomotifai/mintmark">the engine</a> · <a href="https://github.com/lokomotifai/mintmark-banking">banking</a> · <a href="https://github.com/lokomotifai/mintmark-insurance">insurance</a></sub></p>
