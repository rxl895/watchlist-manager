import enum
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class WatchLocation(str, enum.Enum):
    HOME = "home"
    THEATER = "theater"
    MOBILE = "mobile"
    OTHER = "other"

class DeviceType(str, enum.Enum):
    MOBILE = "mobile"
    DESKTOP = "desktop"
    TV = "tv"
    TABLET = "tablet"

class VideoQuality(str, enum.Enum):
    SD = "480p"
    HD = "720p"
    FHD = "1080p"
    UHD = "4K"

class Watch(Base):
    """Model for tracking when content was watched."""
    __tablename__ = "watches"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    
    # Watch details
    watched_at = Column(DateTime, nullable=False)
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    
    # Episode specific (for TV shows)
    season_number = Column(Integer)
    episode_number = Column(Integer)
    episode_title = Column(String)
    
    # Watch session details
    duration_watched = Column(Integer)  # in minutes
    completion_percentage = Column(Float, default=100.0)  # 0-100
    
    # Context and mood
    watch_location = Column(Enum(WatchLocation))  # "home", "theater", "mobile", etc.
    watch_mood = Column(String)      # "relaxed", "excited", "bored", etc.
    companions = Column(Text)        # Who watched with you
    
    # Notes and reactions
    notes = Column(Text)
    rating_after_watch = Column(Float)  # 1-10 rating after this specific watch
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class WatchSession(Base):
    """Model for tracking continuous watch sessions."""
    __tablename__ = "watch_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    
    # Session details
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime)
    paused_duration = Column(Integer, default=0)  # Total paused time in minutes
    
    # Progress tracking
    start_position = Column(Float, default=0.0)    # Starting position (0-100%)
    end_position = Column(Float)                   # Ending position (0-100%)
    
    # Device and platform
    device_type = Column(Enum(DeviceType))         # "mobile", "desktop", "tv", "tablet"
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    
    # Session quality
    quality = Column(Enum(VideoQuality))           # "480p", "720p", "1080p", "4K"
    audio_language = Column(String)
    subtitle_language = Column(String)
    
    # Interruptions and context
    interruptions = Column(Integer, default=0)     # Number of times paused
    watch_mood = Column(String)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
