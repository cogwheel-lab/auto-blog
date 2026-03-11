<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# 日本語のWebページを大量収集する目的で、検索APIを比較したい。

## 前提条件

- 目的：日本のコーダー・Web制作パートナー募集ページを網羅的に収集
- 対象数：推定2,000〜3,000件
- 現状：DuckDuckGo Search（ddgs）を使っているが、オフセット指定ができないため同じ結果が返ってしまう


## 知りたいこと

1. ページネーション（オフセット）に対応している検索API一覧
2. 各APIの無料枠・料金
3. 日本語検索の精度・網羅性
4. レートリミットの有無と制限内容
5. Pythonからの利用のしやすさ

## 比較候補（知っているもの）

- Google Custom Search API（無料100件/日）
- Bing Web Search API
- Brave Search API
- SerpAPI
- Serper.dev

上記以外で見落としているAPIがあれば教えてほしい。

お嬢様、日本語Webページ（コーダー・Web制作募集）を大量収集するための検索APIを比較します。主な候補を表にまとめました。

## API比較表

| API | ページネーション | 無料枠 | 料金（超過分） | 日本語精度・網羅性 | レートリミット | Python利用しやすさ |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Google Custom Search | start (10単位オフセット) [^1_1] | 100件/日 [^1_2][^1_3] | \$5/1,000件 [^1_2] | 高 (日本語対応) [^1_4] | あり (日上限10,000) [^1_2] | 高 (公式ライブラリ) [^1_1] |
| Bing Web Search | offset (max 450程度) [^1_5] | 1,000件/月 (無料ティア) [^1_6] | 有料ティア変動 [^1_6] | 高 (日本語対応) [^1_5] | あり (ティア依存) [^1_6] | 高 (Azure SDK) [^1_5] |
| Brave Search | offset (max 9ページ) [^1_7] | \$5クレジット/月 (~1,000件) [^1_8] | \$5/1,000件 [^1_8] | 中 (日本語対応) [^1_7] | 1-50 QPS (ティア依存) [^1_9] | 高 (シンプルREST) [^1_7] |
| SerpAPI | start (Google等) [^1_4][^1_10] | 100件/月 [^1_11] | \$75/5,000件~ [^1_11] | 高 (Google/Bing/日本語) [^1_12] | 月額20%上限 [^1_13] | 高 (公式Pythonクライアント) [^1_4] |
| Serper.dev | あり (Googleベース) [^1_14] | 2,500クレジット [^1_14][^1_15] | \$50/50,000~ [^1_14] | 高 (Google/日本語) [^1_14] | 50-300 QPS [^1_14] | 高 (Python SDK) [^1_15] |

## その他の候補

- **Tavily Search API**: ページネーション対応、\$0.02~/検索 (無料トライアルなし)、AI向け日本語対応可、Python簡単 。[^1_16][^1_17]
- **Exa API**: ページネーション、\$10無料クレジット、\$5/1k検索、日本語対応、Python REST 。[^1_18][^1_19]
- Bright Data SERP API: 多エンジン（Naver/Yahoo JP）、有料中心、日本語高精度 。[^1_12]

2,000-3,000件収集にはSerper.devかSerpAPIが無料枠広くおすすめ。DuckDuckGo代替にBing/SerpAPIをPythonでoffsetループ実装を。[^1_11][^1_14]
<span style="display:none">[^1_20][^1_21][^1_22][^1_23][^1_24][^1_25][^1_26][^1_27][^1_28][^1_29][^1_30]</span>

<div align="center">⁂</div>

[^1_1]: https://stackoverflow.com/questions/73507286/how-can-i-paginate-my-items-using-custom-search-engine-api

[^1_2]: https://www.oreateai.com/blog/demystifying-google-custom-search-api-pricing-what-you-need-to-know/753e2c891aae2cb0fdbf8d878035a524

[^1_3]: https://junewallack.com/blog/google-search-api-free-limits

[^1_4]: https://serpapi.com/blog/serpapi-pagination/

[^1_5]: https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/page-results

[^1_6]: https://fetchserp.com/bing-search-api-key-limitations-and-quotas

[^1_7]: https://api-dashboard.search.brave.com/app/documentation/web-search/responses

[^1_8]: https://www.implicator.ai/brave-drops-free-search-api-tier-puts-all-developers-on-metered-billing/

[^1_9]: https://www.etavrian.com/news/brave-ai-grounding-api-pricing-metrics

[^1_10]: https://serpapi.com/pagination

[^1_11]: https://linkgo.dev/faq/the-pricing-structure-for-serpapi

[^1_12]: https://brightdata.jp/blog/ウェブデータ/best-serp-apis

[^1_13]: https://www.mattcollins.net/web-search-apis-for-llms

[^1_14]: https://www.buildmvpfast.com/tools/api-pricing-estimator/serper

[^1_15]: https://freeapihub.com/apis/serper-api

[^1_16]: https://www.buildmvpfast.com/tools/api-pricing-estimator/tavily

[^1_17]: https://apify.com/clearpath/tavily-search-api

[^1_18]: https://findmyaitool.io/tool/exa/

[^1_19]: https://exa.ai/pricing?tab=api

[^1_20]: https://semgrep.dev/docs/kb/integrations/pagination

[^1_21]: https://learn.microsoft.com/en-au/answers/questions/1382152/request-more-search-results-on-bing-api

[^1_22]: https://api-dashboard.search.brave.com/app/documentation/web-search/get-started

[^1_23]: https://serpapi.com/google-light-pagination

[^1_24]: https://docs.serverpod.dev/concepts/database/pagination

[^1_25]: https://stackoverflow.com/questions/28436862/bing-search-api-supports-multiple-request

[^1_26]: https://ja.developer.box.com/guides/search/pagination/

[^1_27]: https://developers.google.com/custom-search/docs/paid_element

[^1_28]: https://learn.microsoft.com/en-us/previous-versions/azure/cognitive-services/Bing-Web-Search/paging-search-results

[^1_29]: https://serpapi.com/blog/compare-serpapi-with-the-alternatives-serper-and-searchapi/

[^1_30]: https://aitools.smacient.com/tools/you-com

