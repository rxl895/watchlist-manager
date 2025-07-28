from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class WatchBase(BaseModel):
    content_id: int
    watched_at: datetime
    platform_id: Optional[int] = None
    season_number: Optional[int] = Field(None, ge=1)
    episode_number: Optional[int] = Field(None, ge=1)
    episode_title: Optional[str] = None
    duration_watched: Optional[int] = Field(None, ge=1)  # in minutes
    completion_percentage: float = Field(100.0, ge=0, le=100)
    watch_location: Optional[str] = None
    watch_mood: Optional[str] = None
    companions: Optional[str] = None
    notes: Optional[str] = None
    rating_after_watch: Optional[float] = Field(None, ge=1, le=10)

class WatchCreate(WatchBase):
    pass

class WatchUpdate(BaseModel):
    watched_at: Optional[datetime] = None
    platform_id: Optional[int] = None
    season_number: Optional[int] = Field(None, ge=1)
    episode_number: Optional[int] = Field(None, ge=1)
    episode_title: Optional[str] = None
    duration_watched: Optional[int] = Field(None, ge=1)
    completion_percentage: Optional[float] = Field(None, ge=0, le=100)
    watch_location: Optional[str] = None
    watch_mood: Optional[str] = None
    companions: Optional[str] = None
    notes: Optional[str] = None
    rating_after_watch: Optional[float] = Field(None, ge=1, le=10)

class WatchResponse(WatchBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class WatchSessionBase(BaseModel):
    content_id: int
    started_at: datetime
    device_type: Optional[str] = None
    platform_id: Optional[int] = None
    start_position: float = Field(0.0, ge=0, le=100)
    quality: Optional[str] = None
    audio_language: Optional[str] = None
    subtitle_language: Optional[str] = None
    watch_mood: Optional[str] = None

class WatchSessionCreate(WatchSessionBase):
    pass

class WatchSessionUpdate(BaseModel):
    ended_at: Optional[datetime] = None
    end_position: Optional[float] = Field(None, ge=0, le=100)
    paused_duration: Optional[int] = Field(None, ge=0)
    interruptions: Optional[int] = Field(None, ge=0)

class WatchSessionResponse(WatchSessionBase):
    id: int
    ended_at: Optional[datetime] = None
    end_position: Optional[float] = None
    paused_duration: int = 0
    interruptions: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

class WatchStatistics(BaseModel):
    content_id: int
    total_watches: int
    total_duration: int  # in minutes
    average_rating: Optional[float] = None
    completion_rate: float
    favorite_platform: Optional[str] = None
    last_watched: Optional[datetime] = None
    first_watched: Optional[datetime] = None
