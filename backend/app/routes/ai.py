from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas.ai import (
    RecommendationRequest, 
    RecommendationResponse,
    AnalysisRequest,
    AnalysisResponse,
    MoodSuggestionRequest
)
from ..services.ai_service import AIService

router = APIRouter()

@router.post("/ai/recommend", response_model=List[RecommendationResponse])
def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get AI-powered content recommendations."""
    service = AIService(db)
    return service.get_recommendations(
        user_preferences=request.preferences,
        mood=request.mood,
        limit=request.limit,
        exclude_watched=request.exclude_watched
    )

@router.post("/ai/recommendations")
def get_recommendations_simple(
    request: dict,
    db: Session = Depends(get_db)
):
    """Get AI-powered content recommendations (simple endpoint for frontend)."""
    service = AIService(db)
    recommendations = service.get_recommendations_simple(request.get("user_preferences", ""))
    return {"recommendations": recommendations}

@router.post("/ai/analyze", response_model=AnalysisResponse)
def analyze_viewing_patterns(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze user's viewing patterns and preferences."""
    service = AIService(db)
    return service.analyze_viewing_patterns(
        time_period=request.time_period,
        analysis_type=request.analysis_type
    )

@router.post("/ai/mood-suggest")
def get_mood_based_suggestions(
    request: MoodSuggestionRequest,
    db: Session = Depends(get_db)
):
    """Get content suggestions based on current mood."""
    service = AIService(db)
    return service.get_mood_based_suggestions(
        mood=request.mood,
        time_available=request.time_available,
        platform_preference=request.platform_preference,
        limit=request.limit
    )

@router.post("/ai/chat")
def chat_with_assistant(
    query: str,
    db: Session = Depends(get_db)
):
    """Chat with AI assistant about your watchlist."""
    service = AIService(db)
    response = service.chat_about_watchlist(query)
    return {"response": response}

@router.post("/ai/similar-search")
def semantic_search(
    query: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Semantic search for similar content."""
    service = AIService(db)
    results = service.semantic_search(query, limit)
    return {"results": results}

@router.post("/content/{content_id}/generate-tags")
def generate_ai_tags(
    content_id: int,
    db: Session = Depends(get_db)
):
    """Generate AI tags for content."""
    service = AIService(db)
    tags = service.generate_content_tags(content_id)
    if not tags:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"content_id": content_id, "tags": tags}

@router.post("/ai/insights")
def get_viewing_insights(
    db: Session = Depends(get_db)
):
    """Get AI-generated insights about viewing habits."""
    service = AIService(db)
    insights = service.generate_viewing_insights()
    return {"insights": insights}
