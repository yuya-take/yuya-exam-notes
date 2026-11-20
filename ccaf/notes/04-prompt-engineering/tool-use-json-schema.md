# tool_use と JSON スキーマによる構造化出力

> ドメイン: 4. プロンプトエンジニアリングと構造化出力（20%） ／ 更新: 2026-11-20

!!! abstract "ひとことで"
    抽出したい項目をツールの入力スキーマ（input_schema）にし、tool_use ブロックの `input` を受け取る。==構文の誤りは消えるが、意味の誤りは消えない==。

## 仕組み

抽出用のツールは、実際の処理を持たなくてよい。スキーマを渡す「器」として使い、`input` をそのまま結果にする。これがスキーマどおりの出力を得るいちばん確実な方法だ。ツール定義に `strict: true` を付ける strict tool use は、出力をスキーマに合うトークンだけに絞る（grammar-constrained sampling）。だから型の違い（`"2"` と `2`）や必須項目の抜けも無くなる。必ずツールを呼ばせるのは tool_choice の設定だ。文書の種類が分からず抽出ツールが複数あるなら any、特定の抽出を先に通すなら tool にする（ガイドの書き方。現行モデルの制限は下の折りたたみ。詳細は [tool_choice のノート](../02-tool-design-mcp/tool-choice.md)）。

```mermaid
flowchart LR
  A[文書] --> B["抽出ツール<br/>input_schema + strict: true"]
  B --> C[tool_use ブロック]
  C --> D["input を取り出す<br/>（ツールは実行しなくてよい）"]
  D --> E{"意味の検証<br/>合計・欄の対応"}
  E -- 合う --> F[結果を使う]
  E -- 合わない --> G["誤りを添えて再試行<br/>（上限つき）"]
  G --> B
  E -- 直らない --> H[人の確認に回す]
  classDef run fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1
  classDef judge fill:#fff8e1,stroke:#f9a825,color:#4e342e
  classDef done fill:#e8f5e9,stroke:#43a047,color:#1b5e20
  class A,B,C,D,G run
  class E judge
  class F,H done
```

スキーマが保証するのは形だけだ。その誤りが ==JSON の形の問題か、値の中身の問題か==で手段が分かれる。形ならスキーマで、中身ならアプリ側の検証とプロンプトで直す。

| 誤りの例 | tool use＋厳密なスキーマで | 拾う方法 |
|---|---|---|
| 閉じ括弧の抜けなど、JSON として壊れている | 防げる | — |
| 必須項目の抜け、型の違い（数値が文字列） | 防げる（strict のとき） | — |
| enum に無い値 | 防げる（大文字・小文字の違いは除く） | 大文字・小文字を無視して比べる。大文字・小文字だけが違う enum 値を作らない |
| 明細の合計が total と合わない | 防げない | アプリ側の計算チェック |
| 値が別の欄に入る（請求日と支払期限が逆） | 防げない | 検証＋プロンプトで欄の定義を明記 |
| 元の文書に無い値を作る | 防げない（必須にすると増える） | 任意・nullable にする（[抽出用スキーマのノート](extraction-schema-design.md)） |
| 書き方のばらつき（`2026/3/5` と `5 Mar 2026`） | 型だけでは決まらない | プロンプトに正規化のルールを書く |

`format: "date"`（strict でも対応）で形は縛れる。しかし `03/05` が3月5日か5月3日かは、スキーマでは決まらない。元の書き方をどう解釈するかは、プロンプトに書く。

??? info "スキーマに合わない出力・strict の制限・ガイドとのずれ"
    - `stop_reason: "max_tokens"`: 途中で切れて、スキーマに合わない。`max_tokens` を増やして再実行する
    - `stop_reason: "refusal"`: 安全上の拒否が優先され、スキーマに合わないことがある
    - strict 無しでは何も保証されない。壊れた JSON（構文の誤り）も、型の違い（`"two"`）や必須項目の抜けも起こりうる（頻度は書かれていない）
    - strict でも使えない JSON Schema の機能がある（`minimum` / `maximum`、`minLength` などは 400 エラー）。数値の範囲チェックもアプリ側の検証になる。SDK ヘルパーの多くは、使えない制約を外して description に書き足す。応答を検証するヘルパーなら、元の制約で検証する
    - ガイドとのずれ: ガイドは「tool use＋JSON スキーマ」と書く。現行ドキュメントでは、同じ仕組み（constrained decoding）が structured outputs（`output_config.format`）と strict tool use の2つに分かれている
    - ガイドとのずれ: 現行の define-tools では、Fable 5.2・Mythos 5.2・Opus 5.5・Sonnet 5.5・Fable 5.1・Mythos 5.1 は tool_choice の any / tool を 400 エラーで拒否する（Opus 5・Haiku 5.5 などは受け付ける）。代わりに auto＋strict tool use か structured outputs を勧める。試験はガイドの書き方で覚える
    - モデルに関係なく、手動の extended thinking（`thinking: {type: "enabled"}`）と any / tool を併用するとエラーになる

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| テキストで返させた JSON が、時々パースできない | 抽出ツールの input_schema（＋strict）に変える | プロンプトの頼み方を工夫する |
| スキーマどおりなのに、合計や欄の対応がおかしい | 検証して、誤りを添えて再試行する（[検証・再試行のノート](validation-retry-loop.md)） | スキーマをさらに厳しくする（保証されるのは形だけ） |
| 文書ごとに日付や単位の書き方がばらばら | スキーマに加えて、プロンプトに「日付は YYYY-MM-DD」などの正規化ルールを書く | `format: "date"` などスキーマだけでそろえる |
| 情報が無い文書もある項目 | 任意・nullable にする | 必須にして抜けを無くす（値を作ってしまう） |

</div>

## 確認問題

**Q1.** 経費精算システムで、レシートの画像から `items`（品目と金額の配列）と `total` を抽出している。抽出ツールを `strict: true` にしてから、パースエラーは無くなった。しかし、品目の合計と `total` が時々食い違う。最も適切な対応はどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="A" markdown>

- A. 抽出後にアプリ側で品目の合計を計算して `total` と比べ、合わなければ差を添えて再試行する
- B. `total` に `minimum` と `maximum` を付け、ありえない金額をスキーマで弾けるようにする
- C. `items` と `total` を両方 `required` にし、`additionalProperties: false` を付けて厳しくする
- D. tool_choice で抽出ツールを必ず呼ばせ、テキストでの応答が混ざらないようにする

</div>

??? success "答えと解説"
    **正解: A。** 合計の食い違いは意味の誤りなので、スキーマでは防げず、アプリ側の計算チェックで拾う。

    - B: strict では `minimum` / `maximum` は使えない（400 エラー）。使えたとしても、合計の一致は確かめられない
    - C: strict が保証するのは形だけで、スキーマを厳しくしても中身の誤りは消えない
    - D: ツールを必ず呼ばせても、`input` の値の中身は正しくならない

**Q2.** 契約書の抽出で、`signed_date` に `2026年3月5日`、`03/05/26`、`5.3.2026` のような書き方が混ざって届く。後工程では YYYY-MM-DD でそろえて使いたい。対応として適切なものはどれか。（2つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="A,C" markdown>

- A. プロンプトに正規化のルール（YYYY-MM-DD に直す、`03/05/26` は月/日/年として読む）を書く
- B. スキーマに `format: "date"` を付ければ、元の書き方の解釈も含めてそろうので、ほかは変えない
- C. string 型に `format: "date"` を付けたスキーマは残し、出力の形を縛る
- D. 書き方ごとに `signed_date_ja`、`signed_date_us` のような項目を分け、スキーマに足す
- E. strict を外し、モデルが元の書き方のまま自由に返せるようにしておく

</div>

??? success "答えと解説"
    **正解: A と C。** スキーマで出力の形を縛り、元の書き方をどう解釈するかはプロンプトに書く。

    - B: `format: "date"` は形を縛るだけで、`03/05` が3月5日か5月3日かは決めない
    - D: 項目を分けても、どの解釈で読むかは決まらないまま残る
    - E: strict を外すと、型や必須項目の保証まで失う。書き方もそろわない

**Q3.** 社内文書の抽出結果を、JSON のテキストで返すよう頼んでいる。1,000件に数件、引用符が崩れてパースに失敗する。最も確実な改善はどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="B" markdown>

- A. プロンプトに「必ず正しい JSON だけを返すこと」と書き、出力の例も添えて強調する
- B. 抽出項目を input_schema にしたツールを `strict: true` で定義し、tool_use の `input` を受け取る
- C. 抽出項目を input_schema にしたツールを `strict` なしで定義し、tool_use の `input` を受け取る
- D. パースに失敗した出力を、正規表現で引用符を補ってから読み込む後処理を足す

</div>

??? success "答えと解説"
    **正解: B。** strict tool use は、出力をスキーマに合うトークンだけに絞るので、構文の誤りが無くなる。

    - A: プロンプトの頼み方を工夫しても、構文は保証されない
    - C: strict 無しでは何も保証されず、壊れた JSON も起こりうる
    - D: 壊れた出力を後から繕うだけで、スキーマどおりの出力を得る方法にならない

## 出典
- [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)（公式）
- [Structured outputs — Invalid outputs / JSON Schema limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)（公式）
- [Define tools — Forcing tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use)（公式）
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)（公式。tool_use ブロックの `input`）
- Claude Certified Architect – Foundations Exam Guide v1.1、タスクステートメント 4.3・4.4（公式）
- 未確認: strict 無しの tool use で、JSON の構文そのものが壊れる頻度。ドキュメントは型の違い・必須の抜けの例を挙げるだけで、構文の誤りの発生率は書いていない
