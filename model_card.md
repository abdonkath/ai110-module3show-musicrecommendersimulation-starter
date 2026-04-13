# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

This recommender is designed to suggest songs from a small catalog that best match a user's stated musical preferences. It generates a ranked list of up to 5 songs based on how closely each song aligns with the user's favorite genre, mood, energy level, valence, danceabillity, and acoustic preference. The system assumes the user can describe their taste in advance. It does not learn from listening history or adapt over time. This is built for classroom exploration, not real users. Its purpose is to demonstrate how a scoring-based recommender works conceptually.

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

The information about how the model works is in README.txt.

The changes that I made from starting logic was adding valence and dancebility in UserProfile. Orginally, it included only 4 features, genre, mood, energy, and acoustic. I decided to add valence and danceability because genre and mood alone were too coarse to capture how a song actually feels to listen to. Two songs can share the same genre and mood label but feel completely different.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

There are 18 songs in the catalog, originally it was 10. It includes genres like pop, lofi, rock, jazz, metal, classical, reggae, and fold. The distribution is uneven lofi has 3 songs while genres like reggae, metal, country, and classical each have only 1, meaning users who prefer those genres get poor recommendations by default. Overall, the small catalog size limits recommendation diversity and makes the system repetitive for users whose taste falls outside the most represented genres.

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

The system works best for users whose favorite genre is well-represented in the catalog, particularly lofi and pop listerners. Another strength is transparency. Every recommendation comes with a per-feature breakdown showing exactly why a song ranked where it did, making it easy to spot whether the system is behaving as expected or surfacing something surprising.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

My recommender has several key limitations. First, the genre weight (35%) creates a hard barrier. A lofi fan won't receive an excellent acoustic pop song recommendation even if all other features match perfectly. Second, the acousticness preference is binary (yes/no), not flexible, so users can't express "sometimes acoustic, sometimes electronic." Third, the dataset is tiny (18 songs), limiting diversity and making recommendations repetitive. Finally, some genres are severely underrepresented (only 1 reggae, 1 metal, 1 country song), which means users interested in those genres get poor recommendations. The system also doesn't understand lyrics, artist diversity, or user context (time of day, current mood), which real recommenders use.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

The system was evaluated by running it against seven taste profiles: High-Energy Pop, Chill Lofi, Deep Rock, and four edge cases covering contradictory features, a ghost genre (bossa nova) not in the catalog, all features maxed out, and a contradictory acoustic-metal combination. For each profile, the top 5 results were reviewed manually to check whether the recommendations matched the expected vibe.

The results mostly matched intuition for well-represented genres. The Chill Lofi profile returned exactly the songs you would expect, and the Deep Rock profile correctly surfaced the only rock song at the top. What was surprising was how sharply scores dropped after the top 1 or 2 results for niche genres. The Deep Rock profile's second recommendation scored only 0.57, nearly 0.4 below the first, showing how thin the catalog is for underrepresented genres.

The ghost genre edge case (bossa nova) was particularly revealing. Since no song in the catalog matched the genre, every recommendation started with a 0.0 genre score, meaning the best possible score was capped at 0.65. The system still returned reasonable-sounding songs based on energy and acousticness, but none felt like a true match — which exposed how heavily genre dominates the final score.

Two automated tests were also written to verify that the recommender returns songs sorted by score and that every recommendation includes a non-empty explanation string. These tests confirm the core logic behaves correctly but do not measure recommendation quality, only structural correctness.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

## One clear improvement would be expanding the song catalog well beyond 18 songs to give underrepresented genres like reggae, metal, and country more candidates to surface. Adding genre similarity groupings would also help so that a rock fan could still receive a metal recommendation rather than hitting a hard genre mismatch penalty. The binary acoustic preference could be replaced with a sliding scale, letting users express nuanced preferences like "mostly electronic but open to acoustic." Supporting multiple favorite genres or moods would make the user profile far more realistic, since most people don't listen to just one genre. Finally, adding context-aware inputs like time of day or current mood could push recommendations closer to how real platforms like Spotify actually behave.

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

Building this recommender made it clear how much a single design decision like genre as 35% weight has a huge effect on the output the app produces. It was surprising how quickly scores collapsed for underrepresented genres, where the second-best recommendation could be nearly 0.4 points below the first simply because the catalog had no other matching songs. It made me realized that personalized recommmendation system is often involved math running over a very large catalog. I also learned transparency is a good choice to add in the app, even large platforms like Spotify and Apple music does not explicitly say why a song was recommended. I think it would be a great addition to them.
