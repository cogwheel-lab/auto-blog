#!/usr/bin/env python3
"""
ブログ自動生成スクリプト
src/ をスキャンしてフロントマターをパースし、posts/ にHTMLを生成

使い方:
    python3 build.py          # 記事ビルド（既存HTMLはスキップ）

※ index.htmlの更新には build_index.py を使用してください
"""

import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime

# 設定
SRC_DIR = Path("src")
POSTS_DIR = Path("posts")
TAGS_DIR = Path("tags")
TEMPLATE_FILE = Path("template/template.html")
STYLES_FILE = Path("assets/styles.css")
TAGS_JSON_FILE = Path("assets/tags.json")

# ビルドから除外する記事（slug名）
EXCLUDE_SLUGS = [
    "20260311-search-api-comparison",
    "20260311-leo-long-summary",
    "20260311-blog-ad-revenue-preparation"
]

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

    # 本文をHTMLに変換
    article_body, toc_items = markdown_to_html(body, slug)
    html = html.replace('{{ARTICLE_BODY}}', article_body.lstrip())
    html = html.replace('{{TOC_ITEMS}}', toc_items.lstrip())

    return html, tags

def markdown_to_html(body, slug):
    """MarkdownをHTMLに変換（簡易版）"""
    lines = body.split('\n')
    html_lines = []
    toc_items = []
    in_ul = False
    in_table = False
    in_pre = False
    table_rows = []

    for i, line in enumerate(lines):
        line = line.rstrip()
        
        # <pre>ブロックの開始・終了判定
        if '<pre>' in line:
            in_pre = True
        
        if in_pre:
            html_lines.append(f'                {line}')
            if '</pre>' in line:
                in_pre = False
            continue

        if not line:
            if in_ul:
                html_lines.append('                </ul>')
                in_ul = False
            if in_table:
                # テーブル終了
                html_lines.append('                <div class="table-container">')
                html_lines.append('                    <table>')
                # ヘッダー行
                if table_rows:
                    header_cells = [cell.strip().replace('**', '') for cell in table_rows[0].split('|')[1:-1]]
                    html_lines.append('                        <thead>')
                    html_lines.append('                            <tr>')
                    for cell in header_cells:
                        html_lines.append(f'                                <th>{cell}</th>')
                    html_lines.append('                            </tr>')
                    html_lines.append('                        </thead>')
                # データ行（2行目はセパレータなのでスキップ）
                html_lines.append('                        <tbody>')
                for row in table_rows[1:]:
                    # セパレータ行（---のみ）かチェック
                    stripped = row.replace('|', '').strip()
                    if not stripped or set(stripped).issubset(set('-: ')):
                        continue
                    cells = [cell.strip().replace('**', '') for cell in row.split('|')[1:-1]]
                    html_lines.append('                            <tr>')
                    for cell in cells:
                        html_lines.append(f'                                <td>{cell}</td>')
                    html_lines.append('                            </tr>')
                html_lines.append('                        </tbody>')
                html_lines.append('                    </table>')
                html_lines.append('                </div>')
                in_table = False
                table_rows = []
            continue

        # 見出し
        if line.startswith('## '):
            if in_ul:
                html_lines.append('                </ul>')
                in_ul = False
            text = line[3:]
            id = text.lower().replace(' ', '-').replace('：', '').replace('、', '')
            html_lines.append(f'                <h2 id="{id}">{text}</h2>')
            toc_items.append(f'                    <li><a href="#{id}">{text}</a></li>')
        elif line.startswith('### '):
            if in_ul:
                html_lines.append('                </ul>')
                in_ul = False
            text = line[4:]
            id = text.lower().replace(' ', '-').replace('：', '').replace('、', '')
            html_lines.append(f'                <h3 id="{id}">{text}</h3>')
            toc_items.append(f'                    <li><a href="#{id}">{text}</a></li>')
        # 箇条書き
        elif line.startswith('- '):
            if not in_ul:
                html_lines.append('                <ul>')
                in_ul = True
            text = line[2:]
            # Markdownの太字記号を削除
            text = text.replace('**', '')
            html_lines.append(f'                    <li>{text}</li>')
        # テーブル
        elif line.startswith('|'):
            if in_ul:
                html_lines.append('                </ul>')
                in_ul = False
            if not in_table:
                in_table = True
            table_rows.append(line)
        # 段落
        else:
            if in_ul:
                html_lines.append('                </ul>')
                in_ul = False
            # Markdownの太字記号を削除
            line = line.replace('**', '')
            html_lines.append(f'                <p>{line}</p>')

    # テーブルが閉じていない場合
    if in_table:
        html_lines.append('                <div class="table-container">')
        html_lines.append('                    <table>')
        if table_rows:
            header_cells = [cell.strip().replace('**', '') for cell in table_rows[0].split('|')[1:-1]]
            html_lines.append('                        <thead>')
            html_lines.append('                            <tr>')
            for cell in header_cells:
                html_lines.append(f'                                <th>{cell}</th>')
            html_lines.append('                            </tr>')
            html_lines.append('                        </thead>')
        html_lines.append('                        <tbody>')
        for row in table_rows[1:]:
            stripped = row.replace('|', '').strip()
            if not stripped or set(stripped).issubset(set('-: ')):
                continue
            cells = [cell.strip().replace('**', '') for cell in row.split('|')[1:-1]]
            html_lines.append('                            <tr>')
            for cell in cells:
                html_lines.append(f'                                <td>{cell}</td>')
            html_lines.append('                            </tr>')
        html_lines.append('                        </tbody>')
        html_lines.append('                    </table>')
        html_lines.append('                </div>')

    if in_ul:
        html_lines.append('                </ul>')

    article_body = '\n'.join(html_lines)
    toc_html = '\n'.join(toc_items) if toc_items else '                    <li><a href="#conclusion">結論</a></li>'
    return article_body, toc_html

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
    <title>タグ: {tag} | ゆるもくブログ</title>
    <link rel="stylesheet" href="../assets/styles.css">
    <link rel="icon" type="image/png" href="../assets/favicon.png">
</head>
<body>
    <div class="container">
        <header>
            <a href="../index.html"><div class="logo-space"></div></a>
            <div class="header-content">
                <h1>タグ: {tag}</h1>
            </div>
        </header>
    </div>

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

def extract_toc_from_html(html):
    """HTML内のh2, h3から目次を抽出"""
    toc_items = []
    # 簡易的な正規表現による抽出
    matches = re.finditer(r'<h([23])(?:\s+id="([^"]+)")?>(.*?)</h\1>', html, re.DOTALL)
    for match in matches:
        level, id_attr, text = match.groups()
        # idがない場合はテキストから生成
        if not id_attr:
            id_attr = text.lower().replace(' ', '-').replace('：', '').replace('、', '')
        toc_items.append(f'                    <li><a href="#{id_attr}">{text}</a></li>')
    
    return '\n'.join(toc_items) if toc_items else '                    <li><a href="#conclusion">結論</a></li>'

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
        # 除外リストに含まれていればスキップ
        if slug in EXCLUDE_SLUGS:
            continue
            
        source_md = item / 'source.md'
        source_html = item / 'source.html'
        
        if source_html.exists():
            # HTML源泉を優先
            with open(source_html, 'r', encoding='utf-8') as f:
                content = f.read()
            frontmatter, body = parse_frontmatter(content)
            if not frontmatter:
                print(f"Warning: {source_html} has no frontmatter, skipping")
                continue
            article_body = body.lstrip()
            toc_items = extract_toc_from_html(article_body)
        elif source_md.exists():
            # Markdown源泉
            with open(source_md, 'r', encoding='utf-8') as f:
                content = f.read()
            frontmatter, body = parse_frontmatter(content)
            if not frontmatter:
                print(f"Warning: {source_md} has no frontmatter, skipping")
                continue
            article_body, toc_items = markdown_to_html(body, slug)
        else:
            continue

        # 出力ファイル名（slug）を決定
        output_slug = frontmatter.get('slug', slug)
        
        # テンプレート置換
        title = frontmatter.get('title', '')
        date = frontmatter.get('date', '')
        category = frontmatter.get('category', '')
        tags = frontmatter.get('tags', '').split(',') if frontmatter.get('tags') else []

        html = template
        html = html.replace('{{記事タイトル}}', title)
        html = html.replace('{{YYYY年MM月DD日}}', date)
        html = html.replace('{{カテゴリ}}', category)
        html = html.replace('{{ARTICLE_BODY}}', article_body)
        html = html.replace('{{TOC_ITEMS}}', toc_items)

        # posts/ に保存
        output_file = POSTS_DIR / f'{output_slug}.html'
        # 既存HTMLがある場合の処理
        if output_file.exists():
            print(f"Skipped (already exists): {output_file}")
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(article_html)
            print(f"Generated: {output_file}")

        # タグデータを収集
        for tag in tags:
            tag = tag.strip()
            if tag not in tags_data['tags']:
                tags_data['tags'][tag] = []
            tags_data['tags'][tag].append(output_slug)

        # 記事データを収集
        tags_data['articles'][output_slug] = {
            'title': frontmatter.get('title', slug),
            'file': f'posts/{output_slug}.html',
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

    # index.htmlは build_index.py で生成する
    print("To update index.html, run: python3 build_index.py")

if __name__ == '__main__':
    main()
