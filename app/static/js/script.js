document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const statusDiv = document.getElementById('uploadStatus');
    
    if (!fileInput.files.length) {
        statusDiv.innerHTML = '<p class="error">Please select a file to upload</p>';
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        statusDiv.innerHTML = '<p>Uploading...</p>';
        
        const response = await fetch('/upload/', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            statusDiv.innerHTML = `<p class="success">${result.message}</p>`;
            fileInput.value = ''; // Clear file input
        } else {
            statusDiv.innerHTML = `<p class="error">${result.message}</p>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<p class="error">Upload failed: ${error.message}</p>`;
    }
});

document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const queryInput = document.getElementById('searchQuery');
    const resultsDiv = document.getElementById('searchResults');
    
    if (!queryInput.value.trim()) {
        resultsDiv.innerHTML = '<p class="error">Please enter a search query</p>';
        return;
    }
    
    const formData = new FormData();
    formData.append('query', queryInput.value);
    
    try {
        resultsDiv.innerHTML = '<p>Searching...</p>';
        
        const response = await fetch('/search/', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            if (result.results && result.results.length > 0) {
                let html = '<h3>Search Results:</h3>';
                result.results.forEach((item, index) => {
                    // Highlight the query terms in the result
                    let highlightedText = item[2];
                    const queryTerms = queryInput.value.toLowerCase().split(' ');
                    
                    queryTerms.forEach(term => {
                        if (term.length > 2) {
                            const regex = new RegExp(`(${term})`, 'gi');
                            highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
                        }
                    });
                    
                    html += `
                        <div class="result-item">
                            <h3>${item[1]}</h3>
                            <p>${highlightedText}</p>
                            <p class="similarity">Similarity: ${(1 - item[3]).toFixed(3)}</p>
                        </div>
                    `;
                });
                resultsDiv.innerHTML = html;
            } else {
                resultsDiv.innerHTML = '<p>No results found</p>';
            }
        } else {
            resultsDiv.innerHTML = `<p class="error">${result.message}</p>`;
        }
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Search failed: ${error.message}</p>`;
    }
});