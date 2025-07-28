from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.content import Content
from ..schemas.content import ContentCreate, ContentUpdate, ContentResponse
from ..services.content_service import ContentService
from ..services.tmdb_service import TMDBService

router = APIRouter()

@router.get("/content/", response_model=List[ContentResponse])
def get_content_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    content_type: Optional[str] = Query(None, regex="^(movie|tv)$"),
    status: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of content with optional filtering."""
    service = ContentService(db)
    return service.get_content_list(
        skip=skip,
        limit=limit,
        content_type=content_type,
        status=status,
        genre=genre
    )

@router.post("/content/", response_model=ContentResponse)
def create_content(
    content: ContentCreate,
    db: Session = Depends(get_db)
):
    """Add new content to watchlist."""
    service = ContentService(db)
    
    # If TMDB ID is provided, fetch additional data
    if content.tmdb_id:
        tmdb_service = TMDBService()
        tmdb_data = tmdb_service.get_content_details(content.tmdb_id, content.content_type)
        if tmdb_data:
            # Merge TMDB data with user input
            content = service.merge_tmdb_data(content, tmdb_data)
    
    return service.create_content(content)

@router.get("/content/{content_id}", response_model=ContentResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    """Get specific content by ID."""
    service = ContentService(db)
    content = service.get_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.put("/content/{content_id}", response_model=ContentResponse)
def update_content(
    content_id: int,
    content_update: ContentUpdate,
    db: Session = Depends(get_db)
):
    """Update existing content."""
    service = ContentService(db)
    updated_content = service.update_content(content_id, content_update)
    if not updated_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return updated_content

@router.patch("/content/{content_id}", response_model=ContentResponse)
def patch_content(
    content_id: int,
    content_update: ContentUpdate,
    db: Session = Depends(get_db)
):
    """Partially update existing content (same as PUT for this implementation)."""
    service = ContentService(db)
    updated_content = service.update_content(content_id, content_update)
    if not updated_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return updated_content

@router.delete("/content/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db)):
    """Delete content from watchlist."""
    service = ContentService(db)
    success = service.delete_content(content_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content deleted successfully"}

@router.post("/content/search")
def search_content(
    query: str,
    content_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Search for content using TMDB API."""
    tmdb_service = TMDBService()
    results = tmdb_service.search_content(query, content_type)
    return {"results": results}

@router.post("/content/{content_id}/favorite")
def toggle_favorite(content_id: int, db: Session = Depends(get_db)):
    """Toggle favorite status for content."""
    service = ContentService(db)
    updated_content = service.toggle_favorite(content_id)
    if not updated_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"is_favorite": updated_content.is_favorite}

@router.get("/content/{content_id}/similar")
def get_similar_content(
    content_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get similar content recommendations."""
    service = ContentService(db)
    similar_content = service.get_similar_content(content_id, limit)
    return {"similar": similar_content}
