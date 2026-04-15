# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests up to 5 songs from a small catalog based on a user's preferred genre, mood, energy level, valence, and danceability. It is designed for classroom exploration of how content-based filtering works — not for production use with real users. The system assumes users can clearly state their preferences upfront; it does not learn from listening history or clicks.

---

## 3. How the Model Works

When a user provides their taste profile (favorite genre, mood, and target energy level), VibeFinder reads through all 20 songs in its catalog and gives each one a score:

- A song that **matches the user's genre** earns 2 bonus points — the biggest reward in the system.
- A song that **matches the user's mood** earns 1 bonus point.
- Every song also earns a **proximity score** based on how close its energy, valence, and danceability are to what the user wants. A perfect match on energy gives 1.0 extra points; a song with the opposite energy gives 0.0.

All these points are added together. The five songs with the highest totals are returned, along with a plain-English explanation of exactly which features contributed to each score.

Think of it like a judge at a dog show awarding points for each category. The dog (song) that matches the most categories wins — and you can always read the scorecard to understand why.

---

## 4. Data

The catalog (`data/songs.csv`) contains **20 songs** across a wide range of genres and moods.

- **Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, folk, hip-hop, r&b, metal, classical, country, trap
- **Moods represented:** happy, chill, intense, relaxed, moody, focused, euphoric, melancholic, confident, romantic, peaceful, nostalgic, dark, dreamy
- **Numerical features:** energy (0.20–0.97), valence (0.25–0.90), danceability (0.28–0.92), acousticness (0.03–0.97), tempo_bpm (50–168)

The original 10-song starter set was expanded with 10 additional songs to broaden genre and mood coverage. The dataset reflects a general Western popular music perspective and does not include genres like K-pop, Afrobeats, reggaeton, or classical Indian music, which means users whose tastes center on those styles will get poor results.

---

## 5. Strengths

- **Transparent:** Every recommendation comes with a scored breakdown showing exactly which features matched. There are no hidden weights or black-box decisions.
- **Genre-coherent results:** The 2× genre weight reliably keeps recommendations within the same musical family — a rock listener almost always gets rock and metal, not jazz.
- **Fast and lightweight:** No training required. The system scores 20 songs in milliseconds with pure Python.
- **Works for clear-preference users:** Profiles like "Chill Lofi Listener" or "High-Energy Pop Fan" produce results that feel immediately intuitive.

---

## 6. Limitations and Bias

The system over-prioritizes genre in a way that can feel unfair. A moderately good mood and energy match in the preferred genre will almost always beat a near-perfect energy and valence match in a different genre. This means a user who says "rock" but might genuinely love a high-energy electronic track will never discover it through this recommender.

A second limitation is **filter bubble risk**: because the system scores purely by proximity to stated preferences, it will never suggest something surprising or outside the user's comfort zone. Real growth in musical taste often comes from unexpected exposure — something this algorithm actively prevents.

The dataset also has a **pop/lofi bias** in the original 10 songs (3 lofi, 2 pop out of 10). Even after expansion, genres like classical and folk have only 1 representative song each. Users who prefer those genres will find very little variety in their top-5 results.

Finally, the **Conflicted Dreamer experiment** revealed that the additive model cannot handle contradictory preferences well. A user requesting high energy AND a sad mood gets results driven mainly by genre (ambient), essentially ignoring the energy request because the ambient genre songs are all low-energy.

---

## 7. Evaluation

Four distinct user profiles were tested:

| Profile | Top Result | Surprise? |
|---------|-----------|-----------|
| High-Energy Pop Fan | Sunrise City (pop/happy, score 4.95) | No — perfect match |
| Chill Lofi Listener | Library Rain (lofi/chill, score 4.95) | No — expected |
| Deep Intense Rock Head | Storm Runner (rock/intense, score 4.88) | No — expected |
| Conflicted Dreamer | Spacewalk Thoughts (ambient/chill, score 3.11) | Yes — genre dominated over energy |

The biggest surprise was the Conflicted Dreamer profile. The user asked for `energy: 0.90` but `genre: ambient`. Every ambient song in the catalog is low-energy, so the genre bonus of 2.0 overwhelmed the energy proximity score. The system returned calm ambient songs for a user explicitly requesting high energy — a clear failure mode.

Two experiments were also run:
1. **Doubling energy weight / halving genre weight** — cross-genre high-energy songs flooded the rock profile's results.
2. **Removing the mood check** — results remained broadly correct but lost precision in distinguishing study vs. relaxation moods.

---

## 8. Future Work

1. **Add a diversity penalty** so the top-5 results cannot all come from the same genre — force at least 2 distinct genres in every recommendation list.
2. **Support tempo range matching** — currently `tempo_bpm` is loaded but unused. Matching a user's "feel for tempo" (slow/medium/fast) would improve acoustic and classical recommendations significantly.
3. **Introduce negative preferences** — let users say "no metal" or "nothing dark" so the scoring formula can apply penalties, not just rewards, for unwanted attributes.

---

## 9. Personal Reflection

The biggest learning moment was discovering how much work a single weight does. The genre weight of 2.0 feels like a small number, but it is almost always enough to determine the top result. That means every other feature — mood, energy, valence, danceability — is essentially tiebreaker logic inside the same genre. This is actually how many early recommenders worked: genre was the primary sort key, and everything else was secondary refinement.

Using AI tools (Copilot and Claude) to brainstorm the scoring formula was helpful for generating options quickly, but the final weighting decisions required human judgment about musical intuition. The AI could suggest "use cosine similarity on a feature vector," but only a person could decide that a genre mismatch should be penalized more than a mood mismatch based on actual music listening experience.

What surprised me most was how quickly a simple algorithm can produce results that *feel* intelligent. Showing someone "Sunrise City — Score: 4.95 — genre match, mood match, high energy similarity" reads like a thoughtful recommendation even though it is just arithmetic. The explanation layer is what creates the illusion of understanding.
