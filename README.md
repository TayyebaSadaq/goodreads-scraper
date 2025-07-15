# 📚 Goodreads Book Scraper
Discover top rated books by genre, with:
- cover images
- filtering
- recommendation system
- **NEW: Embeddable widget for websites!**

# 🚀 Live Demo
Try it out here - https://book-explorer.streamlit.app

# 🗂️ Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Embedding](#embedding)
- [Tech Stack](#tech-stack)
- [Future Work](#future-work)
- [About Me](#about-me)

# Features
- **browsing**: Explore books by genre with cover images and links to Goodreads.
- **filtering**: Filter books by rating, popularity, and author
- **recommendations**: Get personalized book recommendations based on genre
- **search**: Find books by author
- **embeddable**: Easy to embed widget for any website

# Getting Started

## Backend API Setup
Install dependencies:
```bash
pip install -r requirements.txt
```

Run the FastAPI backend:
```bash
python backend.py
```

## Streamlit App (Legacy)
Run the original Streamlit app:
```bash
streamlit run app.py
```

# Usage

## Standalone Web App
Visit `http://localhost:8000` to use the web interface directly.

## API Endpoints
- `GET /api/genres` - Get available genres
- `GET /api/books/{genre}` - Get books by genre with filters
- `GET /api/recommendation/{genre}` - Get a random recommendation

# Embedding

## Quick Embed (Auto-initialization)
Add this to any webpage:

```html
<!-- Load the embed script -->
<script src="https://your-domain.com/docs/embed.js"></script>

<!-- Create widget container -->
<div id="book-widget" data-book-explorer data-width="100%" data-height="800px"></div>
```

## Manual Initialization
```html
<script src="https://your-domain.com/docs/embed.js"></script>
<div id="my-book-explorer"></div>
<script>
    BookExplorerWidget.create('my-book-explorer', {
        width: '100%',
        height: '600px',
        baseUrl: 'https://your-domain.com'
    });
</script>
```

## iframe Embed
```html
<iframe 
    src="https://your-domain.com" 
    width="100%" 
    height="800px" 
    frameborder="0"
    style="border-radius: 12px;">
</iframe>
```

# Tech Stack
- **Backend**: FastAPI + uvicorn
- **Frontend**: Vanilla HTML/CSS/JavaScript  
- **Scraping**: Requests + BeautifulSoup
- **Data**: Pandas for processing
- **APIs**: Open Library + Google Books
- **Deployment**: Any platform supporting Python web apps

# Future Work
- more genres
- auto caching to speed up loading
- more filters
- polish up UI
- widget customization options

# About Me
Hi, I'm Tayyeba! I built this to blend my love for reading and coding.  
I like building data driven tools to help make life easier.
