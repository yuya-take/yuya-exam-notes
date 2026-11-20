# CLAUDE.md のモジュール化（@import と .claude/rules/）

> ドメイン: 3. Claude Code の設定とワークフロー（20%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    大きくなった CLAUDE.md は、`@path` の import（取り込み）か `.claude/rules/`（トピック別のルールファイル置き場）に分ける。どちらも整理のための仕組みで、import や `paths` 無しのルールに移すだけでは ==文脈（context）の量は減らない==。

## 仕組み

import は、必要な規約ファイルだけをその CLAUDE.md に選んで取り込む仕組みだ。取り込んだファイルは取り込み元と同時に展開され、さらに `@` で最大4段までたどれる。rules は、1つの巨大な CLAUDE.md をトピックごとのファイルに割る仕組みだ。起動したプロジェクトの `.claude/rules/` にある ==`paths` 無しのルールは起動時に読まれる==。だから import 先も rules も、移しただけでは軽くならない。

```mermaid
flowchart LR
  R[CLAUDE.md] -->|"@docs/standards/x.md"| I["取り込んだファイル<br>同時に展開"]
  I -->|"さらに @..."| I2[最大4段まで]
  D[".claude/rules/*.md"] -->|起動時に読む| C[文脈]
  R --> C
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  class R,I,I2,D,C run
```

| | `@path` の import | `.claude/rules/` |
|---|---|---|
| 書く場所 | CLAUDE.md の本文（コードスパン・コードブロックの外） | `.claude/rules/` の下に `.md` を置く（サブフォルダも再帰で探す） |
| 何を読むか | 名指ししたファイルだけ | ディレクトリ内の全ルールファイル |
| 向いている場面 | パッケージごとに、関係する規約だけを選ぶ | 1ファイル1トピックで、チームで分担して保守する |
| 読み込むとき | 取り込み元の CLAUDE.md と同時 | 起動したプロジェクトの `paths` 無しのルールは起動時（`.claude/CLAUDE.md` と同じ優先度）。サブディレクトリの `.claude/rules/` は必要になったとき |
| 分け方・書き方 | 相対パスは取り込み元のファイルが基準（作業ディレクトリではない） | 1ファイル1トピック。名前は内容が分かるもの（例: `testing.md`） |

!!! example "使い分けの例（自作）"
    `packages/billing/CLAUDE.md` に `@../../docs/standards/payments-security.md` だけを書き、`packages/mobile/` には書かない。これが import の使い方だ。300行の CLAUDE.md を `.claude/rules/` の `code-style.md`・`testing.md`・`release.md` に割るのが rules の使い方だ。

公式の目安は、CLAUDE.md 1ファイル 200行未満だ。長いと従いにくくなる。分けた後は、import 先とルールファイル同士の矛盾を点検する。矛盾すると、Claude はどちらかを任意に選ぶことがある。

??? info "import の書き方の細則と、個人用のルール"
    - バッククォートで囲んだ `` `@README` `` は取り込まれない（コードの中は無視される）
    - 空白を含むパスは `\ ` でエスケープする。引用符で囲むと取り込まれない
    - プロジェクトのメモリファイルから作業ディレクトリの外を指す import は、初回に承認のダイアログが出る。断ると無効のまま。リポジトリ内でも、起動したディレクトリの外なら対象になる
    - `~/.claude/` の CLAUDE.md・rules からの import はダイアログ無し
    - `~/.claude/rules/` は全プロジェクトに効く個人用のルール。プロジェクトのルールより先に読まれる
    - 名前のずれ: ガイドは「@import 構文」、公式ドキュメントは「Import additional files（`@path/to/import`）」と書く。中身は同じ
    - ルールの frontmatter の `paths`（glob で条件付きに読む）は [パス指定ルール](path-scoped-rules.md)（3.3）、階層と `/memory` での確認は [CLAUDE.md の階層](claude-md-hierarchy.md) で扱う

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| パッケージごとに必要な規約が違う | 各パッケージの CLAUDE.md で、関係する規約ファイルだけを `@` で取り込む。どれを取り込むかは、そのパッケージの保守担当が自分の知識で選ぶ | ルートの CLAUDE.md に全部書き、全体に効かせる |
| 1つの CLAUDE.md が長く、担当ごとに編集がぶつかる | `.claude/rules/` にトピック別のファイルで分ける | 何でも1つの CLAUDE.md に書き足す（monolithic。ガイドは rules をその代わりに挙げる） |
| 規約ファイルの中身を複数の CLAUDE.md に書き写している | 1か所に置いて import する | 書き写しを続ける |
| ある領域のファイルを触るときだけ要るルール | `paths` 付きのルールを考える（3.3） | 常時読む rules に置く |
| 文脈の消費を減らしたい | 一部の作業でしか要らない内容を、`paths` 付きのルールやスキルに移す | import で分ける、`paths` 無しの rules に移す（import 先は取り込み元と一緒に読まれ、`paths` 無しの rules は起動時に読まれる） |
| import の相対パス | 取り込み元のファイルを基準に書く | 作業ディレクトリを基準に書く |

</div>

## 確認問題

**Q1.** EC サイトのモノレポで、Claude Code にコードを書かせている。`api/` だけが社内の認証規約に従う必要があり、規約は `docs/auth.md` にある。`web/` の作業では読ませたくない。最も適切な設定はどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="A" markdown>

- A. `api/CLAUDE.md` に `@../docs/auth.md` と書き、`api/` の CLAUDE.md が読まれるときだけ取り込む
- B. ルートの CLAUDE.md に `@docs/auth.md` と書き、「`api/` の作業のときだけ従うこと」と添える
- C. `docs/auth.md` の中身を `api/CLAUDE.md` に書き写し、元のファイルと並べて保守する
- D. `api/CLAUDE.md` に `@docs/auth.md` と、リポジトリのルート（作業ディレクトリ）を基準に書く

</div>

??? success "答えと解説"
    **正解: A。** import は取り込み元と同時に展開されるので、`api/` の CLAUDE.md から名指しすれば `api/` の作業にだけ効く。

    - B: ルートの CLAUDE.md と一緒に展開されるので、`web/` の作業でも読まれる
    - C: 書き写しは保守がずれる。1か所に置いて import する
    - D: import の相対パスは、作業ディレクトリではなく取り込み元のファイルが基準だ

**Q2.** 社内の開発者向けツールのリポジトリで、400行の CLAUDE.md を `@` の import で5ファイルに分けた。担当者は「これで毎回の文脈の消費が減った」と説明している。最も適切な見方はどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="D" markdown>

- A. 正しい。import 先は、Claude が関係あると判断したときにだけ読み込まれるので、そのぶん減る
- B. 一部は正しい。import は最初の1段だけが展開されるので、2段目以降に移した分は起動時に読まれない
- C. 誤り。ただし5ファイルを `paths` 無しで `.claude/rules/` に移せば、起動時には読まれなくなるので減る
- D. 誤り。import 先は取り込み元と同時に展開される。減らすなら、一部の作業でしか要らない内容を `paths` 付きのルールかスキルに移す

</div>

??? success "答えと解説"
    **正解: D。** import は整理の仕組みで、取り込んだ分も一緒に文脈に入る。

    - A: import 先は、Claude の判断ではなく、取り込み元と同時に必ず展開される
    - B: import は `@` で最大4段までたどられる。段を深くしても減らない
    - C: `paths` 無しのルールは起動時に読まれるので、量は変わらない

**Q3.** 同じリポジトリで、フロントエンドとバックエンドの担当者が、1つの CLAUDE.md を毎週書き換えては衝突している。最も適切な整理の仕方はどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="D" markdown>

- A. 衝突を避けるため、各担当が自分の規約を `~/.claude/rules/` に書く
- B. CLAUDE.md の中に担当ごとの見出しを作り、各自そこだけを書き足す
- C. 規約を2つのファイルに分け、ルートの CLAUDE.md から作業ディレクトリ基準のパスで `@` 取り込みする
- D. `.claude/rules/` に `frontend.md`・`backend.md` などトピック別のファイルを作り、担当ごとに保守する

</div>

??? success "答えと解説"
    **正解: D。** rules は1ファイル1トピックで分けられるので、担当ごとに編集がぶつからない。

    - A: `~/.claude/rules/` は自分の全プロジェクトに効く個人用のルールで、チームには届かない
    - B: 1つのファイルに書き足し続ける形（monolithic）のままで、衝突は減らない
    - C: import の相対パスは取り込み元のファイルが基準で、作業ディレクトリ基準では正しく取り込めない

## 出典
- [How Claude remembers your project（Import additional files / Organize rules with .claude/rules/ / My CLAUDE.md is too large）](https://code.claude.com/docs/en/memory)（公式）
- Claude Certified Architect – Foundations Exam Guide v1.1、Task Statement 3.1（公式）
- 未確認: 試験がどの版の Claude Code の挙動（import の段数の上限など）を前提にしているか
