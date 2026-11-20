# CI での Claude Code の非対話実行と構造化出力

> ドメイン: 3. Claude Code の設定とワークフロー（20%） ／ 更新: 2026-11-20

## 3行まとめ
- CI では `claude -p`（`--print`、非対話モード（non-interactive mode））で動かす。対話画面を開かずに応答を出力する
- 結果をプログラムが読むなら `--output-format json` と `--json-schema` を組み合わせる。人がログで読むだけなら既定の `text` で足りる
- 決め手: 「止まらない」は `-p`、「パースできる」は `json` + `--json-schema`、「勝手に危ないことをしない」は `--allowedTools` / `--permission-mode`

## 仕組み

```mermaid
flowchart LR
  E[PR の作成・更新] --> J[CI のジョブ]
  J -->|差分を stdin で渡す| C["claude -p<br>--output-format json<br>--json-schema"]
  C --> O[JSON の structured_output]
  O -->|jq などで読む| P[PR にインラインコメントを投稿]
```

| フラグ | 役割 | CI での使いどころ |
|---|---|---|
| `-p` / `--print` | 非対話で実行して終わる | CI では必ず付ける |
| `--output-format` | `text` / `json` / `stream-json` を選ぶ | 後段のスクリプトが読むなら `json` |
| `--json-schema` | 出力を JSON Schema に合わせて検証する（print mode 専用） | 指摘を file・line・severity などの決まった形で受け取る |
| `--allowedTools` | 確認なしで使えるツールを決める（例: `"Bash(npm test *)"`） | 必要なツールだけ許す |
| `--permission-mode` | セッション全体の権限の基準（`dontAsk`、`acceptEdits` など） | `dontAsk`: 確認が要る呼び出しをすべて拒否。締めた CI 向け |
| `--max-turns` / `--max-budget-usd` | ターン数・推定費用の上限（どちらも print mode 専用） | 暴走と費用の歯止め |
| `--append-system-prompt(-file)` | 既定のシステムプロンプトに指示を足す | レビューの観点を足す |
| `--bare` | hooks・スキル・MCP・CLAUDE.md などの自動読み込みを省いて速く起動する | スクリプト向けに推奨。ただし CLAUDE.md も読まない |

| `--output-format` | 中身 | 向いている場面 |
|---|---|---|
| `text`（既定） | 回答の文章だけ | 人がログで読む |
| `json` | `result`（文章）、`session_id`、`total_cost_usd` など。`--json-schema` を付けると `structured_output` も入る | スクリプトで解析する |
| `stream-json` | 1行1イベントの JSON を順に出す（`--verbose` と一緒に使う） | 進み具合を逐次表示する |

```bash
gh pr diff "$PR" | claude -p "この差分の問題点を挙げて" \
  --output-format json --json-schema "$(cat findings.schema.json)" \
  --allowedTools "Read,Grep" --max-turns 10 > out.json
jq -e '.structured_output.findings' out.json   # 無ければ失敗させる
```

- GitHub Actions: `anthropics/claude-code-action@v1` に `prompt` を渡すと自動実行（automation mode）。CLI のフラグは `claude_args` で渡し、キーは `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}` のように secrets を参照する
- Action の `claude_args` に `--json-schema` を渡すと、全フィールドが1つの JSON 文字列としてアクションの出力 `structured_output` に入る。後続のステップは `fromJSON(steps.<id>.outputs.structured_output).<欄>` で読むか、`env:` で渡して jq で取り出す
- `${{ }}` をスクリプトに直接埋め込まない。引用符などでスクリプトが壊れたり、コマンドとして実行されたりするので `env:` 経由で渡す

## 試験で問われそうなポイント
- レビュー結果を PR のインラインコメントとして自動投稿したい → `--output-format json` + `--json-schema` で形を決め、`structured_output` を読む
- 後段が人だけ → `text`。進み具合を逐次出したい → `stream-json`
- CI で使うツールを絞りたい → `--allowedTools` で必要なものだけ許す。全部拒否が基準なら `--permission-mode dontAsk`
- CI に規約・テストの基準・レビューの観点を伝える → CLAUDE.md（使い方は → 別ノート ci-review-test-quality）
- 再レビューで重複コメントを避ける、既存テストを渡す、生成したセッションとは別のインスタンスでレビューする → 別ノート ci-review-test-quality

## 間違えやすいところ
- アンチパターン: `-p` を付けずに CI で `claude "..."` を実行する。対話モードで起動して入力待ちになり、ジョブがタイムアウトまで止まる
- アンチパターン: 自由な文章の出力を正規表現で切り出して PR コメントにする。形が揺れて壊れる。`--json-schema` で形を固定する
- `--output-format json` だけではスキーマは強制されない。文章は `result` の文字列のまま。決まった形は `--json-schema` を付けたときの `structured_output`
- `structured_output` が無いことがある（Claude が依頼を断ったときなど）。使う前に有無を確かめる
- 不正なスキーマは実行前に `Error: --json-schema is not a valid JSON Schema` で終わる（v2.1.329 で確かめた）。`format`（例: `email`）は注釈扱いで検証されない
- 終了コード: 成功は 0、失敗は 0 以外。ただし実行中の失敗（認証が無いなど）は stdout の結果として出る
- `-p` で許可していないツールは、入力待ちで止まるのではなく拒否される（v2.1.302 以降、`--permission-mode` や `permissions.defaultMode` で何も設定していなければ `-p` は Manual mode で始まる）。「何もせずに終わった」ときは許可を疑う
- `--bare` は CLAUDE.md も読まない。CLAUDE.md の規約を CI で効かせたいなら `--bare` を外すか、`--append-system-prompt-file` で渡す
- `-p` は信頼の確認ダイアログを出さない。プロジェクトの `.claude/settings.json` の hooks や `.mcp.json` のサーバーも動く
- ガイドに出てくるのは `-p`、`--output-format json`、`--json-schema` まで。`--bare` や `--permission-prompts none` は現行ドキュメントにある追加の仕組み

## 確認問題
1. 毎晩のジョブで、Claude に古くなった依存パッケージを調べさせ、後段のスクリプトがパッケージごとに issue を作る。出力の書き方が毎回少しずつ違い、スクリプトがよく失敗する。どう直すか
   <details><summary>答え</summary>`--output-format json` と、`packages`（name・current・latest を持つオブジェクトの配列）を必須にした `--json-schema` を付け、`structured_output.packages` を読む。読む前に `structured_output` があるかを確かめる。プロンプトで「JSON で答えて」と頼むだけでは形が保証されない。</details>
2. `claude -p "テストを実行して、失敗したら直して"` を CI で動かすと、ジョブは成功で終わるのに何も直っていない。ログにはテストのコマンドが拒否された記録がある。原因と直し方は
   <details><summary>答え</summary>`-p` では、許可していない確認の要る呼び出しは拒否されて先に進む。`--allowedTools "Bash(npm test *),Read,Edit"` のように、要るツールだけを許す。`bypassPermissions` で全部許すのは CI では広すぎる。</details>
3. 起動を速くするため CI に `--bare` を足したら、CLAUDE.md に書いたレビューの観点が無視されるようになった。なぜか、どうするか
   <details><summary>答え</summary>`--bare` は CLAUDE.md の自動読み込みも省く。`--bare` を外すか、観点を書いたファイルを `--append-system-prompt-file` で渡す。</details>

## 出典
- [Run Claude Code programmatically（Basic usage、Start faster with bare mode、Get structured output、Auto-approve tools）](https://code.claude.com/docs/en/headless)（公式）
- [CLI reference（CLI flags）](https://code.claude.com/docs/en/cli-reference)（公式）
- [Claude Code GitHub Actions（Interactive and automation modes、Pass CLI arguments）](https://code.claude.com/docs/en/github-actions)（公式）
- [claude-code-action docs/usage.md（Structured Outputs）](https://github.com/anthropics/claude-code-action/blob/main/docs/usage.md)（公式）
- [Claude Certified Architect – Foundations Exam Guide v1.1（Task Statement 3.6）](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf)（公式）
