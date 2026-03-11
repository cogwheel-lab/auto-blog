#!/usr/bin/env python3
"""
index.htmlのタイトルをsource.mdのフロントマターに同期する
"""

import re
from pathlib import Path

def extract_titles_from_index():
    """index.htmlからslugとtitleを抽出"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # <a href="./posts/{slug}.html"> と <h3>{title}</h3> を抽出
    pattern = r'<a href="\./posts/([^"]+)\.html">\s*<h3>([^<]+)</h3>'
    matches = re.findall(pattern, content)

    result = {}
    for slug, title in matches:
        # 【YYYY年M月】プレフィックスを除去
        clean_title = re.sub(r'^【\d{4}年\d+月】', '', title)
        result[slug] = clean_title

    return result

def update_frontmatter_title(source_file, new_title):
    """source.mdのフロントマターのtitleを更新"""
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # title:行を置換
    new_content = re.sub(
        r'^title:.*$',
        f'title: {new_title}',
        content,
        flags=re.MULTILINE
    )

    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    # index.htmlからタイトルを抽出
    titles = extract_titles_from_index()

    if not titles:
        print("No articles found in index.html")
        return

    print(f"Found {len(titles)} articles in index.html")

    # 各source.mdのフロントマターを更新
    updated_count = 0
    for slug, title in titles.items():
        source_file = Path(f'src/{slug}/source.md')
        if not source_file.exists():
            print(f"Warning: {source_file} not found, skipping")
            continue

        update_frontmatter_title(source_file, title)
        print(f"Updated: {slug} -> {title}")
        updated_count += 1

    print(f"\nDone! Updated {updated_count} source.md files")

if __name__ == '__main__':
    main()
