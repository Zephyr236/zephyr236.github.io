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
        mjx-container { display: block !important; text-align: center !important; margin: 20px auto !important; }
    </style>'''

# Header and footer HTML
header_html = '''
    <header style="text-align: center; padding: 30px 0; margin-bottom: 30px;">
        <a href="index.html" class="site-title" style="font-family: 'Lora', Georgia, serif; font-size: 2.2em; color: #5d5d5d; text-decoration: none; letter-spacing: 2px;">Zephyr's Blog</a>
        <nav style="display: flex; justify-content: center; gap: 30px; margin-top: 20px;">
            <a href="../index.html" style="text-decoration: none; color: #8a7f7d;">Home</a>
            <a href="../about.html" style="text-decoration: none; color: #8a7f7d;">About</a>
        </nav>
    </header>
'''

footer_html = '''
    <footer style="margin-top: 60px; padding-top: 30px; border-top: 1px solid #e8e0d8; text-align: center; color: #a0908d; font-size: 0.85em;">
        <p>&copy; 2026 Zephyr. All rights reserved.</p>
    </footer>
'''

# Process HTML files in articles directory
articles = []
if os.path.exists(articles_dir):
    for filename in sorted(os.listdir(articles_dir)):
        if filename.endswith(".html"):
            filepath = os.path.join(articles_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title and date from filename (format: YYYY-MM-DD-title.html)
            # Or from the <title> tag if not in filename format
            date_match = re.search(r'^(\d{4}-\d{2}-\d{2})-(.+)\.html$', filename)
            if date_match:
                date_str = date_match.group(1)
                # Convert YYYY-MM-DD to "March 14, 2026" format
                from datetime import datetime
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    date_formatted = date_obj.strftime('%B %d, %Y')
                except:
                    date_formatted = date_str
                title_from_file = date_match.group(2).replace('-', ' ')
            else:
                date_formatted = ''
                title_from_file = os.path.splitext(filename)[0]

            # Use <title> tag if available, otherwise use filename
            title_match = re.search(r"<title>(.*?)</title>", content)
            title = title_match.group(1) if title_match else title_from_file

            articles.append({
                "title": title,
                "url": articles_dir + "/" + filename,
                "date": date_formatted
            })

            # Remove existing custom CSS and add fresh one
            # Remove old <link> and <style> tags added by our script
            content = re.sub(r'<link rel="stylesheet" href="assets/css/style.css">\s*<style>.*?</style>', '', content, flags=re.DOTALL)
            content = re.sub(r'<link rel="stylesheet" href="\.\./assets/css/style.css">\s*<style>.*?</style>', '', content, flags=re.DOTALL)

            # Remove old header and footer (our added ones)
            content = re.sub(r'<header style="text-align: center;.*?</header>', '', content, flags=re.DOTALL)
            content = re.sub(r'<footer style="margin-top:.*?</footer>', '', content, flags=re.DOTALL)

            # Add CSS if not present
            if 'href="assets/css/style.css"' not in content:
                content = content.replace("<head>", "<head>\n    " + css_style)
            else:
                content = content.replace('href="assets/css/style.css">', 'href="assets/css/style.css">\n    ' + css_style)

            # Add header before body content
            content = content.replace('<body>', '<body>\n' + header_html)

            # Add footer before closing body tag
            content = content.replace('</body>', footer_html + '\n</body>')

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
        if article["date"]:
            items.append(f'<li><span class="post-date">{article["date"]}</span><a href="{article["url"]}">{article["title"]}</a></li>')
        else:
            items.append(f'<li><a href="{article["url"]}">{article["title"]}</a></li>')
    articles_html = '\n            '.join(items)

# Replace placeholder
output = template.replace('<!-- ARTICLES_PLACEHOLDER -->', articles_html)

# Write to index.html
with open(output_file, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Updated {output_file} with {len(articles)} articles")
