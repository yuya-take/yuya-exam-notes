# Claude Certified Architect – Foundations（CCA-F / CCAR-F）学習ノート

> ⚠️ 下記の内容は第三者の解説記事をもとにまとめたもの（2026-11時点）。受験予約の前に、Anthropic 公式の Exam Guide で最新の出題範囲・形式・料金を必ず確認すること。

## 試験概要

| 項目 | 内容 |
|---|---|
| 名称 | Claude Certified Architect – Foundations |
| **受験予定日** | 未定（決まったら YYYY-MM-DD で書く） |
| 最終確認日 | 2026-11-20（`/exam-update` が更新する） |
| 試験コード | CCAR-F（旧称 CCA-F） |
| 問題数 | 60問 |
| 試験時間 | 120分 |
| 合格ライン | スケールスコア 720 / 1000 |
| 形式 | 監督付き（プロクタリング）、シナリオベースの選択問題 |
| 受験料 | 約 $125（要確認） |

関連資格（同じ Foundations シリーズ）:
- CCAO-F: Claude Certified Associate（入門向け）
- CCDV-F: Claude Certified Developer

## 出題ドメインと比重

| # | ドメイン | 比重 | 優先度 |
|---|---|---|---|
| 1 | エージェント設計（Agentic Architecture） | 27% | ★★★ |
| 2 | Claude Code の設定 | 20% | ★★★ |
| 3 | プロンプトエンジニアリング | 20% | ★★☆ |
| 4 | ツール設計と MCP | 18% | ★★☆ |
| 5 | コンテキスト管理 | 15% | ★☆☆ |

ドメイン1と2で全体の半分近くになるので、ここを重点的に固める。

---

## ドメイン別チェックリスト

### 1. エージェント設計（27%）
- [ ] 「ワークフロー」（処理の流れが決まっている）と「エージェント」（モデルが自分で判断して進める）の違い
- [ ] 定番パターン: プロンプトチェーン、ルーティング、並列化、オーケストレーター＋ワーカー、評価＋改善ループ
- [ ] マルチエージェント／サブエージェントの使いどころとデメリット（コストと、受け渡しで情報が落ちること）
- [ ] Claude Agent SDK のエージェントループの仕組み
- [ ] 人の承認を挟む設計（human-in-the-loop）、ガードレール、失敗したときの扱い
- [ ] 単純な構成で足りるなら単純な方を選ぶ、という判断基準

### 2. Claude Code の設定（20%）
- [ ] CLAUDE.md の置き場所と読み込まれる順番（ユーザー／プロジェクト／サブディレクトリ）
- [ ] settings.json の階層（user / project / local）と permissions の allow / deny
- [ ] Hooks（PreToolUse、PostToolUse、SessionStart、Stop など）
- [ ] スラッシュコマンド、Skills、サブエージェント（`.claude/agents/`）
- [ ] MCP サーバーの追加とスコープ
- [ ] ヘッドレス実行（`claude -p`）、CI や GitHub Actions との連携
- [ ] パーミッションモード（default / acceptEdits / plan / auto など）

### 3. プロンプトエンジニアリング（20%）
- [ ] システムプロンプトとユーザープロンプトで何を書き分けるか
- [ ] XML タグで構造を作る、few-shot の例を入れる
- [ ] 段階的に考えさせる手法、extended thinking
- [ ] 出力形式の指定、構造化出力（JSON）
- [ ] プロンプトの評価（eval）を作って改善を回す流れ

### 4. ツール設計と MCP（18%）
- [ ] Tool use の流れ（tool_use → tool_result）
- [ ] 良いツール定義の書き方（名前、説明、入力スキーマ、エラーの返し方）
- [ ] MCP の構成（ホスト / クライアント / サーバー、tools / resources / prompts）
- [ ] トランスポートの種類（stdio / Streamable HTTP）と認証
- [ ] ツールの数や粒度の決め方、セキュリティ（プロンプトインジェクション対策）

### 5. コンテキスト管理（15%）
- [ ] コンテキストウィンドウの上限と、要約・圧縮（compaction）
- [ ] プロンプトキャッシュの仕組みと、キャッシュが効くようにプロンプトを並べる順番
- [ ] RAG と、必要な分だけ段階的に読み込む方式の違い
- [ ] 長期記憶（メモリ）、外部ファイルに状態を保存するやり方
- [ ] サブエージェントを使って本体のコンテキストを汚さない方法

---

## 4週間の学習プラン（目安）

| 週 | やること |
|---|---|
| 1週目 | 公式 Exam Guide を読む → Anthropic Academy のコースを受講 → ドメイン1（エージェント設計）を学ぶ |
| 2週目 | ドメイン2（Claude Code の設定）を実際に手を動かして学ぶ（CLAUDE.md、hooks、サブエージェント、MCP を自分で設定してみる） |
| 3週目 | ドメイン3〜5。Claude API でツール呼び出しとプロンプトキャッシュを実際に動かしてみる |
| 4週目 | `/quiz` で模擬試験 → `/quiz review` で間違えた問題を復習 → `/progress` で苦手なところを確認 |

## 教材
- Anthropic 公式: Exam Guide、Anthropic Academy（コース）、docs.claude.com、Claude Code のドキュメント
- Anthropic の記事 "Building effective agents"（ドメイン1の土台になる内容）
- 第三者の学習ガイド（下記の参考リンク）

## 学習の記録
- 練習問題の記録: [quiz-log.md](quiz-log.md)（`/quiz` が書く）
- 間違えた問題と復習: [mistakes.md](mistakes.md)（`/quiz` が書く）
- 進み具合: `/progress` で確認

## 変更履歴
- 2026-11-20: 作成（第三者の解説記事をもとに作成。公式の Exam Guide との突き合わせは未実施）

## 参考リンク（第三者）
- https://tutorialsdojo.com/ccar-f-claude-certified-architect-foundations-study-guide/
- https://rickhigh.substack.com/p/claude-certified-architect-the-complete
- https://findskill.ai/blog/claude-certified-architect-5-domains-explained/
- https://www.cloudthat.com/resources/blog/inside-claude-certified-architect-foundations-what-anthropics-new-exam-actually-measures
