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
    """Read a songs CSV and return a list of dicts with typed numeric fields."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"],
                "mood":          row["mood"],
                "energy":        float(row["energy"]),
                "tempo_bpm":     int(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (total_score, reasons)."""
    score = 0.0
    reasons = []

    # Support both key naming styles (e.g. main.py uses "genre"; profile CSV uses "favorite_genre")
    user_genre  = user_prefs.get("favorite_genre") or user_prefs.get("genre", "")
    user_mood   = user_prefs.get("favorite_mood")  or user_prefs.get("mood", "")
    user_energy = float(user_prefs.get("target_energy") or user_prefs.get("energy", 0.5))
    user_dance  = user_prefs.get("danceability")

    # EXPERIMENT: genre halved (+1.0), energy doubled (max +2.0); max score stays 5.0
    # Genre match: +1.0 (was +2.0)
    if song["genre"] == user_genre:
        score += 1.0
        reasons.append("genre match (+1.0)")

    # Mood match: +1.5 (unchanged)
    if song["mood"] == user_mood:
        score += 1.5
        reasons.append("mood match (+1.5)")

    # Energy proximity: 0.0–2.0 (was 0.0–1.0)
    energy_points = round((1 - abs(song["energy"] - user_energy)) * 2.0, 2)
    score += energy_points
    reasons.append(f"energy proximity (+{energy_points})")

    # Danceability proximity: 0.0–0.5 (only when user preference is provided)
    if user_dance is not None:
        dance_points = round((1 - abs(song["danceability"] - float(user_dance))) * 0.5, 2)
        score += dance_points
        reasons.append(f"danceability proximity (+{dance_points})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
