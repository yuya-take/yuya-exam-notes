# MCP のツールとリソースの使い分けと、既存の MCP サーバーの活用

> ドメイン: 2. ツール設計と MCP の組み込み（18%） ／ 更新: 2026-11-20

## 3行まとめ
- 動作（書き込み・外部 API の実行）はツール（tools）、読ませたいデータの一覧や中身はリソース（resources）で公開する
- 「何があるか」を探すための呼び出しが多いときは、中身の目録（content catalog）をリソースにして最初から見せる
- Jira や GitHub のような定番の連携は既存の MCP サーバーを使い、自作はチーム独自の業務に限る

## 仕組み

| 部品（primitive） | 誰が使うかを決めるか | 中身 | 例 | 主なメソッド |
|---|---|---|---|---|
| ツール（tools） | モデル（model-controlled） | 実行する関数。入力は JSON Schema | チケットを作る、DB を更新する | `tools/list`、`tools/call` |
| リソース（resources） | アプリ（application-controlled） | URI で指す読み取り用のデータ | 設計書の目次、DB のスキーマ | `resources/list`、`resources/read` |
| プロンプト（prompts） | ユーザー（user-controlled） | サーバーが用意した指示のひな形 | スラッシュコマンド | `prompts/list`、`prompts/get` |

```mermaid
flowchart LR
  Q[エージェントが<br>データを探したい] --> R{目録をリソースで<br>公開している?}
  R -->|はい| C[目録を1回読む<br>→ 必要な1件だけ取る]
  R -->|いいえ| T[検索ツールを何度も試す<br>= 探索のための呼び出し]
```

- リソースは URI（例: `docs://adr/index`）で1件ずつ識別する。引数付きの URI はリソーステンプレート（resource templates、例: `alerts://{service}/open`）
- Claude Code では `@サーバー名:URI` で参照すると、中身が添付として会話に入る
- Claude Code は、リソースを持つサーバーがあると、一覧と読み取りのツール（`ListMcpResourcesTool`、`ReadMcpResourceTool`）を自動で用意する。モデル自身もリソースを読める
- 接続時に、設定した全サーバーのツール・プロンプト・リソースを取得する（設定のしかたは → 別ノート「Claude Code と Agent SDK への MCP サーバーの組み込み」）

### 既存のサーバーか自作か

| 状況 | 選ぶもの |
|---|---|
| 定番の SaaS（課題管理、チャット、リポジトリ）とつなぐ | 既存のコミュニティ・公式の MCP サーバー |
| チーム独自の業務手順・社内システム | 自作の MCP サーバー |

- 既存のサーバーは MCP Registry（公開サーバーの公式の目録。プレビュー版）や Anthropic Directory で探せる
- 信頼できるサーバーか確かめてからつなぐ（外部の内容を取るサーバーはプロンプトインジェクションの入口になる）

## 試験で問われそうなポイント
- エージェントが「どんなデータがあるか」を知るためにツールを何度も呼んでいる → 目録をリソースで公開する
- 書き込みや外部への副作用がある操作 → リソースではなくツールにする
- 定番の課題管理ツールとの連携を一から作ろうとしている → 既存の MCP サーバーを使う
- 社内独自の承認フローなど、既存のものが無い → 自作のサーバーにする
- エージェントが MCP ツールより組み込みの Grep を選んでしまう → ツールの説明文を改善する（→ 別ノート「ツールの説明文と境界の設計」）

## 間違えやすいところ
- アンチパターン: 既存のコミュニティの MCP サーバーで足りるのに、同じ連携を自作する
- アンチパターン: 目録を見せずに、検索ツールの試し打ちで中身を探らせる（呼び出しとトークンが増える）
- リソースは「読むだけ」。更新や送信のような動作をリソースにしない
- プロンプトはユーザーが選んで使うひな形で、モデルが自分で呼ぶ部品ではない
- `claude -p`（非対話）では `@` の参照は普通の文字列のままで、自動では添付されない
- ずれ: ガイドは「接続時に全ツールが見つかり同時に使える」と書くが、現行の Claude Code は既定で tool search（ツールの定義を必要になったときに読み込む仕組み）が有効。試験はガイドの書き方で答える

## 確認問題
1. 社内の設計判断の記録（ADR）が数百件あり、エージェントが関係する記録を探すために検索ツールを毎回5〜6回呼んでいる。まず何をするべきか。
   <details><summary>答え</summary>ADR の目録（タイトル・日付・対象）をリソースで公開する。目録を1回読めば必要な記録だけを取れ、探索のための呼び出しが減る。検索ツールを増やしても試し打ちは減らない。</details>
2. 障害対応のエージェントに「監視のアラートを確認済みにする」機能を足したい。リソースとツールのどちらで公開するか。
   <details><summary>答え</summary>ツール。状態を変える操作はモデルが呼ぶツールにする。リソースは読み取り用のデータで、副作用のある操作には向かない。</details>
3. チームで GitHub の PR 一覧と、社内独自のリリース承認の手順の両方をエージェントに扱わせたい。どう組むか。
   <details><summary>答え</summary>GitHub は既存の MCP サーバーを使い、リリース承認だけを自作のサーバーにする。定番の連携を自作すると、保守の手間が増えるだけで得るものが少ない。</details>

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
