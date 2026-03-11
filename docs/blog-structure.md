# ブログ ディレクトリ構成・設計メモ

## ディレクトリ構成

```
/
├── styles.css
├── template.html
├── index.html
├── tags/
│   └── {タグ名}.html        # タグ一覧ページ（自動生成）
├── posts/
│   └── {slug}.html          # 生成済み記事HTML（自動生成）
└── src/
    └── {slug}/
        ├── source.md        # 元メモ
        └── images/
            └── {リネーム済みスクショ}
```

---

## フロントマター仕様

各記事HTMLの冒頭にコメントとして埋め込む。

```html
<!--
title: 検索API比較
tags: Python,API,SerperDev
date: 2026-03-11
images:
  - file: serper-result.png
    alt: Serper.devの検索結果
-->
```

---

## tags.json 構造

スクリプトがフロントマターをパースして自動生成する。

```json
{
  "tags": {
    "Python": ["20260311-検索API比較"],
    "API": ["20260311-検索API比較"]
  },
  "articles": {
    "20260311-検索API比較": {
      "title": "検索API比較：Webページ大量収集におけるオフセット制約の克服",
      "file": "posts/20260311-検索API比較.html",
      "date": "2026-03-11",
      "tags": ["Python", "API", "SerperDev"]
    }
  }
}
```

---

## スクリプトの役割

- `src/` をスキャンしてフロントマターをパース
- `posts/` に記事HTMLを生成
- `images/` を `posts/` 以下にコピー
- `tags.json` を更新
- `tags/` 以下のタグページを生成

---

## 画像運用

- スクショは手動で `src/{slug}/images/` に移動
- ファイル名はAIがリネーム（フロントマターにファイル名とaltをセットで記載）

---

## 配信・展開方針

| 媒体 | 用途 | 備考 |
|---|---|---|
| 自分のサイト（Cloudflare Pages） | メイン・AdSense | フル記事 |
| はてなブログ | 流入・拡散 | 内容を変える（要約版等） |
| note | 有料販売・自サイト誘導 | 深掘り版 |

同一文章の重複掲載はインデックス評価が下がるため、媒体ごとに内容を変える。
