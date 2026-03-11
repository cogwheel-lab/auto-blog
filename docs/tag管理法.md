# tags.json 設計仕様

## 目的

自分のサイト（Cloudflare Pages）の記事タグを一元管理する。
タグページ（/tags/python.html 等）の自動生成に使う。

## ファイル構造

```json
{
  "tags": {
    "Python": ["api-comparison", "scraping-basics"],
    "API": ["api-comparison"],
    "SerperDev": ["api-comparison"]
  },
  "articles": {
    "api-comparison": {
      "title": "検索API比較：Webページ大量収集におけるオフセット制約の克服",
      "file": "api-comparison.html",
      "date": "2026-03-11",
      "tags": ["Python", "API", "SerperDev"]
    }
  }
}
```

## 運用ルール

- 記事のslugはファイル名から拡張子を除いたもの
- タグ名は英語・日本語どちらでもよいが混在させない
- 記事追加のたびに両方のキー（tags・articles）を更新する

## タグページ生成

tags.jsonを読み込み、タグごとにHTMLを生成して `/tags/{タグ名}.html` に出力する。

## 生成するタグページの構造

- タグ名の見出し
- そのタグを持つ記事の一覧（タイトル・日付・リンク）
