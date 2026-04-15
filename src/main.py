"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "valence": 0.85,
        "danceability": 0.80,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "valence": 0.58,
        "danceability": 0.55,
    },
    "Deep Intense Rock Head": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.93,
        "valence": 0.35,
        "danceability": 0.60,
    },
    "Conflicted Dreamer (edge case)": {
        "genre": "ambient",
        "mood": "sad",
        "energy": 0.90,   # high energy but sad mood — adversarial combo
        "valence": 0.20,
        "danceability": 0.30,
    },
}


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Print top-5 recommendations for a single user profile."""
    print("=" * 60)
    print(f"Profile: {profile_name}")
    print(f"Prefs  : {user_prefs}")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"       Score: {score:.2f}")
        print(f"       Why  : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded songs: {len(songs)}\n")

    for profile_name, user_prefs in PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
