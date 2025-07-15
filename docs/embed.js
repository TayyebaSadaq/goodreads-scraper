(function() {
    'use strict';
    
    // Configuration - Updated with your GitHub username
    const DEFAULT_CONFIG = {
        width: '100%',
        height: '800px',
        // Updated with your actual GitHub username
        widgetUrl: 'https://TayyebaSadaq.github.io/goodreads-scraper/',
        theme: 'default'
    };

    function createBookExplorerWidget(elementId, config = {}) {
        const finalConfig = { ...DEFAULT_CONFIG, ...config };
        const container = document.getElementById(elementId);
        
        if (!container) {
            console.error(`Element with ID "${elementId}" not found`);
            return;
        }

        // Create iframe
        const iframe = document.createElement('iframe');
        iframe.src = finalConfig.widgetUrl;
        iframe.style.width = finalConfig.width;
        iframe.style.height = finalConfig.height;
        iframe.style.border = 'none';
        iframe.style.borderRadius = '12px';
        iframe.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
        iframe.setAttribute('allowfullscreen', '');
        iframe.setAttribute('loading', 'lazy');
        iframe.setAttribute('title', 'Book Explorer Widget');

        // Add responsive behavior
        if (finalConfig.width === '100%') {
            iframe.style.maxWidth = '1200px';
            iframe.style.display = 'block';
            iframe.style.margin = '0 auto';
        }

        // Clear container and add iframe
        container.innerHTML = '';
        container.appendChild(iframe);

        // Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.innerHTML = `
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
                <div style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #b83a66; border-radius: 50%; animation: bookSpin 1s linear infinite; margin: 0 auto 20px;"></div>
                <p style="color: #666; margin: 0;">Loading Book Explorer...</p>
            </div>
            <style>
                @keyframes bookSpin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
        
        loadingDiv.style.position = 'relative';
        loadingDiv.style.height = finalConfig.height;
        container.insertBefore(loadingDiv, iframe);
        
        iframe.onload = function() {
            if (loadingDiv.parentNode) {
                loadingDiv.remove();
            }
        };

        // Handle iframe load errors
        iframe.onerror = function() {
            loadingDiv.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #e74c3c; font-family: sans-serif;">
                    <p>❌ Failed to load Book Explorer widget</p>
                    <p style="font-size: 14px; color: #666;">Please check your internet connection</p>
                </div>
            `;
        };

        return iframe;
    }

    // Make it globally available
    window.BookExplorerWidget = {
        create: createBookExplorerWidget,
        version: '1.0.0'
    };

    // Auto-initialize widgets with data attributes
    document.addEventListener('DOMContentLoaded', function() {
        const widgets = document.querySelectorAll('[data-book-explorer]');
        widgets.forEach((widget, index) => {
            // Generate ID if not present
            if (!widget.id) {
                widget.id = `book-explorer-${index}`;
            }
            
            const config = {
                width: widget.dataset.width || DEFAULT_CONFIG.width,
                height: widget.dataset.height || DEFAULT_CONFIG.height,
                widgetUrl: widget.dataset.widgetUrl || DEFAULT_CONFIG.widgetUrl
            };
            createBookExplorerWidget(widget.id, config);
        });
    });
})();
