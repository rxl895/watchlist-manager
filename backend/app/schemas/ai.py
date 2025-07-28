from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class AnalysisType(str, Enum):
    GENRES = "genres"
    PLATFORMS = "platforms"
    VIEWING_PATTERNS = "viewing_patterns"
    MOOD_ANALYSIS = "mood_analysis"
    RATING_TRENDS = "rating_trends"

class TimePeriod(str, Enum):
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    ALL_TIME = "all_time"

class PreferenceType(str, Enum):
    GENRE = "genre"
    DIRECTOR = "director"
    ACTOR = "actor"
    YEAR = "year"
    PLATFORM = "platform"

class UserPreference(BaseModel):
    type: PreferenceType
    value: str
    weight: float = Field(1.0, ge=0, le=1)

class RecommendationRequest(BaseModel):
    preferences: Optional[List[UserPreference]] = []
    mood: Optional[str] = None
    limit: int = Field(10, ge=1, le=50)
    exclude_watched: bool = True

class RecommendationResponse(BaseModel):
    content_id: Optional[int] = None  # For existing content
    title: str
    content_type: str
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    tmdb_rating: Optional[float] = None
    genres: Optional[List[str]] = []
    confidence_score: float = Field(..., ge=0, le=1)
    reason: str
    source: str = "ai"  # ai, collaborative, content_based, etc.

class AnalysisRequest(BaseModel):
    time_period: TimePeriod = TimePeriod.MONTH
    analysis_type: AnalysisType = AnalysisType.VIEWING_PATTERNS

class GenreInsight(BaseModel):
    genre: str
    count: int
    percentage: float
    average_rating: Optional[float] = None
    trend: str  # "increasing", "decreasing", "stable"

class PlatformInsight(BaseModel):
    platform: str
    watch_count: int
    total_hours: float
    percentage: float
    favorite_genres: List[str]

class ViewingPattern(BaseModel):
    day_of_week: str
    hour_of_day: int
    watch_count: int
    preferred_content_type: str

class AnalysisResponse(BaseModel):
    analysis_type: AnalysisType
    time_period: TimePeriod
    summary: str
    insights: Dict[str, Any]
    recommendations: Optional[List[str]] = []
    generated_at: str

class MoodSuggestionRequest(BaseModel):
    mood: str
    time_available: Optional[int] = Field(None, ge=1, le=600)  # minutes
    platform_preference: Optional[str] = None
    limit: int = Field(5, ge=1, le=20)

class ChatRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = {}

class ChatResponse(BaseModel):
    response: str
    suggestions: Optional[List[str]] = []
    related_content: Optional[List[int]] = []  # content IDs

class SemanticSearchRequest(BaseModel):
    query: str
    limit: int = Field(10, ge=1, le=50)
    content_type: Optional[str] = None

class SemanticSearchResult(BaseModel):
    content_id: int
    title: str
    content_type: str
    similarity_score: float
    snippet: str
