#!/usr/bin/env python3
"""
index.html生成スクリプト
src/ をスキャンしてARTICLES_START〜END間だけを更新
"""

import re
from pathlib import Path

# 設定
SRC_DIR = Path("src")
INDEX_FILE = Path("index.html")
ARTICLES_START = "<!-- ARTICLES_START -->"
ARTICLES_END = "<!-- ARTICLES_END -->"

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

def generate_articles_html(articles):
    """記事リストのHTMLを生成"""
    articles_html = '        <ul class="article-list">\n'
    for article in articles:
        title = article['title']
        date = article['date']
        slug = article['slug']

        # タイトルに年月を付与
        if date and len(date) >= 7:
            year_month = f"【{date[:4]}年{date[5:7].lstrip('0')}月】"
            title = f"{year_month}{title}"

        articles_html += f'''            <li>
                <a href="./posts/{slug}.html">
                    <h3>{title}</h3>
                    <p class="meta">{date}</p>
                </a>
            </li>'''
    articles_html += '\n        </ul>'
    return articles_html

def generate_full_index(articles_html):
    """index.html全体を新規生成（ファイルが存在しない場合のみ）"""
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ゆるもくブログ</title>
    <link rel="stylesheet" href="./assets/styles.css">
    <link rel="icon" type="image/png" href="./assets/favicon.png">
</head>
<body>
    <div class="container">
        <header>
            <div class="logo-space"></div>
            <div class="header-content">
                <h1>ゆるもくブログ</h1>
            </div>
        </header>

        <h2>記事一覧</h2>
        {ARTICLES_START}
{articles_html}
        {ARTICLES_END}
    </div>

    <footer>
        <div class="container">
            <p>&copy; yurumoku</p>
        </div>
    </footer>
</body>
</html>'''

def main():
    # 先にsync_titles.pyを実行して、index.htmlの手動編集をsource.mdに反映
    import sync_titles
    sync_titles.main()

    # src/ をスキャン
    articles = []
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

        frontmatter, _ = parse_frontmatter(content)
        if not frontmatter:
            print(f"Warning: {source_file} has no frontmatter, skipping")
            continue

        # 出力ファイル名（slug）を決定
        output_slug = frontmatter.get('slug', slug)

        articles.append({
            'slug': output_slug,
            'title': frontmatter.get('title', slug),
            'date': frontmatter.get('date', ''),
        })

    # dateの降順でソート
    articles.sort(key=lambda x: x['date'], reverse=True)

    # 記事リストのHTMLを生成
    articles_html = generate_articles_html(articles)

    # index.htmlが存在する場合はマーカー間のみ置換
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # マーカーを確認
        if ARTICLES_START in content and ARTICLES_END in content:
            # マーカー間のみを置換
            pattern = rf'{re.escape(ARTICLES_START)}.*?{re.escape(ARTICLES_END)}'
            replacement = f'{ARTICLES_START}\n{articles_html}\n        {ARTICLES_END}'
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Updated: index.html (articles section only)")
        else:
            print("Warning: ARTICLES_START/END markers not found, regenerating full file")
            new_content = generate_full_index(articles_html)
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Generated: index.html (full)")
    else:
        # ファイルが存在しない場合は全体を新規生成
        new_content = generate_full_index(articles_html)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Generated: index.html (new file)")

if __name__ == '__main__':
    main()
