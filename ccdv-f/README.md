# Claude Certified Developer – Foundations（CCDV-F）学習ノート

> 出典: 公式「Claude Certified Developer – Foundations Exam Guide」Version 1.1（Effective December 7, 2026、2026-11-26 時点で確認）。ガイド自身に「予告なく変更されることがある」とあるので、受験予約の前に公式の最新版を確認すること。2026-12-06 までに受験する場合は v1.0 が対象になる見込み（下の「v1.0 との違い」を参照。v1.0 の終了日はガイドに明記が無く、未確認）。

## 試験概要

| 項目 | 内容 |
|---|---|
| 名称 | Claude Certified Developer – Foundations |
| **受験予定日** | 未定（決まったら YYYY-MM-DD で書く） |
| 最終確認日 | 2026-11-26（`/exam-update` が更新する） |
| 試験コード | CCDV-F |
| 問題数 | 70問（採点される60問＋採点されない10問。どれが採点外かは示されない） |
| 試験時間 | 120分 |
| 合格ライン | スケールスコア 720（100〜1,000 の尺度）。基準に対する絶対評価で、合否は合計スコアだけで決まる |
| 形式 | シナリオ型の選択式。何個選ぶかは問題ごとに書かれている |
| 受験方法 | 監督付き（オンライン監督 OnVUE、またはテストセンター）。申し込みは Anthropic Partner Academy → Pearson VUE。受験できるのは Claude Partner Network のメンバー（公式ブログ） |
| 受験料 | $125 USD（1回の受験ごと）。パートナー割引があれば、Pearson での価格に反映される |
| 前提条件 | なし（推奨の経験のみ） |
| 結果の通知 | 合否とスケールスコア、ドメインごとの正答率（ドメイン別の値は合否に使わない） |
| キャンセル・変更 | OnVUE は予約の1時間前まで、テストセンターは48時間前まで |
| 有効期間 | 認定から12か月。期限内なら、Partner Academy の無料・監督なしの評価で更新できる。失効したら本試験を正規の料金で受け直す |
| 再受験 | 不合格後の待機期間は 1回目 14日、2回目 30日、3回目 90日。受験は直近12か月で4回まで（試験ごとに数える） |
| 言語 | 未確認（ガイドに記載なし） |
| 想定する受験者 | ソフトウェアエンジニア、AI/ML エンジニア、フルスタック・バックエンドの開発者、ソリューションエンジニア。ソフトウェア開発の経験1〜5年、Claude か同等の LLM の実務経験6か月以上、Python か TypeScript、REST API と CLI に慣れていることが目安。Claude Developer Platform（Messages API、Agent SDK、Managed Agents）、Claude Code、MCP、CI/CD を使う |

## 出題ドメインと比重

| # | ドメイン | 比重 | 優先度 |
|---|---|---|---|
| 1 | エージェントとワークフロー（Agents and Workflows） | 17% | ★★★ |
| 2 | アプリケーションと統合（Applications and Integration） | 20% | ★★★ |
| 3 | Claude Code（Claude Code） | 8% | ★☆☆ |
| 4 | 評価・テスト・デバッグ（Eval, Testing, and Debugging） | 10% | ★★☆ |
| 5 | モデルの選択と最適化（Model Selection and Optimization） | 12% | ★★☆ |
| 6 | プロンプトとコンテキストのエンジニアリング（Prompt and Context Engineering） | 15% | ★★★ |
| 7 | セキュリティと安全性（Security and Safety） | 8% | ★☆☆ |
| 8 | ツールと MCP（Tools and MCP） | 10% | ★★☆ |

ドメイン2・1・6で半分を超える。出題項目の動詞は「分析する・評価する・診断する」が中心で、コードやエラー出力、トレースを読んで欠陥を見つけ、直し方を選ぶ問題が多いと読める（推論）。

---

## ドメイン別チェックリスト

各項目の末尾は、ガイドのスキル名（Skill）。

### 1. エージェントとワークフロー（17%）
- [ ] workflow と agent の選択、分解、実行環境の選択（self-hosted の harness と managed な agent runtime、Architecture and Runtime Selection） → [ノート](notes/01-agents-workflows/architecture-runtime-selection.md)
- [ ] Agent SDK でのエージェントの定義と自作のループ（Agent SDK Construction and Hooks） → [ノート](notes/01-agents-workflows/agent-sdk-construction.md)
- [ ] フックで必要な処理を決定的に実行する（Agent SDK Construction and Hooks） → [ノート](notes/01-agents-workflows/hooks-deterministic-actions.md)
- [ ] うまく動かないエージェントのパターンの診断（ループの終了、サブエージェントの分離、memory、コンテキスト、Agent Pattern Diagnosis） → [ノート](notes/01-agents-workflows/agent-pattern-diagnosis.md)

### 2. アプリケーションと統合（20%）
- [ ] Messages API の仕組み（メッセージの構造、tool use、stop reason、thinking、vision、Messages API Mechanics） → [ノート](notes/02-applications-integration/messages-api-mechanics.md)
- [ ] ストリーミングのイベントと終わりの判定（Messages API Mechanics / Integration Resilience） → [ノート](notes/02-applications-integration/streaming-events.md)
- [ ] リアルタイムとバッチの選択（Message Batches API、Messages API Mechanics） → [ノート](notes/02-applications-integration/realtime-vs-batch.md)
- [ ] アプリの境界と、面（surface）ごとの振る舞い（スキーマと session の設計、Application Boundary and Surface Behavior） → [ノート](notes/02-applications-integration/application-boundary-surface.md)
- [ ] 設定と SDLC への組み込み（CLAUDE.md、settings.json、モデルの固定、プロンプトの版管理、CI、Configuration and SDLC Integration） → [ノート](notes/02-applications-integration/configuration-sdlc.md)
- [ ] API のエラーの種類に沿った再試行とフォールバック（rate limit・overloaded・invalid request・timeout、Integration Resilience） → [ノート](notes/02-applications-integration/api-errors-retry.md)
- [ ] Files API による多形式の取り込み（Integration Resilience） → [ノート](notes/02-applications-integration/files-api-ingestion.md)

### 3. Claude Code（8%）
- [ ] Claude Code の操作（CLI・desktop・IDE・web・mobile、session、built-in commands、headless と streaming、Claude Code Operation） → [ノート](notes/03-claude-code/claude-code-operation.md)
- [ ] CLAUDE.md の階層、settings.json、権限モード（Claude Code Operation） → [ノート](notes/03-claude-code/claude-md-settings-permissions.md)
- [ ] 拡張の仕組みの選択と配布（Skill・plugin・Rules・hook・subagent・slash command、Claude Code Customization and Extension） → [ノート](notes/03-claude-code/customization-extension.md)

### 4. 評価・テスト・デバッグ（10%）
- [ ] 評価の設計（golden set、regression test、behavioral check、指標の選択、Evaluation Design） → [ノート](notes/04-eval-testing-debugging/evaluation-design.md)
- [ ] 人のラベルで較正した LLM-as-judge（Evaluation Design） → [ノート](notes/04-eval-testing-debugging/llm-as-judge-calibration.md)
- [ ] 故障の型の診断（hallucination・refusal・under-acting・context loss・format drift、統合の層かモデルの出力か、Failure-Mode Diagnosis） → [ノート](notes/04-eval-testing-debugging/failure-mode-diagnosis.md)

### 5. モデルの選択と最適化（12%）
- [ ] 生成の仕組みとモデルの選択肢（トークン、コンテキストウィンドウ、サンプリングと非決定性、adaptive thinking と effort、Generation Mechanics and Model Options） → [ノート](notes/05-model-selection/generation-mechanics.md)
- [ ] モデルの階層の選択と、リリースをまたぐ変化への備え（Model Tier Selection and Release Planning） → [ノート](notes/05-model-selection/model-tier-release-planning.md)
- [ ] prompt caching のブレークポイントの置き方（single・layered・rolling、Cost Diagnosis and Optimization） → [ノート](notes/05-model-selection/prompt-caching-breakpoints.md)
- [ ] コストの要因の特定と最適化（バッチ、トークンの予算、効果の見積もり、Cost Diagnosis and Optimization） → [ノート](notes/05-model-selection/cost-diagnosis.md)

### 6. プロンプトとコンテキストのエンジニアリング（15%）
- [ ] 長いセッションのコンテキスト管理（compaction、ツール出力の刈り込み、サブエージェントでの分離、新しいセッションの基準、Context Management for Long-Running Sessions） → [ノート](notes/06-prompt-context/long-running-context.md)
- [ ] 回帰の評価で見つかったずれを直すプロンプトの改訂（system と user の置き場所、例、出力の制約、入力の無害化、Prompt Revision） → [ノート](notes/06-prompt-context/prompt-revision.md)
- [ ] 構造化出力と防御的なパース（Structured Output and Defensive Parsing） → [ノート](notes/06-prompt-context/structured-output-parsing.md)
- [ ] 渡した文書にもとづく回答と出典、「見つからない」の返し方、全文か検索か（Grounding and Source Citation） → [ノート](notes/06-prompt-context/grounding-citations.md)

### 7. セキュリティと安全性（8%）
- [ ] プロンプトインジェクションと jailbreak への多層の防御（Prompt Injection and Jailbreak Defense） → [ノート](notes/07-security-safety/prompt-injection-defense.md)
- [ ] 決定的なガードレールと最小権限（Deterministic Guardrails and Least Privilege） → [ノート](notes/07-security-safety/guardrails-least-privilege.md)
- [ ] API キーと認証情報の扱い（サーバー側のプロキシ、workspace のキーと admin キー、環境の分離、ローテーション、API Key and Credential Handling） → [ノート](notes/07-security-safety/api-key-handling.md)

### 8. ツールと MCP（10%）
- [ ] ツールの設計と結果の整形（スキーマ、説明文、エラー、実行する側、承認、Tool Design and Response Shaping） → [ノート](notes/08-tools-mcp/tool-design-response-shaping.md)
- [ ] MCP サーバーの開発と組み込み（resources・tools・prompts、stdio と HTTP、認証、MCP Server Development and Integration） → [ノート](notes/08-tools-mcp/mcp-server-development.md)
- [ ] 機能の仕組みの選択（組み込みツール・カスタムツール・Skills・MCP サーバー、Capability Mechanism Selection） → [ノート](notes/08-tools-mcp/capability-mechanism-selection.md)

---

## v1.0 との違い（2026-12-06 までに受験する場合）

| 項目 | v1.0（Effective July 2026） | v1.1（Effective December 7, 2026） |
|---|---|---|
| 問題数 | 53問 | 70問（採点60＋採点外10） |
| 比重 | D1 14.7%、D2 33.1%、D3 3.1%、D4 2.6%、D5 16.8%、D6 11.0%、D7 8.1%、D8 10.6% | 上の表（Claude Code・評価・プロンプトが上がり、アプリと統合・モデル選択が下がった） |
| 出題項目 | スキルごとに比重つき。Understanding Requirements、Systems Life Cycle、Software Engineering Foundations、Technical Fundamentals（websockets など）、フレームワーク名（Strands・LangGraph・PydanticAI）を含む | 上の項目からそれらが消え、Agent Pattern Diagnosis、Integration Resilience、Claude Code の拡張、評価の設計、Grounding、API キーの扱い、権限モード、MCP の HTTP と認証が加わった |
| キャンセル | 予約の24時間前まで | OnVUE 1時間前、テストセンター 48時間前 |

v1.0 で受けるなら、ドメイン2（33%）とドメイン5（17%）を厚くし、REST・JSON・非同期処理などソフトウェア開発の基礎も見直す。

## 4週間の学習プラン（目安）

受験予定日が未定なので、4週間で仮に組む。ガイドは、ツールを使うエージェントを1つ作って出荷すること（カスタムツールか MCP、構造化出力、prompt caching、golden set での評価、決定的なガードレール）を勧めている。

| 週 | やること |
|---|---|
| 1週目 | 公式の Exam Guide（Dec 7 版）を通して読む → ドメイン2（Messages API、ストリーミング、エラー、バッチ）。Messages API でツールを使う小さなエージェントを書く |
| 2週目 | ドメイン1（workflow と agent、Agent SDK、hooks）とドメイン8（ツール設計、MCP）。作ったエージェントに MCP サーバーと hook を足す |
| 3週目 | ドメイン6（コンテキスト、プロンプトの改訂、構造化出力、grounding）とドメイン5（モデル、caching、コスト）。cache のブレークポイントを置き、使用量で効果を確かめる |
| 4週目 | ドメイン4（評価、LLM-as-judge）・3（Claude Code）・7（セキュリティ）。golden set で評価を回す → [模擬試験](mock-exams/mock-01.md) → `/quiz review` → `/progress` |

## 教材
- 公式: Claude Certified Developer – Foundations Exam Guide（Dec 7 版）
- 公式: platform.claude.com（Messages API、streaming、errors、tool use、structured outputs、prompt caching、extended/adaptive thinking と effort、Message Batches、Files API、citations、Agent SDK、Managed Agents、評価）、code.claude.com（Claude Code、settings、hooks、skills、plugins、subagents、headless）、modelcontextprotocol.io（MCP）
- 公式の模擬試験: 確認できず（ガイドのサンプル問題3問のみ）
- 関連: [CCAR-F のノート](../ccaf/README.md)（エージェントループ、tool_choice、MCP、CLAUDE.md など、重なる範囲が多い）

## 学習の記録
- 模擬試験: [第1回](mock-exams/mock-01.md)、[第2回](mock-exams/mock-02.md)
- 練習問題の記録: [quiz-log.md](quiz-log.md)（`/quiz` が書く）
- 間違えた問題と復習: [mistakes.md](mistakes.md)（`/quiz` が書く）
- 進み具合: `/progress` で確認

## 変更履歴
- 2026-11-26: 公式の Exam Guide v1.1（2026-12-07 から有効）をもとに作成。v1.0 との違いも記録

## 参考リンク
- 公式の Exam Guide（PDF、v1.1、Dec 7 版）: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946771/Claude_Certified_Developer_-_Foundations_Exam_Guide_Updated_Dec_7.pdf
- 公式の Exam Guide（PDF、v1.0）: https://everpath-course-content.s3-accelerate.amazonaws.com/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1783542875/Claude+Certified+Developer+%E2%80%93+Foundations+Exam+Guide.pdf
- 公式ブログ「Four role-based Claude certifications」（2026-07-23）: https://claude.com/blog/four-role-based-claude-certifications
