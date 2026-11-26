# コンテキストの構成とトークンの経済性

> ドメイン: 2. モデル・プロンプト・コンテキストエンジニアリング（13%） ／ 更新: 2026-11-26

!!! abstract "ひとことで"
    1回の呼び出しを「固定の前置き」「毎回変わる入力」「たまっていく履歴」「出力」に分け、==1回あたりの量 × 呼び出し回数==で大きいところから削る。削ってよいのは、その課題に要らない部分だけだ。

## 仕組み

まず内訳を数字で取る。応答の `usage` を集計すれば、キャッシュに書いた量、読んだ量、キャッシュ対象外の入力、出力が分かる。tools や system の大きさは、トークン数を数えるエンドポイントで事前に測れる。内訳に呼び出し回数を掛けると、どこに予算が消えているかが見える。1回では小さな部分も、毎回送れば大きくなる。

減らし方は部分ごとに違う。使わないツールの定義は、tool search の `defer_loading` で必要になるまでコンテキストに入れない。ツールの結果は、要る項目や範囲だけを返す形にし、古い結果は context editing で消す。大きな資料は最初に全部入れず、参照（パスや ID）を渡して必要なときに読ませる。トークンを減らすことは費用だけの話ではない。公式のエンジニアリングブログは、コンテキストが埋まるほど想起の精度が落ちる（context rot）と書いている。

| 部分 | 典型的な肥大 | 情報を失わない削り方 | 削りすぎの例 |
|---|---|---|---|
| tools | 複数の MCP サーバーのツール定義を全部載せる | tool search と `defer_loading`、よく使う3〜5個だけ常に載せる | 必要なツールまで外し、検索で見つからなくする |
| system・例 | 古い規則や重複した例が残る | 重複を消す。残りはキャッシュする | 判断に要る規則まで消す |
| 検索した資料 | 上位20件を毎回まるごと入れる | 要る件数を評価で決める。参照だけ渡して後で読ませる | 1件に絞り、答えの根拠が抜ける |
| 履歴 | ファイル全文やログのツール結果がたまる | 結果を要る範囲だけ返す。古い結果は context editing で消す | まだ使う直近の結果まで消す |
| 出力 | 前置きや冗長な説明 | 長さはプロンプトで指定し、effort で推論量を絞る | `max_tokens` を削って途中で切れさせる |

キャッシュは「量」ではなく「単価」を下げる手段だ。毎回同じ前置きを送ること自体は変わらないが、読み込みの単価は基本料金の1割以下になる。だから、大きく固定された前置きはキャッシュし、変わる部分と履歴は量を削る、と役割を分けて考える。急がない大量処理なら、Message Batches API で入出力とも半額にできる。

??? info "数え方と数字（2026-11-26 に公式で確認）"
    - `usage` の入力の合計は `cache_read_input_tokens + cache_creation_input_tokens + input_tokens`。`input_tokens` は最後のブレークポイントより後ろの、キャッシュ対象外の分だけ
    - thinking は出力として課金される。要約された thinking が見えても、課金は生成した全量。内訳は `usage.output_tokens_details.thinking_tokens` で見る
    - ツールを1つでも渡すと、ツール利用用の system が自動で付く（Opus 5.5・Sonnet 5.5・Haiku 5.5 で 286 トークン）。text editor ツールの定義は、Claude 4.7 以降で 974 トークン
    - tool search の目安: ツールが10個以上、定義が 10k トークン超、MCP サーバーを束ねて 200 個以上。5つの MCP サーバーで定義が約 55k トークンになる例があり、tool search で通常 85% 以上減る。ツールが 30〜50 個を超えると選択の精度が落ちる
    - `defer_loading: true` のツールには `cache_control` を付けられない（400 エラー）
    - Claude 4.7 以降のトークナイザーは、同じ文章で約 30% 多くトークンを数える。文字数からの概算は当てにならない
    - Haiku 5.5 は、キャッシュの読み込みを含むプロンプトが 100,000 トークンを超えると、そのリクエストは高い単価になる
    - Message Batches API は入力・出力とも 50% 引きで、キャッシュの割引とも重ねられる

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| どこから削るか | 1回の量 × 回数で最大の部分から | 目についた system の文章から削る |
| ツール定義が大きい | tool search と `defer_loading` で必要なときだけ載せる | 全ツールを毎回載せたまま、説明文だけ短くする |
| 長い作業で履歴が膨らむ | 結果を要る範囲で返し、古い結果を context editing で消す | もっと大きなコンテキストのモデルに替える（劣化は残る） |
| 費用を下げる | 固定の前置きはキャッシュ、変わる部分は量を削る | 変わる資料を system に入れてキャッシュを狙う |
| 内訳の把握 | `usage` の各項目と、トークン数を数えるエンドポイント | 文字数を4で割って全モデル共通で見積もる |

</div>

## 確認問題

**Q1.** 社内文書を検索するエージェントが1日 20万回呼ばれる。キャッシュはまだ使っていない。1回あたりの入力の内訳は次のとおり。課題に要る情報を失わずに、コンテキストに入るトークンを最も大きく減らせる変更はどれか。（1つ選べ）
{ .quiz-q }

```text
tools      18,000  （3つの MCP サーバーの42ツール。1回で使うのは平均4つ）
system      3,000  （回答の方針と、引用の書き方）
検索結果     6,000  （上位5件。答えの根拠に2〜3件を使う）
履歴        2,000
出力          600
```

<div class="quiz" data-answer="A" markdown>

- A. tool search を入れて大半のツールを `defer_loading: true` にし、よく使う数個だけ常に載せる
- B. system から引用の書き方の節を消し、1,000 トークンに縮める
- C. 検索結果を上位1件だけに絞り、6,000 トークンを約 1,200 にする
- D. `max_tokens` を 300 にして、出力を半分にする

</div>

??? success "答えと解説"
    **正解: A。** 最大の部分は tools で、使わない定義を載せなくても情報は失わない。

    - B: 減る量が小さいうえ、要る規則を失う
    - C: 根拠に2〜3件を使うので、課題に要る情報を失う
    - D: 出力はもともと小さい。途中で切れる応答も生む

**Q2.** コーディングエージェントのトレースで、ファイルを読むたびに全文 8,000 トークンがツール結果として履歴に残り、30ターン目には入力が 180,000 トークンに達している。後半ほど、前に読んだファイルの取り違えが増えた。ファイルはいつでも読み直せる。最も適切な対応はどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="C" markdown>

- A. コンテキストウィンドウの大きなモデルに替え、上限に余裕を持たせる
- B. ツール結果を返す前に、別のモデル呼び出しで毎回要約してから履歴に入れる
- C. 読み込みは要る行の範囲だけ返す形にし、古いツール結果は context editing で消して直近だけ残す
- D. 読んだファイルの内容を system に移し、キャッシュで安くする

</div>

??? success "答えと解説"
    **正解: C。** 読み直せる結果は残す必要が無い。量を減らせば、劣化も費用も下がる。

    - A: 上限は延びても、埋まるほど精度が落ちる問題は残る
    - B: 呼び出しが毎回1つ増え、要約で行番号などの細部が落ちる
    - D: system が毎回変わり、キャッシュは当たらない。量も減らない

**Q3.** 文書要約パイプラインの月額が想定を超えた。どこでトークンが消えているかを正しく把握する方法として適切なものはどれか。（2つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="A,B" markdown>

- A. 応答の `usage` から、キャッシュの書き込み・読み込み・それ以外の入力・出力を集計し、部分ごとの量と回数を見る
- B. tools や system の大きさを、トークン数を数えるエンドポイントで対象のモデルを指定して測る
- C. 文字数を4で割ってトークン数とし、どのモデルでも同じ見積もりを使う
- D. 応答に見えている thinking の要約の長さを、thinking の課金量として扱う
- E. `usage.input_tokens` を、そのリクエストの入力の合計として扱う

</div>

??? success "答えと解説"
    **正解: A と B。** 実際の `usage` と、モデルを指定した事前の計測が当てになる。

    - C: トークナイザーはモデルで違い、Claude 4.7 以降は同じ文章で約 30% 多い
    - D: 課金は生成した thinking の全量で、見える要約とは一致しない
    - E: `input_tokens` は最後のブレークポイントより後ろの分だけで、キャッシュ分を含まない

## 出典
- Claude Certified Architect – Professional Exam Guide v1.1（Dec 7 版）, Domain 2「Context Composition and Token Economics」（公式、PDF）: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946420/Claude_Certified_Architect_-_Professional_Exam_Guide_Updated_Dec_7.pdf
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（公式、エンジニアリングブログ）
- [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)（公式）
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)（公式）
- [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)（公式）
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（公式）
- [Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)（公式）
