"""The pack's conformance suite.

Green here means: the declarations are valid under the strict loader, a mint
produces the shapes the brief describes, no invented name collides with a real
company, the recipes can satisfy the coverage they promise, and both sensitive
boundaries this pack owns are held by a control rather than by review.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from mintmark.annotate import ALL_LABELS
from mintmark.lexicons import load as load_denylist
from mintmark.lexicons import parse as parse_denylist
from mintmark.mint import asset_dir, mint
from mintmark.packs.model import load_pack

ROOT = Path(__file__).resolve().parents[1]
PACK = load_pack(ROOT)
CORE_DENYLIST = load_denylist(asset_dir("denylist") / "institutions-tr.txt")
PACK_DENYLIST = load_denylist(ROOT / "lexicons" / "denylist_extension.txt")


# The pack contains no engine code, and its Python imports only the public API.


def test_no_python_outside_tests_and_tools() -> None:
    offenders = [
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*.py")
        if p.is_file() and not str(p.relative_to(ROOT)).startswith(("tests/", "tools/", ".venv/"))
    ]
    assert not offenders, f"a pack carries no engine code, but found: {offenders}"


def test_tests_import_only_the_public_api() -> None:
    """A pack that reaches into a private core module has coupled itself to it."""
    import ast

    for path in sorted((ROOT / "tests").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("mintmark._"), (
                    f"{path.name} imports a private core module: {node.module}"
                )


def test_no_dataset_is_committed_outside_samples() -> None:
    offenders = [
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*.jsonl")
        if not str(p.relative_to(ROOT)).startswith(("samples/", "tests/", ".venv/", "dist/"))
    ]
    assert not offenders, f"datasets are release artifacts, never committed: {offenders}"


# Identity and pins.


def test_the_pack_name_matches_the_repository() -> None:
    assert PACK.name == "mintmark-hr"


def test_the_core_pin_has_a_closed_upper_bound() -> None:
    """An open pin means a core minor release can silently change our output."""
    assert PACK.requires_core.contains("0.1.0")
    assert not PACK.requires_core.contains("0.2.0")


def test_the_locale_is_turkish() -> None:
    assert PACK.locale == "tr-TR"


# Record shapes the brief settles.

STRUCTURED = ("employee", "position_history", "leave_record", "payroll_entry")
DOCUMENTS = ("performance_note", "recruiter_note", "hr_request")


def test_the_four_structured_record_types_exist() -> None:
    names = {t.type_name for t in PACK.record_types}
    assert set(STRUCTURED) <= names


def test_the_three_document_types_exist_with_their_evaluation_twins() -> None:
    names = {t.type_name for t in PACK.record_types}
    for base in DOCUMENTS:
        assert base in names, base
        assert f"{base}_eval" in names, f"{base}_eval"


def test_payroll_runs_monthly_for_every_employee() -> None:
    """A payroll that varies per employee is not a payroll, it is a transaction log."""
    field = _field("payroll_entry", "employee_id")
    assert field.ref is not None
    assert field.ref.counts == (12,), field.ref.counts
    assert field.ref.weights == ("1",), field.ref.weights


def test_a_leave_type_carries_no_label() -> None:
    """The settled design, asserted so a later edit has to argue with a test.

    A structured leave-type code is an enum, not a health disclosure. The health
    signal this pack exists to exercise lives in the document bodies, where spans
    are labeled. Labeling a code here would put a HEALTH span on the string
    `yillik` and corrupt every evaluation the dataset is used for.
    """
    assert _field("leave_record", "type").pii_label == "none"


def test_the_manager_name_is_a_draw_and_not_a_reference() -> None:
    """Self-references within one record type are out of contract.

    So the manager named on an employee corresponds to no employee record. A test
    holds the line because a reader who does not know that will try to fix it.
    """
    field = _field("employee", "manager_name")
    assert field.type != "ref"
    assert field.ref is None
    assert field.generator.startswith("lexicon:"), field.generator


def test_a_recruiter_note_has_no_parent() -> None:
    """Its subject is a candidate, and a candidate is not an employee.

    Giving this type a parent reference would encode the opposite claim into
    every dataset the pack produces.
    """
    for name in ("recruiter_note", "recruiter_note_eval"):
        record_type = next(t for t in PACK.record_types if t.type_name == name)
        assert not [f for f in record_type.fields if f.type == "ref"], name


def test_employee_addresses_land_in_the_employer_subdomain() -> None:
    field = _field("employee", "email")
    assert field.params.get("subdomain") == "ankaholding"


def test_birth_dates_declare_a_working_age_window() -> None:
    """Without this every employee in a 2026 dataset was also born in 2026."""
    span = _field("employee", "birth_date").params.get("age_years")
    assert span == [18, 65], span


def _field(type_name: str, field_name: str):  # noqa: ANN202 - the core's Field type
    record_type = next(t for t in PACK.record_types if t.type_name == type_name)
    return next(f for f in record_type.fields if f.name == field_name)


# Lexicons.


def test_at_least_twenty_four_fictional_employer_names() -> None:
    employers = PACK.lexicons["employers_fictional"]["values"]
    assert len(employers) >= 24, f"the brief settles at least 24, found {len(employers)}"


@pytest.mark.parametrize("name", sorted(p.stem for p in (ROOT / "lexicons").glob("*.yaml")))
def test_every_lexicon_entry_passes_the_pack_denylist(name: str) -> None:
    """The pack list, not the core list. The core covers banks; this pack invents
    employers, which the banking list was never built to catch."""
    document = yaml.safe_load((ROOT / "lexicons" / f"{name}.yaml").read_text(encoding="utf-8"))
    hits = [
        hit.render()
        for value in document.get("values", [])
        for hit in PACK_DENYLIST.scan(str(value))
    ]
    assert not hits, "\n".join(hits)


@pytest.mark.parametrize("name", sorted(p.stem for p in (ROOT / "lexicons").glob("*.yaml")))
def test_every_lexicon_carries_a_source_note(name: str) -> None:
    document = yaml.safe_load((ROOT / "lexicons" / f"{name}.yaml").read_text(encoding="utf-8"))
    assert len(document.get("source_note", "")) > 40, f"{name} has no real source note"


def test_the_pack_denylist_covers_the_core_one() -> None:
    """Packs may extend the list and may never shrink it."""
    assert PACK_DENYLIST.covers(CORE_DENYLIST), (
        f"missing from the pack list: {sorted(PACK_DENYLIST.missing_from(CORE_DENYLIST))[:5]}"
    )


def test_the_pack_denylist_carries_real_company_names() -> None:
    """The HR brief's verify-at-implementation item, asserted rather than assumed."""
    entries = set(PACK_DENYLIST.entries)
    for expected in ("koc holding", "sabanci", "toros tarim"):
        assert any(expected in entry for entry in entries), f"the list omits {expected!r}"


def test_no_template_names_a_real_company() -> None:
    text = "\n".join(
        p.read_text(encoding="utf-8") for p in sorted((ROOT / "templates").rglob("*.yaml"))
    )
    hits = [hit.render() for hit in PACK_DENYLIST.scan(text)]
    assert not hits, "\n".join(hits)


# Recipes.


def test_the_three_named_recipes_exist() -> None:
    assert set(PACK.recipes) == {"workforce-baseline", "pii-eval", "anomaly-mix"}


def test_every_recipe_ships_with_the_safe_policy() -> None:
    for name, recipe in PACK.recipes.items():
        assert recipe.identifier_policy == "safe", f"{name} does not pin the safe policy"


def test_the_baseline_special_rate_is_the_governed_one() -> None:
    """The rate the sign-off gate covers. Changing it reopens that gate."""
    assert PACK.recipe("workforce-baseline").special_rate == "0.06"
    assert PACK.recipe("anomaly-mix").special_rate == "0.06"


def test_the_evaluation_recipe_declares_a_target_for_every_label() -> None:
    targets = PACK.recipe("pii-eval").coverage_targets
    assert set(targets) == {label.value for label in ALL_LABELS}
    for label in ("PERSON", "HEALTH", "CRIMINAL", "UNION"):
        assert targets[label] >= 300
    for label in ("TCKN", "VKN", "IBAN", "PAN", "PHONE", "EMAIL"):
        assert targets[label] >= 500


def test_the_reference_seeds_are_the_settled_ones() -> None:
    """Changing a seed silently invalidates a published manifest."""
    datasets = json.loads((ROOT / "docs" / "reference-datasets.json").read_text(encoding="utf-8"))
    assert datasets["workforce-baseline"]["seed"] == "20261101"
    assert datasets["pii-eval"]["seed"] == "20261102"
    for name, entry in datasets.items():
        if name.startswith("_"):
            continue
        assert entry["identifier_policy"] == "safe", f"{name} is not pinned to safe"


# The mint itself.

MINT_COUNTS = {
    "employee": 120,
    "position_history": 200,
    "leave_record": 400,
    "payroll_entry": 1440,
    "performance_note": 60,
    "recruiter_note": 40,
    "hr_request": 60,
}


@pytest.fixture(scope="module")
def minted(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("pack") / "run"
    mint(
        pack=ROOT,
        recipe="workforce-baseline",
        seed=1,
        out=out,
        records=MINT_COUNTS,
        invocation="pytest",
    )
    return out


def test_a_mint_produces_every_declared_type(minted: Path) -> None:
    for record_type in PACK.record_types:
        assert (minted / f"{record_type.type_name}.jsonl").exists()


def test_documents_produce_sidecars(minted: Path) -> None:
    for name in DOCUMENTS:
        sidecar = minted / f"{name}.labels.jsonl"
        assert sidecar.exists(), f"{name} produced no sidecar"
        assert sidecar.read_text(encoding="utf-8").strip(), f"{name}'s sidecar is empty"


def test_a_minted_dataset_verifies(minted: Path) -> None:
    from mintmark.api import verify as verify_dataset

    report = verify_dataset(minted)
    assert report.ok, report.problems


def test_no_real_company_appears_in_minted_output(minted: Path) -> None:
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(minted.glob("*.jsonl")))
    hits = [hit.render() for hit in PACK_DENYLIST.scan(text)]
    assert not hits, "\n".join(hits[:10])


def test_every_reference_resolves(minted: Path) -> None:
    def ids(name: str) -> set[str]:
        record_type = next(t for t in PACK.record_types if t.type_name == name)
        key = record_type.fields[0].name
        return {
            json.loads(line)[key]
            for line in (minted / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    employees = ids("employee")
    for child in ("position_history", "leave_record", "payroll_entry", "performance_note",
                  "hr_request"):
        for line in (minted / f"{child}.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            assert json.loads(line)["employee_id"] in employees, f"{child} dangles"


def test_every_employee_is_of_working_age(minted: Path) -> None:
    """The defect this pack found in the core, asserted where a reader would see it."""
    years = [
        int(json.loads(line)["birth_date"][:4])
        for line in (minted / "employee.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert years
    ages = [2026 - year for year in years]
    assert min(ages) >= 18, f"youngest employee is {min(ages)}"
    assert max(ages) <= 65, f"oldest employee is {max(ages)}"


def test_every_employee_address_stays_in_the_reserved_space(minted: Path) -> None:
    for line in (minted / "employee.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        address = json.loads(line)["email"]
        assert address.endswith(".example"), address
        assert "@ankaholding.example" in address, address


def test_the_anomaly_flag_never_disagrees_with_the_kind(minted: Path) -> None:
    for line in (minted / "payroll_entry.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        assert row["is_anomaly"] == (row["anomaly_kind"] != "none"), row


def test_no_emitted_value_is_a_float(minted: Path) -> None:
    for path in sorted(minted.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            for value in json.loads(line).values():
                assert not isinstance(value, float), f"{path.name}: {value!r}"


def test_packcheck_passes_against_the_pinned_core() -> None:
    """The conformance run a pack release may not be tagged without."""
    result = subprocess.run(
        [sys.executable, "-m", "mintmark.cli", "packcheck", str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# Sample freshness.

SAMPLE_COUNTS = dict.fromkeys([*STRUCTURED, *DOCUMENTS], 50)


def test_samples_regenerate_to_the_same_bytes(tmp_path: Path) -> None:
    """A sample that drifted from the declarations misrepresents them silently."""
    out = tmp_path / "regenerated"
    mint(
        pack=ROOT,
        recipe="workforce-baseline",
        seed=1,
        out=out,
        records=SAMPLE_COUNTS,
        invocation="pytest",
    )
    drifted = []
    for committed in sorted((ROOT / "samples").glob("*.jsonl")):
        fresh = out / committed.name
        assert fresh.exists(), f"{committed.name} is committed but no longer produced"
        if committed.read_bytes() != fresh.read_bytes():
            drifted.append(committed.name)
    assert not drifted, (
        f"samples drifted: {drifted}. Regenerate with the command in samples/README.md."
    )


def test_samples_are_capped_at_fifty_records_per_type() -> None:
    for path in sorted((ROOT / "samples").glob("*.jsonl")):
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert len(lines) <= 50, f"{path.name} carries {len(lines)} records"
        assert lines, f"{path.name} is empty and should not be committed"


def test_samples_carry_no_manifest() -> None:
    assert not (ROOT / "samples" / "MINTMARK.json").exists()
    assert not (ROOT / "samples" / "SHA256SUMS").exists()


# The health boundary.

CLINICAL_DENIED = ROOT / "lexicons" / "clinical_denied_tr.txt"
ACCUSATORY_DENIED = ROOT / "lexicons" / "accusatory_denied_tr.txt"


def _terms(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def _as_denylist(path: Path, note: str):  # noqa: ANN202 - the core's Denylist type
    return parse_denylist("\n".join(f"{term}    # {note}" for term in _terms(path)))


def test_the_clinical_denied_list_has_real_content() -> None:
    terms = _terms(CLINICAL_DENIED)
    assert len(terms) >= 20, f"only {len(terms)} denied terms; the list is a placeholder"
    for category in ("teshis", "kemoterapi", "prognoz"):
        assert category in terms, f"the list omits {category!r}"


def test_no_rendered_document_contains_denied_clinical_vocabulary(minted: Path) -> None:
    denied = _as_denylist(CLINICAL_DENIED, "denied clinical vocabulary")
    offenders = [
        f"{name}: {hit.entry!r} in a rendered document"
        for name in DOCUMENTS
        for line in (minted / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
        for hit in denied.scan(json.loads(line)["body"])
    ]
    assert not offenders, "\n".join(offenders[:10])


def test_every_health_span_draws_from_the_core_condition_classes(minted: Path) -> None:
    """Category granularity is enforced by where the surface comes from."""
    from mintmark.annotate import Label
    from mintmark.mint import core_descriptors

    _assert_spans_are_curated(minted, "HEALTH", set(core_descriptors(Label.HEALTH)))


# The accusatory boundary, which only this pack owns.


def test_the_accusatory_denied_list_has_real_content() -> None:
    terms = _terms(ACCUSATORY_DENIED)
    assert len(terms) >= 20, f"only {len(terms)} denied terms; the list is a placeholder"
    for category in ("sabikali", "suc isledi", "mahkum oldu"):
        assert category in terms, f"the list omits {category!r}"


def test_no_rendered_document_accuses_anyone(minted: Path) -> None:
    """A reference check is a process. It records what was requested, never a verdict.

    A synthetic person is still a person-shaped claim, and a model trained on text
    that convicts synthetic people learns to produce that text about real ones.
    """
    denied = _as_denylist(ACCUSATORY_DENIED, "accusatory vocabulary")
    offenders = [
        f"{name}: {hit.entry!r} in a rendered document"
        for name in DOCUMENTS
        for line in (minted / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
        for hit in denied.scan(json.loads(line)["body"])
    ]
    assert not offenders, "\n".join(offenders[:10])


def test_no_template_source_crosses_either_boundary() -> None:
    """Catch it in the template rather than waiting for a draw to surface it."""
    text = "\n".join(
        p.read_text(encoding="utf-8") for p in sorted((ROOT / "templates").rglob("*.yaml"))
    )
    for path, note in ((CLINICAL_DENIED, "clinical"), (ACCUSATORY_DENIED, "accusatory")):
        hits = [hit.entry for hit in _as_denylist(path, note).scan(text)]
        assert not hits, f"a template carries denied {note} vocabulary: {hits}"


def test_every_criminal_span_draws_from_the_core_document_names(minted: Path) -> None:
    """The CRIMINAL surface names a document, never an allegation."""
    from mintmark.annotate import Label
    from mintmark.mint import core_descriptors

    _assert_spans_are_curated(minted, "CRIMINAL", set(core_descriptors(Label.CRIMINAL)))


@pytest.mark.parametrize(
    ("path", "planted"),
    [
        (CLINICAL_DENIED, "Calisanin dosyasina kemoterapi tedavisi notu islendi."),
        (ACCUSATORY_DENIED, "Adayin gecmisinde dolandiricilik sucu bulundugu ogrenildi."),
    ],
)
def test_each_denied_list_would_catch_a_planted_term(path: Path, planted: str) -> None:
    """A control that has never rejected anything is not known to reject anything."""
    assert _as_denylist(path, "denied").scan(planted), f"{path.name} no longer catches an obvious term"


def _assert_spans_are_curated(minted: Path, label: str, allowed: set[str]) -> None:
    seen = 0
    for sidecar in sorted(minted.glob("*.labels.jsonl")):
        stem = sidecar.name.removesuffix(".labels.jsonl")
        bodies = {
            next(v for k, v in json.loads(line).items() if k.endswith("_id")): json.loads(line)[
                "body"
            ]
            for line in (minted / f"{stem}.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        for line in sidecar.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            text = bodies[record["doc_id"]]
            for span in record["spans"]:
                if span["label"] != label:
                    continue
                seen += 1
                surface = text[span["start"] : span["end"]]
                assert surface in allowed, (
                    f"a {label} span carries {surface!r}, which is not a curated descriptor"
                )
    assert seen, f"no {label} span was produced, so this check proved nothing"


# The README's claims about its own contents.

README_EN = ROOT / "README.md"
README_TR = ROOT / "README.tr.md"


def test_the_readme_example_is_real_output_not_an_illustration() -> None:
    """A README that invents its example will invent a stale one eventually."""
    quoted = README_EN.read_text(encoding="utf-8")
    first = json.loads(
        (ROOT / "samples" / "recruiter_note.jsonl").read_text(encoding="utf-8").splitlines()[0]
    )["body"]
    # The README wraps the excerpt, so compare on the distinctive values rather
    # than on the wrapped text.
    for token in first.split()[:6]:
        assert token in quoted, f"the README example does not match the sample: {token!r} missing"


def test_the_readme_states_the_counts_it_claims() -> None:
    employers = len(PACK.lexicons["employers_fictional"]["values"])
    denied = len(_terms(ACCUSATORY_DENIED))
    for path in (README_EN, README_TR):
        text = path.read_text(encoding="utf-8")
        assert f"-{employers}-D11F26" in text, (
            f"{path.name}: the employer count has drifted from the {employers} declared"
        )
    english = README_EN.read_text(encoding="utf-8")
    assert f"{denied} phrases this pack refuses" in english, (
        f"the README claims a different count than the {denied} phrases actually listed"
    )


def test_the_readme_reports_the_special_rate_the_recipes_use() -> None:
    rate = PACK.recipe("workforce-baseline").special_rate
    assert rate in README_EN.read_text(encoding="utf-8")
    assert rate.replace(".", ",") in README_TR.read_text(encoding="utf-8")


def test_both_readmes_exist_and_mirror_each_other() -> None:
    import re

    heading = re.compile(r"^(#{1,6})\s", re.MULTILINE)
    levels_en = [len(m.group(1)) for m in heading.finditer(README_EN.read_text(encoding="utf-8"))]
    levels_tr = [len(m.group(1)) for m in heading.finditer(README_TR.read_text(encoding="utf-8"))]
    assert levels_en == levels_tr, "the Turkish mirror has diverged in structure"


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_declares_the_anomaly_limitation(path: Path) -> None:
    """The anomaly kinds are per-row labels, not temporal structures."""
    text = path.read_text(encoding="utf-8").lower()
    assert "per-row" in text or "satir basi" in text or "satır başı" in text


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_declares_both_boundaries(path: Path) -> None:
    """A pack with two sensitive surfaces states both, in both languages.

    Whitespace is normalized first. A README that wraps a sentence across two
    lines has not lost the claim, and a test that says otherwise fails on
    reflowed prose rather than on a missing statement.
    """
    text = _prose(path)
    assert "not clinical data" in text or "klinik veri değildir" in text
    assert "never record what it contains" in text or "asla kaydetmez" in text


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_names_the_release_that_actually_exists(path: Path) -> None:
    """A README may claim a release, and the claim has to be the right one.

    This replaced a test that asserted nothing was published, which was correct
    until something was. The failure it now guards is subtler and likelier: a
    version bump that leaves the README pointing at a tag nobody cut, or at an
    older one whose datasets no longer reproduce from these declarations.
    """
    text = path.read_text(encoding="utf-8")
    tag = f"v{PACK.version}"
    assert f"/releases/tag/{tag}" in text, (
        f"{path.name} does not point at {tag}, the version this pack declares"
    )
    stale = re.findall(r"/releases/tag/v(\d+\.\d+\.\d+)", text)
    assert set(stale) == {PACK.version}, (
        f"{path.name} names releases {sorted(set(stale))} while the pack is {PACK.version}"
    )


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_neither_readme_claims_the_engine_is_on_a_package_index(path: Path) -> None:
    """It is not, and the name there is unclaimed.

    Telling a reader to install by package name would install whatever somebody
    else eventually puts under that name.
    """
    text = path.read_text(encoding="utf-8").lower()
    assert "pypi.org/project" not in text
    assert "uv tool install mintmark\n" not in text
    assert "pip install mintmark" not in text


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_references_only_committed_assets(path: Path) -> None:
    import re

    for match in re.finditer(r"\((assets/[^)]+)\)", path.read_text(encoding="utf-8")):
        assert (ROOT / match.group(1)).exists(), f"{match.group(1)} is referenced but absent"


def _prose(path: Path) -> str:
    """The README as running text: no emphasis markers, no quote bars, one line.

    These claims are the ones a reader has to be able to find, so the test looks
    for them the way a reader reads them. Matching raw markdown would fail on a
    reflowed paragraph or a bolded phrase rather than on a missing statement.
    """
    import re

    stripped = "\n".join(
        re.sub(r"^\s*>\s?", "", line) for line in path.read_text(encoding="utf-8").splitlines()
    )
    return " ".join(stripped.replace("*", "").replace("`", "").lower().split())


# What a version bump costs.


def test_the_pack_version_is_part_of_what_seeds_the_streams(tmp_path: Path) -> None:
    """Bumping the version changes every emitted byte for a fixed seed.

    The version is part of the pack digest and the digest seeds the streams, so
    version and content correspond exactly: two datasets carrying the same pack
    version cannot differ, and a bump is never a no-op for anyone holding a
    published manifest. Worth a test because it is surprising, and because the
    sample freshness failure it causes reads like a bug until you know why.
    """
    import shutil

    rolled_back = tmp_path / "rolled-back"
    shutil.copytree(
        ROOT,
        rolled_back,
        ignore=shutil.ignore_patterns(".venv", ".git", ".pytest_cache", "samples", "dist"),
    )
    manifest = rolled_back / "pack.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            f"version: {PACK.version}", "version: 9.9.9"
        ),
        encoding="utf-8",
    )

    out = tmp_path / "probe"
    mint(
        pack=rolled_back,
        recipe="workforce-baseline",
        seed=1,
        out=out,
        records={"employee": 20},
        invocation="pytest",
    )
    changed = (out / "employee.jsonl").read_bytes()
    committed = (ROOT / "samples" / "employee.jsonl").read_bytes()
    assert not committed.startswith(changed[:200]), (
        "a different pack version produced identical bytes, so the version is no "
        "longer part of the digest and two datasets can now share a version while "
        "differing in content"
    )
