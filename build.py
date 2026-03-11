#!/usr/bin/env python3
"""
ブログ自動生成スクリプト
src/ をスキャンしてフロントマターをパースし、posts/ にHTMLを生成
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 設定
SRC_DIR = Path("src")
POSTS_DIR = Path("posts")
TAGS_DIR = Path("tags")
TEMPLATE_FILE = Path("template.html")
STYLES_FILE = Path("styles.css")
TAGS_JSON_FILE = Path("tags.json")

# ディレクトリ作成
POSTS_DIR.mkdir(exist_ok=True)
TAGS_DIR.mkdir(exist_ok=True)

def parse_frontmatter(content):
    """フロントマターをパース"""
    match = re.match(r'^<!--\n(.*?)-->\n(.*)$', content, re.DOTALL)
    if not match:
        return None, content

    fm_text, body = match.groups()
    frontmatter = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, body

def read_template():
    """テンプレートを読み込み"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def generate_article_html(slug, frontmatter, body, template):
    """記事HTMLを生成"""
    title = frontmatter.get('title', '')
    date = frontmatter.get('date', '')
    category = frontmatter.get('category', '')
    tags = frontmatter.get('tags', '').split(',') if frontmatter.get('tags') else []

    # テンプレート置換
    html = template
    html = html.replace('{{記事タイトル}}', title)
    html = html.replace('{{YYYY年MM月DD日}}', date)
    html = html.replace('{{カテゴリ}}', category)
    html = html.replace('{{YYYY}}', date[:4])

    # 本文をHTMLに変換
    article_body = markdown_to_html(body, slug)
    html = html.replace('                <h2 id="conclusion">結論</h2>\n                <p>{{結論の内容}}</p>', article_body)

    # タグを更新
    tag_html = '\n                '.join([f'<span class="tag">#{tag.strip()}</span>' for tag in tags])
    html = html.replace('                <span class="tag">#{{タグ1}}</span>\n                <span class="tag">#{{タグ2}}</span>\n                <span class="tag">#{{タグ3}}</span>', tag_html)

    return html, tags

def markdown_to_html(body, slug):
    """MarkdownをHTMLに変換（簡易版）"""
    lines = body.split('\n')
    html_lines = []
    in_ul = False

    for line in lines:
        line = line.rstrip()
        if not line:
            if in_ul:
                html_lines.append('            </ul>')
                in_ul = False
            continue

        # 見出し
        if line.startswith('## '):
            if in_ul:
                html_lines.append('            </ul>')
                in_ul = False
            text = line[3:]
            id = text.lower().replace(' ', '-').replace('：', '').replace('、', '')
            html_lines.append(f'                <h2 id="{id}">{text}</h2>')
        elif line.startswith('### '):
            if in_ul:
                html_lines.append('            </ul>')
                in_ul = False
            text = line[4:]
            html_lines.append(f'                <h3>{text}</h3>')
        # 箇条書き
        elif line.startswith('- '):
            if not in_ul:
                html_lines.append('            <ul>')
                in_ul = True
            text = line[2:]
            html_lines.append(f'                <li>{text}</li>')
        # テーブル（簡易対応）
        elif line.startswith('|'):
            pass  # TODO: テーブル対応
        # 段落
        else:
            if in_ul:
                html_lines.append('            </ul>')
                in_ul = False
            html_lines.append(f'                <p>{line}</p>')

    if in_ul:
        html_lines.append('            </ul>')

    return '\n'.join(html_lines)

def generate_tag_pages(tags_data):
    """タグページを生成"""
    for tag, slugs in tags_data.items():
        articles_html = []
        for slug in slugs:
            article_info = tags_data.get('_articles', {}).get(slug, {})
            title = article_info.get('title', slug)
            date = article_info.get('date', '')
            file = article_info.get('file', f'{slug}.html')
            articles_html.append(f'''
            <li>
                <a href="../{file}">
                    <h3>{title}</h3>
                    <p class="meta">{date}</p>
                </a>
            </li>''')

        tag_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タグ: {tag} | Tech Blog</title>
    <link rel="stylesheet" href="../styles.css">
    <link rel="icon" type="image/png" href="../assets/favicon.png">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo-space"></div>
            <div class="header-content">
                <h1>タグ: {tag}</h1>
            </div>
        </div>
    </header>

    <div class="container">
        <ul class="article-list">
{''.join(articles_html)}
        </ul>
    </div>

    <footer>
        <div class="container">
            <p>&copy; yurumoku</p>
        </div>
    </footer>
</body>
</html>'''

        with open(TAGS_DIR / f'{tag}.html', 'w', encoding='utf-8') as f:
            f.write(tag_html)

def main():
    # テンプレート読み込み
    template = read_template()

    # データ収集
    tags_data = {'tags': {}, 'articles': {}}

    # src/ をスキャン
    for item in SRC_DIR.iterdir():
        if not item.is_dir():
            continue

        slug = item.name
        source_file = item / 'source.md'
        if not source_file.exists():
            continue

        # フロントマターをパース
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter, body = parse_frontmatter(content)
        if not frontmatter:
            print(f"Warning: {source_file} has no frontmatter, skipping")
            continue

        # 記事HTMLを生成
        article_html, tags = generate_article_html(slug, frontmatter, body, template)

        # posts/ に保存
        output_file = POSTS_DIR / f'{slug}.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(article_html)
        print(f"Generated: {output_file}")

        # タグデータを収集
        for tag in tags:
            tag = tag.strip()
            if tag not in tags_data['tags']:
                tags_data['tags'][tag] = []
            tags_data['tags'][tag].append(slug)

        # 記事データを収集
        tags_data['articles'][slug] = {
            'title': frontmatter.get('title', slug),
            'file': f'posts/{slug}.html',
            'date': frontmatter.get('date', ''),
            'category': frontmatter.get('category', ''),
            'tags': [t.strip() for t in tags]
        }

    # tags.json を保存
    with open(TAGS_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(tags_data, f, ensure_ascii=False, indent=2)
    print(f"Generated: {TAGS_JSON_FILE}")

    # タグページを生成
    tags_data_with_articles = tags_data.copy()
    tags_data_with_articles['_articles'] = tags_data['articles']
    generate_tag_pages(tags_data['tags'])
    print(f"Generated tag pages in {TAGS_DIR}/")

if __name__ == '__main__':
    main()
