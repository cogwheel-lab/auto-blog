# Auto Blog

AIとの対話記録をブログ記事として自動生成するシステム。

## v1.1 アーキテクチャ

フロントマター付きMarkdownを自動変換して、HTML・タグページ・tags.jsonを生成する。

## ディレクトリ構成

```
auto-blog/
├── src/                    # ソースMarkdown（ここを編集）
│   └── {slug}/
│       └── source.md       # フロントマター付き記事本文
├── posts/                  # 生成済み記事HTML（build.pyが生成）
├── tags/                   # タグ一覧ページ（build.pyが生成）
│   └── {tagname}.html
├── build.py                # 自動生成スクリプト
├── tags.json               # タグ管理JSON（build.pyが生成）
├── template.html           # 記事HTMLテンプレート
├── styles.css              # 共通スタイル
├── CLAUDE.md               # AIへの指示（記事フォーマット等）
├── FORyou.md               # 人間向けプロジェクト解説
└── docs/
    ├── blog-structure.md   # 設計メモ
    └── tag管理法.md         # tags.json仕様
```

## ワークフロー

1. **記事作成**: `src/{slug}/source.md` にフロントマター付きMarkdownを書く
2. **ビルド**: `python3 build.py` を実行
3. **生成物**:
   - `posts/{slug}.html` — 記事HTML
   - `tags/{tagname}.html` — タグページ
   - `tags.json` — タグ管理JSON

## フロントマター仕様

```html
<!--
title: 記事タイトル
tags: Python,API,SerperDev
date: 2026-03-11
category: 技術調査
-->
```

### 必須フィールド

| フィールド | 説明 |
|-----------|------|
| title | 記事タイトル（HTMLのtitle, h1に使用） |
| tags | カンマ区切りのタグ（タグページ自動生成に使用） |
| date | YYYY-MM-DD形式 |

### 任意フィールド

| フィールド | 説明 |
|-----------|------|
| category | カテゴリ（メタ情報表示に使用） |
| images | 画像ファイル情報（未実装） |

## build.py の処理

1. `src/` をスキャン
2. `source.md` のフロントマターをパース
3. `template.html` に本文を埋め込み、`posts/` に出力
4. タグ情報を集約して `tags.json` を更新
5. `tags/{tagname}.html` を生成

## 記事フォーマット（CLAUDE.md）

各記事は以下の構造:

- 結論
- 何をしたかったか
- 分かったこと
- 試したこと
- 起きた問題

## 技術スタック

- **HTML/CSS**: 純粋なHTML + CSS（レスポンシブ、CSS Grid/Flexbox）
- **ビルド**: Python 3
- **ホスティング**: Cloudflare Pages想定

## 記事追加手順

```bash
# 1. ディレクトリ作成
mkdir -p "src/20260311-新しい記事"

# 2. source.md 作成（フロントマター付き）
# 3. ビルド実行
python3 build.py
```

## 配信先

| 媒体 | 用途 | 備考 |
|------|------|------|
| 自分のサイト（Cloudflare Pages） | メイン | `posts/` のHTMLを使用 |
| はてなブログ | 流入・拡散 | 内容を変える（要約版） |
| note | 有料販売 | 深掘り版 |
