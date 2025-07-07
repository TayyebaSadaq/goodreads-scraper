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

    print("Books found on list page:", len(books))  # Debug: See how many books were scraped
    return pd.DataFrame(books)

def scrape_book_page(book_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(book_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract ISBN (if available)
    isbn = None
    isbn_tag = soup.find('span', itemprop='isbn')
    if isbn_tag:
        isbn = isbn_tag.text.strip()
    else:
        # Try alternate selectors if needed
        isbn_label = soup.find('div', string=lambda s: s and 'ISBN' in s)
        if isbn_label:
            isbn_text = isbn_label.find_next_sibling('div')
            if isbn_text:
                isbn = isbn_text.text.strip().split()[0]

    cover_url = None

    # 1. Try Open Library
    if isbn:
        openlib_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        resp = requests.get(openlib_url)
        if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("image"):
            # Check for Open Library's "no cover" placeholder (very small file)
            if not (resp.headers.get("Content-Type", "").endswith("svg+xml") or len(resp.content) < 2048):
                cover_url = openlib_url

    # 2. Try Google Books if Open Library failed
    if not cover_url and isbn:
        try:
            gb_resp = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}",
                timeout=5
            )
            if gb_resp.status_code == 200:
                gb_data = gb_resp.json()
                items = gb_data.get("items")
                if items and "imageLinks" in items[0]["volumeInfo"]:
                    image_links = items[0]["volumeInfo"]["imageLinks"]
                    cover_url = (
                        image_links.get("large") or
                        image_links.get("medium") or
                        image_links.get("thumbnail") or
                        image_links.get("smallThumbnail")
                    )
        except Exception:
            pass

    # 3. Try Goodreads cover as last resort
    if not cover_url:
        cover_img = soup.find('img', id='coverImage')
        if cover_img and cover_img.has_attr('src'):
            cover_url = cover_img['src']

    book_data = {
        'title': soup.find('span', itemprop='name').text.strip() if soup.find('span', itemprop='name') else None,
        'author': soup.find('span', itemprop='author').text.strip() if soup.find('span', itemprop='author') else None,
        'average_rating': soup.find('span', itemprop='ratingValue').text.strip() if soup.find('span', itemprop='ratingValue') else None,
        'num_ratings': soup.find('meta', itemprop='ratingCount')['content'] if soup.find('meta', itemprop='ratingCount') else None,
        'book_link': book_url,
        'isbn': isbn,
        'cover_url': cover_url,
    }

    return book_data