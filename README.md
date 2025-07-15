# 📚 Goodreads Book Scraper
Discover top rated books by genre, with:
- cover images
- filtering
- recommendation system

# 🚀 Live Demo
Try it out here - https://book-explorer.streamlit.app

# 🗂️ Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Future Work](#future-work)
- [About Me](#about-me)

# Features
- **browsing**: Explore books by genre with cover images and links to Goodreads.
- **filtering**: Filter books by rating, popularity, and author
- **recommendations**: Get personalized book recommendations based on genre
- **search**: Find books by author

# Getting Started
Clone the repo:

```bash
git clone https://github.com/TayyebaSadaq/goodreads-scraper.git
cd goodreads-scraper
```

Install dependencies:

```bash
pip install -r requirements.txt
```
Run the app:
```bash
Edit
streamlit run app.py
```

# Usage
- select a genre to explore from the dropdown
- let it scrape the genre's top list
- use the sidebar to filter and refine your picks
- tap "give me a rec" for a randomised recommendation

# Tech Stack
- Streamlit – UI & deployment
- Requests + BeautifulSoup – scraping Goodreads
- ThreadPoolExecutor – parallel cover fetch
- Open Library covers/API – book art
- Pandas – data handling & filtering

# Future Work
- more genres
- auto caching to speed up loading
- more filters
- polish up UI

# About Me
Hi, I’m Tayyeba! I built this to blend my love for reading and coding.  
I like building data driven tools to help make life easier. 
