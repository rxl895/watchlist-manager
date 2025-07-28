import requests
from typing import List, Optional, Dict, Any
from ..config import settings

class TMDBService:
    """Service for interacting with The Movie Database (TMDB) API."""
    
    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3"
        self.api_key = settings.tmdb_api_key
        self.image_base_url = "https://image.tmdb.org/t/p/w500"

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict]:
        """Make a request to the TMDB API."""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/{endpoint}"
        default_params = {"api_key": self.api_key}
        
        if params:
            default_params.update(params)
        
        try:
            response = requests.get(url, params=default_params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    def search_content(self, query: str, content_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for movies or TV shows."""
        results = []
        
        if not content_type or content_type == "movie":
            movie_results = self._search_movies(query)
            if movie_results:
                results.extend(movie_results)
        
        if not content_type or content_type == "tv":
            tv_results = self._search_tv(query)
            if tv_results:
                results.extend(tv_results)
        
        # Sort by popularity
        return sorted(results, key=lambda x: x.get("popularity", 0), reverse=True)[:20]

    def _search_movies(self, query: str) -> List[Dict[str, Any]]:
        """Search for movies."""
        data = self._make_request("search/movie", {"query": query})
        if not data:
            return []
        
        results = []
        for movie in data.get("results", []):
            results.append({
                "id": movie.get("id"),
                "title": movie.get("title"),
                "content_type": "movie",
                "overview": movie.get("overview"),
                "release_date": movie.get("release_date"),
                "poster_path": f"{self.image_base_url}{movie.get('poster_path')}" if movie.get("poster_path") else None,
                "backdrop_path": f"{self.image_base_url}{movie.get('backdrop_path')}" if movie.get("backdrop_path") else None,
                "tmdb_rating": movie.get("vote_average"),
                "popularity": movie.get("popularity", 0),
                "genre_ids": movie.get("genre_ids", [])
            })
        
        return results

    def _search_tv(self, query: str) -> List[Dict[str, Any]]:
        """Search for TV shows."""
        data = self._make_request("search/tv", {"query": query})
        if not data:
            return []
        
        results = []
        for show in data.get("results", []):
            results.append({
                "id": show.get("id"),
                "title": show.get("name"),
                "content_type": "tv",
                "overview": show.get("overview"),
                "release_date": show.get("first_air_date"),
                "poster_path": f"{self.image_base_url}{show.get('poster_path')}" if show.get("poster_path") else None,
                "backdrop_path": f"{self.image_base_url}{show.get('backdrop_path')}" if show.get("backdrop_path") else None,
                "tmdb_rating": show.get("vote_average"),
                "popularity": show.get("popularity", 0),
                "genre_ids": show.get("genre_ids", [])
            })
        
        return results

    def get_content_details(self, tmdb_id: int, content_type: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a movie or TV show."""
        endpoint = f"movie/{tmdb_id}" if content_type == "movie" else f"tv/{tmdb_id}"
        data = self._make_request(endpoint)
        
        if not data:
            return None
        
        # Get credits (cast and crew)
        credits = self._make_request(f"{endpoint}/credits")
        
        result = {
            "tmdb_id": data.get("id"),
            "title": data.get("title" if content_type == "movie" else "name"),
            "content_type": content_type,
            "overview": data.get("overview"),
            "release_date": data.get("release_date" if content_type == "movie" else "first_air_date"),
            "runtime": data.get("runtime"),
            "poster_path": f"{self.image_base_url}{data.get('poster_path')}" if data.get("poster_path") else None,
            "backdrop_path": f"{self.image_base_url}{data.get('backdrop_path')}" if data.get("backdrop_path") else None,
            "tmdb_rating": data.get("vote_average"),
            "genres": [genre["name"] for genre in data.get("genres", [])],
            "production_companies": [company["name"] for company in data.get("production_companies", [])],
            "countries": [country["name"] for country in data.get("production_countries", [])],
            "languages": [lang["english_name"] for lang in data.get("spoken_languages", [])],
        }
        
        # Add cast and crew information
        if credits:
            result["cast"] = [actor["name"] for actor in credits.get("cast", [])[:10]]  # Top 10 cast
            crew = credits.get("crew", [])
            directors = [person["name"] for person in crew if person.get("job") == "Director"]
            if directors:
                result["director"] = directors[0]
        
        # Add TV-specific fields
        if content_type == "tv":
            result["number_of_seasons"] = data.get("number_of_seasons")
            result["number_of_episodes"] = data.get("number_of_episodes")
            result["episode_run_time"] = data.get("episode_run_time", [])
        
        return result

    def get_trending(self, content_type: str = "all", time_window: str = "week") -> List[Dict[str, Any]]:
        """Get trending content."""
        endpoint = f"trending/{content_type}/{time_window}"
        data = self._make_request(endpoint)
        
        if not data:
            return []
        
        results = []
        for item in data.get("results", []):
            content_type_actual = "movie" if "title" in item else "tv"
            results.append({
                "id": item.get("id"),
                "title": item.get("title" if content_type_actual == "movie" else "name"),
                "content_type": content_type_actual,
                "overview": item.get("overview"),
                "release_date": item.get("release_date" if content_type_actual == "movie" else "first_air_date"),
                "poster_path": f"{self.image_base_url}{item.get('poster_path')}" if item.get("poster_path") else None,
                "tmdb_rating": item.get("vote_average"),
                "popularity": item.get("popularity", 0)
            })
        
        return results

    def get_popular(self, content_type: str = "movie") -> List[Dict[str, Any]]:
        """Get popular movies or TV shows."""
        endpoint = f"{content_type}/popular"
        data = self._make_request(endpoint)
        
        if not data:
            return []
        
        results = []
        for item in data.get("results", []):
            results.append({
                "id": item.get("id"),
                "title": item.get("title" if content_type == "movie" else "name"),
                "content_type": content_type,
                "overview": item.get("overview"),
                "release_date": item.get("release_date" if content_type == "movie" else "first_air_date"),
                "poster_path": f"{self.image_base_url}{item.get('poster_path')}" if item.get("poster_path") else None,
                "tmdb_rating": item.get("vote_average"),
                "popularity": item.get("popularity", 0)
            })
        
        return results
