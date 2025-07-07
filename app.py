import pandas as pd
import streamlit as st
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from scraper import scrape_goodreads_list, scrape_book_page

genre_urls = {
    "Romance": "https://www.goodreads.com/list/show/12362.All_Time_Favorite_Romance_Novels",
    "Fantasy": "https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction_",
    "Science Fiction": "https://www.goodreads.com/list/show/19341.Best_Science_Fiction",
    "Mystery & Thriller": "https://www.goodreads.com/list/show/73283.100_Mysteries_and_Thrillers_to_Read_in_a_Lifetime_Readers_Picks",
    "Historical Fiction": "https://www.goodreads.com/list/show/15.Best_Historical_Fiction",
    "Young Adult": "https://www.goodreads.com/list/show/43.Best_Young_Adult_Books",
    "Non-Fiction": "https://www.goodreads.com/list/show/465.favorite_non_fiction",
    "Classics": "https://www.goodreads.com/list/show/449.Must_Read_Classics",
    "Horror": "https://www.goodreads.com/list/show/135.Best_Horror_Novels",
    "Biography & Memoir": "https://www.goodreads.com/list/show/281.Best_Memoir_Biography_Autobiography",
    "Graphic Novels": "https://www.goodreads.com/list/show/210.Best_Graphic_Novels",
    "Poetry": "https://www.goodreads.com/list/show/36.Best_Poetry_Books",
}


def fetch_books_with_covers(list_url, max_workers=8):
    df = scrape_goodreads_list(list_url)
    books = df.to_dict(orient='records')

    # Fetch detailed book info (with ISBN/OpenLibrary covers) in parallel
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_book = {executor.submit(scrape_book_page, book['book_link']): book for book in books if book['book_link']}
        for future in as_completed(future_to_book):
            try:
                book_data = future.result()
                results.append(book_data)
            except Exception:
                pass

    return pd.DataFrame(results)


genre = st.selectbox("Pick a genre", list(genre_urls.keys()))
selected_url = genre_urls[genre]

with st.spinner(f"Scraping {genre} books..."):
    data = scrape_goodreads_list(selected_url)

print("CSV columns:", data.columns)  # Debug: See your actual column names

# Ensure numeric types for filtering
data['average_rating'] = pd.to_numeric(data['average_rating'], errors='coerce')
data['num_ratings'] = pd.to_numeric(data['num_ratings'], errors='coerce')

RATING_COL = 'average_rating'

# Handle NaN in max for slider
max_num_ratings = data['num_ratings'].max()
if pd.isna(max_num_ratings):
    max_num_ratings = 100000  # fallback default

st.set_page_config(page_title=" Book Explorer", page_icon="📚", layout="wide")
st.title("📚 Book Explorer")
st.write("Explore top-rated books and get cozy recs!")

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Books")
min_rating = st.sidebar.slider("Minimum average rating", 0.0, 5.0, 3.5, 0.1)
min_num_ratings = st.sidebar.slider("Minimum number of ratings", 0, int(max_num_ratings), 1000, 100)
authors = data['author'].dropna().unique()
selected_authors = st.sidebar.multiselect("Author(s)", sorted(authors))

# --- Sorting ---
sort_option = st.sidebar.selectbox(
    "Sort by",
    ["Popularity (most ratings)", "Quality (highest rating)"]
)

# --- Filter Data ---
filtered = data[
    (data[RATING_COL] >= min_rating) &
    (data['num_ratings'] >= min_num_ratings)
]
if selected_authors:
    filtered = filtered[filtered['author'].isin(selected_authors)]

if sort_option == "Popularity (most ratings)":
    filtered = filtered.sort_values(by="num_ratings", ascending=False)
else:
    filtered = filtered.sort_values(by=RATING_COL, ascending=False)

# --- Recommendation Button (moved up) ---
if not filtered.empty:
    if st.button("💡 Give me a rec!"):
        rec = filtered.sample(1).iloc[0]
        st.success(
            f"💡 You might love **{rec['title']}** by {rec['author']}! Avg rating: {rec[RATING_COL]} 🌟"
        )

# --- Custom CSS for Book Cards ---
st.markdown(
    """
    <style>
    .book-card {
        background: #fff0f6;
        padding: 1em;
        margin-bottom: 1em;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(231, 84, 128, 0.2);
        transition: transform 0.2s ease-in-out;
    }
    .book-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(231, 84, 128, 0.4);
    }
    .book-title {
        font-weight: 700;
        font-size: 1.2em;
        color: #b83a66;
    }
    .book-author {
        font-style: italic;
        color: #7a3e5f;
    }
    .rating {
        color: #e75480;
        font-weight: 600;
    }
    a {
        color: #a96bc0;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Display Results ---
st.subheader("📚 Results")
if filtered.empty:
    st.info("No books match your filters. Try adjusting them!")
else:
    cols = st.columns(3)
    for i, (_, row) in enumerate(filtered.iterrows()):
        with cols[i % 3]:
            cover_html = ""
            if 'cover_url' in row and pd.notna(row['cover_url']):
                cover_html = f"<img src='{row['cover_url']}' style='width:120px;height:180px;object-fit:cover;display:block;margin:0 auto 0.7em auto;border-radius:6px;box-shadow:0 2px 8px #e7548033;'/>"
            else:
                cover_html = "<div style='width:120px;height:180px;background:#eee;border-radius:6px;display:flex;align-items:center;justify-content:center;margin:0 auto 0.7em auto;color:#aaa;font-size:1em;'>No Cover</div>"
            st.markdown(
                f"""
                <div class="book-card" style="padding:0.7em;">
                    {cover_html}
                    <div class="book-title" style="font-size:1em;">{row['title']}</div>
                    <div class="book-author" style="font-size:0.95em;">by {row['author']}</div>
                    <div class="rating" style="font-size:0.95em;">{row[RATING_COL]} 🌟 &middot; {row['num_ratings']} ratings</div>
                    <a href="{row['book_link']}" target="_blank">View on Goodreads</a>
                </div>
                """,
                unsafe_allow_html=True,
            )