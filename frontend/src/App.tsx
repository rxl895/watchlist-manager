import React, { useState, useEffect } from 'react';
import './App.css';

interface ContentItem {
  id: number;
  title: string;
  content_type: string;
  status: string;
  tmdb_rating?: number;
  genre?: string;
  platform?: string;
  description?: string;
}

interface AIRecommendation {
  title: string;
  reason: string;
  confidence: number;
}

function App() {
  const [content, setContent] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'watchlist' | 'add' | 'ai' | 'stats'>('watchlist');
  const [aiRecommendations, setAiRecommendations] = useState<AIRecommendation[]>([]);
  const [aiLoading, setAiLoading] = useState(false);
  
  // Form state for adding new content
  const [newContent, setNewContent] = useState({
    title: '',
    content_type: 'movie',
    status: 'planned',
    genre: '',
    platform: '',
    description: ''
  });

  useEffect(() => {
    fetchContent();
  }, []);

  const fetchContent = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/content/');
      if (!response.ok) throw new Error('Failed to fetch content');
      const data = await response.json();
      setContent(data);
      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  const addContent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/v1/content/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newContent)
      });
      
      if (!response.ok) throw new Error('Failed to add content');
      
      // Reset form and refresh content
      setNewContent({
        title: '',
        content_type: 'movie',
        status: 'planned',
        genre: '',
        platform: '',
        description: ''
      });
      
      fetchContent();
      setActiveTab('watchlist');
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getAIRecommendations = async () => {
    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/ai/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_preferences: "based on my watchlist" })
      });
      
      if (!response.ok) throw new Error('Failed to get AI recommendations');
      const data = await response.json();
      setAiRecommendations(data.recommendations || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setAiLoading(false);
    }
  };

  const deleteContent = async (id: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/content/${id}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) throw new Error('Failed to delete content');
      fetchContent();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const updateStatus = async (id: number, newStatus: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/content/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
      });
      
      if (!response.ok) throw new Error('Failed to update status');
      fetchContent();
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>🎬 Watchlist Manager</h1>
          <nav className="nav-tabs">
            <button 
              className={activeTab === 'watchlist' ? 'active' : ''} 
              onClick={() => setActiveTab('watchlist')}
            >
              📚 My Watchlist
            </button>
            <button 
              className={activeTab === 'add' ? 'active' : ''} 
              onClick={() => setActiveTab('add')}
            >
              ➕ Add Content
            </button>
            <button 
              className={activeTab === 'ai' ? 'active' : ''} 
              onClick={() => setActiveTab('ai')}
            >
              🤖 AI Recommendations
            </button>
            <button 
              className={activeTab === 'stats' ? 'active' : ''} 
              onClick={() => setActiveTab('stats')}
            >
              📊 Statistics
            </button>
          </nav>
        </div>
      </header>
      
      <main className="main-content">
        <div className="container">
          {error && (
            <div className="error">
              ❌ {error}
              <button onClick={() => setError(null)}>✕</button>
            </div>
          )}

          {/* Watchlist Tab */}
          {activeTab === 'watchlist' && (
            <div>
              {loading ? (
                <div className="loading">🔄 Loading your watchlist...</div>
              ) : (
                <>
                  <h2>Your Content ({content.length} items)</h2>
                  {content.length === 0 ? (
                    <div className="empty-state">
                      <h3>📭 No content yet!</h3>
                      <p>Start by adding your first movie or TV show.</p>
                      <button onClick={() => setActiveTab('add')} className="btn-primary">
                        Add Your First Item
                      </button>
                    </div>
                  ) : (
                    <div className="content-grid">
                      {content.map(item => (
                        <div key={item.id} className="content-card">
                          <div className="content-header">
                            <h3>{item.title}</h3>
                            <button 
                              className="delete-btn"
                              onClick={() => deleteContent(item.id)}
                              title="Delete"
                            >
                              🗑️
                            </button>
                          </div>
                          <div className="content-info">
                            <p>
                              <span className="label">Type:</span> 
                              {item.content_type === 'movie' ? '🎬' : '📺'} {item.content_type}
                            </p>
                            <div className="status-selector">
                              <span className="label">Status:</span>
                              <select 
                                value={item.status} 
                                onChange={(e) => updateStatus(item.id, e.target.value)}
                                className="status-select"
                              >
                                <option value="planned">📋 Planned</option>
                                <option value="watching">👀 Watching</option>
                                <option value="completed">✅ Completed</option>
                                <option value="on_hold">⏸️ On Hold</option>
                                <option value="dropped">❌ Dropped</option>
                              </select>
                            </div>
                            {item.tmdb_rating && (
                              <p><span className="label">Rating:</span> ⭐ {item.tmdb_rating}/10</p>
                            )}
                            {item.genre && (
                              <p><span className="label">Genre:</span> {item.genre}</p>
                            )}
                            {item.platform && (
                              <p><span className="label">Platform:</span> 📱 {item.platform}</p>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          )}

          {/* Add Content Tab */}
          {activeTab === 'add' && (
            <div>
              <h2>➕ Add New Content</h2>
              <form onSubmit={addContent} className="add-form">
                <div className="form-group">
                  <label>Title *</label>
                  <input
                    type="text"
                    value={newContent.title}
                    onChange={(e) => setNewContent({...newContent, title: e.target.value})}
                    placeholder="Enter movie or TV show title"
                    required
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Type</label>
                    <select
                      value={newContent.content_type}
                      onChange={(e) => setNewContent({...newContent, content_type: e.target.value})}
                    >
                      <option value="movie">🎬 Movie</option>
                      <option value="tv">📺 TV Show</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Status</label>
                    <select
                      value={newContent.status}
                      onChange={(e) => setNewContent({...newContent, status: e.target.value})}
                    >
                      <option value="planned">📋 Planned</option>
                      <option value="watching">👀 Watching</option>
                      <option value="completed">✅ Completed</option>
                      <option value="on_hold">⏸️ On Hold</option>
                      <option value="dropped">❌ Dropped</option>
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Genre</label>
                    <input
                      type="text"
                      value={newContent.genre}
                      onChange={(e) => setNewContent({...newContent, genre: e.target.value})}
                      placeholder="e.g., Action, Drama, Comedy"
                    />
                  </div>

                  <div className="form-group">
                    <label>Platform</label>
                    <input
                      type="text"
                      value={newContent.platform}
                      onChange={(e) => setNewContent({...newContent, platform: e.target.value})}
                      placeholder="e.g., Netflix, Disney+, Prime Video"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    value={newContent.description}
                    onChange={(e) => setNewContent({...newContent, description: e.target.value})}
                    placeholder="Optional description or notes"
                    rows={3}
                  />
                </div>

                <button type="submit" className="btn-primary">
                  ✨ Add to Watchlist
                </button>
              </form>
            </div>
          )}

          {/* AI Recommendations Tab */}
          {activeTab === 'ai' && (
            <div>
              <h2>🤖 AI Recommendations</h2>
              <div className="ai-section">
                <p>Get personalized recommendations based on your watchlist!</p>
                <button 
                  onClick={getAIRecommendations} 
                  disabled={aiLoading}
                  className="btn-primary"
                >
                  {aiLoading ? '🔄 Getting Recommendations...' : '✨ Get AI Recommendations'}
                </button>
                
                {aiRecommendations.length > 0 && (
                  <div className="recommendations">
                    <h3>Recommended for you:</h3>
                    {aiRecommendations.map((rec, index) => (
                      <div key={index} className="recommendation-card">
                        <h4>🎯 {rec.title}</h4>
                        <p>{rec.reason}</p>
                        <div className="confidence">
                          Confidence: {Math.round(rec.confidence * 100)}%
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Statistics Tab */}
          {activeTab === 'stats' && (
            <div>
              <h2>📊 Your Statistics</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>{content.length}</h3>
                  <p>Total Items</p>
                </div>
                <div className="stat-card">
                  <h3>{content.filter(item => item.content_type === 'movie').length}</h3>
                  <p>Movies</p>
                </div>
                <div className="stat-card">
                  <h3>{content.filter(item => item.content_type === 'tv').length}</h3>
                  <p>TV Shows</p>
                </div>
                <div className="stat-card">
                  <h3>{content.filter(item => item.status === 'completed').length}</h3>
                  <p>Completed</p>
                </div>
                <div className="stat-card">
                  <h3>{content.filter(item => item.status === 'watching').length}</h3>
                  <p>Currently Watching</p>
                </div>
                <div className="stat-card">
                  <h3>{content.filter(item => item.status === 'planned').length}</h3>
                  <p>Planned</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
