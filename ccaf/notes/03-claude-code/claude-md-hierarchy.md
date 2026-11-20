# CLAUDE.md の階層（ユーザー / プロジェクト / ディレクトリ）と /memory での確認

> ドメイン: 3. Claude Code の設定とワークフロー（20%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    CLAUDE.md は ==置き場所で「誰に効くか」が決まる==。チーム全員の規約はプロジェクト、自分だけの好みはユーザーの階層に書く。人やセッションで挙動が違うときは、まず読み込まれたファイルを `/memory` などで確かめる。

## 仕組み

CLAUDE.md は、毎セッション読み込まれる指示のファイルだ。ユーザー・プロジェクト・ディレクトリの3階層に置ける。起動したディレクトリと、それより上にある CLAUDE.md は起動時に読み込まれる。サブディレクトリの CLAUDE.md は、必要になってから読み込まれる。

| 階層 | 置き場所 | 共有範囲 | 読み込まれ方 |
|---|---|---|---|
| ユーザー（user-level） | `~/.claude/CLAUDE.md` | 自分だけ（全プロジェクト）。リポジトリに入らない | 起動時 |
| プロジェクト（project-level） | `./CLAUDE.md` または `./.claude/CLAUDE.md` | チーム全員（バージョン管理で共有） | 起動時 |
| ディレクトリ（directory-level） | サブディレクトリの `CLAUDE.md` | チーム全員（リポジトリに入れた場合） | そのサブディレクトリのファイルを読む・書くとき |

`~/.claude/CLAUDE.md` と `./.claude/CLAUDE.md` は名前が似ている。だが共有範囲は逆だ。

```mermaid
flowchart LR
  M[managed policy] --> U["ユーザー<br>~/.claude/CLAUDE.md"] --> P["プロジェクト<br>./CLAUDE.md"] --> D["サブディレクトリの CLAUDE.md<br>必要になってから"]
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  class M,U,P,D run
```

読み込みは上書きではない。すべてが ==連結されて文脈に入り==、作業場所に近いものほど後に読まれる。だから矛盾する指示は優先順位では解決されず、Claude がどちらかを任意に選ぶことがある。また CLAUDE.md は強制ではなく文脈で、ユーザーメッセージとして渡される。必ず実行させたいことはフック（hook）にする。

| やりたいこと | 使うもの |
|---|---|
| メモリファイルの一覧を見て、開いて直す | `/memory` |
| 起動時に読み込まれたファイルを確かめる | `/context all` の Memory files の一覧 |
| サブディレクトリの CLAUDE.md が読み込まれたかを見る | ターミナルに出るパス付きの `Loaded` の行（`/context` の一覧には出ない） |
| いつ・なぜ読み込まれたかを記録する | `InstructionsLoaded` フック（サブディレクトリの分は読み込み理由 `nested_traversal`） |

!!! warning "ガイドと現行ドキュメントのずれ"
    ガイドは「`/memory` で読み込まれたファイルを確かめる」と書く。現行の公式ドキュメントでは、`/memory` は存在しないファイルも含めて一覧・編集する画面だ。読み込みの確認は `/context all` が主になる。試験ではガイドの書き方（`/memory`）で答える。

??? info "そのほかの置き場所と、分割の仕組み"
    - managed policy: 組織全体に IT 部門が配る CLAUDE.md。`claudeMdExcludes` では除外できない
    - `./CLAUDE.local.md`: 自分だけのプロジェクト用。`.gitignore` に入れる
    - `@path` の import と `.claude/rules/` での分割は、[CLAUDE.md のモジュール化](claude-md-modularization.md) で扱う
    - `paths` で特定のファイルだけに効かせるルールは、[パス指定ルール](path-scoped-rules.md)（3.3）で扱う

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| 新しく入ったメンバーに規約が効かない | 規約がユーザー階層にあると疑い、プロジェクトの CLAUDE.md に移す | チームの規約を自分の `~/.claude/CLAUDE.md` に置いたままにする（自分の環境では効くので気づきにくい） |
| 個人の好み（エディタ流儀、口調など） | ユーザー階層か `CLAUDE.local.md` に書く | チームのリポジトリに入れる |
| 一部のディレクトリだけの規約 | そのサブディレクトリの CLAUDE.md。複数ディレクトリにまたがるなら 3.3 のパス指定ルール | ルートの CLAUDE.md に書き、ほかの作業でも毎回文脈を使う |
| セッションごとに挙動が違う | 読み込まれたメモリファイルを確かめてから直す | 先にプロンプトを足して様子を見る |
| サブディレクトリの CLAUDE.md が `/context all` に出ない | 起動時には読まれないので異常ではない | 読み込みの失敗と決めつける |
| 上下の階層で指示が矛盾する | 連結されるだけなので、矛盾は自分で消す | 下の階層が上を上書きすると考える |

</div>

## 確認問題

??? question "Q1. 開発者 A のマシンでは「コミット前に lint を通す」が守られるが、先週入った B のマシンでは守られない。リポジトリの CLAUDE.md にはその記述が無い。まず何を疑い、どう直す？"
    A の `~/.claude/CLAUDE.md`（ユーザー階層）に書かれていると疑う。ユーザー階層はバージョン管理で共有されない。プロジェクトの `./CLAUDE.md` に移してコミットする。必ず守らせたいならフックも検討する。

??? question "Q2. モノレポの `services/billing/` だけで使う命名規則がある。ルートの CLAUDE.md に書くと、ほかのチームの作業でも毎回文脈を使う。どこに書く？"
    `services/billing/CLAUDE.md`（ディレクトリ階層）に書く。そのディレクトリのファイルを扱うときだけ読み込まれる。同じ規則が複数のディレクトリに散らばるファイルに効くなら、3.3 のパス指定ルールを選ぶ。

??? question "Q3. 同じリポジトリで、昨日と今日で Claude の振る舞いが違う。設定を変えた覚えはない。最初の一手は？"
    `/memory`（現行のドキュメントでは `/context all` も）で、どのメモリファイルが読み込まれているかを確かめる。起動したディレクトリの違いや、サブディレクトリの CLAUDE.md の読み込みの有無で、中身が変わっていることがある。

## 出典
- [How Claude remembers your project（Memory）](https://code.claude.com/docs/en/memory)（公式）
- [Hooks reference の InstructionsLoaded](https://code.claude.com/docs/en/hooks)（公式）
- [Claude Certified Architect – Foundations Exam Guide v1.1 の Task Statement 3.1](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf)（公式）
- 未確認: ディレクトリ階層の CLAUDE.md が `/memory` の一覧に出るかどうか（公式ドキュメントに記述が無い）
