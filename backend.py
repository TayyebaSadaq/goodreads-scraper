from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd
from typing import Optional, List
import uvicorn
import os
from scraper import scrape_goodreads_list, scrape_book_page
from concurrent.futures import ThreadPoolExecutor, as_completed

app = FastAPI(title="Book Explorer API", version="1.0.0")

# Enable CORS for embedding
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from docs directory
app.mount("/static", StaticFiles(directory="docs"), name="static")

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

@app.get("/")
async def read_root():
    with open("docs/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/genres")
async def get_genres():
    return {"genres": list(genre_urls.keys())}

@app.get("/api/books/{genre}")
async def get_books(
    genre: str,
    min_rating: Optional[float] = 0.0,
    min_num_ratings: Optional[int] = 0,
    authors: Optional[str] = None,
    sort_by: Optional[str] = "popularity"
):
    if genre not in genre_urls:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    try:
        # Scrape books
        data = scrape_goodreads_list(genre_urls[genre])
        
        # Convert to numeric
        data['average_rating'] = pd.to_numeric(data['average_rating'], errors='coerce')
        data['num_ratings'] = pd.to_numeric(data['num_ratings'], errors='coerce')
        
        # Filter data
        filtered = data[
            (data['average_rating'] >= min_rating) &
            (data['num_ratings'] >= min_num_ratings)
        ]
        
        if authors:
            author_list = [a.strip() for a in authors.split(",")]
            filtered = filtered[filtered['author'].isin(author_list)]
        
        # Sort data
        if sort_by == "popularity":
            filtered = filtered.sort_values(by="num_ratings", ascending=False)
        else:
            filtered = filtered.sort_values(by="average_rating", ascending=False)
        
        # Convert to records and handle NaN values
        books = filtered.fillna("").to_dict(orient='records')
        
        return {"books": books, "total": len(books)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendation/{genre}")
async def get_recommendation(genre: str):
    if genre not in genre_urls:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    try:
        data = scrape_goodreads_list(genre_urls[genre])
        data['average_rating'] = pd.to_numeric(data['average_rating'], errors='coerce')
        data['num_ratings'] = pd.to_numeric(data['num_ratings'], errors='coerce')
        
        # Filter for quality recommendations
        quality_books = data[
            (data['average_rating'] >= 3.5) &
            (data['num_ratings'] >= 1000)
        ]
        
        if quality_books.empty:
            quality_books = data
        
        recommendation = quality_books.sample(1).fillna("").iloc[0].to_dict()
        return {"recommendation": recommendation}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
