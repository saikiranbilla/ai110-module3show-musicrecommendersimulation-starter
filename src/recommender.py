import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio attributes."""
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
    """Represents a user's music taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_song_obj(user: UserProfile, song: Song) -> Tuple[float, str]:
    """Compute a numeric score and explanation for a Song object against a UserProfile."""
    score = 0.0
    reasons = []

    if song.genre.lower() == user.favorite_genre.lower():
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    if song.mood.lower() == user.favorite_mood.lower():
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy similarity: full point when perfect match, zero when 1.0 apart
    energy_gap = abs(song.energy - user.target_energy)
    energy_score = round(1.0 - energy_gap, 2)
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:+.2f})")

    # Acoustic bonus/penalty based on user preference
    if user.likes_acoustic:
        acoustic_score = round(song.acousticness * 0.5, 2)
        score += acoustic_score
        reasons.append(f"acoustic bonus ({acoustic_score:+.2f})")
    else:
        acoustic_penalty = round(-song.acousticness * 0.3, 2)
        score += acoustic_penalty
        reasons.append(f"acoustic penalty ({acoustic_penalty:+.2f})")

    explanation = ", ".join(reasons)
    return round(score, 2), explanation


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        """Initialize with a list of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user profile."""
        scored = [(song, _score_song_obj(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        _, explanation = _score_song_obj(user, song)
        return explanation


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song dict against user preference dict; return (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_gap = abs(song["energy"] - target_energy)
    energy_score = round(1.0 - energy_gap, 2)
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:+.2f})")

    if "valence" in user_prefs:
        valence_gap = abs(song["valence"] - user_prefs["valence"])
        valence_score = round((1.0 - valence_gap) * 0.5, 2)
        score += valence_score
        reasons.append(f"valence similarity ({valence_score:+.2f})")

    if "danceability" in user_prefs:
        dance_gap = abs(song["danceability"] - user_prefs["danceability"])
        dance_score = round((1.0 - dance_gap) * 0.5, 2)
        score += dance_score
        reasons.append(f"danceability similarity ({dance_score:+.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank by score, and return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        s, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, s, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
