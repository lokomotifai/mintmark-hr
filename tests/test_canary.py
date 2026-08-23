"""Security regressions for the private-corpus canary scanner."""

from __future__ import annotations

import gzip
import importlib.util
import io
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("canary", ROOT / "tools" / "canary.py")
assert SPEC is not None
assert SPEC.loader is not None
canary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(canary)


def test_standalone_gzip_and_nested_archives_are_scanned(tmp_path: Path) -> None:
    needle = "private tripwire"
    compressed = gzip.compress(f"prefix {needle} suffix".encode())
    standalone = tmp_path / "payload.txt.gz"
    standalone.write_bytes(compressed)
    assert canary.scan(standalone, needle)

    nested = tmp_path / "nested.zip"
    with zipfile.ZipFile(nested, "w") as archive:
        archive.writestr("payload.txt.gz", compressed)
    assert any("payload.txt.gz" in hit for hit in canary.scan(nested, needle))


def test_symlinks_fail_closed_instead_of_leaving_the_scan_root(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-canary.txt"
    outside.write_text("private tripwire", encoding="utf-8")
    (tmp_path / "linked.txt").symlink_to(outside)
    with pytest.raises(canary.ScanError, match="symlink"):
        canary.scan(tmp_path, "private tripwire")


def test_archive_expansion_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    archive_path = tmp_path / "large.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("large.txt", b"x" * 8192, compress_type=zipfile.ZIP_DEFLATED)
    monkeypatch.setattr(canary, "MAX_FILE_BYTES", 4096)
    with pytest.raises(canary.ScanError, match="size limit"):
        canary.scan(archive_path, "private tripwire")


def test_stream_search_matches_across_chunk_boundaries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(canary, "CHUNK_SIZE", 4)
    found, data = canary._read_stream(
        io.BytesIO(b"xxprivate tripwireyy"),
        b"private tripwire",
        {"bytes": 0, "members": 0},
        "memory",
        collect=False,
    )
    assert found
    assert data is None


def test_ci_scans_built_release_archives_explicitly() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "Build final reference artifacts before the release gate" in workflow
    assert 'for artifact in "${artifacts[@]}"; do test -s "$artifact"; done' in workflow
    assert 'tools/canary.py . "${artifacts[@]}"' in workflow
