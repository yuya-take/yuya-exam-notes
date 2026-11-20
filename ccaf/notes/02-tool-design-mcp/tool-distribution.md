# エージェントへのツールの割り振り

> ドメイン: 2. ツール設計と MCP の組み込み（18%） ／ 更新: 2026-11-20

## 3行まとめ
- 1つのエージェントに渡すツールは、役割に要るものだけに絞る。数が多いほどツール選択の精度が落ちる（ガイドの例: 18個より4〜5個）
- 汎用ツールはそのまま渡さず、入力を検証する制約付きのツールに置き換える。役割外のツールは渡さない
- 役割外でも頻繁に要る処理だけは、範囲を絞ったツール（scoped cross-role tool）を1つ渡す。複雑なケースはコーディネーター経由に残す

## 仕組み
```mermaid
flowchart LR
  C[コーディネーター<br/>Task と振り分け] --> S[検索エージェント<br/>検索・文書の読み込み]
  C --> A[分析エージェント<br/>読む・集計だけ]
  C --> W[執筆エージェント<br/>下書き + 簡易確認ツール1つ]
  W -- 簡易確認で足りない件 --> C
```

| 渡し方 | 何をするか | 選ぶ場面 |
|---|---|---|
| 役割ごとに限定（scoped tool access） | 役割に要るツールだけを渡す | 既定。サブエージェントは原則これ |
| 制約付きの代替ツール | 汎用ツールを、入力を検証する専用ツールに置き換える | 汎用ツールで想定外の使い方が起きる・起きうる |
| 範囲を絞った役割外のツール | 頻繁に要る単純な処理だけを専用ツールで渡す | 単純な依頼の往復がコーディネーター経由で多い |
| コーディネーター経由 | 専門のエージェントに回す | 複雑・まれなケース |

- 精度が落ちる理由: ツールが増えると、どれを使うかの判断が複雑になる（decision complexity）
- 役割外のツールの誤用: 専門外のツールを持つエージェントは、それを使ってしまいがち（ガイドの例: 統合役が自分で Web 検索を始める）
- Agent SDK では `AgentDefinition` の `tools` で絞る。省略すると、サブエージェントが使えるツールをすべて継承する

```python
"report-writer": AgentDefinition(
    description="集めた結果から報告書を書く",
    prompt="あなたは報告書の執筆担当です。…",
    tools=["Read", "lookup_glossary_term"])  # 検索ツールは渡さない。用語確認だけ専用ツールで
```

- tool_choice（auto / any / 特定ツールの強制）で「呼ばせ方」を決める話は → 別ノート「tool_choice の設定」

## 試験で問われそうなポイント
- ツールを十数個持つエージェントが、似たツールを取り違える → 役割ごとにエージェントを分け、1つあたりのツールを絞る
- サブエージェントが専門外の操作をしてしまう → プロンプトで禁止するより、`tools` からそのツールを外す
- 汎用の URL 取得で想定外のサイトを読む → 取得先を検証する専用ツール（ガイドの例: fetch_url → load_document）に置き換える
- 役割外の能力がときどき要る → 最小権限（least privilege）で考える。用途を1つに絞ったツールまでにとどめ、別の役割のツール群は持たせない
- `tools` を書かずにサブエージェントを定義した → 全ツールを継承する。読むだけの役割でも書き込みや実行ができてしまう

## 間違えやすいところ
- 全サブエージェントに全ツールを渡す（`tools` 省略＝全部継承）。役割をまたぐ誤用を招く
- 汎用ツールをそのまま渡す。制約付きのツールに置き換えるのが正解
- 役割外の需要があるとき、ツール一式を渡す。渡すのは範囲を絞った1つだけ
- 数の目安のずれ: ガイドは「18個より4〜5個」。公式の tool search のページは「30〜50個を超えると選択精度が落ちる」。試験ではガイドの考え方（少なく絞る）で答える
- 同じページは、10個以上なら tool search（必要なツールを検索して読み込む仕組み）を検討、とも書く。1回の依頼で読み込むのはふつう3〜5個
- 「ツールを減らす」には、似た操作を1つのツールにまとめる（action 引数）という手もある（公式の define-tools）。役割で絞る話とは別
- 現行 Claude Code では Task ツールは Agent に改名（Task は別名として有効）。ガイドは Task と書く
- 役割外のツールを1つだけ渡す設計（high-frequency の例外）を公式ドキュメントが直接説明しているかは未確認。ガイドの記述に基づく

## 確認問題
1. 社内ヘルプデスクのエージェントに、チケット・人事・経理・在庫など 20 個のツールを渡したら、誤ったツールを呼ぶことが増えた。どう直す？
   <details><summary>答え</summary>領域ごとのサブエージェントに分け、それぞれに4〜5個程度の関連ツールだけを渡す。コーディネーターが振り分ける。ツールが多いと選択の判断が複雑になり精度が落ちる。</details>
2. 議事録を要約するサブエージェントに Bash を渡していたら、要約の途中で勝手にスクリプトを実行していた。最も確実な対策は？
   <details><summary>答え</summary>`tools` から Bash を外し、Read など要約に要るツールだけにする。プロンプトで禁じるより確実で、役割外の誤用を防げる。</details>
3. 契約書チェックのエージェントに、汎用の HTTP リクエストツールを渡して社内の契約書管理システムを読ませている。ときどき社外のサイトにもアクセスしていた。どう直す？
   <details><summary>答え</summary>契約書 ID を受け取り、管理システムの決まった場所だけを読む専用ツール（例: get_contract）に置き換える。汎用ツールのままプロンプトで禁じるより確実で、入力をツール側で検証できる。</details>

## 出典
- [Claude Certified Architect – Foundations Exam Guide v1.1（Task Statement 2.3）](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf)（公式）
- [Subagents in the SDK（Tool restrictions、Common tool combinations）](https://code.claude.com/docs/en/agent-sdk/subagents)（公式。`tools` の省略で全部継承）
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)（公式。Limit tool access、`tools` と `disallowedTools`）
- [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)（公式。30〜50個を超えると選択精度が落ちる）
- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)（公式。関連する操作を少ないツールにまとめる）
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)（公式ブログ。ツールは多いほど良いわけではない、重なるツールは迷わせる）
