# orchestrate
- 目標: ccaf の公式情報を集め、単元ごとの要点ノートを作る（認知負荷を低く）。ノートは GitHub Pages で読めるようにする
- オーケストレータ: session_017JP5Br8ViMpCH6jfqbuZ9u ／ 統合ブランチ: claude/magical-babbage-f5qgza
- 同時実行: 5 ／ モデル・effort: 引き継ぎ ／ 作業セッションの環境: env_01FrJkXT4Kuns344Sxbp7THf（yuya-exam-notes。cc.sj-cdn.net などを許可）
- 完了した作業セッションのアーカイブ: する

## タスク
| # | 種類 | 対象 | 作業セッション | ブランチ | 状態 | 検証 | メモ |
|---|---|---|---|---|---|---|---|
| 1 | exam-add | ccaf を公式の Exam Guide v1.1 で作り直す | session_017JP5BoRvce63isKveaZoxQ | work/ccaf/exam-guide-v2 | 統合済み | OK（差し戻し1回で修正） | 第1波。チェックリストをここで確定。旧セッション session_017JP5BovYpHcB8b2VjdFjYz（Default 環境で PDF を読めず）は停止を指示 |
| 2 | study | ccaf 1. エージェントループと stop_reason による制御 | session_017JP5BrCxbjR3XYoMdXg1sn | work/ccaf/agentic-loop-stop-reason | 統合済み | OK | ccaf/notes/01-agentic-architecture/agentic-loop-stop-reason.md |
| 3 | study | ccaf 1. コーディネーターとサブエージェントのハブ＆スポーク構成 | session_017JP5Bqye9jJJiXSm2pVeeH | work/ccaf/coordinator-subagent-pattern | 統合済み | OK | ccaf/notes/01-agentic-architecture/coordinator-subagent-pattern.md |
| 4 | study | ccaf 1. 調査範囲の分割と、統合結果の抜けを埋める反復ループ | session_017JP5BnTohaTSGJHnUZFwCm | work/ccaf/scope-partitioning-iterative-refinement | 統合済み | OK | ccaf/notes/01-agentic-architecture/scope-partitioning-iterative-refinement.md |
| 5 | study | ccaf 1. Task ツールによるサブエージェントの起動と AgentDefinition | session_017JP5BnDaCCUYnov5bjc1pu | work/ccaf/task-tool-agent-definition | 統合済み | OK | ccaf/notes/01-agentic-architecture/task-tool-agent-definition.md |
| 6 | study | ccaf 1. サブエージェントへのコンテキストの渡し方 | session_017JP5BqftoWoDrku6Acexa7 | work/ccaf/subagent-context-passing | 統合済み | OK | ccaf/notes/01-agentic-architecture/subagent-context-passing.md |
| 7 | study | ccaf 1. ワークフローの順序をプログラムで強制する | session_017JP5BojR6EkGL7t3GCVGsW | work/ccaf/programmatic-workflow-enforcement | 作業中 | — | ccaf/notes/01-agentic-architecture/programmatic-workflow-enforcement.md |
| 8 | study | ccaf 1. 人への引き継ぎの要約と、複数の用件を含む依頼の分解 | session_017JP5BnVZNgfCi6tsogPb2e | work/ccaf/structured-handoff-request-decomposition | 作業中 | — | ccaf/notes/01-agentic-architecture/structured-handoff-request-decomposition.md |
| 9 | study | ccaf 1. Agent SDK のフックによるツール呼び出しの遮断とデータの正規化 | session_017JP5Bp96N8dPjB2McPcf3d | work/ccaf/sdk-hooks-interception | 検証中 | 範囲 OK・形 OK・事実を確認中 | ccaf/notes/01-agentic-architecture/sdk-hooks-interception.md |
| 10 | study | ccaf 1. タスク分解の選び方: プロンプトチェーンと動的な分解 | session_017JP5Bn9XrnVyYGB8fdN7zt | work/ccaf/prompt-chaining-vs-dynamic-decomposition | 作業中 | — | ccaf/notes/01-agentic-architecture/prompt-chaining-vs-dynamic-decomposition.md |
| 11 | study | ccaf 1. セッションの再開とフォーク | session_017JP5BpK39wy3M5FzfYiNph | work/ccaf/session-resume-fork | 作業中 | — | ccaf/notes/01-agentic-architecture/session-resume-fork.md |
| 12 | study | ccaf 2. ツールの説明文と境界の設計 | session_017JP5BnRSp2vGdqm2eJ2nEZ | work/ccaf/tool-descriptions-boundaries | 作業中 | — | ccaf/notes/02-tool-design-mcp/tool-descriptions-boundaries.md |
| 13 | study | ccaf 2. MCP ツールの構造化エラー応答 | — | work/ccaf/mcp-structured-errors | 待ち | — | ccaf/notes/02-tool-design-mcp/mcp-structured-errors.md |
| 14 | study | ccaf 2. エージェントへのツールの割り振り | — | work/ccaf/tool-distribution | 待ち | — | ccaf/notes/02-tool-design-mcp/tool-distribution.md |
| 15 | study | ccaf 2. tool_choice の設定 | — | work/ccaf/tool-choice | 待ち | — | ccaf/notes/02-tool-design-mcp/tool-choice.md |
| 16 | study | ccaf 2. Claude Code と Agent SDK への MCP サーバーの組み込み | — | work/ccaf/mcp-server-integration | 待ち | — | ccaf/notes/02-tool-design-mcp/mcp-server-integration.md |
| 17 | study | ccaf 2. MCP のツールとリソースの使い分けと、既存の MCP サーバーの活用 | — | work/ccaf/mcp-resources-vs-tools | 待ち | — | ccaf/notes/02-tool-design-mcp/mcp-resources-vs-tools.md |
| 18 | study | ccaf 2. 組み込みツール | — | work/ccaf/builtin-tools-incremental-exploration | 待ち | — | ccaf/notes/02-tool-design-mcp/builtin-tools-incremental-exploration.md |
| 19 | study | ccaf 3. CLAUDE.md の階層 | — | work/ccaf/claude-md-hierarchy | 待ち | — | ccaf/notes/03-claude-code/claude-md-hierarchy.md |
| 20 | study | ccaf 3. CLAUDE.md のモジュール化 | — | work/ccaf/claude-md-modularization | 待ち | — | ccaf/notes/03-claude-code/claude-md-modularization.md |
| 21 | study | ccaf 3. パス指定ルールによる規約の条件付き読み込み | — | work/ccaf/path-scoped-rules | 待ち | — | ccaf/notes/03-claude-code/path-scoped-rules.md |
| 22 | study | ccaf 3. カスタムスラッシュコマンドとスキルのスコープ、CLAUDE.md との使い分け | — | work/ccaf/slash-commands-and-skills | 待ち | — | ccaf/notes/03-claude-code/slash-commands-and-skills.md |
| 23 | study | ccaf 3. SKILL.md の frontmatter | — | work/ccaf/skill-frontmatter | 待ち | — | ccaf/notes/03-claude-code/skill-frontmatter.md |
| 24 | study | ccaf 3. プランモードと直接実行の使い分け、Explore サブエージェント | — | work/ccaf/plan-mode-vs-direct | 待ち | — | ccaf/notes/03-claude-code/plan-mode-vs-direct.md |
| 25 | study | ccaf 3. Claude Code での反復的な改善 | — | work/ccaf/iterative-refinement | 待ち | — | ccaf/notes/03-claude-code/iterative-refinement.md |
| 26 | study | ccaf 3. CI での Claude Code の非対話実行と構造化出力 | — | work/ccaf/ci-non-interactive | 待ち | — | ccaf/notes/03-claude-code/ci-non-interactive.md |
| 27 | study | ccaf 3. CI での自動レビューとテスト生成の質を上げる工夫 | — | work/ccaf/ci-review-test-quality | 待ち | — | ccaf/notes/03-claude-code/ci-review-test-quality.md |
| 28 | study | ccaf 4. 明確な基準で誤検知を減らすプロンプト | — | work/ccaf/explicit-criteria-false-positives | 待ち | — | ccaf/notes/04-prompt-engineering/explicit-criteria-false-positives.md |
| 29 | study | ccaf 4. few-shot プロンプティング | — | work/ccaf/few-shot-prompting | 待ち | — | ccaf/notes/04-prompt-engineering/few-shot-prompting.md |
| 30 | study | ccaf 4. tool_use と JSON スキーマによる構造化出力 | — | work/ccaf/tool-use-json-schema | 待ち | — | ccaf/notes/04-prompt-engineering/tool-use-json-schema.md |
| 31 | study | ccaf 4. 抽出用スキーマの設計 | — | work/ccaf/extraction-schema-design | 待ち | — | ccaf/notes/04-prompt-engineering/extraction-schema-design.md |
| 32 | study | ccaf 4. 検証・再試行・フィードバックのループ | — | work/ccaf/validation-retry-loop | 待ち | — | ccaf/notes/04-prompt-engineering/validation-retry-loop.md |
| 33 | study | ccaf 4. Message Batches API を使うバッチ処理の設計 | — | work/ccaf/message-batches-api | 待ち | — | ccaf/notes/04-prompt-engineering/message-batches-api.md |
| 34 | study | ccaf 4. 独立したインスタンスによるレビューと、複数パスのレビュー | — | work/ccaf/independent-multipass-review | 待ち | — | ccaf/notes/04-prompt-engineering/independent-multipass-review.md |
| 35 | study | ccaf 5. 長い対話で重要な事実を保つ | — | work/ccaf/preserving-key-facts | 待ち | — | ccaf/notes/05-context-reliability/preserving-key-facts.md |
| 36 | study | ccaf 5. 位置の影響 | — | work/ccaf/lost-in-the-middle-structured-passing | 待ち | — | ccaf/notes/05-context-reliability/lost-in-the-middle-structured-passing.md |
| 37 | study | ccaf 5. エスカレーションの基準と、曖昧な依頼の確かめ方 | — | work/ccaf/escalation-ambiguity | 待ち | — | ccaf/notes/05-context-reliability/escalation-ambiguity.md |
| 38 | study | ccaf 5. マルチエージェントでのエラーの伝え方 | — | work/ccaf/multiagent-error-propagation | 待ち | — | ccaf/notes/05-context-reliability/multiagent-error-propagation.md |
| 39 | study | ccaf 5. 大きなコードベースの探索でのコンテキスト管理 | — | work/ccaf/large-codebase-context | 待ち | — | ccaf/notes/05-context-reliability/large-codebase-context.md |
| 40 | study | ccaf 5. 人によるレビューの流れと確信度の較正 | — | work/ccaf/human-review-confidence-calibration | 待ち | — | ccaf/notes/05-context-reliability/human-review-confidence-calibration.md |
| 41 | study | ccaf 5. 複数ソースの統合で出典を保ち、矛盾と時期の違いを扱う | — | work/ccaf/information-provenance | 待ち | — | ccaf/notes/05-context-reliability/information-provenance.md |

## 未回答の連絡
- なし

## 判断の記録
- Web 閲覧: GitHub Pages（MkDocs で Markdown から生成）。リポジトリはユーザーが公開に切り替える（判断: ユーザー）
- 計画（第1波 exam-add → 第2波 study → fact-checker で検証して統合）を承認（判断: ユーザー）
- /study の書き方を認知負荷の低い形に変える（3行まとめ、A4 1枚、1見出し1概念、図と表を優先、用語は最初に一言説明）（判断: ユーザー承認）
- 作業セッションは統合後にアーカイブする（判断: ユーザー）
- #1 の README 作り直しでは、既存の「受験予定日」「最終確認日」「変更履歴」の欄を残し、変更履歴に作り直しを1行追記する（判断: オーケストレータ。/exam-update の記録の形に合わせる）
- 第2波は、確定したチェックリストの全項目を1項目1ノートで作る（判断: ユーザー）
- 費用は気にしなくてよい。品質と速さを優先し、同時実行を 3 から 5 に上げる（判断: ユーザーの意向を受けてオーケストレータ）
- #1 質問「公式ガイドの PDF のホストが止められている」→ A: ホストを許可した個人用環境 yuya-exam-notes を作り（ユーザー承認）、#1 は新しい環境の作業セッションで起動し直す（判断: オーケストレータ）
- 作業セッションは、以後すべて環境 env_01FrJkXT4Kuns344Sxbp7THf で起動する（判断: オーケストレータ）
- 第2波の各ノートは、担当のタスクステートメント（TS）の Knowledge / Skills を公式ガイドの PDF から漏れなく拾う。チェックリストの項目は増やさない（判断: オーケストレータ。fact-checker が挙げた未収録の論点は、項目ではなくノートの中身の問題のため）
- TS が重なる項目（tool_choice 2.3・4.3、複数パスのレビュー 1.6・4.6、エラーの伝え方 2.2・5.3）は、チェックリストで番号が付いている側のノートを主にし、もう一方からは参照だけにする（判断: オーケストレータ）
- ガイドと現行ドキュメントの名前・仕様のずれ（Task→Agent など）は、ガイドの書き方を主にし、ずれは「間違えやすいところ」に1行で書く（判断: オーケストレータ。試験はガイドに基づくため）
- 1.3 の「コーディネーターのプロンプトには目的と品質の基準を書く」は subagent-context-passing を主にする（判断: オーケストレータ）
- 例や確認問題の題材も、ガイドの例題から借りない（骨組みが同じ翻案も避ける）（判断: オーケストレータ。fact-checker の指摘を受けて、以後の指示に入れた）
