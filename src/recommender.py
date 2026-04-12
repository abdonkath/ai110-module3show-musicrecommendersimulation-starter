from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences using the weighted scoring formula.
    
    Weights:
    - Genre (35%): Categorical match
    - Energy (20%): Proximity match
    - Valence (20%): Proximity match
    - Acousticness (15%): Preference-based match
    - Danceability (5%): Proximity match
    - Mood (5%): Categorical match
    
    Returns: (score, explanation)
    """
    
    # Genre Match → Categorical (exact match or no match)
    genre_score = 1.0 if user_prefs['favorite_genre'].lower() == song['genre'].lower() else 0.0
    
    # Energy Match → Proximity-based
    energy_score = 1 - abs(user_prefs['target_energy'] - song['energy'])
    
    # Valence Match → Proximity-based (using actual user preference, not 0.70)
    valence_score = 1 - abs(user_prefs['target_valence'] - song['valence'])
    
    # Danceability Match → Proximity-based (using actual user preference, not 0.70)
    danceability_score = 1 - abs(user_prefs['target_danceability'] - song['danceability'])
    
    # Acousticness Match → Preference-based
    if user_prefs['likes_acoustic']:
        acousticness_score = song['acousticness']
    else:
        acousticness_score = 1 - song['acousticness']
    
    # Mood Match → Categorical (exact match or no match)
    mood_score = 1.0 if user_prefs['favorite_mood'].lower() == song['mood'].lower() else 0.0
    
    # Apply weights and sum
    total_score = (
        genre_score * 0.35 +
        energy_score * 0.20 +
        valence_score * 0.20 +
        acousticness_score * 0.15 +
        danceability_score * 0.05 +
        mood_score * 0.05
    )
    
    # Build explanation
    explanation = f"Genre: {genre_score:.2f} | Energy: {energy_score:.2f} | Valence: {valence_score:.2f} | Acousticness: {acousticness_score:.2f} | Dance: {danceability_score:.2f} | Mood: {mood_score:.2f}"
    
    return (total_score, explanation)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
