class BookExplorer {
    constructor() {
        this.baseUrl = window.location.origin;
        this.currentGenre = '';
        this.init();
    }

    async init() {
        await this.loadGenres();
        this.setupEventListeners();
    }

    async loadGenres() {
        try {
            const response = await fetch(`${this.baseUrl}/api/genres`);
            const data = await response.json();
            
            const select = document.getElementById('genre-select');
            select.innerHTML = '<option value="">Select a genre...</option>';
            
            data.genres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre;
                option.textContent = genre;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading genres:', error);
        }
    }

    setupEventListeners() {
        const genreSelect = document.getElementById('genre-select');
        const searchBtn = document.getElementById('search-btn');
        const recommendBtn = document.getElementById('recommend-btn');
        const ratingSlider = document.getElementById('min-rating');
        const ratingValue = document.getElementById('rating-value');

        genreSelect.addEventListener('change', () => {
            this.currentGenre = genreSelect.value;
        });

        ratingSlider.addEventListener('input', () => {
            ratingValue.textContent = ratingSlider.value;
        });

        searchBtn.addEventListener('click', () => {
            if (this.currentGenre) {
                this.searchBooks();
            } else {
                alert('Please select a genre first!');
            }
        });

        recommendBtn.addEventListener('click', () => {
            if (this.currentGenre) {
                this.getRecommendation();
            } else {
                alert('Please select a genre first!');
            }
        });
    }

    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('results').classList.add('hidden');
        document.getElementById('recommendation').classList.add('hidden');
    }

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    }

    async searchBooks() {
        this.showLoading();
        
        try {
            const minRating = document.getElementById('min-rating').value;
            const sortBy = document.getElementById('sort-by').value;
            
            const params = new URLSearchParams({
                min_rating: minRating,
                sort_by: sortBy
            });

            const response = await fetch(`${this.baseUrl}/api/books/${this.currentGenre}?${params}`);
            const data = await response.json();
            
            this.displayBooks(data.books);
        } catch (error) {
            console.error('Error searching books:', error);
            alert('Error loading books. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    async getRecommendation() {
        try {
            const response = await fetch(`${this.baseUrl}/api/recommendation/${this.currentGenre}`);
            const data = await response.json();
            
            this.displayRecommendation(data.recommendation);
        } catch (error) {
            console.error('Error getting recommendation:', error);
            alert('Error getting recommendation. Please try again.');
        }
    }

    displayRecommendation(book) {
        const recDiv = document.getElementById('recommendation');
        recDiv.innerHTML = `
            <h3>💡 Recommended for you:</h3>
            <p><strong>${book.title}</strong> by ${book.author}</p>
            <p>Rating: ${book.average_rating} ⭐ • ${book.num_ratings} ratings</p>
            <a href="${book.book_link}" target="_blank" class="book-link">View on Goodreads</a>
        `;
        recDiv.classList.remove('hidden');
    }

    displayBooks(books) {
        const grid = document.getElementById('books-grid');
        const resultsDiv = document.getElementById('results');
        
        if (books.length === 0) {
            grid.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">No books found. Try adjusting your filters.</p>';
        } else {
            grid.innerHTML = books.map(book => this.createBookCard(book)).join('');
        }
        
        resultsDiv.classList.remove('hidden');
    }

    createBookCard(book) {
        const coverHtml = book.cover_url 
            ? `<img src="${book.cover_url}" alt="${book.title}" class="book-cover" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
               <div class="no-cover" style="display: none;">No Cover</div>`
            : `<div class="no-cover">No Cover</div>`;

        return `
            <div class="book-card">
                ${coverHtml}
                <div class="book-title">${book.title}</div>
                <div class="book-author">by ${book.author}</div>
                <div class="book-rating">${book.average_rating} ⭐ • ${book.num_ratings} ratings</div>
                <a href="${book.book_link}" target="_blank" class="book-link">View on Goodreads</a>
            </div>
        `;
    }
}

// Initialize the widget when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new BookExplorer();
});

// Export for external use
window.BookExplorer = BookExplorer;
