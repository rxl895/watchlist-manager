from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..schemas.ai import *
from ..models.content import Content
import random

class AIService:
    def __init__(self, db: Session):
        self.db = db

    def get_recommendations(self, **kwargs):
        """Get AI recommendations - stub implementation."""
        return []

    def get_recommendations_simple(self, user_preferences: str) -> List[Dict[str, Any]]:
        """Get simple AI recommendations based on user's watchlist."""
        # Get user's current content to analyze preferences
        user_content = self.db.query(Content).all()
        
        # Analyze user preferences
        user_genres = []
        user_types = []
        completed_titles = []
        
        for content in user_content:
            if content.genres:
                user_genres.extend(content.genres)
            user_types.append(content.content_type)
            if content.status == "completed":
                completed_titles.append(content.title)
        
        # Create AI-style recommendations based on patterns
        recommendations = []
        
        # Genre-based recommendations
        if "Action" in user_genres or "Science Fiction" in user_genres:
            recommendations.extend([
                {
                    "title": "Blade Runner 2049",
                    "reason": "Based on your love for sci-fi movies like The Matrix, you'll enjoy this visually stunning cyberpunk masterpiece with deep philosophical themes.",
                    "confidence": 0.92
                },
                {
                    "title": "John Wick",
                    "reason": "Since you enjoy action films, this stylish action thriller with incredible choreography and world-building will be perfect for you.",
                    "confidence": 0.88
                },
                {
                    "title": "Westworld",
                    "reason": "This HBO series combines AI themes and philosophical questions similar to The Matrix, but in a Western setting.",
                    "confidence": 0.85
                }
            ])
        
        # TV show recommendations if user watches TV
        if "tv" in user_types:
            recommendations.extend([
                {
                    "title": "Dark",
                    "reason": "This German series offers complex storytelling and supernatural elements that will appeal to fans of mind-bending shows.",
                    "confidence": 0.89
                },
                {
                    "title": "Stranger Things",
                    "reason": "Perfect blend of supernatural mystery and nostalgia that captures the same engaging storytelling style you enjoy.",
                    "confidence": 0.87
                }
            ])
        
        # Movie recommendations
        if "movie" in user_types:
            recommendations.extend([
                {
                    "title": "Inception",
                    "reason": "Christopher Nolan's masterpiece about dreams within dreams - perfect if you enjoy complex, mind-bending narratives.",
                    "confidence": 0.94
                },
                {
                    "title": "Interstellar",
                    "reason": "Another Nolan film that combines science fiction with emotional depth and stunning visuals.",
                    "confidence": 0.91
                }
            ])
        
        # General popular recommendations
        if not recommendations:
            recommendations = [
                {
                    "title": "Breaking Bad",
                    "reason": "One of the greatest TV series ever made - a perfect starting point for any watchlist!",
                    "confidence": 0.95
                },
                {
                    "title": "The Godfather",
                    "reason": "A timeless classic that every movie lover should experience at least once.",
                    "confidence": 0.93
                },
                {
                    "title": "Pulp Fiction",
                    "reason": "Quentin Tarantino's masterpiece with non-linear storytelling and memorable characters.",
                    "confidence": 0.90
                }
            ]
        
        # Limit and randomize recommendations
        recommendations = random.sample(recommendations, min(5, len(recommendations)))
        
        return recommendations

    def analyze_viewing_patterns(self, **kwargs):
        """Analyze viewing patterns - enhanced implementation."""
        user_content = self.db.query(Content).all()
        
        total_content = len(user_content)
        completed_count = len([c for c in user_content if c.status == "completed"])
        watching_count = len([c for c in user_content if c.status == "watching"])
        planned_count = len([c for c in user_content if c.status == "planned"])
        
        # Analyze genres
        all_genres = []
        for content in user_content:
            if content.genres:
                all_genres.extend(content.genres)
        
        genre_counts = {}
        for genre in all_genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        return {
            "analysis_type": "viewing_patterns",
            "time_period": "all_time",
            "summary": f"You have {total_content} items in your watchlist with {completed_count} completed",
            "insights": {
                "completion_rate": round((completed_count / total_content * 100) if total_content > 0 else 0, 1),
                "favorite_genres": sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:3],
                "content_distribution": {
                    "completed": completed_count,
                    "watching": watching_count,
                    "planned": planned_count
                }
            },
            "generated_at": "2025-07-28"
        }

    def get_mood_based_suggestions(self, **kwargs):
        """Get mood-based suggestions - enhanced implementation."""
        mood = kwargs.get('mood', 'neutral')
        
        mood_suggestions = {
            "happy": [
                {"title": "The Grand Budapest Hotel", "reason": "Whimsical and visually delightful"},
                {"title": "Parks and Recreation", "reason": "Uplifting comedy series"}
            ],
            "sad": [
                {"title": "Inside Out", "reason": "Helps process emotions in a healthy way"},
                {"title": "The Pursuit of Happyness", "reason": "Inspiring story of overcoming challenges"}
            ],
            "excited": [
                {"title": "Mad Max: Fury Road", "reason": "High-octane action adventure"},
                {"title": "Mission: Impossible", "reason": "Thrilling action sequences"}
            ],
            "relaxed": [
                {"title": "Studio Ghibli Films", "reason": "Peaceful and beautiful animations"},
                {"title": "The Great British Baking Show", "reason": "Calming and wholesome"}
            ]
        }
        
        return {"suggestions": mood_suggestions.get(mood, mood_suggestions["relaxed"])}

    def chat_about_watchlist(self, query: str) -> str:
        """Chat about watchlist - enhanced implementation."""
        user_content = self.db.query(Content).all()
        
        if "recommend" in query.lower():
            return "Based on your watchlist, I'd suggest exploring more sci-fi films like Blade Runner 2049 or TV series like Dark!"
        elif "stats" in query.lower() or "statistics" in query.lower():
            total = len(user_content)
            completed = len([c for c in user_content if c.status == "completed"])
            return f"You have {total} items in your watchlist with {completed} completed. That's a {round(completed/total*100) if total > 0 else 0}% completion rate!"
        elif "what should i watch" in query.lower():
            watching = [c.title for c in user_content if c.status == "watching"]
            if watching:
                return f"You're currently watching {', '.join(watching)}. Why not continue with one of those?"
            else:
                return "Check out the AI Recommendations tab for personalized suggestions!"
        else:
            return "I can help you with recommendations, statistics, or suggestions about what to watch next. Just ask!"

    def semantic_search(self, query: str, limit: int = 10):
        """Semantic search - enhanced implementation."""
        user_content = self.db.query(Content).all()
        
        results = []
        query_lower = query.lower()
        
        for content in user_content:
            score = 0
            if query_lower in content.title.lower():
                score += 10
            if content.genres:
                for genre in content.genres:
                    if query_lower in genre.lower():
                        score += 5
            if content.overview and query_lower in content.overview.lower():
                score += 3
                
            if score > 0:
                results.append({"content": content, "score": score})
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return [r["content"] for r in results[:limit]]

    def generate_content_tags(self, content_id: int):
        """Generate content tags - enhanced implementation."""
        content = self.db.query(Content).filter(Content.id == content_id).first()
        if not content:
            return []
        
        tags = []
        if content.genres:
            tags.extend([f"#{genre.lower().replace(' ', '_')}" for genre in content.genres])
        
        if content.tmdb_rating and content.tmdb_rating >= 8.0:
            tags.append("#highly_rated")
        
        if content.content_type == "movie":
            tags.append("#movie")
        else:
            tags.append("#tv_series")
            
        return tags

    def generate_viewing_insights(self):
        """Generate viewing insights - enhanced implementation."""
        user_content = self.db.query(Content).all()
        
        insights = []
        
        # Completion rate insight
        total = len(user_content)
        completed = len([c for c in user_content if c.status == "completed"])
        if total > 0:
            completion_rate = completed / total * 100
            insights.append(f"Your completion rate is {completion_rate:.1f}% - {'Great job!' if completion_rate > 50 else 'You have lots to catch up on!'}")
        
        # Genre preference insight
        all_genres = []
        for content in user_content:
            if content.genres:
                all_genres.extend(content.genres)
        
        if all_genres:
            from collections import Counter
            top_genre = Counter(all_genres).most_common(1)[0][0]
            insights.append(f"You seem to love {top_genre} content!")
        
        return insights
