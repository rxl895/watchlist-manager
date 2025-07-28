from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..services.stats_service import StatsService

router = APIRouter()

@router.get("/stats/overview")
def get_stats_overview(db: Session = Depends(get_db)):
    """Get overall statistics overview."""
    service = StatsService(db)
    return service.get_overview_stats()

@router.get("/stats/viewing-time")
def get_viewing_time_stats(
    period: str = Query("month", regex="^(week|month|quarter|year|all)$"),
    db: Session = Depends(get_db)
):
    """Get viewing time statistics for specified period."""
    service = StatsService(db)
    return service.get_viewing_time_stats(period)

@router.get("/stats/genres")
def get_genre_stats(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get genre distribution statistics."""
    service = StatsService(db)
    return service.get_genre_stats(limit)

@router.get("/stats/platforms")
def get_platform_stats(
    period: str = Query("month", regex="^(week|month|quarter|year|all)$"),
    db: Session = Depends(get_db)
):
    """Get platform usage statistics."""
    service = StatsService(db)
    return service.get_platform_stats(period)

@router.get("/stats/ratings")
def get_rating_stats(db: Session = Depends(get_db)):
    """Get rating distribution and trends."""
    service = StatsService(db)
    return service.get_rating_stats()

@router.get("/stats/completion")
def get_completion_stats(db: Session = Depends(get_db)):
    """Get completion rate statistics."""
    service = StatsService(db)
    return service.get_completion_stats()

@router.get("/stats/trending")
def get_trending_content(
    period: str = Query("week", regex="^(day|week|month)$"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending content based on recent watches."""
    service = StatsService(db)
    return service.get_trending_content(period, limit)

@router.get("/stats/personal-records")
def get_personal_records(db: Session = Depends(get_db)):
    """Get personal viewing records and milestones."""
    service = StatsService(db)
    return service.get_personal_records()

@router.get("/stats/monthly-summary")
def get_monthly_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """Get detailed monthly viewing summary."""
    service = StatsService(db)
    return service.get_monthly_summary(year, month)

@router.get("/stats/year-in-review")
def get_year_in_review(
    year: int,
    db: Session = Depends(get_db)
):
    """Get comprehensive year-end review."""
    service = StatsService(db)
    return service.get_year_in_review(year)
