# Contributing

Thank you for considering a contribution. This is a declaration-and-data
repository, so most of what you will change is YAML rather than code.

## Sign your commits

Contributions are accepted under the Developer Certificate of Origin, version
1.1. There is no contributor license agreement. Every commit carries a sign-off
line matching the commit author:

    git commit -s -m "your message"

## This repository contains no engine code

That is the rule the family is built on, and it is enforced by a test. The only
Python here lives under `tests/` and imports nothing beyond the core's public
API. A helper that generates a lexicon belongs under `tools/`, produces committed
output, and is never imported by a test or run during a mint.

If a declaration cannot express what this pack needs, that is a core change. Open
an issue against the core repository and record the gap. Do not route around it
with a script: a pack that generates its own data has stopped being a pack.

## Before you open a pull request

    uv sync
    uv run mintmark packcheck .
    uv run pytest
    uv run python tools/mdlint.py .

`packcheck` runs against the vendored core wheel, so it works offline.

## Adding to a lexicon

Two things to know.

Every invented name is scanned against the real-institution denylist in required
CI. A collision fails the build and names both sides. A name that collides is
removed rather than defended.

After the first tagged release, adding an entry to an existing lexicon changes
the draw for every subsequent index and therefore changes emitted bytes for a
fixed seed. That makes it a major version bump, not a minor one, because it
breaks the reproducibility of every published manifest.

## Language rules for prose

Enforced by `tools/mdlint.py` in required CI, in both languages: sentence-case
headings, a banned promotional vocabulary, and no em dash or en dash anywhere.
Quoted third-party text is exempted with a marker that carries a reason.

`README.md` is canonical and `README.tr.md` is a full mirror, not a summary. A
change to one without the other fails review.

## What will be declined

Any Python outside `tests/` and `tools/`. Any dataset committed outside
`samples/`. Any real institution, brand, or person anywhere. Any calendar promise
in the README. Any compliance guarantee.
