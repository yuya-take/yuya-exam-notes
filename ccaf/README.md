# Claude Certified Architect – Foundations（CCAR-F）学習ノート

> 出典: 公式「Claude Certified Architect – Foundations Exam Guide」Version 1.1（Effective November 2026、2026-11-20 時点で確認）。ガイド自身に「予告なく変更されることがある」とあるので、受験予約の前に公式の最新版を確認すること。

## 試験概要

| 項目 | 内容 |
|---|---|
| 名称 | Claude Certified Architect – Foundations |
| **受験予定日** | 未定（決まったら YYYY-MM-DD で書く） |
| 最終確認日 | 2026-11-20（`/exam-update` が更新する） |
| 試験コード | CCAR-F |
| 問題数 | 60問 |
| 試験時間 | 120分 |
| 合格ライン | スケールスコア 720（100〜1,000 の尺度）。合否は合計スコアだけで決まる |
| 形式 | 択一（multiple-choice）と複数選択（multiple-response）。何個選ぶかは問題ごとに書かれている。6つのシナリオから4つがランダムに出る |
| 受験方法 | 監督付き（オンライン監督 OnVUE、またはテストセンター）。申し込みは Anthropic Partner Academy → Pearson VUE |
| 受験料 | $125 USD（1回の受験ごと）。パートナー割引があれば、Pearson での価格に反映される |
| 結果の通知 | 合否とスケールスコア、ドメインごとの正答率 |
| 有効期間 | 認定から12か月。期限内なら、Partner Academy の無料・監督なしの評価で更新できる。失効したら本試験を受け直す。試験の内容が大きく変わったときは、更新の評価ではなく本試験の受け直しを求められることがある |
| 再受験 | 不合格後の待機期間は 1回目 14日、2回目 30日、3回目 90日。受験は直近12か月で4回まで（1回目を含む） |
| 言語 | 未確認（ガイドに記載なし） |
| 想定する受験者 | Claude で本番のアプリを設計・実装するソリューションアーキテクト。Claude API・Agent SDK・Claude Code・MCP の実務経験 6か月以上が目安 |

## 出題ドメインと比重

| # | ドメイン | 比重 | 優先度 |
|---|---|---|---|
| 1 | エージェントの構成とオーケストレーション（Agentic Architecture & Orchestration） | 27% | ★★★ |
| 2 | ツール設計と MCP の組み込み（Tool Design & MCP Integration） | 18% | ★☆☆ |
| 3 | Claude Code の設定とワークフロー（Claude Code Configuration & Workflows） | 20% | ★★☆ |
| 4 | プロンプトエンジニアリングと構造化出力（Prompt Engineering & Structured Output） | 20% | ★★☆ |
| 5 | コンテキスト管理と信頼性（Context Management & Reliability） | 15% | ★☆☆ |

ドメイン1だけで4分の1を超えるので最優先にする。ドメイン2〜5の差は小さく、どのシナリオにも複数のドメインがまたがって出るので、★☆☆ のドメインも手は抜かない。

### 出題シナリオ（6つから4つ）

問題は、本番の利用場面を想定したシナリオごとにまとめて出る。ガイドに載っている6つの題材と、主に関わるドメインは次のとおり（要約）。

| # | シナリオの題材 | 主なドメイン |
|---|---|---|
| 1 | Agent SDK で作るカスタマーサポートのエージェント（MCP ツールで社内システムを操作し、必要なら人に引き継ぐ） | 1, 2, 5 |
| 2 | Claude Code を使ったコード生成（スラッシュコマンド、CLAUDE.md、プランモード） | 3, 5 |
| 3 | Agent SDK で作るマルチエージェントの調査システム（コーディネーターと専門のサブエージェント） | 1, 2, 5 |
| 4 | Agent SDK で作る開発者向けの生産性ツール（組み込みツールと MCP サーバー） | 2, 3, 1 |
| 5 | Claude Code を CI/CD に組み込む（自動レビュー、テスト生成、PR へのフィードバック） | 3, 4 |
| 6 | 非構造の文書からの構造化データの抽出（JSON スキーマでの検証） | 4, 5 |

### 出題範囲の外（ガイドの Out-of-Scope から）

- Claude のファインチューニング、カスタムモデルの学習
- Claude API の認証・課金・アカウント管理
- 特定のプログラミング言語・フレームワークの実装の細部（ツールとスキーマの設定に必要な範囲を超えるもの）
- MCP サーバーのデプロイやホスティング（インフラ、ネットワーク、コンテナのオーケストレーション）
- Claude の内部構造、学習の過程、モデルの重み
- Constitutional AI・RLHF・安全性のための学習の方法
- 埋め込みモデル・ベクトル DB の実装の細部
- Computer use（ブラウザの自動操作、デスクトップの操作）
- 画像の解析（Vision）
- ストリーミング API・Server-Sent Events の実装
- レート制限・quotas・API の料金の計算
- OAuth・API キーのローテーション・認証プロトコルの細部
- 特定のクラウド（AWS、GCP、Azure）の設定
- 性能のベンチマークやモデルの比較指標
- プロンプトキャッシュの実装の細部（存在を知っている程度は範囲内）
- トークン数の数え方・トークン化の細部

---

## ドメイン別チェックリスト

各項目の末尾の番号は、ガイドのタスクステートメント（Task Statement）の番号。

### 1. エージェントの構成とオーケストレーション（27%）
- [ ] エージェントループと stop_reason による制御（Agentic loop: tool_use / end_turn、1.1） → [ノート](notes/01-agentic-architecture/agentic-loop-stop-reason.md)
- [ ] コーディネーターとサブエージェントのハブ＆スポーク構成（Coordinator-subagent pattern、1.2） → [ノート](notes/01-agentic-architecture/coordinator-subagent-pattern.md)
- [ ] 調査範囲の分割と、統合結果の抜けを埋める反復ループ（Scope partitioning & iterative refinement、1.2） → [ノート](notes/01-agentic-architecture/scope-partitioning-iterative-refinement.md)
- [ ] Task ツールによるサブエージェントの起動と AgentDefinition（allowedTools、並列起動、1.3） → [ノート](notes/01-agentic-architecture/task-tool-agent-definition.md)
- [ ] サブエージェントへのコンテキストの渡し方（明示的な受け渡しと出典の保持、1.3） → [ノート](notes/01-agentic-architecture/subagent-context-passing.md)
- [ ] ワークフローの順序をプログラムで強制する（前提ゲートとプロンプト指示の違い、1.4） → [ノート](notes/01-agentic-architecture/programmatic-workflow-enforcement.md)
- [ ] 人への引き継ぎの要約と、複数の用件を含む依頼の分解（Structured handoff、1.4） → [ノート](notes/01-agentic-architecture/structured-handoff-request-decomposition.md)
- [ ] Agent SDK のフックによるツール呼び出しの遮断とデータの正規化（PostToolUse など、1.5） → [ノート](notes/01-agentic-architecture/sdk-hooks-interception.md)
- [ ] タスク分解の選び方: プロンプトチェーンと動的な分解（Prompt chaining vs dynamic decomposition、1.6） → [ノート](notes/01-agentic-architecture/prompt-chaining-vs-dynamic-decomposition.md)
- [ ] セッションの再開とフォーク（--resume、fork_session、要約から始め直す判断、1.7） → [ノート](notes/01-agentic-architecture/session-resume-fork.md)

### 2. ツール設計と MCP の組み込み（18%）
- [ ] ツールの説明文と境界の設計（似たツールの区別、改名と分割、2.1） → [ノート](notes/02-tool-design-mcp/tool-descriptions-boundaries.md)
- [ ] MCP ツールの構造化エラー応答（isError、エラーの分類、再試行の可否、2.2） → [ノート](notes/02-tool-design-mcp/mcp-structured-errors.md)
- [ ] エージェントへのツールの割り振り（ツールの数と役割ごとの制限、2.3） → [ノート](notes/02-tool-design-mcp/tool-distribution.md)
- [ ] tool_choice の設定（auto / any / 特定ツールの強制、2.3・4.3） → [ノート](notes/02-tool-design-mcp/tool-choice.md)
- [ ] Claude Code と Agent SDK への MCP サーバーの組み込み（.mcp.json と ~/.claude.json、環境変数の展開、2.4） → [ノート](notes/02-tool-design-mcp/mcp-server-integration.md)
- [ ] MCP のツールとリソースの使い分けと、既存の MCP サーバーの活用（MCP resources、2.4） → [ノート](notes/02-tool-design-mcp/mcp-resources-vs-tools.md)
- [ ] 組み込みツール（Read / Write / Edit / Bash / Grep / Glob）の選び方と、コードを段階的に読む進め方（2.5） → [ノート](notes/02-tool-design-mcp/builtin-tools-incremental-exploration.md)

### 3. Claude Code の設定とワークフロー（20%）
- [ ] CLAUDE.md の階層（ユーザー / プロジェクト / ディレクトリ）と /memory での確認（3.1） → [ノート](notes/03-claude-code/claude-md-hierarchy.md)
- [ ] CLAUDE.md のモジュール化（@import と .claude/rules/、3.1） → [ノート](notes/03-claude-code/claude-md-modularization.md)
- [ ] パス指定ルールによる規約の条件付き読み込み（paths の glob パターン、3.3） → [ノート](notes/03-claude-code/path-scoped-rules.md)
- [ ] カスタムスラッシュコマンドとスキルのスコープ、CLAUDE.md との使い分け（.claude/commands/、.claude/skills/、3.2） → [ノート](notes/03-claude-code/slash-commands-and-skills.md)
- [ ] SKILL.md の frontmatter（context: fork、allowed-tools、argument-hint、3.2） → [ノート](notes/03-claude-code/skill-frontmatter.md)
- [ ] プランモードと直接実行の使い分け、Explore サブエージェント（Plan mode vs direct execution、3.4） → [ノート](notes/03-claude-code/plan-mode-vs-direct.md)
- [ ] Claude Code での反復的な改善（入出力例、テスト駆動、インタビュー、問題の伝え方、3.5） → [ノート](notes/03-claude-code/iterative-refinement.md)
- [ ] CI での Claude Code の非対話実行と構造化出力（-p、--output-format json、--json-schema、3.6）
- [ ] CI での自動レビューとテスト生成の質を上げる工夫（過去の指摘・既存テスト・CLAUDE.md・独立したレビュー、3.6）

### 4. プロンプトエンジニアリングと構造化出力（20%）
- [ ] 明確な基準で誤検知を減らすプロンプト（報告する・しないの基準、重大度の定義、4.1）
- [ ] few-shot プロンプティング（曖昧なケースの判断、出力形式の統一、抽出の精度、4.2）
- [ ] tool_use と JSON スキーマによる構造化出力（構文エラーは防げるが意味の誤りは防げない、4.3）
- [ ] 抽出用スキーマの設計（必須と任意、nullable、enum の "other"＋詳細と "unclear"、4.3）
- [ ] 検証・再試行・フィードバックのループ（エラーを添えた再試行、再試行が効かない場合、detected_pattern、4.4）
- [ ] Message Batches API を使うバッチ処理の設計（向く処理と向かない処理、custom_id、SLA の計算、4.5）
- [ ] 独立したインスタンスによるレビューと、複数パスのレビュー（Self-review の限界、ファイル単位＋横断のパス、4.6）

### 5. コンテキスト管理と信頼性（15%）
- [ ] 長い対話で重要な事実を保つ（要約で落ちる情報、事実ブロック、ツール出力の絞り込み、5.1）
- [ ] 位置の影響（lost in the middle）への対策と、エージェント間で渡す情報の構造化（5.1）
- [ ] エスカレーションの基準と、曖昧な依頼の確かめ方（人への引き継ぎ、方針の空白、複数該当、5.2）
- [ ] マルチエージェントでのエラーの伝え方（アクセス失敗と結果0件の区別、局所的な回復、5.3）
- [ ] 大きなコードベースの探索でのコンテキスト管理（スクラッチパッド、サブエージェント、/compact、マニフェストによる再開、5.4）
- [ ] 人によるレビューの流れと確信度の較正（層別抽出、文書種別・フィールド別の精度、5.5）
- [ ] 複数ソースの統合で出典を保ち、矛盾と時期の違いを扱う（Information provenance、5.6）

---

## 4週間の学習プラン（目安）

受験予定日が未定なので、4週間で仮に組む。ガイドの「How to Prepare」と「Preparation Exercises」（演習4つ）に沿って、読むだけでなく手を動かす。

| 週 | やること |
|---|---|
| 1週目 | 公式の Exam Guide を通して読む → ドメイン1（エージェントループ、サブエージェント、フック、セッション）。ガイドの演習1「Build a Multi-Tool Agent with Escalation Logic」（ドメイン1・2・5）で、ツール付きのエージェントを作る |
| 2週目 | ドメイン3（CLAUDE.md、.claude/rules/、スキル、プランモード、CI）。実際のリポジトリで Claude Code を設定する（演習2） |
| 3週目 | ドメイン4（構造化出力、スキーマ設計、検証と再試行、バッチ）とドメイン2（ツール設計、MCP）。抽出パイプラインを作る（演習3） |
| 4週目 | ドメイン5（コンテキスト管理、エスカレーション、出典の保持）。マルチエージェントの調査パイプライン（演習4）→ `/mock-exam` → `/quiz review` で間違えた問題を復習 → `/progress` で苦手なところを確認 |

## 教材
- 公式: Claude Certified Architect – Foundations Exam Guide（v1.1）、Anthropic Partner Academy、docs.claude.com（Claude API・Agent SDK）、code.claude.com（Claude Code）、modelcontextprotocol.io（MCP）
- ガイドの付録「Technologies and Concepts」「In-Scope Topics」を、チェックリストの抜けの確認に使う

## 学習の記録
- 練習問題の記録: [quiz-log.md](quiz-log.md)（`/quiz` が書く）
- 間違えた問題と復習: [mistakes.md](mistakes.md)（`/quiz` が書く）
- 進み具合: `/progress` で確認

## 変更履歴
- 2026-11-20: 作成（第三者の解説記事をもとに作成。公式の Exam Guide との突き合わせは未実施）
- 2026-11-20: 公式の Exam Guide v1.1 をもとに作り直し（ドメインの番号と名前をガイドに合わせ、チェックリストをタスクステートメントから作り直した）

## 参考リンク
- 公式の Exam Guide（PDF、v1.1）: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf
- 公式の試験ページ: Anthropic Partner Academy の認定ページ（URL は未確認）
