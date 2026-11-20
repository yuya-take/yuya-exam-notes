#!/usr/bin/env python3
"""GitHub Pages 用に、公開するノートだけを site_src/ に集め、ナビゲーションを作る。

MkDocs は、設定ファイルと同じディレクトリを docs_dir にできない。そこで、
公開する Markdown（資格ディレクトリと用語集）を site_src/ に写してから mkdocs build する。
.claude/・.github/・.orchestrate/ と、スキルの説明が中心のトップの README は写さない。

作るもの:
- site_src/index.md: サイトの先頭ページ（資格の一覧とドメイン別のノート数）
- mkdocs.gen.yml: mkdocs.yml を引き継ぎ、nav を足した設定。ノートの並びは
  各資格の README のチェックリストの順にする。ページ下の「前へ」「次へ」もこの順になる

使い方: python3 .claude/scripts/build_site.py && mkdocs build -f mkdocs.gen.yml
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site_src"
GEN_CONFIG = ROOT / "mkdocs.gen.yml"
EXCLUDE_TOP = {".git", ".github", ".claude", ".orchestrate", "site", "site_src"}
INCLUDE_TOP_FILES = {"glossary.md"}
EXCLUDE_PARTS = {"answer"}  # /hands-on の成果物の写しは公開しない
SUFFIXES = {".md", ".png", ".jpg", ".jpeg", ".svg", ".csv"}
NOTE_LINK_RE = re.compile(r"\]\((notes/[^)\s#]+\.md)")


def h1(path):
    m = re.search(r"^#\s+(.+?)\s*$", path.read_text(encoding="utf-8"), flags=re.M)
    return m.group(1) if m else path.stem


def exam_dirs():
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and d.name not in EXCLUDE_TOP and not d.name.startswith("."):
            if (d / "README.md").exists():
                yield d


def checklist_sections(readme):
    """チェックリストの「### ドメイン」見出しごとに、張られたノートを並び順のまま返す。"""
    text = readme.read_text(encoding="utf-8")
    m = re.search(r"^## ドメイン別チェックリスト\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    if not m:
        return []
    sections = []
    for line in m.group(1).splitlines():
        head = re.match(r"^###\s+(.+?)\s*$", line)
        if head:
            sections.append((head.group(1), []))
            continue
        link = NOTE_LINK_RE.search(line)
        if link and sections:
            sections[-1][1].append(link.group(1))
    return [(title, notes) for title, notes in sections if notes]


def copy_files():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for f in INCLUDE_TOP_FILES:
        if (ROOT / f).exists():
            shutil.copy2(ROOT / f, OUT / f)
    for d in exam_dirs():
        for src in d.rglob("*"):
            rel = src.relative_to(ROOT)
            if src.is_dir() or EXCLUDE_PARTS & set(rel.parts) or src.suffix not in SUFFIXES:
                continue
            dst = OUT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def build_nav_and_index():
    nav = [{"ホーム": "index.md"}]
    index = ["# 資格試験の学習ノート", "", "左のメニューか、下の一覧から資格を選ぶ。"
             "ノートのページ下の「前へ」「次へ」で、チェックリストの順に前後の単元へ移れる。", ""]
    for d in exam_dirs():
        name = re.sub(r"\s*学習ノート\s*$", "", h1(d / "README.md"))
        sections = checklist_sections(d / "README.md")
        listed = {f"{d.name}/README.md"}
        children = [{"試験の概要とチェックリスト": f"{d.name}/README.md"}]
        index += [f"## [{name}]({d.name}/README.md)", ""]
        if sections:
            index += ["| ドメイン | ノート | 最初のノート |", "|---|---|---|"]
        for title, notes in sections:
            paths = [f"{d.name}/{n}" for n in notes if (d / n).exists()]
            if not paths:
                continue
            listed.update(paths)
            children.append({title: paths})
            index.append(f"| {title} | {len(paths)}本 | [{h1(ROOT / paths[0])}]({paths[0]}) |")
        others = sorted(
            p.relative_to(OUT).as_posix() for p in (OUT / d.name).rglob("*.md")
        )
        others = [p for p in others if p not in listed]
        if others:
            children.append({"その他": others})
        nav.append({name: children})
        index.append("")
    if (OUT / "glossary.md").exists():
        nav.append({"用語集": "glossary.md"})
        index += ["## [用語集](glossary.md)", "", "資格をまたいだ用語の一覧。", ""]
    (OUT / "index.md").write_text("\n".join(index), encoding="utf-8")
    # YAML は JSON の上位互換なので、値は json.dumps で書けば引用符の扱いを気にしなくてよい
    GEN_CONFIG.write_text(
        "# .claude/scripts/build_site.py が作る。直接編集しない（.gitignore 済み）\n"
        "INHERIT: mkdocs.yml\n"
        f"nav: {json.dumps(nav, ensure_ascii=False)}\n",
        encoding="utf-8",
    )


def main():
    copy_files()
    build_nav_and_index()
    count = sum(1 for p in OUT.rglob("*") if p.is_file())
    print(f"site_src/ に {count} ファイルを集め、{GEN_CONFIG.name} を作りました")


if __name__ == "__main__":
    main()
