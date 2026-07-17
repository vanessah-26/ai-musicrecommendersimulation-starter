# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - genre, mood, energy, dancability
- What information does your `UserProfile` store
  - favorite_genre,favorite_mood,target_energy,danceability
- How does your `Recommender` compute a score for each song
  - Each song is scored by combining categorical matches and continuous proximity signals:
    - **+2.0** if `song.genre` matches `user.favorite_genre`
    - **+1.5** if `song.mood` matches `user.favorite_mood`
    - **0–1.0** energy proximity: `(1 - |song.energy - user.target_energy|) * 1.0`
    - **0–0.5** danceability proximity: `(1 - |song.danceability - user.danceability|) * 0.5`
    - **Maximum possible score: 5.0**

- How do you choose which songs to recommend
  - Every song in the catalog is scored individually, then sorted by score (highest first). The top K songs are returned as recommendations.

You can include a simple diagram or bullet list if helpful.


```
Input (User Prefs)
       │
       ▼
┌─────────────────────────────────┐
│  For each song in the catalog:  │
│                                 │
│  score = 0                      │
│  genre match?   → +2.0          │
│  mood match?    → +1.5          │
│  energy close?  → up to +1.0    │
│  dance close?   → up to +0.5    │
└─────────────────────────────────┘
       │
       ▼
Sort all songs by score (desc)
       │
       ▼
Output: Top K Recommendations
```

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
# e.g.:
# User profile: genre=pop, mood=happy, energy=0.8
# Recommendations:
  Music Recommender — Top 5 Picks
#1  Sunrise City by Neon Echo
    Genre: pop  |  Mood: happy  |  Energy: 0.82
    Score: 4.48 / 5.00
    Why:   genre match (+2.0), mood match (+1.5), energy proximity (+0.98)

#2  Gym Hero by Max Pulse
    Genre: pop  |  Mood: intense  |  Energy: 0.93
    Score: 2.87 / 5.00
    Why:   genre match (+2.0), energy proximity (+0.87)

#3  Rooftop Lights by Indigo Parade
    Genre: indie pop  |  Mood: happy  |  Energy: 0.76
    Score: 2.46 / 5.00
    Why:   mood match (+1.5), energy proximity (+0.96)

#4  Fuego Libre by Celia Vega
    Genre: latin  |  Mood: playful  |  Energy: 0.84
    Score: 0.96 / 5.00
    Why:   energy proximity (+0.96)

#5  Night Drive Loop by Neon Echo
    Genre: synthwave  |  Mood: moody  |  Energy: 0.75
    Score: 0.95 / 5.00
    Why:   energy proximity (+0.95)
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

### Potential Biases

- **Genre dominance** — the +2.0 genre weight is so large that a perfect mood + energy + danceability match (max 3.0) can still lose to a genre-matching song with nothing else in common (2.0). A great folk song could be invisible to a lofi user even if it sounds nearly identical.
- **Mood mismatch blindspot** — the catalog has no lofi songs with mood=happy, so a user who wants lofi + happy will never get a full 3.5-point score. The system quietly settles for chill lofi instead, with no way to signal that the mood preference went unsatisfied.
- **Continuous signals are capped low** — energy and danceability together max out at 1.5 points, meaning a song can be a near-perfect sonic fit but rank below any genre match. Users with contradictory preferences (e.g., lofi genre but energetic target) will receive systematically lower-quality results.
- **Small catalog amplifies all of the above** — with only 18 songs, a single genre match can dominate the entire top-K list, making the recommendations feel repetitive rather than personalized.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



