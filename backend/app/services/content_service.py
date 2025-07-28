from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List, Optional, Dict, Any
from ..models.content import Content, Platform, ContentPlatform
from ..schemas.content import ContentCreate, ContentUpdate, ContentResponse
import json

class ContentService:
    def __init__(self, db: Session):
        self.db = db

    def get_content_list(
        self,
        skip: int = 0,
        limit: int = 100,
        content_type: Optional[str] = None,
        status: Optional[str] = None,
        genre: Optional[str] = None
    ) -> List[Content]:
        """Get list of content with optional filtering."""
        query = self.db.query(Content)
        
        if content_type:
            query = query.filter(Content.content_type == content_type)
        
        if status:
            query = query.filter(Content.status == status)
        
        if genre:
            # Filter by genre (stored as JSON array)
            query = query.filter(Content.genres.contains([genre]))
        
        return query.order_by(desc(Content.updated_at)).offset(skip).limit(limit).all()

    def create_content(self, content: ContentCreate) -> Content:
        """Create new content entry."""
        # Use model_dump for more concise model creation
        content_data = content.model_dump()
        db_content = Content(**content_data)
        
        self.db.add(db_content)
        self.db.commit()
        self.db.refresh(db_content)
        return db_content

    def get_content(self, content_id: int) -> Optional[Content]:
        """Get content by ID."""
        return self.db.query(Content).filter(Content.id == content_id).first()

    def update_content(self, content_id: int, content_update: ContentUpdate) -> Optional[Content]:
        """Update existing content."""
        db_content = self.get_content(content_id)
        if not db_content:
            return None
        
        update_data = content_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_content, field, value)
        
        self.db.commit()
        self.db.refresh(db_content)
        return db_content

    def delete_content(self, content_id: int) -> bool:
        """Delete content by ID."""
        db_content = self.get_content(content_id)
        if not db_content:
            return False
        
        self.db.delete(db_content)
        self.db.commit()
        return True

    def toggle_favorite(self, content_id: int) -> Optional[Content]:
        """Toggle favorite status for content."""
        db_content = self.get_content(content_id)
        if not db_content:
            return None
        
        db_content.is_favorite = not db_content.is_favorite
        self.db.commit()
        self.db.refresh(db_content)
        return db_content

    def search_content(self, query: str, content_type: Optional[str] = None) -> List[Content]:
        """Search content by title."""
        search_query = self.db.query(Content).filter(
            Content.title.ilike(f"%{query}%")
        )
        
        if content_type:
            search_query = search_query.filter(Content.content_type == content_type)
        
        return search_query.order_by(desc(Content.tmdb_rating)).limit(20).all()

    def get_similar_content(self, content_id: int, limit: int = 10) -> List[Content]:
        """Get similar content based on genres and other attributes."""
        base_content = self.get_content(content_id)
        if not base_content:
            return []
        
        # Simple similarity based on shared genres
        similar_query = self.db.query(Content).filter(
            and_(
                Content.id != content_id,
                Content.content_type == base_content.content_type
            )
        )
        
        # If content has genres, filter by similar genres
        if base_content.genres:
            # Make genre matching compatible with both PostgreSQL and SQLite
            if self.db.bind.dialect.name == 'postgresql':
                # Use the efficient array overlap operator for PostgreSQL
                similar_query = similar_query.filter(
                    Content.genres.op('&&')(base_content.genres)
                )
            else:
                # For SQLite (and other backends), use a series of LIKE queries
                # This assumes genres are stored as a JSON string array, e.g., '["Action", "Adventure"]'
                genre_filters = [Content.genres.like(f'%"{genre}"%') for genre in base_content.genres]
                similar_query = similar_query.filter(or_(*genre_filters))
        
        return similar_query.order_by(desc(Content.tmdb_rating)).limit(limit).all()

    def get_by_tmdb_id(self, tmdb_id: int) -> Optional[Content]:
        """Get content by TMDB ID."""
        return self.db.query(Content).filter(Content.tmdb_id == tmdb_id).first()

    def merge_tmdb_data(self, content: ContentCreate, tmdb_data: Dict[str, Any]) -> ContentCreate:
        """Merge TMDB data with user input."""
        # This would integrate with TMDB API data
        # For now, return as-is
        return content

    def get_favorites(self, skip: int = 0, limit: int = 100) -> List[Content]:
        """Get user's favorite content."""
        return self.db.query(Content).filter(
            Content.is_favorite == True
        ).order_by(desc(Content.updated_at)).offset(skip).limit(limit).all()

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Content]:
        """Get content by status."""
        return self.db.query(Content).filter(
            Content.status == status
        ).order_by(desc(Content.updated_at)).offset(skip).limit(limit).all()

    def get_statistics(self) -> Dict[str, Any]:
        """Get basic content statistics."""
        total = self.db.query(Content).count()
        movies = self.db.query(Content).filter(Content.content_type == "movie").count()
        tv_shows = self.db.query(Content).filter(Content.content_type == "tv").count()
        favorites = self.db.query(Content).filter(Content.is_favorite == True).count()
        
        # Get status breakdown
        status_counts = self.db.query(
            Content.status, func.count(Content.id)
        ).group_by(Content.status).all()
        
        return {
            "total_content": total,
            "movies": movies,
            "tv_shows": tv_shows,
            "favorites": favorites,
            "status_breakdown": dict(status_counts)
        }
