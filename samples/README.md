# Samples

Fifty records per type, committed so that a reader can see the shape of this
pack's output without minting anything.

These regenerate exactly:

```bash
mintmark mint --pack . --recipe workforce-baseline --seed 1 \
  --records employee=50 --records position_history=50 \
  --records leave_record=50 --records payroll_entry=50 \
  --records performance_note=50 --records recruiter_note=50 \
  --records hr_request=50 \
  --out ./regenerated
```

A test compares the committed files against a fresh run by digest, so a sample
that drifts from the declarations fails the build rather than quietly
misrepresenting them.

These are samples, not a dataset. They carry no manifest, so nothing binds them
to a provenance claim, and nothing here should be cited as a reference dataset.
The evaluation twins are absent on purpose: the baseline recipe produces none of
them, and an empty committed file represents nothing while looking like coverage.
