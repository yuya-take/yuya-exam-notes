# サブエージェントへのコンテキストの渡し方

> ドメイン: 1. エージェントの構成とオーケストレーション（27%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    サブエージェントは親の会話を引き継がないので、必要な情報は==起動時のプロンプトに全部書く==。前段の結果は要約せず完全な形で渡し、出典は==本文と分けた構造化データ==にする。

## 仕組み

親から子への唯一の経路は、Agent ツール（ガイドでは Task ツール）のプロンプト文字列だ。子から親へは、最後のメッセージだけが返る。子の途中のツール呼び出しは親に届かないので、親に要るものは最後のメッセージに含めさせる。

```mermaid
flowchart LR
  P[コーディネーター] -- "プロンプト文字列（調査結果＋出典＋目的）" --> S["サブエージェント<br/>新しいコンテキスト"]
  S -- "最後のメッセージだけ" --> P
  H[親の会話履歴・ツール結果] -. 渡らない .-> S
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  classDef ng fill:#fdecea,stroke:#e53935,color:#8e1c13
  class P,S run
  class H ng
```

| サブエージェントが受け取るもの | 受け取らないもの |
|---|---|
| 自分のシステムプロンプト（AgentDefinition.prompt）と、Agent ツールのプロンプト | 親の会話履歴とツール結果 |
| プロジェクトの CLAUDE.md（omitClaudeMd を指定すると読まない。この欄は TypeScript SDK だけ） | 親のシステムプロンプト |
| ツールの定義（親から継承、または指定した一部） | 先に読み込んだスキル（AgentDefinition.skills に書いたものは除く） |

親のコンテキストを引き継ぐのは、会話をまるごと複製したフォークの子だけだ（[セッションの再開とフォーク](session-resume-fork.md)）。新しく呼んだ子は前回を覚えていない。続けさせたいなら resume（再開）するか、必要な結果をプロンプトに入れ直す。

前段の結果を親が短く要約してから渡すと、根拠や出典が落ちる。出典を本文の文章に混ぜ込んでも、統合の途中で失われやすい。だから各発見を、本文とメタデータ（その情報についての情報）を分けた形で渡す。

```json
{"findings": [{"claim": "…", "evidence": "抜粋…", "source_url": "https://…", "document": "…", "page": 12, "published": "2025-06"}]}
```

コーディネーターのプロンプトには、手順ではなく「何を調べ、どの水準なら十分か」を書く。手順を1つずつ細かく指定すると、子が想定外の状況に合わせられない。逆に、目的だけの短すぎる指示も失敗する。目的・出力形式・使うツールや情報源・担当範囲の境界は示す（Anthropic のブログ）。起動の仕組みと AgentDefinition・並列起動は [Task ツールと AgentDefinition](task-tool-agent-definition.md) で扱う。

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| 統合役の出力に情報が抜ける | 前段（Web 検索・文書分析）の結果をそのままプロンプトに含める | 子が親のコンテキストを自動で引き継ぐと考える |
| 前段の結果の渡し方 | 完全な結果を渡す | 親が短く要約してから渡す（根拠や出典が落ちる） |
| 最終レポートで出典が消える | claim・抜粋・出典 URL・文書名・ページ番号・日付を構造化データで渡す | 出典を本文の文章に混ぜ込む |
| コーディネーターの指示 | 目的と十分といえる基準を示し、進め方は子に任せる | 手順を1つずつ細かく指定する／目的だけの短すぎる指示にする |
| 前回の続きをさせたい | resume するか、必要な結果をプロンプトに入れ直す | 新しく呼んだ子が前回を覚えていると考える |

</div>

## 確認問題

??? question "Q1. 調査用と分析用のサブエージェントの結果を統合用に渡したい。コーディネーターは「前の調査結果を踏まえて統合して」とだけ書いた。何が起きて、どう直す？"
    統合用の子は前の結果を見ていないので、根拠の無い統合になる。子は親の会話を引き継がない。両方の結果を完全な形でプロンプトに含める。

??? question "Q2. 統合されたレポートで、どの主張がどの文書の何ページから来たかが分からなくなった。最も効果的な対策は？"
    サブエージェント間の受け渡しを、主張・抜粋・出典 URL・文書名・ページを別の欄に持つ構造化データにする。文章で「出典を残して」と頼むだけより確実だ。

??? question "Q3. コーディネーターのプロンプトに「1. 検索を3回 2. 上位5件を読む 3. 箇条書きで要約」と書いたら、資料が少ない話題で質が落ちた。どう書き直す？"
    調べる目的と、十分といえる基準（例: 独立した情報源で裏付ける、出典を付ける）を示し、進め方は子に任せる。

## 出典
- [Subagents in the SDK — What subagents inherit](https://code.claude.com/docs/en/agent-sdk/subagents)（公式）
- [Subagents in the SDK — Resume subagents](https://code.claude.com/docs/en/agent-sdk/subagents#resume-subagents)（公式）
- [Create custom subagents（Claude Code）](https://code.claude.com/docs/en/sub-agents)（公式）
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)（公式・エンジニアリングブログ）
- Claude Certified Architect – Foundations Exam Guide v1.1、Task Statement 1.3（公式）
- 未確認: 試験がツール名を Task と Agent のどちらで出すか（ガイドは Task。現行の SDK は Agent で、旧名 Task も残る）
