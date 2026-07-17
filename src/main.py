"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# --- Standard profiles ---
HIGH_ENERGY_POP = {
    "label": "High-Energy Pop",
    "genre": "pop", "mood": "happy", "energy": 0.9, "danceability": 0.85,
}
CHILL_LOFI = {
    "label": "Chill Lofi",
    "genre": "lofi", "mood": "chill", "energy": 0.35, "danceability": 0.60,
}
DEEP_INTENSE_ROCK = {
    "label": "Deep Intense Rock",
    "genre": "rock", "mood": "intense", "energy": 0.95, "danceability": 0.65,
}

# --- Adversarial / edge-case profiles ---
# Conflicting signals: genre says calm, energy says max intensity
LOFI_BUT_ENERGETIC = {
    "label": "Edge Case — Lofi + Max Energy",
    "genre": "lofi", "mood": "chill", "energy": 0.95, "danceability": 0.90,
}
# Mood that exists nowhere in the catalog — should score 0 on mood for every song
GHOST_MOOD = {
    "label": "Edge Case — Nonexistent Mood (dreamy)",
    "genre": "ambient", "mood": "dreamy", "energy": 0.30, "danceability": 0.40,
}
# Perfectly average preferences — no strong signal in any direction
PERFECTLY_AVERAGE = {
    "label": "Edge Case — All Midpoint Preferences",
    "genre": "jazz", "mood": "relaxed", "energy": 0.50, "danceability": 0.50,
}

ALL_PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    LOFI_BUT_ENERGETIC,
    GHOST_MOOD,
    PERFECTLY_AVERAGE,
]


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    label = user_prefs.get("label", "User")
    print("\n" + "=" * 52)
    print(f"  {label}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 52)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f} / 5.00")
        print(f"       Why:   {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in ALL_PROFILES:
        recs = recommend_songs(profile, songs, k=3)
        print_recommendations(profile, recs)


if __name__ == "__main__":
    main()
