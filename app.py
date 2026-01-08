import streamlit as st
from pathlib import Path
from utils.helpers import sanitize_filename, to_freedium_url
from utils.scraper import fetch_html, parse_article
from utils.qrcode_generator import generate_qr
import json
import markdown
import urllib.parse

# ================= Streamlit Config =================

st.set_page_config(page_title="🎨 Medium Scraper", layout="centered", page_icon="📰")

# ================= Styles =================

st.markdown(
    """
    <style>
    @keyframes rainbowText {
        0% {color:#ff0000;}
        14% {color:#ff7f00;}
        28% {color:#ffff00;}
        42% {color:#00ff00;}
        57% {color:#0000ff;}
        71% {color:#4b0082;}
        85% {color:#8f00ff;}
        100% {color:#ff0000;}
    }
    .rainbow { font-weight:bold; animation: rainbowText 5s infinite; }
    .stButton>button {
        background: linear-gradient(90deg,#ff7e5f,#feb47b);
        color:white;
        font-weight:bold;
        border-radius:10px;
        padding:10px 18px;
    }
    .markdown-card {
        background:#f0f8ff;
        padding:20px;
        border-radius:14px;
        box-shadow:0 4px 12px rgba(0,0,0,.12);
        margin-bottom:25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= Helpers =================


def article_to_html(article: dict) -> str:
    body_html = markdown.markdown(
        article["markdown"], extensions=["fenced_code", "tables"]
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{article['title']}</title>
<style>
body {{
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto;
    max-width: 800px;
    margin: 40px auto;
    line-height: 1.7;
    color: #222;
}}
img {{ max-width:100%; border-radius:8px; margin:20px 0; }}
pre {{ background:#f4f4f4; padding:15px; border-radius:8px; }}
code {{ background:#eee; padding:3px 6px; border-radius:4px; }}
.meta {{ color:#666; font-size:.9em; margin-bottom:30px; }}
</style>
</head>
<body>

<h1>{article['title']}</h1>
<div class="meta">
By {article['author']}<br>
Published: {article['date']}<br>
Source: <a href="{article['canonical']}">{article['canonical']}</a>
</div>

{body_html}

</body>
</html>"""


# ================= Header =================

st.markdown(
    '<h1 class="rainbow">📄 Medium Article Exporter</h1>', unsafe_allow_html=True
)
st.markdown(
    "<p style='color:#6a5acd;font-size:18px;'>"
    "Read, export & share Medium articles beautifully — HTML, QR & instant preview."
    "</p>",
    unsafe_allow_html=True,
)

st.info("📥 Files are generated temporarily. Download instantly — nothing is stored.")

# ================= Query Param Auto-load =================

params = st.query_params
url_from_qr = params.get("url", "")

url = st.text_input(
    "Enter Medium Article URL",
    value=url_from_qr or "",
    placeholder="https://medium.com/...",
)

TEMP_DIR = Path("_temp")
TEMP_DIR.mkdir(exist_ok=True)

# ================= Action =================

if st.button("✨ Scrape Article") or url_from_qr:
    if not url:
        st.warning("⚠️ Please enter a Medium article URL.")
    else:
        try:
            freedium_url = to_freedium_url(url)

            with st.spinner("Fetching article… ⏳"):
                html = fetch_html(freedium_url)
                article = parse_article(html, freedium_url)

            safe_title = sanitize_filename(article["title"])[:80]

            # ================= Preview =================
            st.markdown(
                f"""
                <div class="markdown-card">
                <h2 style="color:#ff6347;">{article["title"]}</h2>
                <p style="color:#20b2aa;">
                <i>By {article["author"]}</i><br>
                <i>Published: {article["date"]}</i>
                </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ================= HTML Download =================
            html_content = article_to_html(article)

            st.download_button(
                "🌐 Download HTML (Recommended)",
                data=html_content,
                file_name=f"{safe_title}.html",
                mime="text/html",
            )

            # ================= QR Code =================
            # Replace this with your Streamlit Cloud app URL
            base_url = "https://medium-unlocked.streamlit.app"
            share_url = f"{base_url}?url={urllib.parse.quote(url)}"

            qr_img = generate_qr(share_url)

            st.markdown("### 📱 Open on another device")
            st.image(qr_img, width=180)
            st.caption("Scan to open this article instantly")

        except Exception as e:
            st.error(f"❌ Error: {e}")
