# Third-party notices

## Vendored core engine

`vendor/` carries a built wheel of the Mintmark core engine so that required CI
runs offline, without resolving anything from a network at check time. Its
SHA-256 is recorded in `vendor/CHECKSUMS`, and a separated, network-labeled
workflow confirms that the vendored artifact matches the core repository at the
pinned tag.

The core is Apache-2.0 and comes from the same organization. Its own third-party
notices travel with it.

## Test dependencies

Test dependencies are not redistributed by this repository. They are pinned in
`uv.lock` and listed in `pyproject.toml`.

## Data

Every lexicon here is invented for this project. Where factual reference data is
used, it carries an inline source note with its public source and retrieval date
at the point of use. No shipped data asset carries third-party terms as of this
revision.
