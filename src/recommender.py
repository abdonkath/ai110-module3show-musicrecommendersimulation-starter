from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
    """Load and type-convert song records from a CSV file into a list of dicts."""
    songs = []
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Convert numerical columns to appropriate types
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
        
        print(f"Successfully loaded {len(songs)} songs from {csv_path}")
        return songs
    
    except FileNotFoundError:
        print(f"Error: File {csv_path} not found.")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []

def score_song(user_prefs: UserProfile, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against a user profile using weighted feature matching."""
    reasons: List[str] = []

    # --- Genre (35%) ---
    genre_score = 1.0 if song['genre'] == user_prefs.favorite_genre else 0.0
    if genre_score == 1.0:
        reasons.append(f"Genre matches ({song['genre']})")
    else:
        reasons.append(f"Genre mismatch ({song['genre']} ≠ {user_prefs.favorite_genre})")

    # --- Energy (20%): 1 - |target - song| ---
    energy_score = 1.0 - abs(user_prefs.target_energy - song['energy'])
    reasons.append(f"Energy score {energy_score:.2f} (song {song['energy']}, target {user_prefs.target_energy})")

    # --- Valence (20%): 1 - |target - song| ---
    valence_score = 1.0 - abs(user_prefs.target_valence - song['valence'])
    reasons.append(f"Valence score {valence_score:.2f} (song {song['valence']}, target {user_prefs.target_valence})")

    # --- Acousticness (15%) ---
    if user_prefs.likes_acoustic:
        acousticness_score = song['acousticness']
        reasons.append(f"Acousticness score {acousticness_score:.2f} (prefers acoustic)")
    else:
        acousticness_score = 1.0 - song['acousticness']
        reasons.append(f"Acousticness score {acousticness_score:.2f} (prefers electronic)")

    # --- Danceability (5%): 1 - |target - song| ---
    danceability_score = 1.0 - abs(user_prefs.target_danceability - song['danceability'])
    reasons.append(f"Danceability score {danceability_score:.2f} (song {song['danceability']}, target {user_prefs.target_danceability})")

    # --- Mood (5%) ---
    mood_score = 1.0 if song['mood'] == user_prefs.favorite_mood else 0.0
    if mood_score == 1.0:
        reasons.append(f"Mood matches ({song['mood']})")
    else:
        reasons.append(f"Mood mismatch ({song['mood']} ≠ {user_prefs.favorite_mood})")

    # --- Weighted final score ---
    final_score = (
        genre_score        * 0.35 +
        energy_score       * 0.20 +
        valence_score      * 0.20 +
        acousticness_score * 0.15 +
        danceability_score * 0.05 +
        mood_score         * 0.05
    )

    return (final_score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs ranked by score, highest first."""
    scored = [(song, score, reasons) for song in songs for score, reasons in [score_song(user_prefs, song)]]
    top_k = sorted(scored, key=lambda x: x[1], reverse=True)[:k]
    return [(song, score, "; ".join(reasons)) for song, score, reasons in top_k]
