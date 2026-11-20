# 人への引き継ぎの要約と、複数の用件を含む依頼の分解（Structured handoff、1.4）

> ドメイン: 1. エージェントの構成とオーケストレーション（27%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    1通に複数の用件があれば、項目に分けて全部を調べ、==1つの回答にまとめる==。人に引き継ぐときは、会話ログを読めない相手でも次の一手を打てるよう、==構造化した要約==で渡す。

## 仕組み

### 複数の用件の分解（decomposition）

まず依頼を別々の項目に分ける。次に、本人確認済みの顧客 ID のような共有の情報を使って、各項目を並行に調べる。最後に結果を1つの回答にまとめる。互いに依存しない調査は並行に、前の結果が要る調査は順番に行う。用件のうち1つだけが人の判断を要するなら、残りは自分で解決し、その1つだけを引き継ぐ。

```mermaid
flowchart LR
  M[1通の依頼] --> S[用件を項目に分ける]
  S --> C["共有の情報<br>本人確認済みの顧客 ID・注文履歴"]
  C --> A[用件A を調査]
  C --> B[用件B を調査]
  C --> D[用件C を調査]
  A & B & D --> U[1つの回答にまとめる]
  B -.自分で解決できない.-> H[構造化した引き継ぎ]
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  classDef done fill:#e8f5e9,stroke:#43a047,color:#1b5e20
  class M,S,C,A,B,D run
  class U,H done
```

並行の調査は、API ではパラレルツール使用（parallel tool use）で行える。1回の応答で複数のツールを呼ぶ機能で、既定で有効だ。並行に呼んだときは、すべての tool_result を次の user メッセージ1通にまとめて返す。分けて返すと、以後 Claude が並行に呼ばなくなる。

### 構造化した引き継ぎ（structured handoff）

受け手の人は会話ログ（transcript）を見られないことがある。だから、ログへの参照ではなく、要点を項目に分けた要約を渡す。作業の途中で人に回すとき（mid-process escalation）も、そこまでの調査結果を引き継ぐ。

| 項目 | ガイドの記載 | 入れる理由 |
|---|---|---|
| 顧客 ID・顧客の情報 | あり | 受け手が本人確認と検索をやり直さずに済む |
| 根本原因（root cause） | あり | 「何が起きたか」を調べ直さずに済む |
| 金額（例: 返金額） | あり | 判断に要る数値をぼかさずに渡す |
| 推奨アクション | あり | 受け手は承認・却下を決めるだけにできる |
| 対応済みのこと・引き継ぐ理由 | なし（自作の補足） | 二重の対応と、同じ説明の繰り返しを防ぐ |

??? info "細かい決まりと、未確認のこと"
    - 実行しなかった呼び出しにも、`is_error: true` の tool_result を返す
    - 「共有の情報（shared context）」は、ガイドに定義が無い。ここでは「各調査が使う、一度だけ取得した顧客情報」と解釈した（未確認）
    - 公式ドキュメントに引き継ぎ要約の決まった形式は無い。項目はガイドの記載に基づく（docs 上は未確認）
    - 形の例（自作）: `{"customer_id": "...", "issue": "...", "root_cause": "...", "amount": 0, "recommended_action": "..."}`
    - `escalate_to_human` はガイドのシナリオの架空のツール名。公式のツールではない
    - 要約で金額・日付・顧客の言った期待をぼかすと、引き継ぎが役に立たない（要約の劣化は 5.1 の論点）
    - ここでの分解は「依頼を項目に分ける」こと。多エージェントのタスク分解（1.6 のプロンプトチェーンと動的な分解）とは別の論点
    - いつ引き継ぐか（基準）は 5.2 が主で、別ノート（escalation-ambiguity）。前提の手順をプログラムで強制する話は、同じ 1.4 の別ノート（programmatic-workflow-enforcement）

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| 受け手が会話ログを見られない | 顧客 ID・根本原因・金額・推奨アクションを項目にした要約を渡す | 「詳しくは会話を参照」「返金希望」だけを渡す（受け手が調べ直しになる） |
| 1通に用件が3つ | 項目に分けて全部を調べ、1つの返事にまとめる | 最初の用件だけに答える。用件ごとにばらばらの返事を返す |
| 独立した調査が2つ | 1回の応答で並行に呼ぶ | 依存が無いのに順番に呼ぶ |
| 1件だけ人の判断が要る | 残りは自分で解決し、その1件だけ引き継ぐ | 全件をまとめて人に回す |

</div>

## 確認問題

??? question "Q1. 旅行予約のエージェントに「ホテルの日付変更」「二重請求の返金」「ポイントが付いていない」の3件が1通で届いた。どう処理する？"
    3つの項目に分け、本人確認済みの会員情報を共有して並行に調べ、結果を1つの返事にまとめる。最初の1件だけに答えたり、3回に分けて返したりすると、取りこぼしや混乱が起きる。

??? question "Q2. 上の返金が上限を超え、人の担当者へ回す。担当者のツールには会話ログが表示されない。何を渡す？"
    会員 ID、二重請求の根本原因（どの決済が重複したか）、返金額、推奨アクション（例: 2件目の決済の全額返金）を構造化して渡す。他の2件は解決済みと添えると、二重対応を防げる。

??? question "Q3. 「ポイントの付与状況」と「付与の規約」を調べたい。どちらも会員 ID だけで引ける。順番に呼ぶべき？"
    互いに依存しないので、1回の応答で並行に呼んでよい。結果の tool_result 2つは、次の user メッセージ1通にまとめて返す。

## 出典
- Claude Certified Architect – Foundations Exam Guide v1.1、Task Statement 1.4・Exercise 1（公式。PDF はリポジトリに置かない）
- [Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use)（公式）
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)（公式）
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)（公式ブログ。並列化の sectioning、人の判断に戻す checkpoint）
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)（公式ブログ。委任時に目的・出力形式・境界を渡す、並行の調査と統合）
- [Customer support agent](https://platform.claude.com/docs/en/about-claude/use-case-guides/customer-support-chat)（公式。エスカレーションの指標はあるが、引き継ぎの形式は書かれていない）
