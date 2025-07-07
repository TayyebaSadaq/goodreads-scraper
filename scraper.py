import requests
from bs4 import BeautifulSoup
import csv

goodread_list = "https://www.goodreads.com/list/show/12362.All_Time_Favorite_Romance_Novels"

headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(goodread_list, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

books = []

# Find all book rows
for row in soup.select("tr[itemtype='http://schema.org/Book']"):
    # Title
    title_tag = row.select_one("a.bookTitle span")
    title = title_tag.text.strip() if title_tag else ""

    # Author
    author_tag = row.select_one("a.authorName span")
    author = author_tag.text.strip() if author_tag else ""

    # Average rating
    avg_rating_tag = row.select_one("span.minirating")
    avg_rating = ""
    num_ratings = ""
    if avg_rating_tag:
        # Example: "4.25 avg rating — 1,234,567 ratings"
        parts = avg_rating_tag.text.strip().split(" — ")
        if len(parts) == 2:
            avg_rating = parts[0].split()[0]
            num_ratings = parts[1].split()[0].replace(",", "")

    # Book detail link
    link_tag = row.select_one("a.bookTitle")
    book_link = "https://www.goodreads.com" + link_tag['href'] if link_tag else ""

    books.append({
        "title": title,
        "author": author,
        "average_rating": avg_rating,
        "num_ratings": num_ratings,
        "book_link": book_link
    })

# Save to CSV
with open("romance_books.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "author", "average_rating", "num_ratings", "book_link"])
    writer.writeheader()
    writer.writerows(books)

# Print a few sample rows
for book in books[:5]:
    print(book)

