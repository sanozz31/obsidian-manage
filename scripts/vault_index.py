#!/usr/bin/env python3
"""Utilities for Obsidian vault indexes, date headers, and setup detection."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path

DATE_RE = re.compile(r"^\n```text\n最后修改日期：\d{4}-\d{2}-\d{2}\n```\n\n", re.M)
SKIP_DIRS = {".git", ".hg", ".svn", ".obsidian", "node_modules", "Library", "Applications", "System", "Volumes"}


def iter_markdown(vault: Path):
    for path in sorted(vault.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def note_type(rel: str, name: str) -> str:
    if name == "AGENTS.md" or rel.startswith("00-系统规则/"):
        return "rule"
    if name.startswith("00-") and name.endswith("说明.md"):
        return "index"
    return "note"


def make_record(vault: Path, path: Path, date: str) -> dict[str, str]:
    rel = path.relative_to(vault).as_posix()
    area = "00-系统规则" if rel == "AGENTS.md" else rel.split("/")[0]
    return {
        "date": date,
        "path": rel,
        "title": path.stem,
        "area": area,
        "type": note_type(rel, path.name),
        "status": "active",
    }


def index_dir_for(vault: Path) -> Path:
    preferred = vault / "00-系统规则" / "03-索引文件"
    if preferred.exists() or (vault / "00-系统规则").exists():
        return preferred
    return vault / "00-system" / "03-indexes"


def area_sort_key(area: str) -> tuple[int, str]:
    match = re.match(r"^(\d+)-", area)
    if match:
        return int(match.group(1)), area
    if area == "AGENTS.md":
        return -1, area
    return 999, area


def index_file_name(position: int, area: str) -> str:
    if area == "all":
        return "01-全库索引.jsonl"
    clean = re.sub(r"^[0-9]+-", "", area).strip() or area
    clean = re.sub(r"[\\/:*?\"<>|]", "-", clean)
    return f"{position:02d}-{clean}索引.jsonl"


def infer_index_paths(vault: Path, records: list[dict[str, str]]) -> dict[str, Path]:
    idx_dir = index_dir_for(vault)
    areas = sorted({rec["area"] for rec in records}, key=area_sort_key)
    paths = {"all": idx_dir / index_file_name(1, "all")}
    for offset, area in enumerate(areas, start=2):
        existing = sorted(idx_dir.glob(f"*-{re.sub(r'^[0-9]+-', '', area)}索引.jsonl")) if idx_dir.exists() else []
        paths[area] = existing[0] if existing else idx_dir / index_file_name(offset, area)
    return paths


def rebuild_index(vault: Path, date: str) -> None:
    records = [make_record(vault, md, date) for md in iter_markdown(vault)]
    index_paths = infer_index_paths(vault, records)
    idx_dir = index_dir_for(vault)
    idx_dir.mkdir(parents=True, exist_ok=True)
    for old in idx_dir.glob("*.jsonl"):
        old.write_text("", encoding="utf-8")
    for path in index_paths.values():
        path.write_text("", encoding="utf-8")

    for rec in records:
        line = json.dumps(rec, ensure_ascii=False)
        with index_paths["all"].open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        area_path = index_paths.get(rec["area"])
        if area_path:
            with area_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")


def check_dates(vault: Path) -> list[str]:
    bad = []
    for md in iter_markdown(vault):
        text = md.read_text(encoding="utf-8", errors="replace")
        if not DATE_RE.match(text):
            bad.append(md.relative_to(vault).as_posix())
    return bad


def run_quiet(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, text=True, capture_output=True, timeout=5)
    except Exception:
        return ""
    return (result.stdout or "").strip()


def detect_obsidian_app() -> list[str]:
    system = platform.system().lower()
    home = Path.home()
    found: list[str] = []
    candidates: list[Path] = []
    if system == "darwin":
        candidates.extend([Path("/Applications/Obsidian.app"), home / "Applications/Obsidian.app"])
        mdfind = shutil.which("mdfind")
        if mdfind:
            output = run_quiet([mdfind, "kMDItemCFBundleIdentifier == 'md.obsidian'"])
            found.extend([line for line in output.splitlines() if line])
    else:
        which = shutil.which("obsidian")
        if which:
            found.append(which)
        for command in (["flatpak", "list"], ["snap", "list", "obsidian"]):
            if shutil.which(command[0]):
                output = run_quiet(command)
                for line in output.splitlines():
                    if "obsidian" in line.lower():
                        found.append(line)
        candidates.extend([home / "Applications/Obsidian.AppImage", home / ".local/share/applications/obsidian.desktop"])
    found.extend(str(path) for path in candidates if path.exists())
    return sorted(dict.fromkeys(found))


def install_command() -> list[str] | None:
    system = platform.system().lower()
    if system == "darwin" and shutil.which("brew"):
        return ["brew", "install", "--cask", "obsidian"]
    return None


def install_obsidian_app(yes_install: bool) -> int:
    existing = detect_obsidian_app()
    if existing:
        print("Obsidian already appears to be installed:")
        for item in existing:
            print(item)
        return 0
    command = install_command()
    if not command:
        print("No automatic Obsidian install command is available.")
        print("If this is macOS, install Homebrew first or install Obsidian manually.")
        print("Official download: https://obsidian.md/download")
        print("After installing Obsidian, rerun detection.")
        return 2
    print("Install command:", " ".join(command))
    if not yes_install:
        print("Dry run only. Rerun with --yes-install to execute this command.")
        return 0
    return subprocess.run(command, check=False).returncode


def current_dir_signals(path: Path) -> tuple[int, list[str]]:
    score = 0
    signals: list[str] = []
    if (path / ".obsidian").is_dir():
        score += 5
        signals.append(".obsidian/")
    if (path / "AGENTS.md").is_file():
        score += 3
        signals.append("AGENTS.md")
    try:
        direct_md = sum(1 for child in path.iterdir() if child.is_file() and child.suffix.lower() == ".md")
    except (OSError, PermissionError):
        return 0, []
    if direct_md >= 5:
        score += 2
        signals.append("5+ direct markdown files")
    elif direct_md > 0:
        score += 1
        signals.append(f"{direct_md} direct markdown file(s)")
    return score, signals


def find_vaults(search_roots: list[Path], max_depth: int, max_dirs: int) -> list[dict[str, object]]:
    results: dict[str, dict[str, object]] = {}
    visited = 0
    for root in search_roots:
        root = root.expanduser()
        if not root.exists() or not root.is_dir():
            continue
        stack = [(root, 0)]
        while stack and visited < max_dirs:
            current, depth = stack.pop()
            visited += 1
            score, signals = current_dir_signals(current)
            if score >= 3:
                results[str(current)] = {"path": str(current), "score": score, "signals": signals}
                continue
            if depth >= max_depth:
                continue
            try:
                children = list(current.iterdir())
            except (OSError, PermissionError):
                continue
            for child in children:
                if not child.is_dir() or child.name.startswith("."):
                    continue
                if child.name in SKIP_DIRS:
                    continue
                stack.append((child, depth + 1))
    return sorted(results.values(), key=lambda item: (-int(item["score"]), str(item["path"])))


def default_search_roots() -> list[Path]:
    home = Path.home()
    return [home / name for name in ["Documents", "Desktop", "Downloads", "Obsidian", "Notes"] if (home / name).exists()]


def require_vault(path_value: str | None) -> Path:
    if not path_value:
        raise SystemExit("--vault is required for this operation")
    vault = Path(path_value).expanduser()
    if not vault.exists():
        raise SystemExit(f"Vault not found: {vault}")
    return vault


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", help="Path to the Obsidian vault root")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--rebuild-index", action="store_true")
    parser.add_argument("--check-dates", action="store_true")
    parser.add_argument("--detect-app", action="store_true", help="Best-effort read-only Obsidian app detection")
    parser.add_argument("--find-vaults", action="store_true", help="Best-effort read-only scan for candidate vault folders")
    parser.add_argument("--install-app", action="store_true", help="Print or run an Obsidian app install command")
    parser.add_argument("--yes-install", action="store_true", help="Actually execute the install command for --install-app")
    parser.add_argument("--search-root", action="append", help="Root folder to scan for vaults; can be repeated")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum directory depth for --find-vaults")
    parser.add_argument("--max-dirs", type=int, default=5000, help="Maximum directories to inspect for --find-vaults")
    args = parser.parse_args()

    if args.detect_app:
        found = detect_obsidian_app()
        if found:
            print("Obsidian app candidates:")
            for item in found:
                print(item)
        else:
            print("No Obsidian app candidates found.")

    if args.install_app:
        code = install_obsidian_app(args.yes_install)
        if code != 0:
            return code

    if args.find_vaults:
        roots = [Path(p) for p in args.search_root] if args.search_root else default_search_roots()
        candidates = find_vaults(roots, args.max_depth, args.max_dirs)
        if candidates:
            print("Candidate vaults:")
            for item in candidates:
                signals = ", ".join(item["signals"])
                print(f'{item["path"]}  [score={item["score"]}; {signals}]')
        else:
            print("No candidate vaults found.")

    if args.check_dates:
        vault = require_vault(args.vault)
        bad = check_dates(vault)
        if bad:
            print("Bad or missing date headers:")
            for rel in bad:
                print(rel)
        else:
            print("All Markdown date headers look valid.")

    if args.rebuild_index:
        vault = require_vault(args.vault)
        rebuild_index(vault, args.date)
        print(f"Rebuilt indexes for {vault} with date {args.date}.")

    if not any([args.detect_app, args.install_app, args.find_vaults, args.check_dates, args.rebuild_index]):
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
