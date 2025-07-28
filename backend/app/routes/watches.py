from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..schemas.watches import WatchCreate, WatchResponse, WatchSessionCreate
from ..services.watch_service import WatchService

router = APIRouter()

@router.post("/watches/", response_model=WatchResponse)
def record_watch(
    watch: WatchCreate,
    db: Session = Depends(get_db)
):
    """Record a new watch session."""
    service = WatchService(db)
    return service.create_watch(watch)

@router.get("/watches/", response_model=List[WatchResponse])
def get_watch_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    content_id: Optional[int] = Query(None),
    platform_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get watch history with optional filtering."""
    service = WatchService(db)
    return service.get_watch_history(
        skip=skip,
        limit=limit,
        content_id=content_id,
        platform_id=platform_id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/watches/{watch_id}", response_model=WatchResponse)
def get_watch(watch_id: int, db: Session = Depends(get_db)):
    """Get specific watch record."""
    service = WatchService(db)
    watch = service.get_watch(watch_id)
    if not watch:
        raise HTTPException(status_code=404, detail="Watch record not found")
    return watch

@router.delete("/watches/{watch_id}")
def delete_watch(watch_id: int, db: Session = Depends(get_db)):
    """Delete a watch record."""
    service = WatchService(db)
    success = service.delete_watch(watch_id)
    if not success:
        raise HTTPException(status_code=404, detail="Watch record not found")
    return {"message": "Watch record deleted successfully"}

@router.post("/watches/session/start")
def start_watch_session(
    session: WatchSessionCreate,
    db: Session = Depends(get_db)
):
    """Start a new watch session."""
    service = WatchService(db)
    return service.start_watch_session(session)

@router.post("/watches/session/{session_id}/end")
def end_watch_session(
    session_id: int,
    end_position: float,
    db: Session = Depends(get_db)
):
    """End a watch session."""
    service = WatchService(db)
    return service.end_watch_session(session_id, end_position)

@router.get("/content/{content_id}/watch-count")
def get_watch_count(content_id: int, db: Session = Depends(get_db)):
    """Get total watch count for specific content."""
    service = WatchService(db)
    count = service.get_watch_count(content_id)
    return {"content_id": content_id, "watch_count": count}
