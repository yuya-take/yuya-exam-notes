# yuya-exam-notes

資格試験の学習ノート。

| 資格 | ノート |
|---|---|
| Claude Certified Architect – Foundations | [ccaf/](ccaf/README.md) |

## 学習の流れ

1. `/exam-add <資格名>` で資格を追加 → `/exam-update` で公式情報を最新にする
2. 毎日 `/daily`（復習・新しい項目・小テストを30分に収めて進める）
3. まとめて進めたいときは `/orchestrate`（ノート作りを作業セッションに任せる）
4. 仕上げに `/mock-exam` → `/cheatsheet` → 受験 → `/exam-retro`

## スキル

| 分類 | コマンド | すること |
|---|---|---|
| 資格の管理 | `/exam-add <資格名> [受験予定日]` | 公式の試験ガイドを調べて、資格のディレクトリ（概要・ドメイン・チェックリスト・学習プラン）を作る |
| | `/exam-update [資格 or all]` | 公式情報（試験ガイドの版・形式・比重・出題項目・改訂予定）の変更を調べ、承認したものを反映する |
| | `/exam-retro` | 受験後の振り返り（守秘義務に触れない範囲）。合格なら更新期限、不合格なら学習プランを組み直す |
| 学ぶ | `/study <トピック or ドメイン番号>` | 公式ドキュメントで調べてノートにまとめ、チェックリストに紐付ける |
| | `/compare <A> vs <B>` | 混同しやすい概念の比較表と「どれを選ぶか」の判断の流れを作る |
| | `/hands-on [トピック]` / `/hands-on check <演習>` | 手を動かす演習を作り、成果を確かめて講評する |
| | `/glossary [update or 用語]` | 資格をまたいだ用語集を作る・引く |
| 確かめる | `/quiz [ドメイン番号 or トピック] [問題数]` | 本番形式の4択問題を1問ずつ出して採点・記録する |
| | `/quiz review` | 間違えた問題を、復習日が来たものから出し直す（1→3→7→14日） |
| | `/explain-back [トピック]` | 自分の言葉で説明して採点してもらう。誤解は復習に回る |
| | `/mock-exam [--half]` | 本番と同じ問題数・時間・配分の模擬試験。問題は出題前に別のエージェントが点検する |
| 続ける・仕上げる | `/daily [分]` | 今日の学習メニューを時間内に収めて組み、順に進める |
| | `/progress` | 進み具合・推定得点率・復習待ちを集計して、次にやることを示す |
| | `/cheatsheet` | 直前に読み返すまとめ（A4 4枚程度）を作る |
| | `/flashcards [ドメイン]` | Anki に取り込める暗記カード（CSV）を作る |
| 運用 | `/orchestrate <目標>` | このセッションを管理者にして、作業を1件ずつ作業セッションに任せる。成果物は別のエージェントが事実を確認してから統合する |
| | `/secret-check` | コミット・PR の前に、キー・個人情報・受験者 ID・本番問題の再現などが含まれていないかを調べる |
| | `/pr [タイトル]` | `/secret-check` とノートのチェックを通してから push し、PR を作る（対話中は作る前に確認） |
| | `/model-tune [モデル名]` | 新しい Claude モデルや Claude Code の仕様変更に合わせて、スキル・エージェント・設定を調整する |

## エージェントと自動のチェック

- **エージェント（`.claude/agents/`）:** `fact-checker`、`question-reviewer`、`exam-researcher`、`secret-reviewer`。どれも読むだけで、書いた本人とは別の目で確かめる役
- **フック:** Claude が `git commit` / `git push` するとき、機微情報をパターンで検査して止める
- **GitHub Actions:** PR と `main` への push で、機微情報の検査とノートのチェックを行う（Claude 以外のコミットも対象）

詳しい規則は [CLAUDE.md](https://github.com/yuya-take/yuya-exam-notes/blob/main/CLAUDE.md)。

ノートは GitHub Pages でも読める（`main` に入ると `.github/workflows/pages.yml` が MkDocs でサイトを作り直す）。
