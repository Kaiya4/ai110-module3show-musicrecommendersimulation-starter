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

Real-world recommenders use the same general pattern at a larger scale. They
combine item data such as genre and audio features with user history, likes,
skips, and listening time. The song catalog is the input data, the profile is
the user's preference input, and the score is used to rank and select what is
shown. Production systems also learn weights from many users and add diversity
and safety rules.

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

The following output was produced by running `python -m src.main`:

```
Loaded songs: 17

High-Energy Pop
Top recommendations:

Sunrise City - Score: 5.81
Because: genre match (+2.0), mood match (+1.0), energy similarity (+1.84), tempo similarity (+0.47), acousticness preference match (+0.5)

Gym Hero - Score: 4.91
Because: genre match (+2.0), energy similarity (+1.94), tempo similarity (+0.47), acousticness preference match (+0.5)

Rooftop Lights - Score: 3.72
Because: mood match (+1.0), energy similarity (+1.72), tempo similarity (+0.50), acousticness preference match (+0.5)

Electric Bloom - Score: 2.91
Because: energy similarity (+1.92), tempo similarity (+0.49), acousticness preference match (+0.5)

Storm Runner - Score: 2.87
Because: energy similarity (+1.98), tempo similarity (+0.39), acousticness preference match (+0.5)


Chill Lofi
Top recommendations:

Library Rain - Score: 5.99
Because: genre match (+2.0), mood match (+1.0), energy similarity (+2.00), tempo similarity (+0.49), acousticness preference match (+0.5)

Midnight Coding - Score: 5.85
Because: genre match (+2.0), mood match (+1.0), energy similarity (+1.86), tempo similarity (+0.49), acousticness preference match (+0.5)

Focus Flow - Score: 4.88
Because: genre match (+2.0), energy similarity (+1.90), tempo similarity (+0.48), acousticness preference match (+0.5)

Spacewalk Thoughts - Score: 3.80
Because: mood match (+1.0), energy similarity (+1.86), tempo similarity (+0.44), acousticness preference match (+0.5)

Coffee Shop Stories - Score: 2.90
Because: energy similarity (+1.96), tempo similarity (+0.44), acousticness preference match (+0.5)


Deep Intense Rock
Top recommendations:

Storm Runner - Score: 5.85
Because: genre match (+2.0), mood match (+1.0), energy similarity (+1.88), tempo similarity (+0.47), acousticness preference match (+0.5)

Gym Hero - Score: 3.79
Because: mood match (+1.0), energy similarity (+1.84), tempo similarity (+0.45), acousticness preference match (+0.5)

Sunrise City - Score: 2.83
Because: energy similarity (+1.94), tempo similarity (+0.39), acousticness preference match (+0.5)

Electric Bloom - Score: 2.75
Because: energy similarity (+1.82), tempo similarity (+0.43), acousticness preference match (+0.5)

Rooftop Lights - Score: 2.73
Because: energy similarity (+1.82), tempo similarity (+0.41), acousticness preference match (+0.5)


Conflicting Preferences
Top recommendations:

Blue Neon - Score: 4.90
Because: genre match (+2.0), mood match (+1.0), energy similarity (+1.22), tempo similarity (+0.18), acousticness preference match (+0.5)

Storm Runner - Score: 2.47
Because: energy similarity (+1.98), tempo similarity (+0.49)

Gym Hero - Score: 2.36
Because: energy similarity (+1.94), tempo similarity (+0.42)

Electric Bloom - Score: 2.33
Because: energy similarity (+1.92), tempo similarity (+0.41)

Iron Horizon - Score: 2.27
Because: energy similarity (+1.84), tempo similarity (+0.42)
```

```
Output with doubled weight:
Loaded songs: 17

High-Energy Pop
Top recommendations:

Sunrise City - Score: 6.65
Because: genre match (+1.0), mood match (+1.0), energy similarity (+3.68), tempo similarity (+0.47), acousticness preference match (+0.5)

Gym Hero - Score: 5.85
Because: genre match (+1.0), energy similarity (+3.88), tempo similarity (+0.47), acousticness preference match (+0.5)

Rooftop Lights - Score: 5.44
Because: mood match (+1.0), energy similarity (+3.44), tempo similarity (+0.50), acousticness preference match (+0.5)

Storm Runner - Score: 4.85
Because: energy similarity (+3.96), tempo similarity (+0.39), acousticness preference match (+0.5)

Electric Bloom - Score: 4.83
Because: energy similarity (+3.84), tempo similarity (+0.49), acousticness preference match (+0.5)


Chill Lofi
Top recommendations:

Library Rain - Score: 6.99
Because: genre match (+1.0), mood match (+1.0), energy similarity (+4.00), tempo similarity (+0.49), acousticness preference match (+0.5)

Midnight Coding - Score: 6.71
Because: genre match (+1.0), mood match (+1.0), energy similarity (+3.72), tempo similarity (+0.49), acousticness preference match (+0.5)

Focus Flow - Score: 5.78
Because: genre match (+1.0), energy similarity (+3.80), tempo similarity (+0.48), acousticness preference match (+0.5)

Spacewalk Thoughts - Score: 5.66
Because: mood match (+1.0), energy similarity (+3.72), tempo similarity (+0.44), acousticness preference match (+0.5)

Coffee Shop Stories - Score: 4.86
Because: energy similarity (+3.92), tempo similarity (+0.44), acousticness preference match (+0.5)


Deep Intense Rock
Top recommendations:

Storm Runner - Score: 6.73
Because: genre match (+1.0), mood match (+1.0), energy similarity (+3.76), tempo similarity (+0.47), acousticness preference match (+0.5)

Gym Hero - Score: 5.63
Because: mood match (+1.0), energy similarity (+3.68), tempo similarity (+0.45), acousticness preference match (+0.5)

Sunrise City - Score: 4.77
Because: energy similarity (+3.88), tempo similarity (+0.39), acousticness preference match (+0.5)

Electric Bloom - Score: 4.57
Because: energy similarity (+3.64), tempo similarity (+0.43), acousticness preference match (+0.5)

Rooftop Lights - Score: 4.55
Because: energy similarity (+3.64), tempo similarity (+0.41), acousticness preference match (+0.5)


Conflicting Preferences
Top recommendations:

Blue Neon - Score: 5.12
Because: genre match (+1.0), mood match (+1.0), energy similarity (+2.44), tempo similarity (+0.18), acousticness preference match (+0.5)

Storm Runner - Score: 4.45
Because: energy similarity (+3.96), tempo similarity (+0.49)

Gym Hero - Score: 4.30
Because: energy similarity (+3.88), tempo similarity (+0.42)

Electric Bloom - Score: 4.25
Because: energy similarity (+3.84), tempo similarity (+0.41)

Iron Horizon - Score: 4.11
Because: energy similarity (+3.68), tempo similarity (+0.42)
```

```
Output if feature removal:
Loaded songs: 17

High-Energy Pop
Top recommendations:

Gym Hero - Score: 5.85
Because: genre match (+1.0), energy similarity (+3.88), tempo similarity (+0.47), acousticness preference match (+0.5)

Sunrise City - Score: 5.65
Because: genre match (+1.0), energy similarity (+3.68), tempo similarity (+0.47), acousticness preference match (+0.5)

Storm Runner - Score: 4.85
Because: energy similarity (+3.96), tempo similarity (+0.39), acousticness preference match (+0.5)

Electric Bloom - Score: 4.83
Because: energy similarity (+3.84), tempo similarity (+0.49), acousticness preference match (+0.5)

Iron Horizon - Score: 4.50
Because: energy similarity (+3.68), tempo similarity (+0.32), acousticness preference match (+0.5)


Chill Lofi
Top recommendations:

Library Rain - Score: 5.99
Because: genre match (+1.0), energy similarity (+4.00), tempo similarity (+0.49), acousticness preference match (+0.5)

Focus Flow - Score: 5.78
Because: genre match (+1.0), energy similarity (+3.80), tempo similarity (+0.48), acousticness preference match (+0.5)

Midnight Coding - Score: 5.71
Because: genre match (+1.0), energy similarity (+3.72), tempo similarity (+0.49), acousticness preference match (+0.5)

Coffee Shop Stories - Score: 4.86
Because: energy similarity (+3.92), tempo similarity (+0.44), acousticness preference match (+0.5)

Spacewalk Thoughts - Score: 4.66
Because: energy similarity (+3.72), tempo similarity (+0.44), acousticness preference match (+0.5)


Deep Intense Rock
Top recommendations:

Storm Runner - Score: 5.73
Because: genre match (+1.0), energy similarity (+3.76), tempo similarity (+0.47), acousticness preference match (+0.5)

Sunrise City - Score: 4.77
Because: energy similarity (+3.88), tempo similarity (+0.39), acousticness preference match (+0.5)

Gym Hero - Score: 4.63
Because: energy similarity (+3.68), tempo similarity (+0.45), acousticness preference match (+0.5)

Electric Bloom - Score: 4.57
Because: energy similarity (+3.64), tempo similarity (+0.43), acousticness preference match (+0.5)

Rooftop Lights - Score: 4.55
Because: energy similarity (+3.64), tempo similarity (+0.41), acousticness preference match (+0.5)


Conflicting Preferences
Top recommendations:

Storm Runner - Score: 4.45
Because: energy similarity (+3.96), tempo similarity (+0.49)

Gym Hero - Score: 4.30
Because: energy similarity (+3.88), tempo similarity (+0.42)

Electric Bloom - Score: 4.25
Because: energy similarity (+3.84), tempo similarity (+0.41)

Blue Neon - Score: 4.12
Because: genre match (+1.0), energy similarity (+2.44), tempo similarity (+0.18), acousticness preference match (+0.5)

Iron Horizon - Score: 4.11
Because: energy similarity (+3.68), tempo similarity (+0.42)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I ran the recommender for High-Energy Pop, Chill Lofi, Deep Intense Rock, and a
conflicting sad-blues/high-energy profile. Each profile produced different top
results, which matched the intended preferences. In the weight-shift experiment,
genre was reduced from 2.0 to 1.0 and energy was increased from 2.0 to 4.0;
high-energy songs moved upward even without a genre match. In the feature-removal
experiment, mood matching was disabled; results became less sensitive to the
user's emotional preference and more driven by energy and tempo. I restored the
original weights and mood rule after the experiments.

---

## Limitations and Risks

The catalog is small and uneven, so one-off genres do not have enough examples
to represent them well. Fixed genre and mood bonuses can create a filter bubble
and push down songs that match a user's audio preferences in a different genre.
The model does not understand lyrics, language, culture, popularity, or changing
context such as workout versus study time. See the [model card](model_card.md)
for the detailed limitations and evaluation.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

This project showed me that a recommender turns structured data and user
preferences into a prediction by adding weighted evidence. Small changes to the
weights or removing one feature can noticeably change the ranking, so the design
can reflect bias even when the code is simple. AI tools helped me draft formulas,
profiles, and explanations, but I had to verify the types, scores, and output by
running the CLI. If I continued, I would learn weights from user feedback and
add diversity rules so recommendations did not become repetitive.
