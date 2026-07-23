# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version simulates a content-based music recommender. It compares each song's
genre, mood, energy, and acoustic properties with a user's taste profile, gives
each song a weighted similarity score, and returns the highest-scoring songs with
short explanations. Because the system uses song attributes instead of ratings
from other users, it can recommend items based on the user's stated preferences.

---

## How The System Works

The system follows this process:

1. Each `Song` stores an ID, title, artist, genre, mood, energy, tempo, valence,
   danceability, and acousticness. The ID and text fields identify a song; the
   genre, mood, and audio measurements describe its content.
2. A `UserProfile` stores the user's favorite genre, favorite mood, target energy,
   and whether they like acoustic songs.
3. For each song, the recommender awards points for matching the preferred genre
   and mood. For numerical energy, it rewards closeness to the target rather than
   simply rewarding high energy:

   `energy_score = 1 - abs(song.energy - user.target_energy)`

   The component scores are combined with weights. Genre and mood receive the
   largest weights because they are direct categorical preferences; energy and
   acousticness contribute smaller adjustments. A matching acoustic preference
   adds points, while a mismatch does not make the whole song impossible.
4. The recommender computes one total score per song, sorts songs from highest to
   lowest score, and returns the top `k` results. The explanation names the
   matching features so the recommendation is interpretable.

In short:

`user profile + song features -> feature scores -> weighted total -> sorted top k`

### User Profile

The example user prefers energetic, mostly non-acoustic rock:

```python
user_prefs = {
    "genre": "rock",
    "mood": "intense",
    "energy": 0.85,
    "tempo_bpm": 140,
    "valence": 0.55,
    "danceability": 0.65,
    "acousticness": 0.15,
}
```

This profile should separate an intense rock song from chill lofi because genre
and mood are categorical matches, while energy, tempo, and acousticness provide
additional numerical evidence. It is specific enough to express a preference,
but not so narrow that only one exact song can match.

### Algorithm Recipe (Scoring and Ranking)

For every song in `songs.csv`, calculate these points:

- Add `2.0` points when the song's genre matches the user's preferred genre.
- Add `1.0` point when the song's mood matches the user's preferred mood.
- Add up to `2.0` energy points based on closeness to the target:
  `2.0 * (1 - abs(song.energy - user.energy))`.
- Add up to `0.5` tempo points using normalized closeness to the target tempo.
- Add `0.5` points when acousticness agrees with the user's acoustic preference.

The total is the song's score. Numerical features are compared by closeness,
not by simply rewarding high or low values. After scoring every song, sort the
results from highest to lowest and return the top `k` songs. Ties can be broken
consistently by the song ID.

### Data Flow Sketch

```text
CSV songs + UserProfile
          |
          v
  Loop through every song
          |
          v
 Apply genre/mood matches and numerical-similarity rules
          |
          v
 Store (song, score, explanation)
          |
          v
 Sort by score descending
          |
          v
 Return top K recommendations
```

### Expected Biases and Limitations

The fixed weights may over-prioritize genre and hide songs that match the user's
mood but have a different genre. The small catalog also has many one-off genres,
so category matches may be brittle. The system uses metadata only; it does not
understand lyrics, cultural context, or a user's changing tastes. Weights should
eventually be adjusted using user feedback rather than assumed to work equally
well for everyone.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 17

Top recommendations:

Sunrise City - Score: 4.96
Because: genre match (+2.0), mood match (+1.0), energy similarity (+1.96)

Gym Hero - Score: 3.74
Because: genre match (+2.0), energy similarity (+1.74)

Rooftop Lights - Score: 2.92
Because: mood match (+1.0), energy similarity (+1.92)

Golden Hour Cipher - Score: 1.96
Because: energy similarity (+1.96)

Night Drive Loop - Score: 1.90
Because: energy similarity (+1.90)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

