#!/usr/bin/env python3
"""学習ノートを機械的にチェックする。

- Markdown の相対リンクの切れ
- 資格の README のチェックリストから張ったノートへのリンクの切れ
- notes/ 以下のノートに、必須の見出しと冒頭の「ひとことで」の箱が揃っているか
- ノートの「出典」に URL が1つ以上あるか
- notes/ 以下に、どのチェックリスト項目からも張られていないノートが無いか（警告）
- 「⚠️ 要更新」の印が付いたノートの数（情報）

エラーがあれば exit 1。警告と情報だけなら exit 0。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_HEADINGS = ["仕組み", "試験での見分け方", "確認問題", "出典"]
SUMMARY_RE = re.compile(r'^!!! abstract "ひとことで"\s*$', flags=re.M)  # 冒頭の結論の箱
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKIP_DIRS = {".git", "node_modules", ".claude", "site", "site_src"}  # .claude はスキルのテンプレート（プレースホルダのリンクを含む）
# 使うスキルが初めて実行されたときに作られるファイル。まだ無くてもリンク切れにしない
LAZY_FILES = {"quiz-log.md", "mistakes.md", "cheatsheet.md", "flashcards.csv", "study-log.md", "retro.md", "glossary.md"}

errors, warnings, infos = [], [], []


def md_files():
    for p in ROOT.rglob("*.md"):
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            yield p


def strip_code(text):
    """コードブロックとインラインコードの中は、リンクとして扱わない。"""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def rel(p):
    return p.relative_to(ROOT).as_posix()


def check_links(path, text):
    for m in LINK_RE.finditer(strip_code(text)):
        target = m.group(1)
        if re.match(r"^(?:[a-z]+:|#|<)", target) or "<" in target:
            continue
        target_path = (path.parent / target.split("#")[0]).resolve()
        if not target_path.exists() and target_path.name not in LAZY_FILES:
            errors.append(f"{rel(path)}: リンク切れ → {target}")


def exam_dirs():
    for readme in ROOT.glob("*/README.md"):
        if "## ドメイン別チェックリスト" in readme.read_text(encoding="utf-8"):
            yield readme.parent


def check_note(note):
    text = note.read_text(encoding="utf-8")
    body = strip_code(text)
    headings = set(re.findall(r"^##\s+(.+?)\s*$", body, flags=re.M))
    missing = [h for h in REQUIRED_HEADINGS if h not in headings]
    if missing:
        errors.append(f"{rel(note)}: 見出しが足りない → {', '.join(missing)}")
    if not SUMMARY_RE.search(text):
        errors.append(f"{rel(note)}: 冒頭の「!!! abstract \"ひとことで\"」の箱が無い")
    m = re.search(r"^##\s+出典\s*$(.*?)(?=^##\s|\Z)", text, flags=re.M | re.S)
    if m and not re.search(r"https?://", m.group(1)):
        errors.append(f"{rel(note)}: 出典に URL が無い")
    if "⚠️ 要更新" in text:
        infos.append(f"{rel(note)}: 要更新の印あり")


def main():
    for p in md_files():
        check_links(p, p.read_text(encoding="utf-8"))

    for exam in exam_dirs():
        readme_text = (exam / "README.md").read_text(encoding="utf-8")
        linked = {
            (exam / t).resolve()
            for t in re.findall(r"\]\((notes/[^)\s#]+)", readme_text)
        }
        for note in sorted((exam / "notes").rglob("*.md")) if (exam / "notes").exists() else []:
            check_note(note)
            if note.resolve() not in linked:
                warnings.append(f"{rel(note)}: README のチェックリストから張られていない")

    for label, items in (("エラー", errors), ("警告", warnings), ("情報", infos)):
        if items:
            print(f"## {label}（{len(items)}）")
            for i in items:
                print(f"- {i}")
    if not (errors or warnings or infos):
        print("ノートのチェック: 問題なし")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
