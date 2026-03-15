import os
import re
import sys

articles_dir = "articles"
template_file = "index.template.html"
output_file = "index.html"

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

# Read template
if not os.path.exists(template_file):
    print(f"Template file {template_file} not found")
    sys.exit(1)

with open(template_file, "r", encoding="utf-8") as f:
    template = f.read()

# Build articles HTML
if len(articles) == 0:
    articles_html = '<li>No articles yet.</li>'
else:
    items = []
    for article in articles:
        items.append(f'<li><a href="{article["url"]}">{article["title"]}</a></li>')
    articles_html = '\n            '.join(items)

# Replace placeholder
output = template.replace('<!-- ARTICLES_PLACEHOLDER -->', articles_html)

# Write to index.html
with open(output_file, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Updated {output_file} with {len(articles)} articles")
