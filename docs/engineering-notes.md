# Engineering notes

Decisions a reader of the declarations would otherwise have to reverse engineer,
and the reasoning that would be lost if only the outcome were recorded.

## The core wheel is bound to an immutable source revision

`pack.yaml` requires Mintmark `>=0.3.1,<0.4`, while required CI installs the
vendored `mintmark-0.3.1-py3-none-any.whl` whose SHA-256 is recorded in
`vendor/CHECKSUMS`. The separated network workflow checks out core commit
`8017e894210c1f3649e66b0ac0fe8e0af18d0a3b`, builds it with its locked backend,
and byte-compares that independently sourced wheel with the vendored artifact.
Repository-local checksums establish integrity; the immutable core checkout and
reproducible comparison establish provenance.

## Why a leave type carries no label

`leave_record.type` is a structured enum: `yillik`, `mazeret`, `ucretsiz`,
`raporlu`. It carries `pii_label: none`.

The last of those values is a sick-leave code, and the instinct is to label it
HEALTH. That instinct is wrong here, and the reason is what the dataset is for.
A HEALTH span on the literal string `raporlu` teaches a detector that a
seven-character enum value in a structured column is a health disclosure. Every
evaluation run against such a dataset would then score a detector on whether it
flags database codes.

The health signal this pack exists to exercise lives in the document bodies,
where a person's condition class appears in running Turkish text and a span
points at it. That is the thing worth detecting. A test asserts the label stays
`none`, so a later edit has to argue with a test rather than quietly flip it.

## Why a recruiter note has no parent

Every other document type in this pack points at an employee. A recruiter note
does not, and that is deliberate: its subject is a candidate, and a candidate is
by definition not yet an employee. Giving the type a parent reference would
encode the opposite claim into every dataset the pack produces, and a downstream
consumer joining on it would silently be joining candidates to unrelated staff.

The cost is that the type is an orphan in the record graph. That is the honest
shape of the data.

## Why the manager name is a draw and not a reference

`employee.manager_name` is a surname lexicon draw. The pack contract has no
self-reference: a record type cannot point at itself, because references resolve
against parents generated earlier and a type is not its own parent.

So the manager named on an employee corresponds to no employee record in the
dataset. That is a real modeling loss for anyone testing an org-chart traversal,
and it is stated in both READMEs rather than discovered after ingest. A test
holds the line because a reader who does not know the constraint will try to
"fix" it into a reference.

## The accusatory boundary, and why it needs its own list

The CRIMINAL label is in the pinned taxonomy and this pack reaches it through the
one place it naturally appears in HR text: a reference check.

The boundary is procedural. A document may record that a criminal record document
was **requested**, **received**, or is **pending**. It may never record what the
document contains. Text asserting that a person committed an offence, was
convicted, or is under investigation is an accusation about a person, and a
synthetic person is still a person-shaped claim. A model trained on text that
convicts synthetic people learns to produce that text about real ones.

Two controls hold it, the same shape as the health boundary:

- Every CRIMINAL span draws from the core's curated descriptors, which are
  written as document names rather than allegations.
- `lexicons/accusatory_denied_tr.txt` lists the vocabulary this pack refuses, and
  a test scans every rendered document against it.

The health boundary's list is inherited from the insurance pack unchanged, since
the constraint is identical and two divergent copies of one rule is how a rule
stops being one.

## Why the evaluation templates are a separate family

Eight special-category labels at 300 spans each is 2400 injections. The baseline
recipe runs `special_rate` at 0.06, which across the baseline document volume
produces nowhere near that. Raising the baseline rate to reach the target would
misrepresent how often special categories actually appear in HR text, which is
the whole point of the baseline.

So the evaluation twins are separate record types with their own template family
at `special_rate: 1`, two special slots per template, spread evenly across the
eight labels. The baseline recipe emits zero of them and the evaluation recipe
emits zero baseline documents. Three document families rather than the insurance
pack's two makes the arithmetic comfortable here.

## Why birth dates carry an age window

`birth_date` used to be a plain `datetime_window` draw, which meant every employee
in a dataset describing 2026 was also born in 2026. Nothing in the suite caught
it: the field is a valid date, the label is right, the span aligns, the manifest
verifies. It is only wrong to a reader, which is the one check that had not run.

Finding it here changed the core. `datetime_window` now accepts an optional
`age_years: [low, high]` and draws from the span that would give a person that age
at the start of the recipe window. The parameter is optional and a field that
omits it behaves exactly as before, so no other declaration in the family had to
move. This pack declares `[18, 65]`, since employment gives the window a floor and
a ceiling the other packs do not have.

## Regenerating the samples

    mintmark mint --pack . --recipe workforce-baseline --seed 1 \
      --records employee=4 --records position_history=4 \
      --records leave_record=8 --records payroll_entry=48 \
      --records performance_note=4 --records recruiter_note=50 \
      --records hr_request=4 \
      --out ./regenerated

Then copy the JSONL files into `samples/`. The freshness test compares by bytes,
so a drift fails the build.

Do not commit a sample file that is empty. The evaluation twins produce nothing
under the baseline recipe, and an empty committed file represents nothing while
looking like coverage.

## Adding to a lexicon after the first release

It changes the draw for every subsequent index, which changes emitted bytes for a
fixed seed, which breaks the reproducibility of every published manifest. That
makes it a major version bump.

Before the first tagged release it is free. After, it is a decision.

## A version bump changes every emitted byte

The pack version is one of the six inputs the engine derives every generation
stream from, alongside the seed, the engine's major version, the pack name, the
recipe name, and the site path. So raising `version` in `pack.yaml` changes every
value in every record for a fixed seed, and the sample freshness test fails until
the samples are regenerated.

That reads like a bug the first time it happens. It is the opposite: version and
content correspond exactly, so two datasets carrying the same pack version cannot
differ, and nobody can quietly change what a version emits. The cost is that a
bump is never free for anyone holding a published manifest, which is the reason
the family treats one as a decision rather than a formality.

The pack digest is a separate thing and does not seed anything. It records which
declarations produced a dataset, so a consumer can tell whether the pack they
hold is the pack it came from. An earlier note here said the version reached the
streams by way of the digest. That was wrong, and worth correcting rather than
quietly deleting: it is the kind of plausible mechanism somebody would go on to
reason from.
