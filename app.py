import pandas as pd
import streamlit as st
import random

# Load data
data = pd.read_csv("romance_books.csv")
print("CSV columns:", data.columns)  # Debug: See your actual column names

# Ensure numeric types for filtering
data['average_rating'] = pd.to_numeric(data['average_rating'], errors='coerce')
data['num_ratings'] = pd.to_numeric(data['num_ratings'], errors='coerce')

# If your rating column is named differently, e.g., 'avg_rating', set this:
RATING_COL = 'average_rating'  # Change this to match your CSV, e.g., 'avg_rating'

st.set_page_config(page_title="Romance Book Explorer", page_icon="💘", layout="wide")
st.title("💘 Romance Book Explorer")
st.write("Explore top-rated romance books and get cozy recs!")

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Books")
min_rating = st.sidebar.slider("Minimum average rating", 0.0, 5.0, 3.5, 0.1)
min_num_ratings = st.sidebar.slider("Minimum number of ratings", 0, int(data['num_ratings'].max()), 1000, 100)
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

# --- Display Results ---
st.subheader("📚 Results")
if filtered.empty:
    st.info("No books match your filters. Try adjusting them!")
else:
    for _, row in filtered.iterrows():
        st.markdown(
            f"""
            <div style="background:#fff6fa;padding:1em;margin-bottom:1em;border-radius:10px;box-shadow:0 2px 8px #f3e6ee;">
                <b style="font-size:1.1em;">{row['title']}</b> by <i>{row['author']}</i><br>
                <span style="color:#e75480;">{row[RATING_COL]} 🌟</span> &middot; {row['num_ratings']} ratings<br>
                <a href="{row['book_link']}" target="_blank" style="color:#b983ff;">View on Goodreads</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Recommendation Button ---
if not filtered.empty:
    if st.button("💡 Give me a rec!"):
        rec = filtered.sample(1).iloc[0]
        st.success(
            f"💡 You might love **{rec['title']}** by {rec['author']}! Avg rating: {rec[RATING_COL]} 🌟"
        )
