# MCP のツールとリソースの使い分けと、既存の MCP サーバーの活用

> ドメイン: 2. ツール設計と MCP の組み込み（18%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    動作（書き込み・外部 API の実行）は ==ツール（tools）==、読ませたいデータの一覧や中身は ==リソース（resources）== で公開する。Jira や GitHub のような定番の連携は既存の MCP サーバーを使い、自作はチーム独自の業務に限る。

## 仕組み

MCP サーバーが公開する部品（primitive）は3つで、違いは「誰が使うかを決めるか」にある。ツールはモデルが自分で呼ぶ。リソースは読み取り用のデータで、副作用のある操作には向かない。プロンプトはユーザーが選んで使うひな形で、モデルが自分で呼ぶ部品ではない。

| 部品 | 誰が使うかを決めるか | 中身 | 例 | 主なメソッド |
|---|---|---|---|---|
| ツール | モデル（model-controlled） | 実行する関数。入力は JSON Schema | チケットを作る、DB を更新する | `tools/list`、`tools/call` |
| リソース | アプリ（application-controlled） | URI で指す読み取り用のデータ | 設計書の目次、DB のスキーマ | `resources/list`、`resources/read` |
| プロンプト（prompts） | ユーザー（user-controlled） | サーバーが用意した指示のひな形 | スラッシュコマンド | `prompts/list`、`prompts/get` |

エージェントが「何があるか」を探すために呼び出しを重ねているなら、中身の目録（content catalog）をリソースにして最初から見せる。目録を1回読めば、必要な1件だけを取りに行ける。目録が無いと、検索ツールの試し打ちが続き、呼び出しとトークンが増える。

```mermaid
flowchart LR
  Q["エージェントがデータを探したい"] --> R{"目録をリソースで公開している?"}
  R -->|はい| C["目録を1回読む → 必要な1件だけ取る"]
  R -->|いいえ| T["検索ツールを何度も試す = 探索のための呼び出し"]
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  classDef judge fill:#fff8e1,stroke:#f9a825,color:#4e342e
  classDef done fill:#e8f5e9,stroke:#43a047,color:#1b5e20
  classDef ng fill:#fdecea,stroke:#e53935,color:#8e1c13
  class Q run
  class R judge
  class C done
  class T ng
```

既存のサーバーか自作かは、つなぐ先で決める。課題管理、チャット、リポジトリのような定番の SaaS には、既存のコミュニティ・公式の MCP サーバーを使う。チーム独自の業務手順や社内システムだけを自作する。既存のサーバーは MCP Registry（公開サーバーの公式の目録。プレビュー版）や Anthropic Directory で探せる。外部の内容を取るサーバーはプロンプトインジェクションの入口になるので、信頼できるか確かめてからつなぐ。

??? info "Claude Code でのリソースの扱い・ガイドとのずれ"
    - リソースは URI（例: `docs://adr/index`）で1件ずつ識別する。引数付きの URI はリソーステンプレート（resource templates、例: `alerts://{service}/open`）
    - Claude Code では `@サーバー名:URI` で参照すると、中身が添付として会話に入る。`claude -p`（非対話）では `@` の参照は普通の文字列のままで、自動では添付されない
    - Claude Code は、リソースを持つサーバーがあると、一覧と読み取りのツール（`ListMcpResourcesTool`、`ReadMcpResourceTool`）を自動で用意する。モデル自身もリソースを読める
    - 接続時に、設定した全サーバーのツール・プロンプト・リソースを取得する（設定のしかたは別ノート「[Claude Code と Agent SDK への MCP サーバーの組み込み](mcp-server-integration.md)」）
    - ずれ: ガイドは「接続時に全ツールが見つかり同時に使える」と書く。現行の Claude Code は既定で tool search（ツールの定義を必要になったときに読み込む仕組み）が有効。試験はガイドの書き方で答える

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| 「どんなデータがあるか」を知るためにツールを何度も呼んでいる | 目録をリソースで公開する | 検索ツールの試し打ちで中身を探らせる |
| 書き込みや外部への副作用がある操作 | ツールにする | リソースにする（リソースは読むだけ） |
| 定番の課題管理ツールと、社内独自の承認フローをつなぐ | 課題管理は既存の MCP サーバー、既存のものが無い承認フローだけ自作する | 既存のサーバーで足りるのに、同じ連携を一から作る |
| エージェントが MCP ツールより組み込みの Grep を選ぶ | ツールの説明文を改善する（別ノート「[ツールの説明文と境界の設計](tool-descriptions-boundaries.md)」） | 説明文を「検索する」程度のままにする（Claude は説明文で選ぶので、なじみのある Grep と区別できない） |

</div>

## 確認問題

**Q1.** 開発者の質問に答えるエージェントを作っている。社内の設計判断の記録（ADR）が数百件あり、エージェントは関係する記録を探すために、検索ツールを毎回5〜6回呼んでいる。まず行うべき対応として最も適切なものはどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="A" markdown>

- A. ADR の目録をリソースで公開し、最初に読めるようにする
- B. 検索ツールを、タイトル検索用と本文検索用の2つに分けて増やす
- C. システムプロンプトに「検索ツールは2回までしか呼ばないこと」と書き足す
- D. ADR を探す手順を、プロンプト（prompts）のひな形としてサーバーに用意する

</div>

??? success "答えと解説"
    **正解: A。** 目録を1回読めば、必要な記録だけを取りに行けるので、探索のための呼び出しが減る。

    - B: 検索ツールを増やしても、何があるか分からないままの試し打ちは減らない
    - C: 回数を縛っても、目録が無いという原因は残る。必要な記録に届かないまま終わりやすい
    - D: プロンプトはユーザーが選んで使うひな形で、モデルが自分で呼ぶ部品ではない

**Q2.** 開発チームの運用を手伝うエージェントに、「監視のアラートを確認済みにする」機能を MCP サーバーで足したい。最も適切な公開のしかたはどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="C" markdown>

- A. 未対応のアラートの一覧をリソースにし、読み取られたら確認済みにする
- B. 確認済みにする手順を、プロンプト（prompts）のひな形として用意する
- C. 確認済みにする操作を、アラート ID を受け取るツールとして公開する
- D. `alerts://{id}/ack` というリソーステンプレートを作り、読むと確認済みになるようにする

</div>

??? success "答えと解説"
    **正解: C。** 状態を変える操作は、モデルが呼ぶツールにする。

    - A: リソースは読み取り用のデータで、読んだら状態が変わるような副作用には向かない
    - B: プロンプトはユーザーが選んで使うもので、エージェントが自分で実行できない
    - D: リソーステンプレートも引数付きのリソースにすぎず、読むだけの部品だ

**Q3.** 開発者の生産性を上げるため、エージェントに、GitHub の PR 一覧を見ることと、社内独自のリリース承認システム（社内 API）で承認を申請し、状況を確かめることの両方をさせたい。MCP サーバーの組み方として最も適切なものはどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="C" markdown>

- A. 両方の連携を1つの自作サーバーにまとめ、GitHub の部分も社内で実装する
- B. 既存の GitHub の MCP サーバーだけをつなぎ、承認の手順はシステムプロンプトに書く
- C. GitHub は既存の MCP サーバーを使い、リリース承認だけを自作のサーバーにする
- D. 承認の手順に使える公開サーバーを MCP Registry で探し、GitHub の連携は自作する

</div>

??? success "答えと解説"
    **正解: C。** 定番の連携は既存のサーバーを使い、自作はチーム独自の業務に限る。

    - A: 既存のサーバーで足りる連携を、一から作ることになる
    - B: 社内の承認システムを操作する手段が無い。既存のものが無い承認フローは自作する
    - D: 逆になっている。社内独自の手順に既存の公開サーバーは無く、定番の GitHub は既存のものを使う

## 出典
- [MCP Specification 2026-07-28: Server Features Overview](https://modelcontextprotocol.io/specification/2026-07-28/server/index)（公式）
- [MCP Specification 2026-07-28: Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)（公式）
- [MCP Specification 2026-07-28: Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)（公式）
- [MCP Specification 2026-07-28: Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)（公式）
- [Understanding MCP servers](https://modelcontextprotocol.io/docs/learn/server-concepts)（公式）
- [The MCP Registry](https://modelcontextprotocol.io/registry/about)（公式）
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)（公式。Use MCP resources、Scale with MCP tool search、Find and build MCP servers）
- [Tools reference](https://code.claude.com/docs/en/tools-reference)（公式。ListMcpResourcesTool、ReadMcpResourceTool）
- Claude Certified Architect – Foundations Exam Guide v1.1（公式。タスクステートメント 2.4）
- 未確認: 「既存のサーバーを選ぶべき」という判断基準そのものは公式ドキュメントに明文が無く、ガイドの記述に基づく
