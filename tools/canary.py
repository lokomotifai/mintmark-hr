#!/usr/bin/env python3
"""Private-corpus canary check.

Section 7.2 of the lokomotifai public repository standard requires that a known
canary string from the organization's private materials be absent from the
repository tree and from built artifacts. This script is that check.

The canary itself is never committed. Committing it would plant the very string
the check exists to find, and the first run would fail on its own tripwire.
Instead the canary is supplied at run time and this repository commits only its
SHA-256, so that a run can prove it was given the right string rather than an
empty one:

    MINTMARK_CANARY='...' python tools/canary.py .
    python tools/canary.py . --canary-file ~/private/canary.txt

The committed digest is a tripwire, not a secret. A short canary phrase is
recoverable from its hash by anyone who guesses it, which costs nothing here:
the check detects accidental leakage of private planning material, and it does
not defend against an adversary who already holds the material.

Scanning covers text files in the tree and, when a path is given, the contents
of built sdists and wheels. Binary files are compared byte-wise against the
UTF-8 encoding of the canary.

Exit codes: 0 clean, 1 canary found, 2 usage or configuration error.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
import stat
import subprocess
import sys
import tarfile
import zipfile
from collections.abc import Iterator
from pathlib import Path

# SHA-256 of the canary phrase for this repository family. Set by WP-00 and
# changed only when the canary itself is rotated, which is a Decision Log event.
EXPECTED_DIGEST = "b0c48e6c4b8ccb15439bebcec60a9939806771157a38407686782c85ede7cd16"

SKIP_DIRS = frozenset(
    {".git", ".venv", "node_modules", "__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache"}
)
ARCHIVE_SUFFIXES = frozenset({".whl", ".zip", ".tar", ".gz", ".tgz"})
CHUNK_SIZE = 64 * 1024
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 10_000
MAX_ARCHIVE_DEPTH = 3


class ScanError(RuntimeError):
    """The requested scan cannot be completed safely and fully."""


def load_canary() -> str:
    value = os.environ.get("MINTMARK_CANARY", "").strip()
    if value:
        return value
    raise SystemExit(
        "canary: no canary supplied. Set MINTMARK_CANARY or pass --canary-file.\n"
        "The canary is never committed to this repository; see the module docstring."
    )


def verify_digest(canary: str) -> None:
    digest = hashlib.sha256(canary.encode("utf-8")).hexdigest()
    if digest != EXPECTED_DIGEST:
        raise SystemExit(
            "canary: the supplied canary does not match the committed digest.\n"
            f"  expected {EXPECTED_DIGEST}\n  received {digest}\n"
            "A mismatch means the check would scan for the wrong string, which is "
            "worse than not running it at all."
        )


def tracked_files(root: Path) -> Iterator[Path]:
    try:
        out = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        for rel in out.split("\0"):
            if rel:
                yield root / rel
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    for path in root.rglob("*"):
        if path.is_file() and not any(part in SKIP_DIRS for part in path.parts):
            yield path


def _archive_kind(name: str) -> str | None:
    lowered = name.lower()
    if lowered.endswith((".whl", ".zip")):
        return "zip"
    if lowered.endswith((".tar.gz", ".tgz", ".tar")):
        return "tar"
    if lowered.endswith(".gz"):
        return "gzip"
    return None


def _consume(budget: dict[str, int], size: int, display: str) -> None:
    budget["bytes"] += size
    if budget["bytes"] > MAX_TOTAL_BYTES:
        raise ScanError(f"aggregate scan budget exceeded while reading {display}")


def _read_stream(
    handle: object,
    needle: bytes,
    budget: dict[str, int],
    display: str,
    *,
    collect: bool,
) -> tuple[bool, bytes | None]:
    tail = b""
    collected = bytearray() if collect else None
    read_size = 0
    found = False
    while chunk := handle.read(CHUNK_SIZE):  # type: ignore[attr-defined]
        read_size += len(chunk)
        if read_size > MAX_FILE_BYTES:
            raise ScanError(f"expanded file exceeds {MAX_FILE_BYTES}-byte limit: {display}")
        _consume(budget, len(chunk), display)
        found = found or needle in tail + chunk
        if collected is not None:
            collected.extend(chunk)
        tail = (tail + chunk)[-(len(needle) - 1) :] if len(needle) > 1 else b""
    return found, bytes(collected) if collected is not None else None


def _scan_member(
    handle: object,
    name: str,
    display: str,
    needle: bytes,
    budget: dict[str, int],
    depth: int,
) -> list[str]:
    nested = _archive_kind(name)
    found, data = _read_stream(handle, needle, budget, display, collect=nested is not None)
    hits = [display] if found else []
    if nested is not None:
        if depth >= MAX_ARCHIVE_DEPTH:
            raise ScanError(f"archive nesting exceeds depth {MAX_ARCHIVE_DEPTH}: {display}")
        assert data is not None
        hits.extend(scan_archive(io.BytesIO(data), needle, name, display, budget, depth + 1))
    return hits


def scan_archive(
    source: Path | io.BytesIO,
    needle: bytes,
    name: str | None = None,
    display: str | None = None,
    budget: dict[str, int] | None = None,
    depth: int = 0,
) -> list[str]:
    name = name or str(source)
    display = display or str(source)
    budget = budget or {"bytes": 0, "members": 0}
    hits: list[str] = []
    kind = _archive_kind(name)
    try:
        if kind == "zip":
            with zipfile.ZipFile(source) as archive:
                for member in archive.infolist():
                    if member.is_dir():
                        continue
                    member_display = f"{display}::{member.filename}"
                    budget["members"] += 1
                    if budget["members"] > MAX_ARCHIVE_MEMBERS:
                        raise ScanError(f"archive member budget exceeded: {member_display}")
                    if member.file_size > MAX_FILE_BYTES:
                        raise ScanError(f"archive member exceeds size limit: {member_display}")
                    if needle in member.filename.encode("utf-8", errors="surrogateescape"):
                        hits.append(member_display)
                    with archive.open(member) as handle:
                        hits.extend(
                            _scan_member(
                                handle, member.filename, member_display, needle, budget, depth
                            )
                        )
        elif kind == "tar":
            fileobj = source if isinstance(source, io.BytesIO) else None
            filename = None if fileobj is not None else str(source)
            with tarfile.open(name=filename, fileobj=fileobj, mode="r:*") as archive:
                for member in archive:
                    member_display = f"{display}::{member.name}"
                    if member.issym() or member.islnk():
                        raise ScanError(f"refusing archive link: {member_display}")
                    if not member.isfile():
                        continue
                    budget["members"] += 1
                    if budget["members"] > MAX_ARCHIVE_MEMBERS:
                        raise ScanError(f"archive member budget exceeded: {member_display}")
                    if member.size > MAX_FILE_BYTES:
                        raise ScanError(f"archive member exceeds size limit: {member_display}")
                    if needle in member.name.encode("utf-8", errors="surrogateescape"):
                        hits.append(member_display)
                    handle = archive.extractfile(member)
                    if handle is None:
                        raise ScanError(f"cannot read archive member: {member_display}")
                    with handle:
                        hits.extend(
                            _scan_member(handle, member.name, member_display, needle, budget, depth)
                        )
        elif kind == "gzip":
            fileobj = source if isinstance(source, io.BytesIO) else None
            filename = None if fileobj is not None else str(source)
            with gzip.GzipFile(filename=filename, fileobj=fileobj, mode="rb") as handle:
                hits.extend(
                    _scan_member(handle, name[:-3], f"{display}::gzip", needle, budget, depth)
                )
        else:
            raise ScanError(f"unsupported archive type: {display}")
    except (gzip.BadGzipFile, zipfile.BadZipFile, tarfile.TarError, EOFError, OSError) as exc:
        raise ScanError(f"cannot read archive {display}: {exc}") from exc
    return hits


def scan(root: Path, canary: str) -> list[str]:
    needle = canary.encode("utf-8")
    hits: list[str] = []
    budget = {"bytes": 0, "members": 0}

    root = root.absolute()
    try:
        root_mode = root.lstat().st_mode
    except OSError as exc:
        raise ScanError(f"cannot inspect scan target {root}: {exc}") from exc
    if stat.S_ISLNK(root_mode):
        raise ScanError(f"refusing symlink scan target: {root}")

    if stat.S_ISREG(root_mode):
        inventory_root = root.parent
        targets: Iterator[Path] = iter([root])
    elif stat.S_ISDIR(root_mode):
        inventory_root = root
        targets = tracked_files(root)
    else:
        raise ScanError(f"refusing non-file scan target: {root}")

    resolved_root = inventory_root.resolve(strict=True)
    for path in targets:
        path = path.absolute()
        try:
            relative = path.relative_to(inventory_root)
        except ValueError as exc:
            raise ScanError(f"path escapes scan root: {path}") from exc
        current = inventory_root
        for part in relative.parts:
            current /= part
            try:
                mode = current.lstat().st_mode
            except OSError as exc:
                raise ScanError(f"cannot inspect {current}: {exc}") from exc
            if stat.S_ISLNK(mode):
                raise ScanError(f"refusing symlink in scan inventory: {current}")
        try:
            resolved = path.resolve(strict=True)
        except OSError as exc:
            raise ScanError(f"cannot resolve {path}: {exc}") from exc
        if not resolved.is_relative_to(resolved_root):
            raise ScanError(f"resolved path escapes scan root: {path}")
        metadata = path.lstat()
        if not stat.S_ISREG(metadata.st_mode):
            raise ScanError(f"refusing non-regular scan target: {path}")
        if metadata.st_size > MAX_FILE_BYTES:
            raise ScanError(f"file exceeds {MAX_FILE_BYTES}-byte scan limit: {path}")
        if _archive_kind(path.name) is not None:
            hits.extend(scan_archive(path, needle, budget=budget))
            continue
        try:
            with path.open("rb") as handle:
                found, _ = _read_stream(handle, needle, budget, str(path), collect=False)
            if found:
                hits.append(str(path))
        except OSError as exc:
            raise ScanError(f"cannot read {path}: {exc}") from exc
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "targets", nargs="*", default=["."], help="directories, files, or built artifacts to scan"
    )
    parser.add_argument(
        "--canary-file", type=Path, help="read the canary from this file instead of the environment"
    )
    parser.add_argument(
        "--print-digest",
        action="store_true",
        help="print the SHA-256 of the supplied canary and exit",
    )
    args = parser.parse_args(argv)

    if args.canary_file:
        try:
            canary = args.canary_file.read_text(encoding="utf-8").strip()
        except OSError as exc:
            print(f"canary: cannot read {args.canary_file}: {exc}", file=sys.stderr)
            return 2
    else:
        canary = load_canary()

    if args.print_digest:
        print(hashlib.sha256(canary.encode("utf-8")).hexdigest())
        return 0

    verify_digest(canary)

    all_hits: list[str] = []
    try:
        for target in args.targets or ["."]:
            path = Path(target).absolute()
            if not path.exists() and not path.is_symlink():
                print(f"canary: no such path: {path}", file=sys.stderr)
                return 2
            all_hits.extend(scan(path, canary))
    except ScanError as exc:
        print(f"canary: {exc}", file=sys.stderr)
        return 2

    if all_hits:
        print("canary: private-corpus canary found in:", file=sys.stderr)
        for hit in all_hits:
            print(f"  {hit}", file=sys.stderr)
        print(
            "\nPrivate planning material has leaked into the tree or an artifact.", file=sys.stderr
        )
        return 1

    print(f"canary: clean, {len(args.targets or ['.'])} target(s) scanned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
