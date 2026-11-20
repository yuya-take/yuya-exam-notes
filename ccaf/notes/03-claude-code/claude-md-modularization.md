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

??? question "Q1. モノレポの `api/` だけが社内の認証規約に従う必要がある。規約は `docs/auth.md` にある。`web/` の作業では読ませたくない。どうする？"
    `api/CLAUDE.md` に `@../docs/auth.md` を書く。import は取り込み元と一緒に読まれるので、`api/` の CLAUDE.md が読まれるときだけ効く。ルートの CLAUDE.md に書くと全体に効いてしまう。なお `api/` から起動すると、取り込み先は作業ディレクトリの外になるので、初回に承認が要る。

??? question "Q2. 400行の CLAUDE.md を `@` で5ファイルに分けた。「文脈の消費が減ったはず」という説明は正しい？"
    誤り。import 先は取り込み元と一緒に展開されるので、量は同じだ。減らしたいなら、一部の作業でしか要らない内容を `paths` 付きのルールやスキルに移す。

??? question "Q3. フロントとバックエンドの担当者が、同じ CLAUDE.md を毎週書き換えて衝突している。どう整理する？"
    `.claude/rules/` に `frontend/`・`backend/` などトピック別のファイルを作って分ける。1ファイル1トピックなので、担当ごとに保守できる。

## 出典
- [How Claude remembers your project（Import additional files / Organize rules with .claude/rules/ / My CLAUDE.md is too large）](https://code.claude.com/docs/en/memory)（公式）
- Claude Certified Architect – Foundations Exam Guide v1.1、Task Statement 3.1（公式）
- 未確認: 試験がどの版の Claude Code の挙動（import の段数の上限など）を前提にしているか
