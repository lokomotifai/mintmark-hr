# Normative verification

What this pack asserts about the world, where each assertion came from, and what
could not be confirmed. A claim with no record here is a claim nobody checked.

## Publicly listed and widely known Turkish companies

**Why it matters.** This pack invents employer names. The core's denylist is built
from the payment systems participant register, which lists banks, and the
insurance pack's extension lists insurers. Neither was built to catch a collision
with an industrial holding, a retailer, or a technology company, which is exactly
the shape of name an HR pack invents.

**What was done.** A compilation of 51 widely known Turkish corporates and
holdings was assembled and checked entry by entry, then folded into
`lexicons/denylist_extension.txt` on top of everything the banking and insurance
lists already carried. Every lexicon in this pack is scanned against the combined
list in required CI, and so is every rendered document in a real mint.

**Retrieved.** 2026-08-22.

**What could not be confirmed.** The exchange publishes the authoritative listing
of traded companies, and it was not available as a machine-readable public
endpoint from here. So the list used is a compilation, not the register. It is
enough to catch the collisions it contains. It is not enough to prove there are
none, and a manual read of the exchange's own company list belongs in the release
checklist alongside the same open item the insurance pack carries for insurers.

**A finding from building it.** The first cut of the list reduced every company
name to its distinctive part, so `Dogan Holding` became `dogan` and `Yildiz
Holding` became `yildiz`. Both are among the most common surnames in Turkey, and
both are drawn by the core's own surname lexicon. The list fired on the pack's own
synthetic people: four hits in a single baseline mint, none of them a real
collision.

A denylist that flags the pack's own data is a denylist somebody switches off, so
the rule changed. A one-word core is now checked against the core's given-name,
surname, province, and street lexicons, and a name whose distinctive part is an
ordinary Turkish word keeps the whole company name instead. Four names are carried
whole under that rule: Koc Holding, Dogan Holding, Yildiz Holding, and Opet.

The same rule is why `Toros Tarim` is listed as two words. `Toros` is the Taurus
mountain range, and an invented `Toros Lojistik` does not collide with a real
fertilizer producer, while the real producer is still covered.

## Everything the core already verified

This pack inherits the core's records without restating them: the VKN checksum
algorithm against two independent implementations over 200 000 inputs, the TCMB
bank code reserved for synthetic IBANs, the permanent UTC+3 offset for Turkey
against the IANA database, and the negative result that the Turkish numbering plan
reserves no fictional mobile range. See
[the core's record](https://github.com/lokomotifai/mintmark/blob/main/docs/normative-verification.md).

## Facts this pack deliberately does not assert

**Payroll amounts are not calibrated to any wage statistic.** Gross and net are
drawn from a log-normal table, and the net-to-gross relationship is a draw, not a
tax calculation. Nothing here models Turkish income tax, social security
contributions, or the minimum wage, and no figure in this pack should be read as
one. A pack that claimed otherwise would need a normative source per tax year and
would be wrong the moment the rates changed.

**Leave entitlements are not calibrated to the Labour Act.** Leave-day counts are
drawn from a declared distribution. They are not the statutory entitlement for a
given seniority, and they do not encode any accrual rule.

**Job titles and departments are invented, not drawn from a classification.**
There is a national occupational classification and this pack does not use it. The
titles are curated for readability in Turkish HR text, which is what the document
templates need.
