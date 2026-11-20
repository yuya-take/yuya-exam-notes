# Agent SDK のフックによるツール呼び出しの遮断とデータの正規化

> ドメイン: 1. エージェントの構成とオーケストレーション（27%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    呼び出す前に止めるなら ==PreToolUse==、結果をモデルに渡す前に整えるなら ==PostToolUse==。業務ルールを「必ず」守らせるなら、プロンプトの指示ではなくフックを選ぶ。

## 仕組み

フック（hook）は、エージェントの実行の決まった時点で必ず呼ばれる自分のコードだ。プロンプトの指示は確率的で、守られない率がゼロにならない。フックはコードなので、確定的に制御できる。PostToolUse の時点でツールはもう実行済みなので、変えられるのはモデルに見える結果だけだ。止めたいなら PreToolUse に置く。

```mermaid
flowchart LR
  M[モデルがツール呼び出しを決める] --> P{PreToolUse}
  P -- deny + 理由 --> M
  P -- "allow / 何も返さない" --> T[ツールを実行]
  T --> Q[PostToolUse]
  Q -- 形を整えた結果 --> M
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  classDef judge fill:#fff8e1,stroke:#f9a825,color:#4e342e
  class M,T,Q run
  class P judge
```

| 時点 | できること（返す値） | 試験での用途 |
|---|---|---|
| PreToolUse | `permissionDecision: "deny"` で止める。`permissionDecisionReason` でモデルに理由を伝える。`updatedInput` で引数を書き換える | ルール違反の操作を止めて、別の手順（人への引き継ぎなど）に回す |
| PostToolUse | `updatedToolOutput` で結果を差し替える。`additionalContext` で結果に情報を足す | MCP ツールごとにばらばらな形式をそろえる |

フックは `ClaudeAgentOptions(hooks=...)` に、イベント名ごとに matcher とコールバックの組で登録する。matcher は、どのツールに効かせるかの絞り込みだ。matcher なしだと全ツールで動く。MCP ツールの名前は `mcp__<サーバー名>__<ツール名>` なので、`mcp__crm__.*` のような正規表現で絞れる。

!!! example "最小の例（Python。割引率の上限を強制する。題材は自作）"
    ```python
    async def cap_discount(input_data, tool_use_id, context):
        if input_data["tool_input"].get("discount_pct", 0) > 20:
            return {"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "20%超の割引は不可。request_manager_approval で承認を依頼すること"}}
        return {}  # 意見なし

    options = ClaudeAgentOptions(hooks={
        "PreToolUse": [HookMatcher(matcher="mcp__billing__apply_discount", hooks=[cap_discount], on_failure="block")],
        "PostToolUse": [HookMatcher(matcher="mcp__(orders|shipping)__.*", hooks=[normalize_dates])]})
    ```
    `normalize_dates` は、Unix 時刻（1970年からの秒数）や数値のステータスコードを ISO 8601 の日時や `"shipped"` などの語に直し、`updatedToolOutput` で返す想定。

??? info "細かい決まりと、ガイドとの対応"
    - 複数のフックの判断が食い違うと、制限が強いほうが勝つ（deny ＞ defer ＞ ask ＞ allow）
    - PostToolUse の `decision: "block"` は理由を結果の横に添えるだけで、元の出力はモデルに見える。差し替えるのは `updatedToolOutput`
    - 組み込みツールの `updatedToolOutput` は、出力の形が合わないと無視され、元の出力が使われる。MCP ツールの出力は形を検証されない
    - 既定では、コールバックが例外を出すと操作はそのまま進む。ガードは `on_failure="block"`（TS は `onFailure`）で、失敗時も止まるようにする（SDK の版の条件あり）
    - `systemMessage` はユーザー向けの表示。モデルに伝えるのは `permissionDecisionReason` や `additionalContext`
    - `updatedMCPToolOutput` は MCP ツール専用の古い項目。現行の公式は `updatedToolOutput` を勧める。ガイドはこの項目名を挙げていない
    - ガイドの Knowledge は PreToolUse という名前を出さず「呼び出しを遮るフック」と書く。公式ドキュメントでは PreToolUse にあたる
    - ツールの呼び出し順の強制（前提ゲート）は、1.4 の `programmatic-workflow-enforcement` のノートが主

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| 金額や割合の上限を絶対に超えさせない | PreToolUse で deny する | システムプロンプトに「必ず〜すること」と書き足す |
| 止めたあとの行き先 | `permissionDecisionReason` で代わりの手順（エスカレーション用ツールなど）を示す | 理由を `systemMessage` に書く（ユーザー向けの表示でモデルに届かない） |
| MCP ツールごとに日時やステータスの形式がばらばら | PostToolUse で1つの形式にそろえてから渡す | プロンプトで「変換して比べよ」と頼む |
| 実行前に止めたい | PreToolUse に置く | PostToolUse で確かめる（もう実行済み） |
| 1つの操作だけに効かせる | matcher でツール名を絞る | matcher なしで登録する（全ツールで動く） |

</div>

## 確認問題

??? question "Q1. 社内の2つの MCP サーバーが、片方は在庫の更新日時を Unix 時刻、もう片方は ISO 8601 で返す。エージェントが「どちらが新しいか」をよく取り違える。最も確実な対策は？"
    PostToolUse フックで両方の結果を ISO 8601 にそろえ、`updatedToolOutput` で渡す。プロンプトで「変換して比べよ」と頼むのは確率的で、取り違えが残る。

??? question "Q2. 経費精算のエージェントで「1件10万円を超える支払いは経理の承認が要る」。PostToolUse で金額を確かめて警告を出す案は良いか？"
    良くない。PostToolUse の時点で支払いは実行済みだ。PreToolUse で金額を見て deny し、理由に承認依頼ツールを使うよう書いて誘導する。

??? question "Q3. 上の PreToolUse のガードがバグで例外を出した。既定の動作と、止まるようにする設定は？"
    既定では、例外のまま通常の許可の流れに進み、操作が通りうる。matcher に `on_failure="block"`（TS は `onFailure: "block"`）を付けると、失敗時も止まる。

## 出典
- [Claude Certified Architect – Foundations Exam Guide v1.1](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf)（公式、Task Statement 1.5）
- [Intercept and control agent behavior with hooks](https://code.claude.com/docs/en/agent-sdk/hooks)（公式、Agent SDK）
- [Hooks reference](https://code.claude.com/docs/en/hooks)（公式、PostToolUse decision control と matcher のルール）
- [Get started with hooks](https://code.claude.com/docs/en/hooks-guide)（公式、フックは確定的な制御を与えるという説明）
