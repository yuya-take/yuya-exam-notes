# Claude Certified Architect – Professional（CCAR-P）学習ノート

> 出典: 公式「Claude Certified Architect – Professional Exam Guide」Version 1.1（Effective December 7, 2026、2026-11-26 時点で確認）。ガイド自身に「予告なく変更されることがある」とあるので、受験予約の前に公式の最新版を確認すること。2026-12-06 までに受験する場合は、旧版（v1.0 と、同じ内容の November 2026 版 v1.1）が対象になる見込み（下の「旧版との違い」を参照。旧版の終了日はガイドに明記が無く、未確認）。

## 試験概要

| 項目 | 内容 |
|---|---|
| 名称 | Claude Certified Architect – Professional |
| **受験予定日** | 未定（決まったら YYYY-MM-DD で書く） |
| 最終確認日 | 2026-11-26（`/exam-update` が更新する） |
| 試験コード | CCAR-P |
| 問題数 | 70問（採点される60問＋採点されない10問。どれが採点外かは示されない） |
| 試験時間 | 120分 |
| 合格ライン | スケールスコア 720（100〜1,000 の尺度）。基準に対する絶対評価で、合否は合計スコアだけで決まる |
| 形式 | シナリオ型の選択式。何個選ぶかは問題ごとに書かれている。構成図・設定ファイル・ログやトレース・評価の結果・コードを読ませて判断させる問題がある |
| 受験方法 | 監督付き（オンライン監督 OnVUE、またはテストセンター）。申し込みは Anthropic Partner Academy → Pearson VUE。受験できるのは Claude Partner Network のメンバー（公式ブログ） |
| 受験料 | $175 USD（1回の受験ごと）。パートナー割引があれば、Pearson での価格に反映される |
| 前提条件 | なし。Claude Certified Architect – Foundations（[ccaf/](../ccaf/README.md)）は推奨だが必須ではない。ただし ==Foundations の範囲は既知のものとして扱われる== |
| 結果の通知 | 合否とスケールスコア、ドメインごとの正答率（ドメイン別の値は合否に使わない） |
| キャンセル・変更 | OnVUE は予約の1時間前まで、テストセンターは48時間前まで |
| 有効期間 | 認定から12か月。期限内なら、Partner Academy の無料・監督なしの評価で更新できる。失効したら本試験を正規の料金で受け直す |
| 再受験 | 不合格後の待機期間は 1回目 14日、2回目 30日、3回目 90日。受験は直近12か月で4回まで（試験ごとに数える） |
| 言語 | 未確認（ガイドに記載なし。第三者情報は「英語と日本語」「英語のみ」で食い違う・要確認） |
| 想定する受験者 | ソリューションアーキテクト、AI/ML エンジニア、テックリード、シニアエンジニア。システムアーキテクチャかプラットフォームエンジニアリングの経験3年以上、本番での Claude の経験6か月以上が目安。Claude Developer Platform、Agent Skills、Claude Code と Agent SDK、MCP、Claude Managed Agents を日常的に使い、Anthropic API と Amazon Bedrock・Google Vertex AI・Microsoft Foundry の違いを理解している |

## 出題ドメインと比重

| # | ドメイン | 比重 | 優先度 |
|---|---|---|---|
| 1 | ソリューションの設計とアーキテクチャ（Solution Design and Architecture） | 18% | ★★★ |
| 2 | モデル・プロンプト・コンテキストエンジニアリング（Claude Models, Prompting, and Context Engineering） | 13% | ★★☆ |
| 3 | 統合（Integration） | 21% | ★★★ |
| 4 | 評価・テスト・最適化（Evaluation, Testing, and Optimization） | 17% | ★★☆ |
| 5 | ガバナンス・安全性・リスク管理（Governance, Safety, and Risk Management） | 16% | ★★☆ |
| 6 | 関係者とのコミュニケーションとライフサイクル管理（Stakeholder Communication and Lifecycle Management） | 7% | ★☆☆ |
| 7 | 開発者の生産性と運用の支援（Developer Productivity and Operational Enablement） | 8% | ★☆☆ |

ドメイン3（統合）とドメイン1（設計）で約4割になる。どの項目も「条件を示された場面で、評価・分析・選択する」形で書かれており、知識の暗記より、示された制約（遅延・コスト・データの所在・権限など）のうち==どれが効いているか==を見抜く力が問われる。Foundations の範囲（エージェントループ、tool_use、CLAUDE.md、MCP の基本など）は前提知識なので、怪しければ [CCAR-F のノート](../ccaf/README.md) を先に読む。

### 旧版との違い（2026-12-06 までに受験する場合）

| 項目 | 旧版（v1.0 = July 2026、v1.1 = November 2026。出題内容は同じ） | 新版 v1.1（Effective December 7, 2026） |
|---|---|---|
| 問題数 | 63問 | 70問（採点60＋採点外10） |
| 比重 | D1 17%、D2 13%、D3 19%、D4 16%、D5 14%、D6 14%、D7 7% | D1 18%、D2 13%、D3 21%、D4 17%、D5 16%、**D6 7%**、D7 8% |
| 出題項目 | 1行のタスク40項目（A/B テスト、GDPR・HIPAA・FedRAMP、倫理の一般論などを含む） | スキル名＋説明の38項目（下のチェックリスト） |
| 新しく入った要素 | — | Claude と人の分担、デプロイ先（Bedrock・Vertex・Foundry）と実行環境（Managed Agents など）の選択、native thinking と effort、context editing・memory tool・compaction、contextual retrieval、冪等性・再試行・フォールバック、LLM-as-judge のバイアス、試行回数、モデルの移行、プロンプトインジェクションの面、サプライチェーン、ZDR とテナント分離、ADR、引き継ぎの runbook、Claude Code の plugins と managed settings、権限モード、AI が書いたコードの責任 |

旧版で受けるなら、ドメイン6（14%）の比重が大きい点に注意する。旧版の出題項目の大半は、新版のノートで覆える。

---

## ドメイン別チェックリスト

各項目の末尾は、ガイドのスキル名（Skill）。

### 1. ソリューションの設計とアーキテクチャ（18%）
- [ ] Claude と人の分担（取り消せるか・影響の大きさ・責任で振り分ける、Task Delegation Between Claude and Humans） → [ノート](notes/01-solution-design/task-delegation.md)
- [ ] エンドツーエンドの構成の評価（拡張性・保守性・アクセス制御、最初に壊れる部品、End-to-End Architecture Evaluation） → [ノート](notes/01-solution-design/end-to-end-architecture.md)
- [ ] 構成パターンの選択（workflow・agentic・augmented LLM・Skills ベース、Architectural Pattern Selection） → [ノート](notes/01-solution-design/architectural-patterns.md)
- [ ] オーケストレーターとサブエージェントの分解の評価（観測性・エラーからの回復、Orchestrator and Subagent Decomposition） → [ノート](notes/01-solution-design/orchestrator-subagent.md)
- [ ] 価値にもとづく設計の判断（コストや SLA の上限の中での価値の最大化、Value-Based Architectural Decisions） → [ノート](notes/01-solution-design/value-based-decisions.md)
- [ ] デプロイ先と実行環境の選択（Anthropic API・Bedrock・Vertex AI・Foundry、Messages API・Agent SDK・headless Claude Code・Managed Agents、Deployment Surface and Agent Runtime Selection） → [ノート](notes/01-solution-design/deployment-surface-runtime.md)

### 2. モデル・プロンプト・コンテキストエンジニアリング（13%）
- [ ] モデルの階層の選択（遅延・コスト・品質の制約、Model Tier Selection） → [ノート](notes/02-models-prompting-context/model-tier-selection.md)
- [ ] システムプロンプトの診断と書き直し（仕様の抜け、縛りすぎない、System Prompt Diagnosis and Revision） → [ノート](notes/02-models-prompting-context/system-prompt-diagnosis.md)
- [ ] プロンプトの技法の選択（zero-shot・few-shot・プロンプトでの推論と native thinking・構造化出力、Prompting Technique Selection） → [ノート](notes/02-models-prompting-context/prompting-technique-selection.md)
- [ ] コンテキストの構成とトークンの経済性（Context Composition and Token Economics） → [ノート](notes/02-models-prompting-context/context-token-economics.md)
- [ ] キャッシュのブレークポイントと再利用できる形（安定した内容を先に、Skills、Cache Breakpoints and Reusable Packaging） → [ノート](notes/02-models-prompting-context/cache-breakpoints-packaging.md)
- [ ] 推論の量とコンテキストのライフサイクル（effort、context editing・memory tool・compaction、Reasoning Effort and Context Lifecycle） → [ノート](notes/02-models-prompting-context/reasoning-effort-context-lifecycle.md)

### 3. 統合（21%）
- [ ] 最小権限のツール構成（外す・絞る・コンテキストに優しい形に置き換える、Least-Privilege Tool Configuration） → [ノート](notes/03-integration/least-privilege-tools.md)
- [ ] 認証と認可（認証情報の露出、権限の昇格、Authentication and Authorization Posture） → [ノート](notes/03-integration/authn-authz-posture.md)
- [ ] 効いている性能の制約を緩める（検索の深さ・モデル・キャッシュ・呼び出し方、Relieving the Binding Performance Constraint） → [ノート](notes/03-integration/binding-performance-constraint.md)
- [ ] 計測と監視の抜け（Instrumentation and Monitoring Gaps） → [ノート](notes/03-integration/monitoring-gaps.md)
- [ ] 検索の構成の選択（RAG・ツールでの agentic search・全文をコンテキストに、contextual retrieval とフォールバック、Retrieval Architecture Selection） → [ノート](notes/03-integration/retrieval-architecture.md)
- [ ] 接続の仕組みの選択（MCP・API/CLI・エージェント間の引き継ぎ、Connection Mechanism Selection） → [ノート](notes/03-integration/connection-mechanism.md)
- [ ] 段階的な発見と一括の読み込み（Progressive Discovery vs. Monolithic Context Loading） → [ノート](notes/03-integration/progressive-discovery.md)
- [ ] 本番の信頼性の制御（レート制限・再試行とバックオフ・冪等性・フォールバック、Production Reliability Controls） → [ノート](notes/03-integration/reliability-controls.md)

### 4. 評価・テスト・最適化（17%）
- [ ] 評価の抜け（正確さ・根拠・遅延・コスト・安全・セキュリティ、Evaluation Coverage Gaps） → [ノート](notes/04-evaluation-testing/evaluation-coverage-gaps.md)
- [ ] 業務から評価を作る（モデルの変更・プロンプトの変更・リリースの関門、Deriving Evaluations from Business Processes） → [ノート](notes/04-evaluation-testing/evals-from-business-processes.md)
- [ ] LLM-as-judge の設計とバイアス（位置・長さ・自己びいき・ドリフト、LLM-as-Judge Design and Bias） → [ノート](notes/04-evaluation-testing/llm-as-judge.md)
- [ ] 設定を比べる実験の設計（1件あたりの試行回数とばらつき、Experimental Design for Configuration Comparison） → [ノート](notes/04-evaluation-testing/experimental-design.md)
- [ ] ログとトレースからの原因の切り分け（Root-Cause Isolation from Logs and Traces） → [ノート](notes/04-evaluation-testing/root-cause-isolation.md)
- [ ] コストと遅延の最適化（キャッシュのヒット率、品質の下限、Cost and Latency Optimization） → [ノート](notes/04-evaluation-testing/cost-latency-optimization.md)
- [ ] モデルのバージョンの移行（固定・再調整・基準の取り直し・延期、Model Version Migration） → [ノート](notes/04-evaluation-testing/model-version-migration.md)

### 5. ガバナンス・安全性・リスク管理（16%）
- [ ] ガードレールの置き場所（Guardrail Placement） → [ノート](notes/05-governance-safety/guardrail-placement.md)
- [ ] プロンプトインジェクションの面と対策（検索した文書・ツールの結果・MCP の応答・第三者の Skills、Prompt Injection Surface and Controls） → [ノート](notes/05-governance-safety/prompt-injection.md)
- [ ] リスクの評価と順位付け（攻撃面・故障の型・トークンと割り当ての枯渇・サプライチェーン、Risk Assessment and Ranking） → [ノート](notes/05-governance-safety/risk-assessment.md)
- [ ] 人による確認の関門（Human-in-the-Loop Checkpoints） → [ノート](notes/05-governance-safety/human-in-the-loop.md)
- [ ] コンプライアンスのための構成上の制御（データの所在・保持と ZDR・PII の検出と黒塗り・監査ログ・テナント分離、Architectural Controls for Compliance Obligations） → [ノート](notes/05-governance-safety/compliance-controls.md)
- [ ] バイアスの出どころの特定と対策（データ・プロンプトの枠組み・評価の設計、Bias Source Identification and Mitigation） → [ノート](notes/05-governance-safety/bias-sources.md)

### 6. 関係者とのコミュニケーションとライフサイクル管理（7%）
- [ ] 要件と SLA の守れない約束（Unsupportable Commitments in Requirements and SLAs） → [ノート](notes/06-stakeholder-lifecycle/unsupportable-commitments.md)
- [ ] アーキテクチャの決定記録（ADR、トレードオフと残るリスク、Architecture Decision Records） → [ノート](notes/06-stakeholder-lifecycle/architecture-decision-records.md)
- [ ] 運用への引き継ぎの完全さ（前提・依存・runbook、Operational Handoff Completeness） → [ノート](notes/06-stakeholder-lifecycle/operational-handoff.md)

### 7. 開発者の生産性と運用の支援（8%）
- [ ] Claude Code のワークフローの配布（plugins・marketplace・managed settings、Packaging and Distributing Claude Code Workflows） → [ノート](notes/07-developer-productivity/claude-code-distribution.md)
- [ ] Agent SDK と Claude Code の設定（権限モード・hooks・サブエージェント・headless/CI、Agent SDK and Claude Code Configuration） → [ノート](notes/07-developer-productivity/sdk-claude-code-configuration.md)
- [ ] AI が書いたコードの責任（Accountability for AI-Generated Code） → [ノート](notes/07-developer-productivity/ai-generated-code-accountability.md)

---

## 4週間の学習プラン（目安）

受験予定日が未定なので、4週間で仮に組む。ガイドは、Foundations のガイドを読むこと、構成図・設定・ログ・評価結果・コードを読む練習、4つのデプロイ先の違いを公式ドキュメントで読むことを勧めている。

| 週 | やること |
|---|---|
| 1週目 | 公式の Exam Guide（Dec 7 版）を通して読む → Foundations の範囲を [CCAR-F](../ccaf/README.md) で復習 → ドメイン1（設計、デプロイ先と実行環境） |
| 2週目 | ドメイン3（統合: 最小権限、認証、検索、接続、信頼性）→ ドメイン2（モデル、キャッシュ、effort、コンテキストのライフサイクル） |
| 3週目 | ドメイン4（評価、LLM-as-judge、実験、原因の切り分け、移行）→ ドメイン5（ガードレール、インジェクション、HITL、コンプライアンス） |
| 4週目 | ドメイン6・7 → [模擬試験](mock-exams/mock-01.md) → `/quiz review` → `/progress` |

## 教材
- 公式: Claude Certified Architect – Professional Exam Guide（Dec 7 版）、Claude Certified Architect – Foundations Exam Guide
- 公式: platform.claude.com（Claude Developer Platform: モデル、プロンプト、prompt caching、extended thinking と effort、context editing・memory tool・compaction、tool use、Agent Skills、評価）、code.claude.com（Claude Code・Agent SDK・plugins・settings）、modelcontextprotocol.io（MCP）、anthropic.com/engineering（contextual retrieval、multi-agent research system など）
- 公式: Amazon Bedrock・Google Vertex AI・Microsoft Foundry 上の Claude のドキュメント（機能の提供状況の違い）
- 公式の模擬試験: 確認できず（ガイドのサンプル問題3問のみ）

## 学習の記録
- 模擬試験: [第1回](mock-exams/mock-01.md)、[第2回](mock-exams/mock-02.md)
- 練習問題の記録: [quiz-log.md](quiz-log.md)（`/quiz` が書く）
- 間違えた問題と復習: [mistakes.md](mistakes.md)（`/quiz` が書く）
- 進み具合: `/progress` で確認

## 変更履歴
- 2026-11-26: 公式の Exam Guide v1.1（2026-12-07 から有効）をもとに作成。旧版との違いも記録

## 参考リンク
- 公式の Exam Guide（PDF、Dec 7 版）: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946420/Claude_Certified_Architect_-_Professional_Exam_Guide_Updated_Dec_7.pdf
- 公式の Exam Guide（PDF、November 2026 版）: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946331/Claude_Certified_Architect_-_Professional_Exam_Guide.pdf
- 公式ブログ「Four role-based Claude certifications」（2026-07-23）: https://claude.com/blog/four-role-based-claude-certifications
