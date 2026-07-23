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
    """Load songs from a CSV file with numeric fields converted to numbers."""
    # Keep the CSV loader independent of pandas so it works in the smallest
    # possible environment.  DictReader uses the header row as dictionary keys.
    integer_fields = {"id", "tempo_bpm"}
    float_fields = {
        "energy",
        "valence",
        "danceability",
        "acousticness",
    }

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            song: Dict = dict(row)
            for field in integer_fields:
                if field in song and song[field] != "":
                    song[field] = int(song[field])
            for field in float_fields:
                if field in song and song[field] != "":
                    song[field] = float(song[field])
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons for its score."""
    score = 0.0
    reasons: List[str] = []

    # Categorical matches are direct signals from the user's profile.
    if user_prefs.get("genre") and song.get("genre") == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")
    if user_prefs.get("mood") and song.get("mood") == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Reward closeness to the target energy, not merely high energy.
    if user_prefs.get("energy") is not None and song.get("energy") is not None:
        energy_similarity = max(0.0, 1.0 - abs(float(song["energy"]) - float(user_prefs["energy"])))
        energy_points = 2.0 * energy_similarity
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    # Tempo is optional because the starter profile does not require it.
    if user_prefs.get("tempo_bpm") is not None and song.get("tempo_bpm") is not None:
        tempo_similarity = max(
            0.0,
            1.0 - abs(float(song["tempo_bpm"]) - float(user_prefs["tempo_bpm"])) / 120.0,
        )
        tempo_points = 0.5 * tempo_similarity
        score += tempo_points
        reasons.append(f"tempo similarity (+{tempo_points:.2f})")

    # Interpret likes_acoustic as a preference for higher/lower acousticness.
    if user_prefs.get("likes_acoustic") is not None and song.get("acousticness") is not None:
        is_acoustic = float(song["acousticness"]) >= 0.5
        if bool(user_prefs["likes_acoustic"]) == is_acoustic:
            score += 0.5
            reasons.append("acousticness preference match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top k recommendations."""
    scored_songs: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no direct preference matches"
        scored_songs.append((song, score, explanation))

    # sorted() returns a new list, leaving the input catalog in its original order.
    # The ID tie-breaker makes equal scores deterministic.
    ranked_songs = sorted(
        scored_songs,
        key=lambda item: (item[1], -int(item[0].get("id", 0))),
        reverse=True,
    )
    return ranked_songs[:max(0, k)]
