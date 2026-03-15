import os
import re
import sys

articles_dir = "articles"
index_file = "index.html"

# CSS style to add to each article
css_style = '''<link rel="stylesheet" href="assets/css/style.css">
    <style>
        body { max-width: 800px; margin: 0 auto; padding: 40px 20px; background: linear-gradient(135deg, #fdfbf7 0%, #faf5f0 100%); min-height: 100vh; }
        h1, h2, h3 { font-family: 'Lora', Georgia, serif; color: #4a4a4a; }
        h1 { border-bottom: 2px solid #e8e0d8; padding-bottom: 0.4em; }
        h2 { border-bottom: 1px solid #e8e0d8; padding-bottom: 0.3em; }
        a { color: #b8a5a2; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        table th, table td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        table th { background-color: #f5efe9; }
        img { max-width: 100%; height: auto; }
        pre { background-color: #faf5f0; padding: 20px; border-radius: 8px; overflow-x: auto; border: 1px solid #e8e0d8; }
        code { background-color: #f5efe9; padding: 3px 8px; border-radius: 4px; }
        blockquote { border-left: 3px solid #d4c4c0; margin: 25px 0; padding: 15px 25px; background-color: #faf5f0; border-radius: 0 8px 8px 0; }
    </style>'''

# Process HTML files in articles directory
articles = []
if os.path.exists(articles_dir):
    for filename in sorted(os.listdir(articles_dir)):
        if filename.endswith(".html"):
            filepath = os.path.join(articles_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title
            title_match = re.search(r"<title>(.*?)</title>", content)
            title = title_match.group(1) if title_match else os.path.splitext(filename)[0]

            articles.append({
                "title": title,
                "url": articles_dir + "/" + filename
            })

            # Add CSS if not present
            if 'href="assets/css/style.css"' not in content:
                content = content.replace("<head>", "<head>\n    " + css_style)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Styled: {filepath}")

print(f"Found {len(articles)} articles")

# Update index.html
if not os.path.exists(index_file):
    print("index.html not found")
    sys.exit(1)

with open(index_file, "r", encoding="utf-8") as f:
    index_content = f.read()

# Find and replace the article list section
old_marker = '<ul class="post-list" id="typora-articles">'
end_marker = '</ul>'

if old_marker in index_content:
    # Find the start position
    start_pos = index_content.find(old_marker)
    # Find the end position
    end_pos = index_content.find(end_marker, start_pos) + len(end_marker)

    # Build new section
    if len(articles) == 0:
        new_section = old_marker + '\n            <li>No articles yet.</li>\n        ' + end_marker
    else:
        items = []
        for article in articles:
            items.append(f'            <li><a href="{article["url"]}">{article["title"]}</a></li>')
        new_section = old_marker + '\n' + '\n'.join(items) + '\n        ' + end_marker

    # Replace
    index_content = index_content[:start_pos] + new_section + index_content[end_pos:]

    with open(index_file, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"Updated index.html with {len(articles)} articles")
else:
    print("Could not find typora-articles section in index.html")
