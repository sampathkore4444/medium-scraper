import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime, timezone

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MediumScraper/1.0)"}


def fetch_html(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=25)
    r.raise_for_status()
    return r.text


def parse_article(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.select_one("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    author_tag = soup.select_one("a[href*='@']")
    author = author_tag.get_text(strip=True) if author_tag else "Unknown"

    date_tag = soup.find("time")
    date = date_tag.get("datetime") or date_tag.get_text(strip=True) if date_tag else ""

    canonical = soup.find("link", rel="canonical")
    canonical = canonical["href"] if canonical and canonical.get("href") else url

    main = soup.select_one(".main-content")
    if not main:
        raise ValueError(
            "Could not find .main-content container — Freedium layout may have changed."
        )

    markdown = md(str(main))
    images = [
        {"src": img.get("src"), "alt": img.get("alt", "")}
        for img in main.find_all("img")
        if img.get("src")
    ]

    return {
        "url": url,
        "title": title,
        "author": author,
        "date": date,
        "canonical": canonical,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "images": images,
        "markdown": markdown.strip(),
    }
