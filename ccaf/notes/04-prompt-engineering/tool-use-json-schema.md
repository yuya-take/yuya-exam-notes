# tool_use と JSON スキーマによる構造化出力

> ドメイン: 4. プロンプトエンジニアリングと構造化出力（20%） ／ 更新: 2026-11-20

## 3行まとめ
- 抽出したい項目を「ツールの入力スキーマ（input_schema）」として定義し、tool_use ブロックの `input` を受け取るのが、スキーマどおりの出力を得るいちばん確実な方法
- **構文の誤りは消えるが、意味の誤りは消えない**。合計が合わない、別の欄に入る、はアプリ側の検証で拾う
- 試験の決め手は「その誤りは JSON の形の問題か、値の中身の問題か」。形ならスキーマ、中身なら検証・プロンプト

## 仕組み

```mermaid
flowchart LR
  A[文書] --> B["抽出ツール<br/>input_schema + strict: true"]
  B --> C[tool_use ブロック]
  C --> D["input を取り出す<br/>（ツールは実行しなくてよい）"]
  D --> E[意味の検証<br/>合計・欄の対応]
```

- ツールは実際の処理を持たなくてよい。スキーマを渡す「器」として使い、`input` をそのまま結果にする
- strict tool use（ツール定義に `strict: true`。出力をスキーマに合うトークンだけに絞る grammar-constrained sampling）で、型の違い（`"2"` と `2`）や必須項目の抜けも無くなる
- 必ずツールを呼ばせる設定は tool_choice（→ [tool_choice の設定](../02-tool-design-mcp/tool-choice.md)）

### 防げる誤り／防げない誤り

| 誤りの例 | tool use＋厳密なスキーマで | 拾う方法 |
|---|---|---|
| 閉じ括弧の抜けなど、JSON として壊れている | 防げる | — |
| 必須項目の抜け、型の違い（数値が文字列） | 防げる（strict のとき） | — |
| enum に無い値 | 防げる（大文字・小文字の違いは除く） | 大文字・小文字を無視して比べる。大文字・小文字だけが違う enum 値を作らない |
| 明細の合計が total と合わない | 防げない | アプリ側の計算チェック |
| 値が別の欄に入る（請求日と支払期限が逆） | 防げない | 検証＋プロンプトで欄の定義を明記 |
| 元の文書に無い値を作る | 防げない（必須にすると増える） | 任意・nullable にする（→ 別ノート: 抽出用スキーマの設計） |
| 書き方のばらつき（`2026/3/5` と `5 Mar 2026`） | 型だけでは決まらない | プロンプトに正規化のルールを書く |

### 例外: スキーマに合わない出力が返る場合
- `stop_reason: "max_tokens"`: 途中で切れる → `max_tokens` を増やして再実行
- `stop_reason: "refusal"`: 安全上の拒否が優先され、スキーマに合わないことがある

## 試験で問われそうなポイント
- JSON をテキストで返させたら、時々パースできない → プロンプトの工夫より、抽出ツールの input_schema（＋strict）に変える
- スキーマどおりなのに、合計や欄の対応がおかしい → スキーマを厳しくしても直らない。検証して、誤りを添えて再試行（→ 別ノート: 検証・再試行・フィードバックのループ）
- 文書ごとに日付や単位の書き方がばらばら → スキーマに加えて、プロンプトに「日付は YYYY-MM-DD」などの正規化ルールを書く
- 文書の種類が分からず抽出ツールが複数ある → tool_choice の any、特定の抽出を先に通す → tool（詳細は tool_choice のノート）

## 間違えやすいところ
- スキーマに従っているから値も正しい、と思い込む。保証されるのは形だけ
- 厳密なスキーマだけで形式をそろえようとする。`format: "date"`（strict でも対応）で形は縛れても、`03/05` が3月5日か5月3日かはスキーマでは決まらない。解釈のルールはプロンプトに書く
- 「必須にすれば抜けが無くなるから安全」は誤り。情報が無い文書では値を作ってしまう
- strict 無しでは何も保証されない。壊れた JSON（構文の誤り）も、型の違い（`"two"`）や必須項目の抜けも起こりうる（頻度は書かれていない）
- ガイドとのずれ: ガイドは「tool use＋JSON スキーマ」と書くが、現行ドキュメントでは同じ仕組み（constrained decoding）が structured outputs（`output_config.format`）と strict tool use の2つに分かれている
- ガイドとのずれ: 現行の define-tools では、Fable 5.2・Mythos 5.2・Opus 5.5・Sonnet 5.5・Fable 5.1・Mythos 5.1 は tool_choice の any / tool を 400 エラーで拒否し（Opus 5・Haiku 5.5 などは受け付ける）、auto＋strict tool use か structured outputs を勧める。試験はガイドの書き方で覚える
- モデルに関係なく、手動の extended thinking（`thinking: {type: "enabled"}`）と any / tool を併用するとエラーになる
- strict でも使えない JSON Schema の機能がある（`minimum` / `maximum`、`minLength` などは 400 エラー）。数値の範囲チェックもアプリ側の検証になる。SDK ヘルパーの多くは、使えない制約を外して description に書き足し、応答を検証するヘルパーなら元の制約で検証する

## 確認問題
1. 経費精算のレシートから `items`（品目と金額の配列）と `total` を抽出している。strict なツールにしてからパースエラーは無くなったが、品目の合計と total が食い違う結果が時々ある。スキーマに何を足せば防げるか?
   <details><summary>答え</summary>スキーマでは防げない。合計の一致は意味の誤りで、strict が保証するのは形（型・必須・enum）だけ。抽出後にアプリ側で合計を計算して比べ、食い違えば差を添えて再試行するか、人の確認に回す。</details>
2. 契約書の抽出で、`signed_date` に `2026年3月5日`、`03/05/26`、`5.3.2026` が混ざって届く。`"type": "string", "format": "date"` を付けた以外に何をするべきか?
   <details><summary>答え</summary>プロンプトに正規化ルール（YYYY-MM-DD に直す、`03/05/26` のような並びは月/日/年として読む、年が2桁なら20XX など）を書く。スキーマは出力の型を縛るだけで、元の書き方をどう解釈するかは決めない。</details>
3. 抽出結果を JSON のテキストで返すようプロンプトで頼んでいるが、1,000件に数件、末尾が切れたり引用符が崩れたりしてパースに失敗する。最も確実な改善は?
   <details><summary>答え</summary>抽出項目を input_schema にしたツールを定義し（strict: true）、tool_use の <code>input</code> を受け取る。構文の誤りが無くなる。ただし末尾が切れるのが <code>max_tokens</code> のせいなら、上限も見直す（その場合はスキーマに合わない出力になりうる）。</details>

## 出典
- [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)（公式）
- [Structured outputs — Invalid outputs / JSON Schema limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)（公式）
- [Define tools — Forcing tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use)（公式）
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)（公式。tool_use ブロックの `input`）
- Claude Certified Architect – Foundations Exam Guide v1.1、タスクステートメント 4.3・4.4（公式）
- 未確認: strict 無しの tool use で、JSON の構文そのものが壊れる頻度。ドキュメントは型の違い・必須の抜けの例を挙げるだけで、構文の誤りの発生率は書いていない
