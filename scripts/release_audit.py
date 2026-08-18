"""Audit candidate repository files for release-boundary violations."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
from typing import Iterable


MAX_FILE_BYTES = 10 * 1024 * 1024
TEXT_SUFFIXES = {
    "",
    ".bib",
    ".cff",
    ".csv",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sty",
    ".tex",
    ".txt",
    ".yml",
    ".yaml",
}
PARTICIPANT_DATA_PREFIXES = (
    "data/private/",
    "validation/consent/",
    "validation/private/",
    "validation/raw/",
    "validation/recruitment/",
    "validation/responses/",
)
LOCAL_PATH_RE = re.compile(r"/(?:Users|home)/[^\s\"']+")
CREDENTIAL_RES = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{10,}"),
    re.compile(r"gh[oprsu]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def candidate_files(root: Path) -> list[Path]:
    """Return tracked and untracked, non-ignored files under a Git worktree."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode == 0:
        names = [name for name in result.stdout.decode().split("\0") if name]
        return [root / name for name in names if (root / name).is_file()]

    return [
        path
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    ]


def audit_files(root: Path, files: Iterable[Path]) -> list[str]:
    """Return deterministic human-readable findings for candidate files."""
    findings: list[str] = []
    for path in sorted(files):
        relative = path.relative_to(root).as_posix()

        if relative.startswith(PARTICIPANT_DATA_PREFIXES):
            findings.append(f"{relative}: participant-data path is prohibited")

        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            findings.append(f"{relative}: file exceeds 10 MiB release limit")

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if LOCAL_PATH_RE.search(content):
            findings.append(f"{relative}: contains an absolute local path")
        if any(pattern.search(content) for pattern in CREDENTIAL_RES):
            findings.append(f"{relative}: contains a credential-like value")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    findings = audit_files(root, candidate_files(root))

    if findings:
        print("Release audit failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Release audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
