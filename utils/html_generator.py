import markdown


def article_to_html(article: dict) -> str:
    html_body = markdown.markdown(
        article["markdown"], extensions=["fenced_code", "tables"]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{article['title']}</title>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
    max-width: 800px;
    margin: 40px auto;
    line-height: 1.7;
    color: #222;
    padding: 0 20px;
}}
h1 {{ color: #ff6347; }}
.meta {{
    color: #666;
    font-size: 0.9em;
    margin-bottom: 30px;
}}
img {{
    max-width: 100%;
    border-radius: 8px;
    margin: 20px 0;
}}
pre {{
    background: #f4f4f4;
    padding: 15px;
    border-radius: 8px;
    overflow-x: auto;
}}
code {{
    background: #eee;
    padding: 3px 6px;
    border-radius: 4px;
}}
</style>
</head>
<body>

<h1>{article['title']}</h1>
<!--
<div class="meta">
    By {article['author']}<br>
    Published: {article['date']}<br>
    Source: <a href="{article['canonical']}">{article['canonical']}</a>
</div>
-->

{html_body}

</body>
</html>
"""
