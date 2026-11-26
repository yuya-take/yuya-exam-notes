# デプロイ先と実行環境の選択

> ドメイン: 1. ソリューションの設計とアーキテクチャ（18%） ／ 更新: 2026-11-26

!!! abstract "ひとことで"
    デプロイ先（surface）で、推論を誰が運用しデータを誰が預かるかと、使える機能が決まる。実行環境（runtime）で、エージェントのループ・セッションの状態・サンドボックスを誰が持つかが決まる。==データの所在やコンプライアンスの制約が先に候補を絞り==、その代わりに機能の遅れや運用の負担を受け入れる。

## 仕組み

選ぶ順は、外せない制約から。データの所在（residency）や監査の義務で使えるデプロイ先が決まり、その中で必要な機能があるかを確かめ、最後に誰がループを運用するかを決める。クラウド事業者が推論を運用するデプロイ先は、データを自社のクラウドの境界に置ける。そのかわり、サーバー側のツールやエージェント基盤の機能が無いか、遅れて入る。

| デプロイ先 | 推論の運用者 | 機能の入り方 | 主に使えない機能 | Managed Agents |
|---|---|---|---|---|
| Anthropic API（Claude API） | Anthropic | 最も早い | — | ○（ベータ） |
| Amazon Bedrock | AWS（Anthropic の担当者は推論基盤に触れない） | Bedrock の予定に従う | Files API、サーバー側ツール（コード実行・Web 検索・Web 取得）、Agent Skills、MCP コネクタ、Message Batches | × |
| Google Vertex AI | Google（Agent Platform の一部） | 未確認 | Files API、コード実行、Web 取得、Agent Skills、MCP コネクタ、Message Batches（Web 検索は使える） | × |
| Microsoft Foundry | Anthropic（Azure 上か Anthropic 上かをデプロイごとに選ぶ） | 未確認 | Message Batches、Managed Agents。Azure 上では加えてコード実行・Agent Skills・Files API | × |

| 実行環境 | ループを持つ | セッションの状態 | サンドボックス | 使えるデプロイ先 |
|---|---|---|---|---|
| Messages API のループ | 自社のコード | 自社が保存する | 自社が用意する | すべて |
| Agent SDK / headless Claude Code（`claude -p`） | 自社のコンテナ内のサブプロセス | 既定でローカルディスク。残すなら `SessionStore` | 自社のコンテナ | Claude API、Bedrock、Google Cloud、Foundry |
| Claude Managed Agents | Anthropic | サーバー側に会話の履歴・サンドボックスの状態・成果物を保存 | セッションごとの専用コンテナ（Anthropic 運用）か、自社ホストのサンドボックス | Claude API と、Anthropic が運用する AWS・Google Cloud の提供形態のみ |

Managed Agents は、ループ・ツールの実行・サンドボックスを Anthropic が持つ、構築済みのエージェントの土台だ。長時間・非同期の作業に向き、セッションは止まっても再開できる。状態をサーバー側に持つ設計なので、==ZDR と HIPAA の対象外==になる（例外は、サービス全体を自社で動かす self-hosted Managed Agents の ZDR）。自社ホストのサンドボックスにしても、ファイルとプロセスが自社に残るだけで、会話の履歴とツールの結果は Anthropic に届く。

??? info "デプロイ先の細部（2026-11-26 時点）"
    - ガイドの「Google Vertex AI」は、現行ドキュメントの「Claude Models on Google Cloud (Google managed)」に当たる（推論。旧ページの URL がここに転送され、SDK のクライアント名が `AnthropicVertex`）
    - ドキュメントには、ガイドに名前の無い Anthropic 運用の提供形態もある。Claude Platform on AWS（AWS の認証と課金。新しいモデルは通常 Claude API と同日に出る。機能もほぼ同じだが、fast mode・HIPAA-ready・OAuth などの未対応の一覧がある）と、Claude Models on Google Cloud (Anthropic managed)。どちらも Managed Agents が使える。試験がこれらを扱うかは未確認
    - Claude Platform on AWS の Managed Agents は、利用者のイベント無しに自律で動けるのが6時間まで。HIPAA-ready の対象外で、FedRAMP High や HIPAA が要る組織には Bedrock を勧めている
    - サーバー側のフォールバック（`fallbacks`）は Bedrock・Google 管理版・Foundry で使えない。クライアント側のフォールバックで代える
    - データの所在: Claude API は `inference_geo`（`us` は 1.1 倍の料金、Claude 4.6 以降）。Bedrock と Google 管理版は地域のエンドポイント（グローバルより 10% 高い）。Foundry は Azure 上のデプロイで US Data Zone を選べる（1.1 倍）
    - デプロイ先ごとの遅延の差は、公式ドキュメントで確認できなかった（未確認）

??? info "Managed Agents の細部"
    - 構成要素は、エージェント（モデル・プロンプト・ツール・MCP・スキル。版を持つ）、環境（サンドボックスの設定）、セッション、イベント（SSE で受け取る）
    - 環境は複数のセッションで共有できるが、セッションごとに新しい Linux コンテナが割り当てられ、ファイルシステムは共有されない。環境は版を持たない
    - ネットワークは `limited`（許可したホストだけ）か `unrestricted`。API で省略すると `unrestricted` になる
    - 料金はトークン代と、セッションが `running` の間の実行時間（1時間 $0.08）。`idle` の間はかからない。バッチ割引は効かない
    - ベータで、ヘッダー `managed-agents-2026-04-01` が要る

## 試験での見分け方

<div class="vs" markdown>

| 問われること | ○ 正しい | × ひっかけ |
|---|---|---|
| データを自社クラウドの境界から出せない | クラウド事業者が運用するデプロイ先を選び、機能の遅れと自前の実行環境を受け入れる | ZDR の契約で所在の要件を満たしたことにする（ZDR は保持期間の話） |
| Bedrock でスキルやコード実行が要る | 機能の無いデプロイ先だと認め、デプロイ先か設計を変える | ベータヘッダーを足せば使えると考える |
| HIPAA の対象が要る長時間エージェント | 対象のデプロイ先で、自社ホストの Agent SDK を動かし、状態を自社で保存する | Managed Agents を使い、自社ホストのサンドボックスで対象にする |
| ループや状態を運用したくない | Managed Agents（使えるデプロイ先の上で） | どのデプロイ先でもホスト型の実行環境があると考える |

</div>

## 確認問題

**Q1.** 製造業の情報システム部門が、Microsoft Foundry に作った Claude のデプロイで、報告書を作るエージェントを動かしている。PDF の加工に Agent Skills とコード実行を使うようにしたところ、次のエラーが返った。推論を Azure の基盤の上で行う必要は無いと、法務の確認が取れている。最も適切な対応はどれか。（1つ選べ）
{ .quiz-q }

```text
POST https://example-resource.services.ai.azure.com/anthropic/v1/messages
model=claude-sonnet-5-5 (deployment: Hosted on Azure)
-> 400 Bad Request
```

<div class="quiz" data-answer="B" markdown>

- A. スキルとコード実行のベータヘッダーをリクエストに足して送り直す
- B. 同じモデルを「Hosted on Anthropic」でデプロイし直し、`model` に新しいデプロイ名を渡す
- C. Amazon Bedrock に移し、同じリクエストを `bedrock-runtime` で送る
- D. 一時的な障害とみなし、指数バックオフで再試行する

</div>

??? success "答えと解説"
    **正解: B。** Foundry の Azure 上のデプロイは、コード実行・Agent Skills・Files API を受け付けず、400 を返す仕様だ。Azure 上である必要が無いなら、Anthropic 上のデプロイに切り替える。

    - A: 機能がそのホストに無いので、ヘッダーでは使えない
    - C: Bedrock も Agent Skills とコード実行に対応していない
    - D: 仕様による拒否なので、再試行しても同じエラーになる

**Q2.** 医療系のスタートアップが、患者の記録を数日かけて整理する長時間のエージェントを作る。HIPAA の対象になる構成が必須で、作業は途中で止めて再開できなければならない。最も適切な構成はどれか。（1つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="C" markdown>

- A. Claude Managed Agents のクラウド環境で動かし、セッションの再開機能を使う
- B. Claude Managed Agents の自社ホストのサンドボックスで動かし、ファイルを自社に残す
- C. Agent SDK を自社のコンテナで動かし、HIPAA の対象になっている提供先のモデルを呼び、セッションの記録は `SessionStore` で自社の保管先に残す
- D. Claude Platform on AWS の Managed Agents で動かし、AWS の課金と認証で対象にする

</div>

??? success "答えと解説"
    **正解: C。** Managed Agents はサブ機能を含めて HIPAA の対象外なので、ループと状態を自社で持つ。Agent SDK の記録は既定でローカルディスクにあるので、再開のために `SessionStore` で残す。

    - A: Managed Agents は HIPAA の対象外
    - B: 自社ホストのサンドボックスでも、会話の履歴とツールの結果は Anthropic に届き、対象範囲は変わらない
    - D: Managed Agents が対象外なのは同じで、Claude Platform on AWS は HIPAA-ready の対象外でもある

**Q3.** 実行環境についての説明として正しいものはどれか。（2つ選べ）
{ .quiz-q }

<div class="quiz" data-answer="A,E" markdown>

- A. Managed Agents では、同じ環境を参照するセッション同士でも、それぞれ専用のコンテナを持ち、ファイルシステムを共有しない
- B. Managed Agents は Amazon Bedrock でも使え、その場合は AWS がデータの処理者になる
- C. Agent SDK を自前でホストすると、セッションの記録は既定でサービス側に残るので、コンテナを捨てても再開できる
- D. Managed Agents で自社ホストのサンドボックスを使えば、会話の履歴もツールの結果も Anthropic に届かない
- E. Managed Agents の実行時間の料金は `running` の間だけかかり、承認を待つ `idle` の間はかからない

</div>

??? success "答えと解説"
    **正解: A と E。** セッションごとに新しいコンテナが割り当てられる。実行時間は `running` の間だけ数える。

    - B: Bedrock では Managed Agents は使えない
    - C: 既定の記録はコンテナのローカルディスクにあり、再起動や縮退で消える
    - D: 自社に残るのはサンドボックスのファイルとプロセスで、履歴とツールの結果は Anthropic に届く

## 出典
- Claude Certified Architect – Professional Exam Guide v1.1, Domain 1「Deployment Surface and Agent Runtime Selection」（公式、PDF）: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946420/Claude_Certified_Architect_-_Professional_Exam_Guide_Updated_Dec_7.pdf
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)（公式）
- [Choosing an agent environment](https://platform.claude.com/docs/en/managed-agents/choosing-an-environment)（公式、Managed Agents）
- [Cloud environment setup](https://platform.claude.com/docs/en/managed-agents/environments)（公式、Managed Agents）
- [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock)（公式）
- [Claude on Amazon Bedrock (bedrock-runtime)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy)（公式）
- [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws)（公式）
- [Claude Models on Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/overview)（公式）
- [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/google-managed)（公式）
- [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry)（公式）
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（公式）
- [Hosting the Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting)（公式、Agent SDK）
- [Run Claude Code programmatically](https://code.claude.com/docs/en/headless)（公式、Claude Code）
