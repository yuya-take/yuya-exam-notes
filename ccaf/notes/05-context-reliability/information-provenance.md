# 複数ソースの統合で出典を保ち、矛盾と時期の違いを扱う

> ドメイン: 5. コンテキスト管理と信頼性（15%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    サブエージェントに==主張と出典の対応表（claim-source mapping）==を構造化して返させ、統合でも保つ。信頼できる出典どうしが食い違ったら、片方を選ばず==両方を出典付きで並べて注記する==。

## 仕組み

要約で発見を圧縮すると、「どの主張がどの出典か」が消える。だからサブエージェントには、主張・出典・抜粋・日付を欄に分けて返させる。統合エージェントは、複数のサブエージェントの対応表を「保ち、まとめる（preserve and merge）」。文章に書き直して対応を捨てない。

```mermaid
flowchart LR
  S1[サブエージェントA] -->|claim＋出典＋日付| C[コーディネーター<br>矛盾を注記のまま受け取り<br>扱いを決める]
  S2[サブエージェントB] -->|claim＋出典＋日付| C
  C -->|対応表を保ったまま| Y[統合エージェント]
  Y --> R[レポート<br>確立した発見／争いのある発見]
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  classDef judge fill:#fff8e1,stroke:#f9a825,color:#4e342e
  classDef done fill:#e8f5e9,stroke:#43a047,color:#1b5e20
  class S1,S2,Y run
  class C judge
  class R done
```

| 欄（ガイドが挙げる項目） | 中身 |
|---|---|
| claim | 主張 |
| 出典 | 出典 URL・文書名 |
| 抜粋 | 根拠になる箇所（relevant excerpt） |
| 日付 | 公開日またはデータの収集日 |

文書分析は、矛盾する値を両方含め、明示的に注記した状態で完了させる。和解（reconcile）は、コーディネーターが統合の前に決める。日付の欄が要るのは、時期の違いを矛盾と取り違えないためだ。日付があれば「2022年の調査で40%、2025年の調査で55%」は変化として読める。日付が無いと矛盾に見える。

レポートは、確立した発見（well-established）と争いのある発見（contested）を明示的な節に分ける。元の出典の言い方と方法の文脈も残す（例の「推定」「暫定値」「調査対象・手法」は私の解釈による具体化）。形式は内容の種類で変える（ガイドの例）。財務データは表、ニュースは文章、技術的な発見は構造化した箇条書きにする。

??? info "公式ドキュメントでの裏付け（API・プロンプト側）"
    - Citations（引用機能）: 文書ごとに有効にすると、主張ごとに `cited_text`・`document_index`・`document_title` と位置（文字・ページ）を返す
    - 長い文書では、先に関係する箇所を引用させてから作業させる。引用で裏付けられない主張は撤回させる（Reduce hallucinations）
    - Anthropic の調査システムは、発見をまとめた後に CitationAgent（文書とレポートから引用箇所を特定する役）へ渡す
    - Skill authoring best practices の調査統合の例: 出典どうしが一致・対立する点を確かめ、各論点を支える出典を記し、要約に対立する見方を含める

??? info "ずれと関連ノート"
    - ずれ: Citations は structured outputs（JSON スキーマでの出力）と同時に使えない（400 エラー）。ガイドの「構造化した対応表」は設計パターンで、Citations の機能名ではない。回避策は1フィールド1行で答えさせてコードで解析する（「JSON だけを返せ」は引用が減るので避ける）
    - 補足（私の解釈）: `conflict_detected` は抽出時の矛盾フラグ（4.4、[検証と再試行のループ](../04-prompt-engineering/validation-retry-loop.md)）。5.6 は統合での扱いが主
    - サブエージェントへ構造化メタデータを渡す側の話は [サブエージェントへのコンテキストの渡し方](../01-agentic-architecture/subagent-context-passing.md)。日付・出典を返させる受け渡しの構造化は、別ノート「[位置の影響への対策と、エージェント間で渡す情報の構造化](lost-in-the-middle-structured-passing.md)」

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| 最終レポートで出典が消えている | サブエージェントに claim・抜粋・URL/文書名・日付を構造化で返させ、統合でも保つ | 出典を本文の文章に混ぜる、「出典を残して」と頼むだけ（統合で落ちやすい。私の推論）。欄を分けた構造化データにする（ガイドの Exercise 4） |
| 信頼できる2つの統計が食い違う | 両方を出典付きで載せて注記し、争いのある発見の節に置く | 一方を勝手に選ぶ、平均を取る、新しいほうだけ残す（「平均」「新しいほう」はガイドの「arbitrarily selecting」を私が具体化した例） |
| 古い資料と新しい資料で値が違い「矛盾」と報告される | 出力に公開日・収集日を必須にする | 時期の違うデータを同じ時点の値として並べる（変化を矛盾と誤読させる） |
| 文書分析の段で矛盾を見つけた | 注記して返し、コーディネーターに決めさせる | 分析の段で解決する |
| 不確かさのある発見を書く | 確立した発見と争いのある発見を節で分け、元の言い方を残す | 同じ調子で書く、「推定」を断定に言い換える（不確かさが消える） |
| 統合結果が全部同じ形式で読みにくい | 内容の種類ごとに表・文章・箇条書きを使い分ける | すべて同じ形式で書く |

</div>

## 確認問題

??? question "Q1. 市場調査エージェントのレポートに「国内の家庭用蓄電池の普及率は 8% と 12%」と出典なしで両方書かれ、読者が混乱している。2つの値は別の年の統計だった。何を直す？"
    サブエージェントの出力に、出典（URL・文書名）と公開日・収集日を必須にし、統合でも保つ。日付があれば年による変化と読め、矛盾ではないと分かる。

??? question "Q2. 2つの公的機関が、同じ年の同じ指標で違う値を出していた。統合エージェントは中間の値を書いた。どう設計し直す？"
    両方の値を出典付きで残し、矛盾として注記する。争いのある発見の節に置き、元の出典の言い方や調査方法の違いも添える。平均は根拠の無い値を作るので不可。

??? question "Q3. 文書分析のサブエージェントが、矛盾を見つけるたびに自分で片方を選んで報告している。どうさせるべきか？"
    矛盾する値を両方含めて注記したまま、分析を完了させる。扱いは、コーディネーターが統合の前に決める。

## 出典
- [Claude Certified Architect – Foundations Exam Guide v1.1（タスクステートメント 5.6、Exercise 4）](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf)（公式）
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)（公式。引用の欄、structured outputs と併用不可）
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)（公式。文書を `<document>`・`<source>` タグで渡す、先に引用させる、出力形式の指示）
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)（公式。引用で裏付けられない主張を撤回させる）
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)（公式。Research synthesis workflow の例: 一致・対立の確認、論点ごとの出典、Conflicting viewpoints）
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)（公式。CitationAgent、一次情報を優先する評価）
- 未確認: 矛盾する統計の扱い方や、時期の違いを日付で区別することまで書いた公式ドキュメント（ガイド以外では見つからなかった）
