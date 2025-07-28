from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.sql import func
from ..database import Base

class Content(Base):
    """Model for movies and TV shows."""
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content_type = Column(String, nullable=False)  # 'movie' or 'tv'
    
    # External IDs
    tmdb_id = Column(Integer, unique=True, index=True)
    imdb_id = Column(String, unique=True, index=True)
    
    # Basic Info
    overview = Column(Text)
    release_date = Column(DateTime)
    runtime = Column(Integer)  # in minutes
    poster_path = Column(String)
    backdrop_path = Column(String)
    
    # Ratings and Reviews
    tmdb_rating = Column(Float)
    personal_rating = Column(Float)  # User's personal rating (1-10)
    personal_review = Column(Text)
    
    # Additional Info
    genres = Column(JSON)  # List of genre names
    cast = Column(JSON)    # List of main cast members
    director = Column(String)
    production_companies = Column(JSON)
    countries = Column(JSON)
    languages = Column(JSON)
    
    # Status
    status = Column(String, default="planned")  # planned, watching, completed, dropped
    is_favorite = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Additional fields for TV shows
    number_of_seasons = Column(Integer)
    number_of_episodes = Column(Integer)
    episode_run_time = Column(JSON)  # List of episode runtimes
    
    # AI/ML fields
    embedding = Column(JSON)  # Vector embedding for similarity search
    ai_tags = Column(JSON)    # AI-generated tags
    mood_tags = Column(JSON)  # Mood-based tags for recommendations

class Platform(Base):
    """Model for streaming platforms."""
    __tablename__ = "platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    logo_path = Column(String)
    homepage = Column(String)
    
    created_at = Column(DateTime, server_default=func.now())

class ContentPlatform(Base):
    """Model for content availability on platforms."""
    __tablename__ = "content_platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, nullable=False)
    platform_id = Column(Integer, nullable=False)
    available = Column(Boolean, default=True)
    url = Column(String)  # Direct link to content on platform
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
