import streamlit as st
from pathlib import Path
from utils.helpers import sanitize_filename, to_freedium_url
from utils.scraper import fetch_html, parse_article
import json

# ================= Streamlit App =================

st.set_page_config(page_title="🎨 Medium Scraper", layout="centered", page_icon="📰")

st.markdown(
    """
    <style>
    /* Title animation */
    @keyframes rainbowText {
        0% {color: #ff0000;}
        14% {color: #ff7f00;}
        28% {color: #ffff00;}
        42% {color: #00ff00;}
        57% {color: #0000ff;}
        71% {color: #4b0082;}
        85% {color: #8f00ff;}
        100% {color: #ff0000;}
    }
    .rainbow { font-weight: bold; animation: rainbowText 5s infinite; }
    .stButton>button {background: linear-gradient(90deg, #ff7e5f, #feb47b); color:white; font-weight:bold; border-radius:10px; padding:10px; transition: transform 0.2s;}
    .stButton>button:hover {transform: scale(1.05); box-shadow:0px 4px 15px rgba(0,0,0,0.2);}
    .markdown-card {background:#f0f8ff; padding:15px; border-radius:12px; box-shadow:0px 4px 12px rgba(0,0,0,0.1); margin-bottom:20px; transition: transform 0.2s;}
    .markdown-card:hover {transform: scale(1.01);}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="rainbow">📄 Medium Articles Scraper</h1>', unsafe_allow_html=True
)
st.markdown(
    "<p style='color: #6a5acd; font-size: 18px;'>Scrape Medium articles and save them as Markdown and JSON with style and animations!</p>",
    unsafe_allow_html=True,
)

# Input
url = st.text_input("Enter Medium Article URL:", placeholder="https://medium.com/...")
output_dir = st.text_input(
    "Output folder (optional, default: scraped_articles):", "scraped_articles"
)

if st.button("✨ Scrape Article"):
    if not url:
        st.warning("⚠️ Please enter a URL first!")
    else:
        try:
            freedium_url = to_freedium_url(url)
            with st.spinner("Fetching the article... ⏳"):
                html = fetch_html(freedium_url)
                article = parse_article(html, freedium_url)

            # Show preview
            st.markdown(
                f'<div class="markdown-card"><h2 style="color:#ff6347;">{article["title"]}</h2>'
                f'<p style="color:#20b2aa;">_By {article["author"]}_  <br>_Published: {article["date"]}_</p>'
                f"<hr>"
                f'<div style="color:#333333;">{article["markdown"].replace("\\n","<br>")}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

            # Save files
            outdir = Path(output_dir)
            outdir.mkdir(exist_ok=True)
            safe_title = sanitize_filename(article["title"])[:80]
            json_path = outdir / f"{safe_title}.json"
            md_path = outdir / f"{safe_title}.md"
            json_path.write_text(
                json.dumps(article, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            md_path.write_text(
                f"# {article['title']}\n\n_By {article['author']}_  \n_Published: {article['date']}_\n\n{article['markdown']}",
                encoding="utf-8",
            )

            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Markdown",
                    data=md_path.read_text(encoding="utf-8"),
                    file_name=md_path.name,
                    mime="text/markdown",
                )
            with col2:
                st.download_button(
                    "📥 Download JSON",
                    data=json_path.read_text(encoding="utf-8"),
                    file_name=json_path.name,
                    mime="application/json",
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")
