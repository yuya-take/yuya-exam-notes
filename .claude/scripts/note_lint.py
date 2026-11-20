#!/usr/bin/env python3
"""学習ノートを機械的にチェックする。

- Markdown の相対リンクの切れ
- 資格の README のチェックリストから張ったノートへのリンクの切れ
- notes/ 以下のノートに、必須の見出しと冒頭の「ひとことで」の箱が揃っているか
- ノートの「出典」に URL が1つ以上あるか
- notes/ 以下に、どのチェックリスト項目からも張られていないノートが無いか（警告）
- 確認問題（<div class="quiz" data-answer="…">）の正解の記号が選択肢にあるか、
  選ぶ数が問題文の「（Nつ選べ）」と合うか、直後に「答えと解説」があるか
- 1つ選ぶ問題の正解の位置が A〜D で偏っていないか（警告）
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

QUIZ_RE = re.compile(r'<div class="quiz" data-answer="([A-Z](?:,[A-Z])*)" markdown>(.*?)</div>', flags=re.S)
CHOOSE_RE = re.compile(r"（(\d+)つ選べ）")

errors, warnings, infos = [], [], []
answer_counts = {}


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
    check_quiz(note, text)
    if "⚠️ 要更新" in text:
        infos.append(f"{rel(note)}: 要更新の印あり")


def check_quiz(note, text):
    quizzes = list(QUIZ_RE.finditer(text))
    if not quizzes:
        errors.append(f'{rel(note)}: 確認問題が選択式（<div class="quiz" data-answer=…>）になっていない')
    prev_end = 0
    for i, m in enumerate(quizzes, 1):
        answers = m.group(1).split(",")
        letters = re.findall(r"^- ([A-Z])\. ", m.group(2), flags=re.M)
        choose = CHOOSE_RE.findall(text[prev_end:m.start()])
        where = f"{rel(note)}: 確認問題 {i}"
        if any(a not in letters for a in answers):
            errors.append(f"{where}: 正解 {m.group(1)} が選択肢 {''.join(letters)} に無い")
        if letters != [chr(ord("A") + k) for k in range(len(letters))]:
            errors.append(f"{where}: 選択肢の記号が A から順に並んでいない")
        if not choose or int(choose[-1]) != len(answers):
            errors.append(f"{where}: 問題文の「（Nつ選べ）」と、正解の数（{len(answers)}）が合わない")
        if not re.match(r'\s*\?\?\? success "答えと解説"', text[m.end():m.end() + 200]):
            errors.append(f'{where}: 直後に「??? success "答えと解説"」が無い')
        if len(answers) == 1:
            answer_counts[answers[0]] = answer_counts.get(answers[0], 0) + 1
        prev_end = m.end()


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

    if answer_counts:
        total = sum(answer_counts.values())
        dist = "、".join(f"{k}: {answer_counts[k]}" for k in sorted(answer_counts))
        if total >= 8 and (len(answer_counts) < 4 or max(answer_counts.values()) > total * 0.4):
            warnings.append(f"1つ選ぶ問題の正解の位置が偏っている → {dist}")
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
