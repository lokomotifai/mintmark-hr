# Samples

Up to fifty records per type, committed so that a reader can see the shape of
this pack's output without minting anything. The counts follow the pack's
relationship bounds: every employee must carry its declared minimum of leave
records and payroll entries, so the employee-anchored types are minted at four
parents and at what four parents require, while the unanchored recruiter notes
are minted at fifty.

These regenerate exactly:

```bash
mintmark mint --pack . --recipe workforce-baseline --seed 1 \
  --records employee=4 --records position_history=4 \
  --records leave_record=8 --records payroll_entry=48 \
  --records performance_note=4 --records recruiter_note=50 \
  --records hr_request=4 \
  --out ./regenerated
```

A test compares the committed files against a fresh run by digest, so a sample
that drifts from the declarations fails the build rather than quietly
misrepresenting them.

These are samples, not a dataset. They carry no manifest, so nothing binds them
to a provenance claim, and nothing here should be cited as a reference dataset.
The evaluation twins are absent on purpose: the baseline recipe produces none of
them, and an empty committed file represents nothing while looking like coverage.
