# Origin and attribution

## Origin

This repository is a sector pack in the Mintmark family, which is part of the
lokomotifai product family. It carries declarations and data. The engine that
reads them lives in the `mintmark` repository.

## Attribution register

| Item | Source | What is used | Terms |
| --- | --- | --- | --- |
| Mintmark core engine | The `mintmark` repository | A vendored wheel under `vendor/`, so that required CI runs offline | Apache-2.0, same organization |
| Personal-data label taxonomy | The hushmark-tr closed v0.1 label set, through the core's pin | The twelve NER label names | Same organization |
| Code of conduct | Contributor Covenant | Adapted text | CC BY 4.0, attribution retained in the file |
| Real-institution denylist | The core's list, built from a public payment systems participant register | Inherited in full and extended | Public register, source-noted with a retrieval date |

## Data provenance

This repository declares what to generate. It ingests nothing. No real personal
data, no customer data, and no production data of any kind was used to build
anything here.

Every invented name is scanned against the real-institution denylist in required
CI. Factual reference data, where any is used, carries an inline source note with
the public source and the retrieval date at the point of use.

## Adding an entry

A new vendored artifact, a borrowed text, or a factual list adds a row above in
the same change that introduces it. An entry added later than the thing it
describes records what was believed rather than what was checked.
