# 抽出用スキーマの設計（必須と任意、nullable、enum の "other"＋詳細と "unclear"）

> ドメイン: 4. プロンプトエンジニアリングと構造化出力（20%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    文書に無いこともある項目は、==null を許す（nullable）==。分類の enum には、想定外の受け皿の "other"＋詳細と、決めきれないときの "unclear" を足す。

## 仕組み

抽出用スキーマ（extraction schema）は、抽出ツールの `input_schema` に書く JSON Schema だ。無いこともある項目を必須の値にすると、モデルはスキーマを満たすために値を作り上げてしまう（fabrication）。だから「その情報は文書に必ずあるか」「分類の候補は閉じているか」「曖昧さを区別して後で拾いたいか」で書き方を決める。tool_use で構造化出力を得る仕組みそのものは、[構造化出力のノート](tool-use-json-schema.md)が主。どのツールを呼ばせるか（any・特定ツールの強制）は [tool_choice のノート](../02-tool-design-mcp/tool-choice.md)が主。

```mermaid
flowchart TD
  A[項目] --> B{文書に必ずある?}
  B -- はい --> C[必須]
  B -- いいえ --> D[nullable にして null を許す]
  A --> E{分類の項目?}
  E -- 候補が増える --> F[enum に other＋詳細の項目]
  E -- 曖昧な記述がある --> G[enum に unclear]
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  classDef judge fill:#fff8e1,stroke:#f9a825,color:#4e342e
  classDef done fill:#e8f5e9,stroke:#43a047,color:#1b5e20
  class A run
  class B,E judge
  class C,D,F,G done
```

| パターン | 書き方 | 使うとき | 使わないとき |
|---|---|---|---|
| 必須（required） | `required` に入れる | 文書に必ずある項目（例: 求人票の職種名） | 無いこともある項目 |
| 任意（optional） | `required` に入れない | キーごと省いてよい項目 | 「無かった」と明示して残したい項目 |
| nullable | `"type": ["string", "null"]` | 文書に無ければ null と返させたい項目 | 必ずある項目（null に逃げられる） |
| enum＋"other"＋詳細 | enum に `"other"`、別項目に `*_detail` | 候補が後から増える分類 | 候補が閉じていて増えない分類 |
| enum＋"unclear" | enum に `"unclear"` | 文書の記述が曖昧で決めきれないことがある | 曖昧さを区別する必要がない |

"unclear" と null は別物だ。=="unclear" は書いてあるが決めきれない、null は書いていない==。ガイドは「optional (nullable)」とまとめて書くが、JSON Schema では任意（キーが無い）と nullable（キーはあり、値が null）は別の指定になる。

!!! example "求人票の抽出（自作）"
    ```json
    {
      "type": "object",
      "properties": {
        "job_title": {"type": "string"},
        "salary_min_yen": {"type": ["integer", "null"], "description": "記載が無ければ null。推定しない"},
        "employment_type": {"type": "string", "enum": ["full_time", "part_time", "contract", "other", "unclear"]},
        "employment_type_detail": {"type": ["string", "null"], "description": "other のときだけ原文の表記を入れる"}
      },
      "required": ["job_title", "salary_min_yen", "employment_type", "employment_type_detail"],
      "additionalProperties": false
    }
    ```

説明（description）に「無ければ null」「推定しない」を書く。公式は、説明を詳しく書くことをツールの性能で最も大事な要素としている。日付の書き方や金額の単位などの揺れは、スキーマだけでなく、プロンプトに正規化のルール（normalization rules）を書いてそろえる。

??? info "strict（`strict: true`）で使うときの制限"
    - `enum`・`required` は使える。`minimum`/`maximum`、`minLength`/`maxLength`、`oneOf` は使えない。オブジェクトには `additionalProperties: false` が要る
    - `["string","null"]` の型の配列が使えることは、上限の表の記述（type arrays の例）で確かめた
    - 上限は、1リクエスト内のすべての strict スキーマ（strict ツールと `output_config.format` の両方）の合計で数える。任意の項目は24個まで、型の配列や `anyOf` を使う項目は16個まで。strict ツールは1リクエスト20個まで
    - 長さや数値の範囲は、strict のスキーマでは書けない。説明とプロンプトに書き、受け取った後に検証する（[検証・再試行のノート](validation-retry-loop.md)）
    - strict でも enum の値の大文字・小文字は保証されない。"other" や "unclear" を後工程で拾うときは、大文字・小文字を区別せずに比べる

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| 一部の文書にしか無い項目に、もっともらしい値が埋まる | nullable にし、無ければ null と返させる | 必須の値のままにする（スキーマを満たすために値を作る） |
| 想定外の分類が、近い候補に押し込まれる | enum に "other" と、原文を残す詳細の項目を足す | "other" だけ足す（何だったかが失われ、足すべき候補も見えない） |
| 曖昧な文書だけを人のレビューに回したい | enum に "unclear" を足し、"unclear" を拾って回す | null で代用する（「書いていない」と区別できない） |
| 日付や単位の表記がばらばら | スキーマに加えて、プロンプトに正規化のルールを書く | スキーマの型だけでそろえようとする |
| スキーマに合っているのに中身がおかしい（明細の合計が総額と合わない、値が別の項目に入る） | 意味の誤りとして、受け取った後に検証する | スキーマを直せば防げると考える |

</div>

## 確認問題

**Q1.** 契約書から「解約予告期間（日数）」を抽出するツールを作っている。この条項が無い契約書でも、モデルが「30」と返してくる。最も適切な直し方はどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="B" markdown>

- A. 条項の無い契約書の例を few-shot で足し、スキーマは必須の integer のまま残す
- B. 項目を `["integer","null"]` にし、説明に「条項が無ければ null。推定しない」と書く
- C. 項目は必須の integer のまま、説明に「推定しないこと」とだけ書き足す
- D. 項目を文字列の enum にして "unclear" を足し、条項が無いときは "unclear" と返させる

</div>

??? success "答えと解説"
    **正解: B。** 文書に無いこともある項目は nullable にし、値を作らずに済む逃げ道をスキーマに用意する。

    - A: few-shot を足すより先に、スキーマに逃げ道を作る。必須の値のままでは、スキーマを満たすために値を作りうる
    - C: 必須の値のままなので、スキーマを満たすためにありそうな値を作る
    - D: "unclear" は「書いてあるが決めきれない」に使う。「書いていない」は null で表す

**Q2.** EC サイトの製品レビューから、製品カテゴリを enum（5種類）で抽出している。新しく扱い始めた種類の製品のレビューが、近いだけの既存カテゴリに入ってしまう。スキーマの直し方として最も適切なものはどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="C" markdown>

- A. enum に "other" を足し、当てはまらないレビューは "other" と返させる
- B. enum に "unclear" を足し、既存カテゴリに当てはまらないものは "unclear" にさせる
- C. enum に "other" を足し、`category_detail` に原文の製品名を入れさせる
- D. カテゴリを nullable にし、どれにも当てはまらないときは null を返させる

</div>

??? success "答えと解説"
    **正解: C。** "other" で押し込みを防ぎ、詳細の項目に原文を残せば、enum に足すべき候補も集計で分かる。

    - A: "other" だけでは何だったかが失われ、足すべき候補も見えない
    - B: "unclear" は記述が曖昧で決めきれないときに使う。想定外の候補の受け皿ではない
    - D: null は「書いていない」の意味になり、何の製品だったかも残らない

**Q3.** 工場の設備点検の報告書から、緊急度（high / medium / low）を抽出している。本文の記述が曖昧で緊急度を決めきれない報告書だけを、人の確認に回したい。設計として最も適切なものはどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="A" markdown>

- A. 緊急度の enum に "unclear" を足し、"unclear" の件だけを人の確認に回す
- B. 緊急度を nullable にし、null が返った件だけを人の確認に回す
- C. 緊急度の enum に "other" と `urgency_detail` を足し、"other" の件を人の確認に回す
- D. 緊急度を `required` から外し、キーが無い件だけを人の確認に回す

</div>

??? success "答えと解説"
    **正解: A。** "unclear" は「書いてあるが決めきれない」を明示するので、曖昧な件だけを拾える。後で拾うときは、大文字・小文字を区別せずに比べる。

    - B: null は「書いていない」の意味で、曖昧な件と記載の無い件を区別できない
    - C: "other" は想定外の候補の受け皿で、決めきれない件の印ではない
    - D: キーが無いことも「書いていない」と区別できず、曖昧さを明示させられない

## 出典
- [Claude Certified Architect – Foundations Exam Guide v1.1](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf)（公式、Task Statement 4.3、演習3）
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)（公式。対応する JSON Schema の機能、Schema complexity limits、Enum value casing）
- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)（公式。説明を詳しく書く）
