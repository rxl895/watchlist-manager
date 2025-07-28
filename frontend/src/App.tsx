import React, { useState, useEffect } from 'react';

interface ContentItem {
  id: number;
  title: string;
  content_type: string;
  status: string;
  tmdb_rating?: number;
}

function App() {
  const [content, setContent] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch content from backend
    fetch('http://localhost:8000/api/v1/content/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch content');
        }
        return response.json();
      })
      .then(data => {
        setContent(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>🎬 Watchlist Manager</h1>
        </div>
      </header>
      
      <main className="main-content">
        <div className="container">
          {loading && <div className="loading">Loading your watchlist...</div>}
          
          {error && (
            <div className="error">
              Error: {error}
              <br />
              <small>Make sure the backend server is running on http://localhost:8000</small>
            </div>
          )}
          
          {!loading && !error && (
            <div>
              <h2>Your Content ({content.length} items)</h2>
              {content.length === 0 ? (
                <p>No content yet. Start by adding your first movie or TV show!</p>
              ) : (
                <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
                  {content.map(item => (
                    <div key={item.id} style={{ 
                      background: '#2a2a2a', 
                      padding: '1rem', 
                      borderRadius: '8px',
                      border: '1px solid #444'
                    }}>
                      <h3 style={{ margin: '0 0 0.5rem 0', color: '#fff' }}>{item.title}</h3>
                      <p style={{ margin: '0.25rem 0', color: '#ccc' }}>
                        Type: {item.content_type} | Status: {item.status}
                      </p>
                      {item.tmdb_rating && (
                        <p style={{ margin: '0.25rem 0', color: '#ffd700' }}>
                          ⭐ {item.tmdb_rating}/10
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
