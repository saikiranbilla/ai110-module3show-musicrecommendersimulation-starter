# Music Recommender Simulation

## Project Summary

This project builds a content-based music recommender system in Python. The system reads a catalog of songs from a CSV file, scores each song against a user's taste profile, and returns a ranked list of the top matches with plain-language explanations for every suggestion.

Unlike collaborative filtering (which says "people like you also liked X"), this simulator uses **content-based filtering**: it compares the features of each song (genre, mood, energy, etc.) directly to the user's stated preferences. This mirrors part of what Spotify's "Taste Profile" and YouTube Music's "Audio Features" matching do under the hood.

---

## How The System Works

### Real-World Context

Major streaming platforms like Spotify and YouTube combine two main strategies:

- **Collaborative filtering** – "Users who listened to what you listen to also loved this song." The algorithm finds clusters of listeners with similar histories and borrows their taste. It is powerful but needs huge amounts of behavioral data.
- **Content-based filtering** – "This song has the same energy, tempo, and mood as songs you already like." The algorithm compares audio features directly. It works even for brand-new users with no listening history.

Our simulator uses content-based filtering because it is fully explainable: every point in a score can be traced back to a specific feature match.

### Algorithm Recipe

For each song in the catalog, the system calculates a **score** using these rules:

| Rule | Points |
|------|--------|
| Genre matches user's favorite genre | +2.0 |
| Mood matches user's favorite mood | +1.0 |
| Energy similarity (`1.0 - abs(song.energy - target_energy)`) | 0.0 – 1.0 |
| Valence similarity (`(1.0 - abs(song.valence - target_valence)) × 0.5`) | 0.0 – 0.5 |
| Danceability similarity (`(1.0 - abs(song.danceability - target_dance)) × 0.5`) | 0.0 – 0.5 |

Genre is weighted highest (2.0 pts) because genre is the strongest single predictor of whether a listener will enjoy a song. Mood comes second (1.0 pt). Numerical features use a **proximity score** — songs closer to the target value earn more points, so "a little off" is always better than "very far off."

Once every song has a score, the list is sorted from highest to lowest and the top k songs are returned.

### Song Features Used

Each `Song` object stores:
- `genre` – musical genre (pop, rock, lofi, jazz, etc.)
- `mood` – emotional tone (happy, chill, intense, melancholic, etc.)
- `energy` – overall intensity from 0.0 (very calm) to 1.0 (very intense)
- `valence` – musical positivity from 0.0 (dark/sad) to 1.0 (bright/happy)
- `danceability` – how suitable for dancing, 0.0–1.0
- `tempo_bpm` – beats per minute (loaded but not currently used in scoring)
- `acousticness` – proportion of acoustic vs electronic sound, 0.0–1.0

### User Profile Fields

Each `UserProfile` stores:
- `favorite_genre` – the genre the user prefers most
- `favorite_mood` – the emotional vibe the user is seeking
- `target_energy` – desired intensity level (0.0–1.0)
- `likes_acoustic` – boolean preference for acoustic sound texture

The functional `recommend_songs` also accepts optional `valence` and `danceability` keys in the preference dict for more precise matching.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Experiments You Tried

### Experiment 1 – Weight Shift (Energy × 2, Genre ÷ 2)

When energy weight was doubled and genre halved, the "Intense Rock Head" profile started recommending pop songs with high energy (like "Gym Hero") over lower-energy rock tracks. This showed that genre is the anchor that keeps results stylistically coherent — without it, any high-energy song dominates regardless of style.

### Experiment 2 – Removing the Mood Check

Commenting out the mood bonus caused "Chill Lofi" to rank "Focus Flow" (lofi/focused) equally with "Library Rain" (lofi/chill). The top results still felt reasonable — but the nuance between a study session and a relaxation session was lost.

### Experiment 3 – Adversarial Profile (High Energy + Sad Mood)

A profile requesting `energy: 0.90` but `mood: sad` exposed a real tension. The system defaulted to genre (ambient) as the tiebreaker and returned calm ambient tracks — ignoring the high-energy request almost entirely. This revealed that conflicting numerical and categorical preferences are not well handled by a purely additive score.

---

## Limitations and Risks

- The catalog has only 20 songs; genre categories with just 1–2 songs dominate for users who prefer rare genres.
- The system cannot understand lyrics, language, cultural context, or personal associations.
- Genre is weighted at 2×, which means a great mood/energy match in the wrong genre scores lower than a mediocre same-genre track.
- There is no diversity enforcement — the top 5 could all be the same genre.
- Users with intersecting tastes (e.g., high-energy chill) are poorly served by an additive model.

---

## Reflection

See [model_card.md](model_card.md) for full analysis.

Building this recommender made it clear that even a handful of weighted rules can produce outputs that *feel* intelligent. Genre weighting alone is enough to create genre-coherent playlists, which is the baseline expectation most users have of any music app. The surprising part was how quickly the system broke down at the edges: an adversarial profile with conflicting preferences revealed that additive scoring cannot represent "I want calm music, but only if it is also energetic" — a contradiction a human DJ would just resolve by intuition.

Real platforms likely handle this with learned embeddings and multi-objective ranking. Our simulator shows the conceptual skeleton those systems are built on — and exactly where that skeleton runs out of bones.

---

## Terminal Output Screenshots

### High-Energy Pop Fan

```
Profile: High-Energy Pop Fan
#1  Sunrise City by Neon Echo       Score: 4.95
    Why: genre match (+2.0), mood match (+1.0), energy similarity (+0.97), ...
#2  Sunday Smoothie by Citrus Band  Score: 4.78
#3  Gym Hero by Max Pulse           Score: 3.84
#4  Rooftop Lights by Indigo Parade Score: 2.88
#5  Electric Daydream by Pulse Grid Score: 1.88
```

### Chill Lofi Listener

```
Profile: Chill Lofi Listener
#1  Library Rain by Paper Lanterns  Score: 4.95
#2  Midnight Coding by LoRoom       Score: 4.92
#3  Focus Flow by LoRoom            Score: 3.95
#4  Spacewalk Thoughts by Orbit Bloom Score: 2.79
#5  Coffee Shop Stories by Slow Stereo Score: 1.91
```

### Deep Intense Rock Head

```
Profile: Deep Intense Rock Head
#1  Storm Runner by Voltline        Score: 4.88
#2  Thunderclap Echo by Iron Dome   Score: 2.92
#3  Gym Hero by Max Pulse           Score: 2.65
#4  Trap Palace by SilverMask       Score: 1.76
#5  Night Drive Loop by Neon Echo   Score: 1.68
```

### Conflicted Dreamer (edge case)

```
Profile: Conflicted Dreamer (edge case)
#1  Spacewalk Thoughts by Orbit Bloom Score: 3.11
#2  Ocean Haze by Drift Current      Score: 3.03
#3  Thunderclap Echo by Iron Dome    Score: 1.74
#4  Storm Runner by Voltline         Score: 1.67
#5  Trap Palace by SilverMask        Score: 1.66
```
