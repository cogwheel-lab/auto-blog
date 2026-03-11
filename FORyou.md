# Auto Blog プロジェクト解説

## これは何？

AIとの対話記録を、読みやすいブログ記事として自動生成するシステムです。

GeminiやClaudeなどで行った技術調査や作業メモを、ナレッジとして蓄積・公開するために作りました。

## 仕組み

```
あなたの作業メモ（AI対話）
    ↓
source.md にまとめる（フロントマター付き）
    ↓
python3 build.py を実行
    ↓
記事HTML と タグページ が自動生成
    ↓
python3 build_index.py を実行（index.html更新時のみ）
    ↓
index.html が生成
```

## ディレクトリ構成

```
auto-blog/
├── src/               # ここにMarkdownを置く
│   └── {slug}/
│       └── source.md  # フロントマター付きの記事本文
├── posts/             # ここにHTMLができる（自動生成）
├── tags/              # タグページができる（自動生成）
├── build.py           # 変換スクリプト
├── template.html      # 記事HTMLのテンプレート
└── styles.css         # 共通スタイル
```

## 新しい記事を追加する手順

1. `src/{YYYYMMDD-記事名}/` ディレクトリを作成
2. その中に `source.md` を作成
3. **AI対話ログから作る場合**：最初にフロントマターを追加すること
4. 以下の形式で書く：

```
<!--
title: 記事タイトル
tags: Python,API,WebScraping
date: 2026-03-11
category: 技術調査
-->

## 結論

結論の本文

## 何をしたかったか

- 目的
- 内容
```

4. `python3 build.py` を実行
5. `posts/` と `tags/` にHTMLが生成される
6. index.htmlを更新する場合は `python3 build_index.py` を実行

## フロントマターに書ける項目

| 項目 | 必須 | 説明 |
|------|------|------|
| title | ✅ | 記事タイトル |
| tags | ✅ | カンマ区切りのタグ（例: Python,API） |
| date | ✅ | 日付（YYYY-MM-DD形式） |
| category | - | カテゴリ名 |

## 自動生成されるもの

- `posts/{slug}.html` — 記事HTML
- `tags/{タグ名}.html` — タグ一覧ページ
- `assets/tags.json` — タグ管理用JSON
- `index.html` — トップページ（build_index.pyで生成）

## ビルドスクリプト

### build.py - 記事のビルド
新しい記事を追加したときに実行します。

```bash
python3 build.py
```

既存のHTMLはスキップされるので、安心して実行できます。

### build_index.py - トップページの生成
index.htmlを更新するときに実行します。手動で編集した内容は上書きされるので注意してください。

```bash
python3 build_index.py
```

## 記事の書き方ルール

各記事は以下の構造で書く（CLAUDE.md参照）：

1. 結論
2. 何をしたかったか
3. 分かったこと
4. 試したこと
5. 起きた問題

## 用語

- **slug**: 記事の識別子（ディレクトリ名）
- **フロントマター**: 記事の冒頭にあるメタデータ（`<!-- -->` で囲まれた部分）

## 注意点

- タグ名は英語推奨（URLになるため）
- 記事追加後は必ず `build.py` を実行（記事HTMLの生成）
- `source.md` の変更も `build.py` で反映
- index.htmlを更新するには `build_index.py` を実行

## 手動編集した記事をビルドから除外する方法

手動でHTMLを編集した記事など、ビルドで上書きされたくない場合は `build.py` の `EXCLUDE_SLUGS` にslug名を追加します。

## 手動編集した記事をgitの追跡から除外する方法

手動で編集したHTMLファイルをgitの変更検知から除外する場合：

```bash
git update-index --assume-unchanged posts/20260311-search-api-comparison.html
```

これでそのファイルの変更はgit diffに表示されなくなります。

```python
# ビルドから除外する記事（slug名）
EXCLUDE_SLUGS = ["20260311-search-api-comparison", "別のslug"]
```

slugはディレクトリ名のことです：
```
src/20260311-search-api-comparison/source.md
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     これがslug
```
