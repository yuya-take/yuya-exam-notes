# 大きなコードベースの探索でのコンテキスト管理

> ドメイン: 5. コンテキスト管理と信頼性（15%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    長い探索では文脈が劣化（context degradation）する。重要な事実は==会話の外（ファイル・要約）に置き==、次の段階には要約を明示的に渡す。

## 仕組み

長い探索を続けると、前に見つけた具体的なクラス名ではなく「一般的には〜」と、よくあるパターンで答え始める。同じ問いへの答えが前と食い違うのも、劣化の合図だ。会話の中だけにある事実は、compaction（要約で詰めること）や文脈の境目で失われる。だから発見はファイルに書き出し、うるさい探索はサブエージェントに出して、要約だけを受け取る。

```mermaid
flowchart LR
  M[メインのエージェント<br>全体の調整] -->|具体的な問い| S1[サブエージェント<br>段階1の探索]
  S1 -->|要約だけ返す| M
  M -->|発見を書く| P[(スクラッチパッド)]
  M -->|段階1の要約を最初の文脈に入れる| S2[サブエージェント<br>段階2の探索]
  S1 & S2 -->|状態を書き出す| F[(決まった場所の状態ファイル)]
  F -->|再開時にマニフェストを読む| M
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  classDef done fill:#e8f5e9,stroke:#43a047,color:#1b5e20
  class M,S1,S2 run
  class P,F done
```

| 手法 | 使う状況 | やること | 使わない状況 |
|---|---|---|---|
| スクラッチパッド（scratchpad file） | 探索が長く、前の事実を後の質問で使う | 主要な発見（クラス名・呼び出し関係・結論）をファイルに書き、次の質問の前に読み返す | 数ターンで終わる小さな調査 |
| サブエージェント | 検索結果・ファイルの中身など、出力が多い調査 | 「`retry` を独自に実装している箇所を挙げて」のような具体的な問いを渡し、要約だけ受け取る | やり取りを何度も重ねる作業、すぐ終わる直し |
| `/compact`（会話を要約して詰めるコマンド） | 探索の出力で文脈が埋まってきた | `/compact <焦点>` で、残したい論点を指定して要約させる | 無関係な作業に切り替える（`/clear` を使う） |
| マニフェスト（manifest。エージェントごとの構造化した状態の書き出し） | 複数エージェントの長い処理が途中で落ちうる | 各エージェントが決まった場所に状態を書き出し、コーディネーターが再開時に読んでプロンプトに入れる | 1回で終わる短い処理 |

段階をまたぐときは、段階1（例: 依存関係の洗い出し）の発見を要約し、段階2のサブエージェントの最初の文脈に入れる。フォークでないサブエージェントは空の文脈で始まり、親の会話を引き継がない。渡さなければ、同じ探索を最初からやり直すことになる。

??? info "compaction で残るもの・用語のずれ・関連ノート"
    - `/compact` で残るもの: ルートの CLAUDE.md とプランモードのプランは読み込み直される。会話の細かい指示や、`paths:` 付きのルールは要約に埋もれうる
    - `paths:` 付きのルールと入れ子の CLAUDE.md は、対象のファイルを読むと読み込み直される。常に残したいなら `paths:` を外すか、ルートの CLAUDE.md に移す
    - フォークのサブエージェントは親の会話の写しを持つ。公式ではフォークモードが既定でオン
    - ガイドとのずれ: ガイドは「サブエージェントで文脈を守る」と書く。現行の Best practices は、1M トークンと自動 compaction があるのでこれを古い助言とし、今も有効な利点を並列作業・うるさい出力を外に出す・独立したレビューとしている
    - 公式ドキュメントの「マニフェスト」はプラグインの `plugin.json`（plugin manifest）のこと。クラッシュ回復のための状態の書き出しという意味は、ガイド独自の用語
    - 関連: 組み込みツールの選び方と段階的な探索は [builtin-tools-incremental-exploration](../02-tool-design-mcp/builtin-tools-incremental-exploration.md)、プランモードと Explore サブエージェントは [plan-mode-vs-direct](../03-claude-code/plan-mode-vs-direct.md)、セッションの再開とフォークは [session-resume-fork](../01-agentic-architecture/session-resume-fork.md)

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| 探索の後半で、答えが前の発見と食い違う | 発見をスクラッチパッドに記録し、次の質問の前に読み返させる | 発見を会話の中だけに置く（compaction や文脈の境目で失われる） |
| メインの会話が検索結果で埋まる | 具体的な問いごとにサブエージェントへ任せ、メインは全体の調整に専念する | 「全部調べて」と曖昧に丸投げする |
| 次の段階のサブエージェントを起動する | 前の段階の要約を最初の文脈に入れて渡す | 何も渡さずに起動する（同じ探索をやり直す） |
| 複数エージェントの処理が落ちた | マニフェストから各エージェントの状態を読み、プロンプトに入れて続きから動かす | 最初からやり直す（状態を書き出しておけば、終わった分は読み込むだけで済む） |
| 探索の出力で文脈が満杯 | `/compact <焦点>` で、今後も使う論点を指定して詰める | `/clear` で会話を空にする（別の作業向け） |

</div>

## 確認問題

??? question "Q1. 決済ライブラリの移行調査を3時間続けたら、最初に特定した `LedgerAdapter` について聞いても「一般的なアダプターは〜」と答えるようになった。まず何をする？"
    文脈の劣化の症状だ。特定したクラス名や呼び出し関係をスクラッチパッドに書き出させ、以後の質問ではそれを読み返させる。必要なら `/compact <焦点>` で詰める。会話の中で同じ質問を繰り返しても戻らない。

??? question "Q2. 「ログ出力の呼び出し元を全部洗い出す」段階が終わった。次は「各呼び出し元を新しい API に置き換える計画」をサブエージェントに作らせる。どう起動する？"
    段階1の発見（呼び出し元の一覧と注意点）を要約し、段階2のサブエージェントの最初の文脈に入れる。フォークでないサブエージェントは空の文脈で始まるので、渡さないと洗い出しをやり直す。

??? question "Q3. 5つのサブエージェントで夜間に依存関係を調べる処理が、3つ目の途中で落ちた。再開をどう設計する？"
    各エージェントが決まった場所に状態（終わった範囲・発見・未完了）を書き出しておく。コーディネーターは再開時にマニフェストを読み、終わっていない分のエージェントのプロンプトに状態を入れて続きから動かす。最初からやり直さない。

## 出典
- [Exam Guide v1.1 タスクステートメント 5.4](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf)（公式）
- [Explore the context window](https://code.claude.com/docs/en/context-window)（公式。compaction で残るもの、`/compact` の焦点、サブエージェントへの委任）
- [Best practices](https://code.claude.com/docs/en/best-practices)（公式。サブエージェントが役立つ場面、古い助言の表）
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)（公式。うるさい出力の隔離、サブエージェントの連鎖）
- [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)（公式。plugin manifest の意味）
- [Commands](https://code.claude.com/docs/en/commands)（公式。`/compact [instructions]`、`/clear`）
- [Set up Claude Code in a monorepo or large codebase](https://code.claude.com/docs/en/large-codebases)（公式。プランのファイルは compaction 後も残る）
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（公式。context rot、構造化したメモ、サブエージェントは要約だけ返す）
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（公式。進捗ファイルと git 履歴で新しい文脈から状態をつかむ。クラッシュ回復やコーディネーターの話ではなく、マニフェストに近いとみなすのはこのノートの解釈）
