---
name: pr
description: 作業ブランチの変更を /secret-check で確かめてから push し、main 向けの PR を作る（既にあれば更新する）。
argument-hint: "[PR のタイトル（省略時は変更から作る）]"
---

# PR

作業ブランチの変更を確かめてから push し、`main` 向けの PR を作る。PR が既にあれば、本文を更新する。

## Step 1: 状態を確かめる

- 今のブランチが `main` なら、`<type>/<短い説明>` のブランチを切ってから進める。クラウドのセッションで、push 先のブランチが指定されているときは、それに従う
- 未コミットの変更があれば、意味のまとまりごとにコミットする。コミットメッセージは CLAUDE.md の形式に従う
- `git fetch origin main` をして、`origin/main..HEAD` のコミットと差分を把握する

## Step 2: 機微情報を確かめる

`/secret-check --range origin/main..HEAD` を実行する（Skill ツールで `secret-check` を呼ぶ）。
- **要対応:** `/secret-check` の「見つかったとき」に従う。解消するまで、push も PR の作成もしない
- **問題なし:** 次へ進む

続けて `python3 .claude/scripts/note_lint.py` を実行する。エラーがあれば直す（GitHub Actions でも同じチェックが動く）。

`git push` のときは、PreToolUse フックでも同じ機械的な検出が動く。フックに止められたら、その出力に従って直す。フックを外したり、すり抜けたりしない。

## Step 3: 確認を取る

ユーザーと対話しながら作業しているときは、`AskUserQuestion` で「PR を作ってよいか」を確認する。質問文には、PR のタイトルと変更の要約（3行程度）を入れる。
- **作ってよいと言われた:** 次へ進む
- **まだと言われた:** push までにとどめる
- **ユーザーが `/pr` を明示的に実行したとき:** それを承認とみなし、確認しない

## Step 4: push する

`git push -u origin <ブランチ>` を実行する。ネットワークのエラーなら、間隔を空けて4回まで試し直す。

## Step 5: PR を作る・更新する

1. `.github/pull_request_template.md` があれば、その見出しに沿って本文を書く
2. 無ければ、次の形で書く

```markdown
## 概要
<何のための変更か、1〜3文>

## 変更内容
- <ファイルやスキルごとの変更>

## 確認したこと
- /secret-check: 問題なし（機械的な検出と、文脈での判断）
- <動かして確かめたこと。確かめていないことは、確かめていないと書く>
```

3. GitHub の MCP ツールを使う。同じブランチの open の PR を `list_pull_requests` で探す
   - **ある:** `update_pull_request` で本文を更新する
   - **無い:** `create_pull_request` で作る（base は `main`）
4. PR の URL をユーザーに伝える。マージはしない
