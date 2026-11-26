# Claude Certified Associate – Foundations（CCAO-F）学習ノート

> 出典: 公式「Claude Certified Associate – Foundations Exam Guide」Version 1.1（Effective December 7, 2026、2026-11-26 時点で確認）。ガイド自身に「予告なく変更されることがある」とあるので、受験予約の前に公式の最新版を確認すること。2026-12-06 までに受験する場合は v1.0 が対象になる見込み（下の「v1.0 との違い」を参照。v1.0 の終了日はガイドに明記が無く、未確認）。

## 試験概要

| 項目 | 内容 |
|---|---|
| 名称 | Claude Certified Associate – Foundations |
| **受験予定日** | 未定（決まったら YYYY-MM-DD で書く） |
| 最終確認日 | 2026-11-26（`/exam-update` が更新する） |
| 試験コード | CCAO-F |
| 問題数 | 70問（採点される60問＋採点されない10問。どれが採点外かは示されない） |
| 試験時間 | 120分 |
| 合格ライン | スケールスコア 720（100〜1,000 の尺度）。基準に対する絶対評価で、合否は合計スコアだけで決まる |
| 形式 | シナリオ型の選択式。何個選ぶかは問題ごとに書かれている |
| 受験方法 | 監督付き（オンライン監督 OnVUE、またはテストセンター）。申し込みは Anthropic Partner Academy → Pearson VUE。受験できるのは Claude Partner Network のメンバー（公式ブログ） |
| 受験料 | $99 USD（1回の受験ごと）。パートナー割引があれば、Pearson での価格に反映される |
| 前提条件 | なし。必須のコースも無い。Claude を仕事で日常的に使った経験が推奨 |
| 結果の通知 | 合否とスケールスコア、ドメインごとの正答率（ドメイン別の値は合否に使わない） |
| キャンセル・変更 | OnVUE は予約の1時間前まで、テストセンターは48時間前まで。それより遅いと受験料は没収 |
| 有効期間 | 認定から12か月。期限内なら、Partner Academy の無料・監督なしの評価で更新できる。失効したら本試験を正規の料金で受け直す。内容が大きく変わったときは本試験の受け直しを求められることがある |
| 再受験 | 不合格後の待機期間は 1回目 14日、2回目 30日、3回目 90日。受験は直近12か月で4回まで（試験ごとに数える） |
| 言語 | 未確認（ガイドに記載なし。英語のみとする第三者情報あり・要確認） |
| 想定する受験者 | Claude を仕事の中心的な道具として使い、Claude Projects を作る人（業務分析、PM、オペレーション、マーケティング、広報、人事、教育、コンサルタント、ナレッジワーカー）。claude.ai（web / desktop / mobile）の chat・Projects・Artifacts・モデル選択・research・コード実行による分析・ファイルと画像のアップロード・Skills・connectors・memory と incognito chats を使いこなす |

## 出題ドメインと比重

| # | ドメイン | 比重 | 優先度 |
|---|---|---|---|
| 1 | タスクの定義とプロンプト（Task Definition and Prompting） | 15% | ★☆☆ |
| 2 | 出力の評価と品質管理（Output Evaluation and Quality Control） | 20% | ★★★ |
| 3 | 機能・モデル・コンテキストの選択（Capability, Model, and Context Selection） | 15% | ★☆☆ |
| 4 | ワークフローの設計と組み込み（Workflow Design and Integration） | 18% | ★★☆ |
| 5 | 設定とナレッジの管理（Configuration and Knowledge Management） | 15% | ★☆☆ |
| 6 | 責任ある利用・データ保護・ガバナンス（Responsible Use, Data Protection, and Governance） | 17% | ★★☆ |

比重の差は 15〜20% と小さく、どのドメインも落とせない。ドメイン2（出力の評価）が最大なので最優先にし、次にドメイン4・6を厚くする。ガイドは「問題は仕事の場面での判断を問う。料金、コンテキストウィンドウの大きさ、レート制限など公表された数値の暗記は問わない」と明記している。

### 全ドメインの土台: AI Fluency の4つのコンピテンシー

ガイドは、Anthropic の AI Fluency Framework の4つのコンピテンシー（Delegation・Description・Discernment・Diligence）が、すべてのドメインの目標を支えるとしている。ノートは [AI Fluency の4D](notes/04-workflow-design/ai-fluency-4d.md) を参照。

### 出題範囲の外（ガイドから）

- API を使って開発するソフトウェア開発者や、エージェント型システムの設計者向けの内容（Developer / Architect の範囲）
- 機械学習の専門知識、ソフトウェアエンジニアリング、高度な AI システム設計
- 料金、コンテキストウィンドウの大きさ、レート制限など、公表された数値の暗記

### v1.0 との違い（2026-12-06 までに受験する場合）

| 項目 | v1.0（Effective July 2026） | v1.1（Effective December 7, 2026） |
|---|---|---|
| 問題数 | 60問 | 70問（採点60＋採点外10） |
| ドメイン | 7つ（Prompting and Task Execution 14%、Output Evaluation and Validation 21%、Product and Model Selection 12%、Workflow Integration and Solution Design 16%、Configuration and Knowledge Management 12%、Governance, Risk, and Responsible Use 15%、Troubleshooting and Optimization 10%） | 6つ（上の表）。Troubleshooting は独立したドメインでなくなり、中身はドメイン1の「プロンプトの診断」とドメイン5の「設定の劣化」に移ったとみられる（推論） |
| 新しく入った要素 | — | Skills、effort レベル、memory と incognito chats、AI Fluency の4D、Anthropic Usage Policy |
| 消えた要素 | モデル名（Haiku / Sonnet / Opus）の区別 | 出題項目からモデル名が消え、「数値の暗記は問わない」と明記 |
| キャンセル | 予約の24時間前まで | OnVUE 1時間前、テストセンター 48時間前 |

v1.0 の出題項目の大半は v1.1 のノートで覆える。v1.0 で受けるなら、Haiku / Sonnet / Opus の使い分け（[モデルと effort の選び方](notes/03-capability-model-context/model-effort-selection.md)）を厚めに読む。

---

## ドメイン別チェックリスト

各項目の末尾は、ガイドのスキル名（Skill）。

### 1. タスクの定義とプロンプト（15%）
- [ ] プロンプトの組み立て（役割・文脈・タスク・出力形式、Claude が知らない文脈を渡す、Prompt Construction） → [ノート](notes/01-task-definition-prompting/prompt-construction.md)
- [ ] 例・資料・構造で狙いを伝える（例示、資料の渡し方、区切りと見出し、Prompt Construction） → [ノート](notes/01-task-definition-prompting/examples-and-structure.md)
- [ ] 大きな成果物の分解と順序付け（段階的なプロンプト、follow-up、ステップ間の確認、Task Decomposition and Sequencing） → [ノート](notes/01-task-definition-prompting/task-decomposition.md)
- [ ] タスクの種類に合わせたプロンプトの戦略（分析・調査・起草・ブレインストーミング、Task Decomposition and Sequencing） → [ノート](notes/01-task-definition-prompting/strategy-by-task-type.md)
- [ ] うまくいかないプロンプトの診断と、直す・やり直す・やり方を変えるの判断（Prompt Diagnosis and Iteration） → [ノート](notes/01-task-definition-prompting/prompt-diagnosis-iteration.md)

### 2. 出力の評価と品質管理（20%）
- [ ] 出力の評価と目的への適合（そのまま使える・修正が必要・人の手で直す、Output Evaluation and Fitness for Purpose） → [ノート](notes/02-output-evaluation/fitness-for-purpose.md)
- [ ] ハルシネーションの見つけ方（作られた引用、自信ありげな具体値、矛盾、偏り、Hallucination Detection and Verification） → [ノート](notes/02-output-evaluation/hallucination-patterns.md)
- [ ] 使う前の検証（出典の確認、引用の点検、独立した確認、Hallucination Detection and Verification） → [ノート](notes/02-output-evaluation/verification-techniques.md)
- [ ] レビューの深さとエスカレーション（誤りの影響、社内の下書きと社外に出すもの、Review Depth and Escalation） → [ノート](notes/02-output-evaluation/review-depth-escalation.md)
- [ ] 読み手に合わせた編集と出力形式の選択（インライン・Artifacts・構造化データ・コード実行の結果・Skill が作る文書、Output Adaptation and Format Selection） → [ノート](notes/02-output-evaluation/output-format-selection.md)

### 3. 機能・モデル・コンテキストの選択（15%）
- [ ] タスクに合う機能の組み合わせ（chat・Projects・Artifacts・research・Skills・connectors・memory、Capability Selection） → [ノート](notes/03-capability-model-context/capability-selection.md)
- [ ] research とコード実行による分析の使いどころ（Capability Selection） → [ノート](notes/03-capability-model-context/research-and-code-execution.md)
- [ ] モデルの階層と effort レベルの選び方（品質・速さ・コスト、Model and Effort Selection） → [ノート](notes/03-capability-model-context/model-effort-selection.md)
- [ ] 長い作業のコンテキスト管理（続ける・要約して新しく始める・Project に残す、Context and Memory Management） → [ノート](notes/03-capability-model-context/context-management.md)
- [ ] memory の仕組みと質の保ち方（見直し・編集・削除・incognito chats、Context and Memory Management） → [ノート](notes/03-capability-model-context/memory-and-incognito.md)

### 4. ワークフローの設計と組み込み（18%）
- [ ] AI Fluency の4D（Delegation・Description・Discernment・Diligence） → [ノート](notes/04-workflow-design/ai-fluency-4d.md)
- [ ] 調査・分析・計画の成果物を最初から最後まで作る流れ（要件、出典つきの調査、データ分析、実行できる計画、End-to-End Deliverable Workflows） → [ノート](notes/04-workflow-design/end-to-end-deliverables.md)
- [ ] 任せる・人が持つ・人がレビューするの振り分けと、任せすぎ（Delegation and Workflow Redesign） → [ノート](notes/04-workflow-design/delegation-workflow-redesign.md)
- [ ] 繰り返す作業の仕組み化と、同僚への引き継ぎ（Repeatable Workflow Design） → [ノート](notes/04-workflow-design/repeatable-workflows.md)
- [ ] AI になじみの薄い関係者への、できること・できないことの伝え方（Capability Communication） → [ノート](notes/04-workflow-design/capability-communication.md)

### 5. 設定とナレッジの管理（15%）
- [ ] Project の設定と、instructions・knowledge・Skill の使い分け（Project Configuration） → [ノート](notes/05-configuration-knowledge/project-configuration.md)
- [ ] Skills の仕組みと使いどころ（作成・共有・バージョン、Project Configuration） → [ノート](notes/05-configuration-knowledge/skills.md)
- [ ] connectors とアップロードの使い分け、ナレッジを新しく保つ（Connector and Knowledge Management） → [ノート](notes/05-configuration-knowledge/connectors-and-knowledge.md)
- [ ] 永続的な指示の設計（Project instructions・プロフィールの設定・styles と、依頼ごとのプロンプトの役割分担、Persistent-Instruction Design） → [ノート](notes/05-configuration-knowledge/persistent-instructions.md)
- [ ] 設定の劣化の原因の層を特定する（instructions・知識の鮮度・Skill のバージョン・たまった memory、Configuration Lifecycle and Degradation） → [ノート](notes/05-configuration-knowledge/configuration-degradation.md)

### 6. 責任ある利用・データ保護・ガバナンス（17%）
- [ ] ユースケースの適切さの分類（適切・安全策つきで適切・不適切、Use-Case Appropriateness） → [ノート](notes/06-responsible-use/use-case-appropriateness.md)
- [ ] Anthropic Usage Policy の要点（禁止・高リスクの用途、Use-Case Appropriateness） → [ノート](notes/06-responsible-use/usage-policy.md)
- [ ] 第三者の Skills と connectors を信頼してよいか（Use-Case Appropriateness） → [ノート](notes/06-responsible-use/third-party-trust.md)
- [ ] 機密データの扱い（分類、黒塗りと匿名化、コード実行の分析へのアップロードの判断、Data Protection in Practice） → [ノート](notes/06-responsible-use/data-protection.md)
- [ ] プライバシーの設定（incognito chats、memory、データの保持と学習への利用の設定、Data Protection in Practice） → [ノート](notes/06-responsible-use/privacy-controls.md)
- [ ] 組織の AI ポリシー・倫理・Diligence（ポリシーの抜けと教育の抜けの区別、是正策、Policy, Ethics, and Diligence） → [ノート](notes/06-responsible-use/policy-ethics-diligence.md)

---

## 4週間の学習プラン（目安）

受験予定日が未定なので、4週間で仮に組む。ガイドの「How to Prepare」に沿って、読むだけでなく claude.ai で実際に手を動かす。

| 週 | やること |
|---|---|
| 1週目 | 公式の Exam Guide v1.1 を通して読む（サンプル問題3問も） → AI Fluency の4D → ドメイン1（プロンプト）。自分の仕事のプロンプトを1つ選び、「仕様の抜け」の観点で直してみる |
| 2週目 | ドメイン2（出力の評価、ハルシネーション、レビューの深さ）とドメイン3（機能・モデル・memory）。research の出力の引用を実際に1つずつ確かめる |
| 3週目 | ドメイン5（Projects、Skills、connectors）とドメイン4（ワークフロー）。繰り返す作業1つについて、instructions・knowledge・Skill を持つ Project を作り、Google Drive などの connector をつなぐ。memory を見直し、編集・削除する |
| 4週目 | ドメイン6（Usage Policy、データ保護、ポリシー）。機密を含むデータを匿名化してから分析する手順を練習する → [模擬試験](mock-exams/mock-01.md) → `/quiz review` → `/progress` |

## 教材
- 公式: Claude Certified Associate – Foundations Exam Guide（v1.1）、Anthropic Partner Academy の準備用コース（中身は未確認）
- 公式: Anthropic の AI Fluency Framework（Delegation / Description / Discernment / Diligence）と、Anthropic Academy の AI Fluency コース
- 公式: claude.ai のヘルプセンター（support.claude.com。Projects、Artifacts、Skills、research、コード実行、connectors、memory、incognito chats）、プロンプトのガイド（docs.claude.com）、Anthropic Usage Policy（anthropic.com/legal/aup）
- 公式の模擬試験: 確認できず（ガイドのサンプル問題3問のみ）

## 学習の記録
- 模擬試験: [第1回](mock-exams/mock-01.md)、[第2回](mock-exams/mock-02.md)
- 練習問題の記録: [quiz-log.md](quiz-log.md)（`/quiz` が書く）
- 間違えた問題と復習: [mistakes.md](mistakes.md)（`/quiz` が書く）
- 進み具合: `/progress` で確認

## 変更履歴
- 2026-11-26: 公式の Exam Guide v1.1（2026-12-07 から有効）をもとに作成。v1.0 との違いも記録

## 参考リンク
- 公式の Exam Guide（PDF、v1.1）: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946609/Claude_Certified_Associate_-_Foundations_Exam_Guide_Updated_Dec_7.pdf
- 公式ブログ「Four role-based Claude certifications」（2026-07-23）: https://claude.com/blog/four-role-based-claude-certifications
- Partner Academy の準備用パス（403 で中身は未確認）: https://anthropic-partners.skilljar.com/path/claude-certified-associate-foundations
