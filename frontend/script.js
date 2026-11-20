const API_URL = '';
const RECENT_SEARCHES_KEY = 'recent_searches';
const MAX_RECENT = 10;

function loadRecentSearches() {
    try {
        return JSON.parse(localStorage.getItem(RECENT_SEARCHES_KEY)) || [];
    } catch {
        return [];
    }
}

function saveRecentSearches(searches) {
    localStorage.setItem(RECENT_SEARCHES_KEY, JSON.stringify(searches));
}

function addRecentSearch(query) {
    let searches = loadRecentSearches();
    searches = searches.filter(s => s !== query);
    searches.unshift(query);
    if (searches.length > MAX_RECENT) searches.pop();
    saveRecentSearches(searches);
    renderRecentSearches();
}

function clearRecentSearches() {
    localStorage.removeItem(RECENT_SEARCHES_KEY);
    renderRecentSearches();
}

function renderRecentSearches() {
    const container = document.getElementById('recent-searches');
    const clearBtn = document.getElementById('clear-searches');
    const searches = loadRecentSearches();
    
    if (searches.length === 0) {
        container.innerHTML = '<span class="empty-state">No recent searches.</span>';
        clearBtn.classList.add('hidden');
        return;
    }
    
    clearBtn.classList.remove('hidden');
    container.innerHTML = '';
    searches.forEach(query => {
        const chip = document.createElement('span');
        chip.className = 'search-chip';
        chip.textContent = query;
        chip.addEventListener('click', () => {
            document.getElementById('search-query').value = query;
            document.getElementById('search-form').dispatchEvent(new Event('submit'));
        });
        container.appendChild(chip);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    renderRecentSearches();

    document.getElementById('clear-searches').addEventListener('click', clearRecentSearches);

    // Add Document Form
    document.getElementById('add-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const titleInput = document.getElementById('doc-title');
        const contentInput = document.getElementById('doc-content');
        const submitBtn = e.target.querySelector('button');
        const messageDiv = document.getElementById('add-message');
        
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        
        if (!title || !content) return;
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Adding...';
        messageDiv.className = 'message hidden';
        
        try {
            const response = await fetch(`${API_URL}/documents`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, content })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showMessage(messageDiv, `Success: Document added (ID: ${data.id})`, 'success');
                titleInput.value = '';
                contentInput.value = '';
                fetchStats(); // Update stats
            } else {
                showMessage(messageDiv, `Error: ${data.detail || 'Failed to add document'}`, 'error');
            }
        } catch (error) {
            showMessage(messageDiv, `Error: Network issue or server down.`, 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Add Document';
        }
    });

    // Search Form
    document.getElementById('search-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const queryInput = document.getElementById('search-query');
        const topKSelect = document.getElementById('top-k');
        const resultsContainer = document.getElementById('results-container');
        const loadingDiv = document.getElementById('search-loading');
        
        const query = queryInput.value.trim();
        const top_k = parseInt(topKSelect.value, 10);
        
        if (!query) return;
        
        addRecentSearch(query);
        
        resultsContainer.innerHTML = '';
        resultsContainer.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        
        try {
            const response = await fetch(`${API_URL}/search`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, top_k })
            });
            
            const data = await response.json();
            
            loadingDiv.classList.add('hidden');
            resultsContainer.classList.remove('hidden');
            
            if (response.ok) {
                if (data.results && data.results.length > 0) {
                    renderResults(data.results, resultsContainer);
                } else {
                    resultsContainer.innerHTML = '<div class="empty-state">No relevant documents found.</div>';
                }
            } else {
                resultsContainer.innerHTML = `<div class="message error">Error: ${data.detail || 'Search failed'}</div>`;
            }
        } catch (error) {
            loadingDiv.classList.add('hidden');
            resultsContainer.classList.remove('hidden');
            resultsContainer.innerHTML = '<div class="message error">Error: Network issue or server down.</div>';
        }
    });
});

async function fetchStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        const stats = await response.json();
        
        const statsGrid = document.getElementById('stats-grid');
        statsGrid.innerHTML = `
            <div class="stat-box">
                <div class="stat-value">${stats.total_documents}</div>
                <div class="stat-label">Documents</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${stats.embedding_dimension}</div>
                <div class="stat-label">Vector Dimension</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">FAISS</div>
                <div class="stat-label">${stats.index_type}</div>
            </div>
        `;
    } catch (error) {
        console.error("Failed to fetch stats", error);
    }
}

function renderResults(results, container) {
    results.forEach(result => {
        let simScore = Math.max(0, result.score);
        const percentage = (simScore * 100).toFixed(2);
        
        const snippet = result.content.length > 150 
            ? result.content.substring(0, 150) + '...' 
            : result.content;
            
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
            <div class="result-title">${escapeHTML(result.title)}</div>
            <div class="result-content">${escapeHTML(snippet)}</div>
            <div class="result-meta">
                <span class="similarity-badge">Sim: ${percentage}%</span>
                <span class="doc-id">ID: ${result.id}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

function showMessage(element, text, type) {
    element.textContent = text;
    element.className = `message ${type}`;
    
    setTimeout(() => {
        element.className = 'message hidden';
    }, 5000);
}

function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag])
    );
}
