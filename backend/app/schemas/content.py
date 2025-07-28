from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    MOVIE = "movie"
    TV = "tv"

class ContentStatus(str, Enum):
    PLANNED = "planned"
    WATCHING = "watching"
    COMPLETED = "completed"
    DROPPED = "dropped"
    ON_HOLD = "on_hold"

class ContentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content_type: ContentType
    overview: Optional[str] = None
    release_date: Optional[datetime] = None
    runtime: Optional[int] = Field(None, ge=1)
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    tmdb_rating: Optional[float] = Field(None, ge=0, le=10)
    personal_rating: Optional[float] = Field(None, ge=1, le=10)
    personal_review: Optional[str] = None
    genres: Optional[List[str]] = []
    cast: Optional[List[str]] = []
    director: Optional[str] = None
    production_companies: Optional[List[str]] = []
    countries: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    status: ContentStatus = ContentStatus.PLANNED
    is_favorite: bool = False
    number_of_seasons: Optional[int] = Field(None, ge=1)
    number_of_episodes: Optional[int] = Field(None, ge=1)
    episode_run_time: Optional[List[int]] = []

class ContentCreate(ContentBase):
    tmdb_id: Optional[int] = None
    imdb_id: Optional[str] = None

class ContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    overview: Optional[str] = None
    runtime: Optional[int] = Field(None, ge=1)
    personal_rating: Optional[float] = Field(None, ge=1, le=10)
    personal_review: Optional[str] = None
    status: Optional[ContentStatus] = None
    is_favorite: Optional[bool] = None
    ai_tags: Optional[List[str]] = None
    mood_tags: Optional[List[str]] = None

class ContentResponse(ContentBase):
    id: int
    tmdb_id: Optional[int] = None
    imdb_id: Optional[str] = None
    ai_tags: Optional[List[str]] = []
    mood_tags: Optional[List[str]] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContentSearchResult(BaseModel):
    id: int
    title: str
    content_type: ContentType
    overview: Optional[str] = None
    release_date: Optional[str] = None
    poster_path: Optional[str] = None
    tmdb_rating: Optional[float] = None
    genres: Optional[List[str]] = []

class ContentSimilarity(BaseModel):
    content: ContentResponse
    similarity_score: float
    reason: Optional[str] = None
