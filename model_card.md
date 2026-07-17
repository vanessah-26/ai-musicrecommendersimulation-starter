# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder 1.0 is a rule-based music recommender built for classroom exploration. Given a user profile that describes their favorite genre, mood, target energy level, and danceability preference, the system scores every song in a small catalog and returns the top matches in ranked order.

It assumes the user can express their taste as a single, stable profile — one genre, one mood, one energy number. It does not learn from listening history, handle multiple moods, or adapt over time. It is designed for educational use to demonstrate how scoring logic, data representation, and bias interact in a real recommender system, not for deployment as a consumer product.

---

## 3. How the Model Works  

Every song in the catalog has a label (its genre and mood) and a set of numbers (energy, danceability, tempo, and a few others). The user also has a profile with their own labels and target numbers. VibeFinder compares the two and assigns a score out of 5.0.

The scoring works like a point system. A song earns **2.0 points** if its genre matches the user's favorite genre, and **1.5 points** if its mood matches. On top of that, the system measures how close the song's energy is to the user's target — the closer, the more points, up to **1.0**. Danceability works the same way, worth up to **0.5 points**. Every song in the catalog is judged this way, then the list is sorted from highest score to lowest, and the top results are returned.

The original starter logic awarded +2.0 for genre and +1.0 for mood. This version bumps mood up to +1.5 because mood is an equally explicit user preference and a strong factor in whether music feels right. The danceability signal was also added to the scoring after it replaced acousticness in the user profile.

---

## 4. Data  

The catalog contains **18 songs** stored in `data/songs.csv`. The original starter file had 10 songs; 8 more were added to expand genre and mood coverage.

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, r&b, country, metal, folk, electronic, latin

**Moods represented:** happy, chill, intense, relaxed, moody, focused, energetic, peaceful, romantic, nostalgic, angry, melancholic, euphoric, playful

Despite the expansion, the catalog is still small and uneven. Lofi has 3 songs while most other genres have exactly 1. This means lofi users consistently get a competitive top-3, while jazz, classical, or latin users effectively get one guaranteed match and then filler. Lyrics, language, tempo feel, instrumentation, and cultural context are entirely absent — the system knows a song is "latin" only because the genre label says so, not because of anything it can hear.

---

## 5. Strengths  

The system works best for users whose preferences align cleanly with a well-represented genre. The **Chill Lofi** profile produced a near-perfect top pick (4.99/5.00) and a tight, coherent top-3 — all quiet, acoustic, study-friendly songs. Similarly, **Deep Intense Rock** correctly surfaced *Storm Runner* as a dominant #1 with the next-closest song scoring nearly 2 points lower, showing the system can identify a strong match confidently when one exists.

The scoring also correctly separates profiles that should be different. High-Energy Pop and Chill Lofi returned completely non-overlapping results, which matches the intuition that those two listeners have nothing in common. The "Why" output is also genuinely readable — seeing "genre match (+2.0), mood match (+1.5)" tells a user in plain terms why a song ranked where it did, which is more transparent than most real recommenders.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

### Discovered Weakness: Categorical Bonuses Override Continuous Signals

The most significant weakness revealed during testing is that the fixed genre and mood bonuses are large enough to completely override the energy and danceability signals, even when those signals directly contradict the user's intent. In the "Lofi + Max Energy" edge case, a user who explicitly requested energy=0.95 still received two low-energy lofi songs (energy 0.35 and 0.42) as their top picks, simply because they matched on genre and mood — earning 2.5 points from category bonuses that the high-energy songs could never recover from. This creates a hidden contract with the user: the system behaves as if genre is the only preference that truly matters, while energy and danceability function more like minor tiebreakers than real criteria. A user who trusts the "Why" output would see "genre match" and "mood match" listed and assume those were helpful — not that those two bonuses were actively suppressing songs that actually sounded like what they asked for. The fix would be to either cap the genre bonus relative to the energy gap, or add a minimum energy threshold that disqualifies songs too far from the target before scoring even begins.

---

## 7. Evaluation  

Six user profiles were tested: three "normal" profiles representing real listener types, and three edge cases designed to break or stress the system.

### Profiles Tested

- **High-Energy Pop** — someone who wants upbeat, danceable pop at high intensity
- **Chill Lofi** — someone studying or relaxing who wants quiet, low-energy background music
- **Deep Intense Rock** — someone who wants loud, heavy, driving music
- **Edge Case: Lofi + Max Energy** — a contradictory user who says "lofi" but also wants maximum energy
- **Edge Case: Nonexistent Mood (dreamy)** — a user whose mood preference doesn't exist anywhere in the catalog
- **Edge Case: All Midpoint Preferences** — a user with perfectly average settings, no strong pull in any direction

---

### Profile Comparisons

**High-Energy Pop vs. Chill Lofi**

These two profiles are near-opposites on every axis — different genre, different mood, different energy. The results were completely different, which is a good sign. High-Energy Pop's top pick was *Sunrise City* (pop, happy, energy 0.82); Chill Lofi's top pick was *Library Rain* (lofi, chill, energy 0.35). This makes intuitive sense: one person wants something to dance to, the other wants something to study to, and the system correctly sent them in opposite directions. The scores were also high for both (#1 scored 4.89 and 4.99 out of 5.00), meaning each profile had at least one song in the catalog that matched almost everything they wanted.

**High-Energy Pop vs. Deep Intense Rock**

Both profiles want high energy, but the genre and mood differ. The interesting result here is that *Gym Hero* (pop, intense) appeared in the top 3 for **both** profiles — #2 for High-Energy Pop and #2 for Deep Intense Rock. For the pop user, it ranked because it matched the genre label. For the rock user, it ranked because the mood ("intense") and energy (0.93) were close enough, even though it is a pop song, not rock. This is the "Gym Hero problem": the song keeps showing up because it is the highest-energy pop song in the catalog, so any profile that values energy will keep pulling it in. It is not a bad recommendation — the song genuinely feels intense — but it reveals that the system does not understand *why* something sounds intense, only that the numbers match.

**Chill Lofi vs. Edge Case: Lofi + Max Energy**

Both users said they want lofi, but their energy targets were completely different (0.35 vs. 0.95). The top 3 results for both profiles were the same three lofi songs, just in slightly different order. This is the most surprising and revealing result: even though the Lofi + Max Energy user explicitly asked for very high energy, they still got the same quiet study music as the Chill Lofi user. The genre and mood bonuses (worth 2.5 points combined) were so large that the low-energy lofi songs outscored every high-energy non-lofi song. In plain terms: the system heard "lofi" and decided that was the most important thing the user said, then mostly ignored the rest. A real recommender should recognize that no lofi song in the catalog can satisfy this energy request and either warn the user or widen the search.

**Deep Intense Rock vs. Edge Case: Nonexistent Mood (dreamy)**

The rock profile had a strong, clear match: *Storm Runner* scored 4.95/5.00 and the #1 spot was obvious. The dreamy profile, by contrast, had a ceiling of 3.5 points because no song could ever earn the +1.5 mood bonus — "dreamy" simply does not exist in the catalog. The #1 pick (*Spacewalk Thoughts*, ambient) scored 3.47 but the gap to #2 (1.48) was enormous, meaning the system was essentially guessing after the first result. This comparison shows that the system has no way to tell the user "I could not find what you actually want." It always returns K results no matter what, even when most of them have almost nothing in common with the request.

**Edge Case: All Midpoint Preferences vs. All Other Profiles**

The midpoint profile (jazz, relaxed, energy=0.5, danceability=0.5) produced the most uneven top-3 of any run: #1 scored 4.85 and #2 scored only 1.43 — a gap of more than 3 points. This happened because jazz has only one song in the catalog (*Coffee Shop Stories*), so that song ran away with the top spot while everything else competed on energy and danceability proximity alone. Compared to profiles like Chill Lofi — where three genre-matching songs created a genuinely competitive top-3 (4.99, 4.92, 3.45) — the midpoint profile exposes how much catalog size per genre shapes the quality of recommendations. A user who likes a rare genre is not getting a ranked list; they are getting one guaranteed pick and then filler.

---

### What Was Surprising

The biggest surprise was how little energy actually mattered when genre was in play. It felt like energy should be the deciding factor for a music recommender — after all, choosing between something calm and something intense is one of the most basic listening decisions people make. But in practice, the genre label dominated so strongly that two users with completely opposite energy needs (0.35 vs. 0.95) ended up with nearly identical recommendation lists, as long as they shared a genre preference. That felt wrong in a way that a score alone would not reveal — you have to look at the actual songs to notice it.

---

### Terminal Output — All Profiles

```
====================================================
  High-Energy Pop
  Genre: pop  |  Mood: happy  |  Energy: 0.9
====================================================

  #1  Sunrise City by Neon Echo
       Genre: pop  |  Mood: happy  |  Energy: 0.82
       Score: 4.89 / 5.00
       Why:   genre match (+2.0), mood match (+1.5), energy proximity (+0.92), danceability proximity (+0.47)

  #2  Gym Hero by Max Pulse
       Genre: pop  |  Mood: intense  |  Energy: 0.93
       Score: 3.45 / 5.00
       Why:   genre match (+2.0), energy proximity (+0.97), danceability proximity (+0.48)

  #3  Rooftop Lights by Indigo Parade
       Genre: indie pop  |  Mood: happy  |  Energy: 0.76
       Score: 2.84 / 5.00
       Why:   mood match (+1.5), energy proximity (+0.86), danceability proximity (+0.48)

====================================================
  Chill Lofi
  Genre: lofi  |  Mood: chill  |  Energy: 0.35
====================================================

  #1  Library Rain by Paper Lanterns
       Genre: lofi  |  Mood: chill  |  Energy: 0.35
       Score: 4.99 / 5.00
       Why:   genre match (+2.0), mood match (+1.5), energy proximity (+1.0), danceability proximity (+0.49)

  #2  Midnight Coding by LoRoom
       Genre: lofi  |  Mood: chill  |  Energy: 0.42
       Score: 4.92 / 5.00
       Why:   genre match (+2.0), mood match (+1.5), energy proximity (+0.93), danceability proximity (+0.49)

  #3  Focus Flow by LoRoom
       Genre: lofi  |  Mood: focused  |  Energy: 0.4
       Score: 3.45 / 5.00
       Why:   genre match (+2.0), energy proximity (+0.95), danceability proximity (+0.5)

====================================================
  Deep Intense Rock
  Genre: rock  |  Mood: intense  |  Energy: 0.95
====================================================

  #1  Storm Runner by Voltline
       Genre: rock  |  Mood: intense  |  Energy: 0.91
       Score: 4.95 / 5.00
       Why:   genre match (+2.0), mood match (+1.5), energy proximity (+0.96), danceability proximity (+0.49)

  #2  Gym Hero by Max Pulse
       Genre: pop  |  Mood: intense  |  Energy: 0.93
       Score: 2.87 / 5.00
       Why:   mood match (+1.5), energy proximity (+0.98), danceability proximity (+0.39)

  #3  Iron Collapse by Vulcan Riff
       Genre: metal  |  Mood: angry  |  Energy: 0.97
       Score: 1.43 / 5.00
       Why:   energy proximity (+0.98), danceability proximity (+0.45)

====================================================
  Edge Case — Lofi + Max Energy
  Genre: lofi  |  Mood: chill  |  Energy: 0.95
====================================================

  #1  Midnight Coding by LoRoom
       Genre: lofi  |  Mood: chill  |  Energy: 0.42
       Score: 4.33 / 5.00
       Why:   genre match (+2.0), mood match (+1.5), energy proximity (+0.47), danceability proximity (+0.36)

  #2  Library Rain by Paper Lanterns
       Genre: lofi  |  Mood: chill  |  Energy: 0.35
       Score: 4.24 / 5.00
       Why:   genre match (+2.0), mood match (+1.5), energy proximity (+0.4), danceability proximity (+0.34)

  #3  Focus Flow by LoRoom
       Genre: lofi  |  Mood: focused  |  Energy: 0.4
       Score: 2.80 / 5.00
       Why:   genre match (+2.0), energy proximity (+0.45), danceability proximity (+0.35)

====================================================
  Edge Case — Nonexistent Mood (dreamy)
  Genre: ambient  |  Mood: dreamy  |  Energy: 0.3
====================================================

  #1  Spacewalk Thoughts by Orbit Bloom
       Genre: ambient  |  Mood: chill  |  Energy: 0.28
       Score: 3.47 / 5.00
       Why:   genre match (+2.0), energy proximity (+0.98), danceability proximity (+0.49)

  #2  Withered Letters by Emmeline Grey
       Genre: folk  |  Mood: melancholic  |  Energy: 0.3
       Score: 1.48 / 5.00
       Why:   energy proximity (+1.0), danceability proximity (+0.48)

  #3  Library Rain by Paper Lanterns
       Genre: lofi  |  Mood: chill  |  Energy: 0.35
       Score: 1.36 / 5.00
       Why:   energy proximity (+0.95), danceability proximity (+0.41)

====================================================
  Edge Case — All Midpoint Preferences
  Genre: jazz  |  Mood: relaxed  |  Energy: 0.5
====================================================

  #1  Coffee Shop Stories by Slow Stereo
       Genre: jazz  |  Mood: relaxed  |  Energy: 0.37
       Score: 4.85 / 5.00
       Why:   genre match (+2.0), mood match (+1.5), energy proximity (+0.87), danceability proximity (+0.48)

  #2  Dusty Porch Swing by The Lonesome Crows
       Genre: country  |  Mood: nostalgic  |  Energy: 0.52
       Score: 1.43 / 5.00
       Why:   energy proximity (+0.98), danceability proximity (+0.45)

  #3  Midnight Coding by LoRoom
       Genre: lofi  |  Mood: chill  |  Energy: 0.42
       Score: 1.36 / 5.00
       Why:   energy proximity (+0.92), danceability proximity (+0.44)
```

---

## 8. Future Work  

The most impactful next step would be adding a **minimum energy threshold** — if a song's energy is more than 0.4 away from the user's target, it gets filtered out before scoring even begins. This would fix the Lofi + Max Energy failure without changing the weights at all.

A **genre similarity map** would help users of adjacent genres (e.g., "indie pop" and "pop," or "metal" and "rock") still receive partial genre credit instead of zero. Right now the exact string match means closely related genres are treated as completely unrelated.

Adding a **confidence signal** to the output would make the system more honest. If the top result scores 3.5 or lower, the system should say something like "Best available match — no songs in the catalog fully match your preferences" rather than presenting a weak result with the same confidence as a 4.9 match.

Finally, expanding the catalog to at least 5 songs per genre would make rankings meaningful for every user type, not just the ones whose genre happens to have 3 entries.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
    - It can be highly generalized or highly personalized. Also, there is levels to personalization, and it can be generic or very detailed oriented.   
- Something unexpected or interesting you discovered 
    - There are many other things besides genre and tempo that goes into consideration for recommendation system. 
- How this changed the way you think about music recommendation apps  
    - It clarified how my preferneces and how generalizing formula for personalization can affect the results recommended to me.  
