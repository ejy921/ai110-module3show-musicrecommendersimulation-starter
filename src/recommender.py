import csv
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
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Returns (score, reasons) where:
      score   — float, max 4.0 (genre 1.0 + mood 1.0 + energy 2.0)
      reasons — list of strings explaining what contributed to the score

    EXPERIMENT — Weight Shift:
      Energy weight doubled (1.0 → 2.0); genre weight halved (2.0 → 1.0).
      Max score unchanged at 4.0, so comparisons across runs remain valid.
      Hypothesis: rankings should favour songs whose energy closely matches
      the user's target even when the genre differs.
    """
    score = 0.0
    reasons = []

    # Genre match: +1.0 (halved — EXPERIMENT: reduced from 2.0)
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.0
        reasons.append(f"genre match: {song['genre']} (+1.0)")
    else:
        reasons.append(f"genre mismatch: {song['genre']} vs {user_prefs['favorite_genre']} (+0.0)")

    # Mood match: +1.0 (contextual intent signal — unchanged)
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")
    else:
        reasons.append(f"mood mismatch: {song['mood']} vs {user_prefs['favorite_mood']} (+0.0)")

    # Energy similarity: 0.0–2.0 (doubled — EXPERIMENT: increased from 1.0)
    energy_score = (1.0 - abs(song["energy"] - user_prefs["target_energy"])) * 2.0
    score += energy_score
    reasons.append(
        f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} "
        f"(+{energy_score:.2f})"
    )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, score, " · ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda result: result[1], reverse=True)[:k]
