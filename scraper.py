import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_goodreads_list(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for row in soup.select("tr[itemtype='http://schema.org/Book']"):
        title_tag = row.select_one("a.bookTitle span")
        title = title_tag.text.strip() if title_tag else ""

        author_tag = row.select_one("a.authorName span")
        author = author_tag.text.strip() if author_tag else ""

        avg_rating = ""
        num_ratings = ""
        rating_tag = row.select_one("span.minirating")
        if rating_tag:
            parts = rating_tag.text.strip().split(" — ")
            if len(parts) == 2:
                avg_rating = parts[0].split()[0]
                num_ratings = parts[1].split()[0].replace(",", "")

        link_tag = row.select_one("a.bookTitle")
        book_link = "https://www.goodreads.com" + link_tag['href'] if link_tag else ""

        cover_tag = row.select_one("img.bookSmallImg") or row.select_one("img")
        cover_url = ""
        if cover_tag:
            cover_url = cover_tag.get("data-original") or cover_tag.get("src") or ""
        print("Sample cover_url:", cover_url)

        books.append({
            "title": title,
            "author": author,
            "average_rating": avg_rating,
            "num_ratings": num_ratings,
            "book_link": book_link,
            "cover_url": cover_url
        })
        print("Sample cover_url:", books[0]["cover_url"])

    return pd.DataFrame(books)
