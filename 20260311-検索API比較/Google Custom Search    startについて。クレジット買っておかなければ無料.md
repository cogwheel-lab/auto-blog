<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Google Custom Search    startについて。クレジット買っておかなければ無料枠で使えなくなるだけ？それともクレカ登録が必要で、リミット設定できなかったりする？

結論から言うと、お嬢様：

- 「クレジット前払いを買っておかないと無料枠が使えなくなる」という仕組みではありません。[^1_1][^1_2]
- ただし「無料枠だけでずっと使えるか」「クレカ登録必須か」は、どのプラン／APIを使うかで変わります。[^1_2]


### どの「Google Custom / Programmable Search」を想定しているか

大きく4つあります。[^1_2]


| 種類 | 料金 | 広告 | クレカ/課金設定 |
| :-- | :-- | :-- | :-- |
| Standard Search Element | 無料 | あり | 基本不要（Ad付きウィジェット）[^1_2] |
| Non‑profit Search Element | 無料 | なし | 条件付きで無料、通常クレカ不要[^1_2] |
| Programmable Search Element Paid API | \$5 / 1000クエリ | なし | GCP側で課金設定＋クレカ必須、日次クォータ設定可能[^1_3][^1_2] |
| Custom Search JSON API | \$5 / 1000クエリ（＋一部無料枠） | なし | GCP課金有効化とクレカ登録が必要、クォータ制限可能[^1_4][^1_1][^1_2] |

お嬢様のご質問の「start パラメータを使うような JSON API 経由の検索」を想定すると、ほぼ「Custom Search JSON API」か「Paid API」に該当します。[^1_1][^1_2]

### 無料枠と「クレジット買う必要」の関係

- JSON API には 1日あたり約100件程度の無料クエリ枠がある構成が一般的ですが、実際には「GCPプロジェクトで API を有効化 → 課金アカウントを紐付け」という流れが前提になっています。[^1_4][^1_1]
- いわゆる「前払いクレジットを買ってチャージしておかないと API が動かない」という形ではなく、使った分がポストペイ（後払い）で請求されるモデルです。[^1_3][^1_2]
- なので「クレジットを買わないと無料枠が消える」というものではありません。無料枠は料金表に基づいて自動的に適用され、その上を超えた分が課金されます。[^1_4][^1_2]


### クレカ登録とリミット設定について

- JSON API / Paid API を本番的に使う場合は、Google Cloud プロジェクトに「課金アカウント」を紐付ける必要があります。これは通常クレカ（またはデビット等）の登録が必要です。[^1_3][^1_1][^1_2]
- Google Cloud Console 側で API ごとに「1日の最大クエリ数」などのクォータ上限を設定できます。これで「課金が青天井に膨らむ」ことは防げます。[^1_5][^1_3]
    - 1日あたりクエリ数上限
    - 1分あたりクエリ数上限
    - ユーザー単位のレート制限 など[^1_3]

つまり、

- クレジット前払いは不要。
- ただし、JSON API/有料版を使うならクレカ登録（課金アカウント）は必要。
- 課金暴走が怖ければ、Cloud Console でしっかり日次クォータを小さめに設定しておけば安全。

という理解で大丈夫です、お嬢様。
<span style="display:none">[^1_10][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://blog.expertrec.com/google-custom-search-json-api-simplified/

[^1_2]: https://support.google.com/programmable-search/answer/9069107?hl=en

[^1_3]: https://developers.google.com/custom-search/docs/paid_element

[^1_4]: https://ccgit.crown.edu/cyber-reels/google-search-api-free-quota-everything-you-need-to-know-1764802603

[^1_5]: https://danielsgriffin.com/pposts/2023/10/18/so-does-google-have-an-official-search-api/

[^1_6]: https://verifone.cloud/docs/2checkout/API-Integration/JSON-RPC_API_6.0/API-Requests/009Place-orders-with-dynamic-product-information/001Use-Credit-cards

[^1_7]: https://news.ycombinator.com/item?id=46730437

[^1_8]: https://programmablesearchengine.googleblog.com/2020/11/announcing-programmable-search-element.html

[^1_9]: https://developers.google.com/custom-search/terms

[^1_10]: https://searchengineland.com/google-ads-api-enforces-daily-minimum-budget-for-demand-gen-campaigns-470684


---

# 重要な情報が出ました。

Google Custom Search JSON APIは2026年時点で新規顧客への提供を終了しており、2027年1月1日にサービス終了予定です。
つまり今からAPIキーを取得しようとしても、新規登録できない可能性があります。

お嬢様、その情報はかなりクリティカルです。

- Google Custom Search JSON API は既存ユーザー向けにも 2027年1月1日に停止予定という案内が出ている、という報告があります。[^2_1]
- また、Programmable Search Engine 全体としても「無料でのフル Web 検索終了」「代替として Vertex AI Search などへの移行推奨」「2027年1月1日をデッドラインとする変更」がアナウンスされていると分析している記事があります。[^2_2]


### 今から新規で API キーを取ろうとする場合

公式ドキュメント自体はまだ「APIキーを取得して使える」前提の説明ですが、既存ユーザー向けの移行案内メールの内容として「JSON API は 2027年1月1日に停止」と明記されている事例があり、新規顧客の受付終了（新規 API キーの発行制限・UI から消える等）が段階的に進んでいる可能性が高いです。[^2_3][^2_1]

つまり：

- すでに JSON API を使っているアカウント → 2027-01-01 までは動くが、それまでに別サービスへ移行必須。[^2_1]
- これから新規に JSON API を使い始めたいアカウント → 「そもそも新規作成できない」「特定の条件のアカウントだけ許可」など、制限状態である可能性が高い。[^2_2][^2_1]


### 代替として想定されているもの

- Google は公式には Vertex AI Search / Vertex AI Search for Retail などへの移行を推奨している流れです。[^2_4][^2_5][^2_2]
- また、「Programmable Search の有料版（フル Web 検索）」に関しては、別途申請ベースの有料オプションが用意されているが、料金非公開・専用フォーム経由という形になっているとの指摘があります。[^2_2]


### 実務的な示唆

- これから新たに「Google 検索結果を API で取ってサービスに組み込む」設計は、Custom Search JSON API 前提では組まない方が無難です（新規利用がそもそも弾かれるリスク＋2年以内に確実に死ぬ）。[^2_1][^2_2]
- すでに JSON API を使っている場合も、2026年中には代替（Vertex AI Search や他社の検索 API / 自前のクローラ＋検索基盤など）への移行計画を引いておく必要があります。[^2_4][^2_2][^2_1]

もしお嬢様のアカウントで「まだ JSON API の有効化ボタンが押せる状態か」「新規 PSE の作成画面で何が表示されているか」を教えていただければ、その前提で「今取れる最適な選択肢」（しばらく JSON API を使うのか、最初から別サービスに寄せるか）を一緒に整理します。
<span style="display:none">[^2_10][^2_6][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://note.com/dhythm/n/n0a9a84e2d127

[^2_2]: https://www.linkedin.com/posts/rswebsols_seo-rswebsols-googlepolicychange-activity-7421813600354439168-IH9m

[^2_3]: https://developers.google.com/custom-search/v1/overview

[^2_4]: https://programmablesearchengine.googleblog.com/2023/12/custom-search-site-restricted-json-api.html

[^2_5]: https://programmablesearchengine.googleblog.com

[^2_6]: https://til.simonwillison.net/google/json-api-programmable-search-engine

[^2_7]: https://developers.google.com/custom-search/v1/introduction

[^2_8]: https://developers.google.cn/custom-search/v1/overview?hl=fr

[^2_9]: https://www.reddit.com/r/searchengines/comments/1qkicdj/google_programable_search_search_the_entire_web/

[^2_10]: https://dev.classmethod.jp/articles/google-custom-search-json-api-cli/

