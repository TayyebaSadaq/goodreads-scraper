(function() {
    'use strict';
    
    // Configuration
    const DEFAULT_CONFIG = {
        width: '100%',
        height: '800px',
        baseUrl: window.location.origin, // Use current origin instead of hardcoded URL
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
        iframe.src = finalConfig.baseUrl;
        iframe.style.width = finalConfig.width;
        iframe.style.height = finalConfig.height;
        iframe.style.border = 'none';
        iframe.style.borderRadius = '12px';
        iframe.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
        iframe.setAttribute('allowfullscreen', '');
        iframe.setAttribute('loading', 'lazy');

        // Add responsive behavior
        if (finalConfig.width === '100%') {
            iframe.style.maxWidth = '1200px';
        }

        container.appendChild(iframe);

        // Optional: Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.innerHTML = `
            <div style="text-align: center; padding: 40px; font-family: sans-serif;">
                <div style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #b83a66; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px;"></div>
                <p>Loading Book Explorer...</p>
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
        
        container.appendChild(loadingDiv);
        
        iframe.onload = function() {
            loadingDiv.remove();
        };

        return iframe;
    }

    // Make it globally available
    window.BookExplorerWidget = {
        create: createBookExplorerWidget
    };

    // Auto-initialize widgets with data attributes
    document.addEventListener('DOMContentLoaded', function() {
        const widgets = document.querySelectorAll('[data-book-explorer]');
        widgets.forEach(widget => {
            const config = {
                width: widget.dataset.width || DEFAULT_CONFIG.width,
                height: widget.dataset.height || DEFAULT_CONFIG.height,
                baseUrl: widget.dataset.baseUrl || DEFAULT_CONFIG.baseUrl
            };
            createBookExplorerWidget(widget.id, config);
        });
    });
})();
