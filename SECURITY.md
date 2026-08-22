# Security policy

## Report privately

Use GitHub private vulnerability reporting on this repository's security tab. If
that route is unavailable, email
[fatih@komunite.com.tr](mailto:fatih@komunite.com.tr?subject=Mintmark%20security%20contact)
and ask for a secure channel. Do not open a public issue to ask whether a report
is in scope; ask privately instead.

## Response targets

These are targets, not contractual service levels:

- acknowledgement within three business days;
- initial triage within seven business days; and
- a proposed remediation or coordination plan for a confirmed high-impact report
  within fourteen business days.

## Security boundaries

This repository contains declarations and data. It executes nothing: the engine
that reads it lives elsewhere. Its threat model follows from that.

**In scope.** A declaration that causes the core engine to behave unsafely. A
lexicon entry that names a real institution, person, or brand. A template that
produces a checksum-valid identifier under a safe policy. A published reference
dataset whose checksums do not match its manifest. Anything in this repository
that would let private material reach a release artifact.

**Out of scope.** The realism of the generated data, which is a quality question.
Coincidence between a generated phone number and an assigned one, which is
documented as a known limitation because the Turkish numbering plan reserves no
fictional range. Anything a consumer does with a dataset after downloading it.

**Explicitly not a vulnerability.** That the core's validator policy produces
checksum-valid identifiers. That is its documented purpose, it is opt-in, and
every such dataset carries a warning in its manifest. Reference datasets from
this repository are always minted with the safe policy.

## What this repository does not claim

No compliance guarantee under any regulation. Not anonymization of real data.
Using these datasets does not by itself make any downstream system lawful.
