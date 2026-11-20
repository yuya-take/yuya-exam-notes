#!/usr/bin/env python3
"""GitHub Pages 用に、公開するノートだけを site_src/ に集める。

MkDocs は、設定ファイルと同じディレクトリを docs_dir にできない。そこで、
公開する Markdown（資格ディレクトリ、トップの README、用語集）を site_src/ に写してから
mkdocs build する。.claude/・.github/・.orchestrate/ など、学習ノート以外は写さない。
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site_src"
EXCLUDE_TOP = {".git", ".github", ".claude", ".orchestrate", "site", "site_src"}
INCLUDE_TOP_FILES = {"README.md", "glossary.md"}
EXCLUDE_PARTS = {"answer"}  # /hands-on の成果物の写しは公開しない


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for f in INCLUDE_TOP_FILES:
        if (ROOT / f).exists():
            shutil.copy2(ROOT / f, OUT / f)
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name in EXCLUDE_TOP or d.name.startswith("."):
            continue
        if not (d / "README.md").exists():
            continue
        for src in d.rglob("*"):
            rel = src.relative_to(ROOT)
            if src.is_dir() or EXCLUDE_PARTS & set(rel.parts):
                continue
            if src.suffix not in {".md", ".png", ".jpg", ".jpeg", ".svg", ".csv"}:
                continue
            dst = OUT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    print(f"site_src/ に {sum(1 for p in OUT.rglob('*') if p.is_file())} ファイルを集めました")


if __name__ == "__main__":
    main()
