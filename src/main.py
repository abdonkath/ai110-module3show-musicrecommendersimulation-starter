"""
Command line runner for the Music Recommender Simulation.

Defines three standard taste profiles and four adversarial / edge-case
profiles designed to stress-test the scoring logic.
"""

try:
    from src.recommender import load_songs, recommend_songs, UserProfile
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs, UserProfile

DIVIDER = "=" * 60
THIN    = "-" * 60

def print_profile(user_profile, label):
    print(DIVIDER)
    print(f"  Music Recommender Simulation")
    print(f"  Taste Profile: {label}")
    print(THIN)
    print(f"  Genre:        {user_profile.favorite_genre}")
    print(f"  Mood:         {user_profile.favorite_mood}")
    print(f"  Energy:       {user_profile.target_energy}")
    print(f"  Valence:      {user_profile.target_valence}")
    print(f"  Danceability: {user_profile.target_danceability}")
    print(f"  Acoustic:     {user_profile.likes_acoustic}")
    print(DIVIDER)


def print_recommendations(recommendations):
    print(f"\n  Top {len(recommendations)} Recommendations\n")
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"  {i}. {song['title']}  —  {song['artist']}")
        print(f"     Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"     Score: {score:.2f} / 1.00")
        print(f"     Reasons:")
        for reason in explanation.split("; "):
            print(f"       • {reason}")
        print()


# ---------------------------------------------------------------------------
# Standard profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.90,
    target_valence=0.85,
    target_danceability=0.85,
    likes_acoustic=False,
)

CHILL_LOFI = UserProfile(
    favorite_genre="lofi",
    favorite_mood="chill",
    target_energy=0.35,
    target_valence=0.60,
    target_danceability=0.58,
    likes_acoustic=True,
)

DEEP_INTENSE_ROCK = UserProfile(
    favorite_genre="rock",
    favorite_mood="intense",
    target_energy=0.92,
    target_valence=0.30,
    target_danceability=0.65,
    likes_acoustic=False,
)

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles
# ---------------------------------------------------------------------------

# Edge case 1 — Contradictory energy + mood.
# Very high energy (0.9) paired with a melancholic mood.  The scorer assigns
# energy and mood weights independently, so we want to see which dimension
# wins and whether the top songs feel coherent.
CONTRADICTORY_ENERGY_MOOD = UserProfile(
    favorite_genre="pop",
    favorite_mood="melancholic",
    target_energy=0.90,
    target_valence=0.20,       # low valence matches melancholic
    target_danceability=0.80,
    likes_acoustic=False,
)

# Edge case 2 — Ghost genre.
# "bossa nova" does not exist in the dataset, so genre_score will always be
# 0.0 (35 % zeroed out).  We want to confirm the system still surfaces
# reasonable songs rather than returning garbage or crashing.
GHOST_GENRE = UserProfile(
    favorite_genre="bossa nova",
    favorite_mood="relaxed",
    target_energy=0.45,
    target_valence=0.70,
    target_danceability=0.55,
    likes_acoustic=True,
)

# Edge case 3 — All features maxed out.
# Every numeric preference is pegged to 1.0.  This reveals whether any
# scoring path overflows, clamps incorrectly, or produces a tie storm.
ALL_MAX = UserProfile(
    favorite_genre="electronic",
    favorite_mood="energetic",
    target_energy=1.0,
    target_valence=1.0,
    target_danceability=1.0,
    likes_acoustic=False,
)

# Edge case 4 — Acoustic headbanger.
# likes_acoustic=True (prefers low-energy, organic sound) but genre=metal
# and high target energy.  The acousticness weight (15 %) will penalise
# every loud metal track, creating tension with the genre preference (35 %).
ACOUSTIC_HEADBANGER = UserProfile(
    favorite_genre="metal",
    favorite_mood="angry",
    target_energy=0.97,
    target_valence=0.25,
    target_danceability=0.55,
    likes_acoustic=True,       # contradicts metal's typical low acousticness
)


def main() -> None:
    songs = load_songs("data/songs.csv")

    runs = [
        # --- Standard profiles ---
        (HIGH_ENERGY_POP,          "High-Energy Pop"),
        (CHILL_LOFI,               "Chill Lofi"),
        (DEEP_INTENSE_ROCK,        "Deep Intense Rock"),
        # --- Adversarial / edge-case profiles ---
        (CONTRADICTORY_ENERGY_MOOD, "Edge Case 1 — Contradictory Energy + Mood"),
        (GHOST_GENRE,               "Edge Case 2 — Ghost Genre (bossa nova)"),
        (ALL_MAX,                   "Edge Case 3 — All Features Maxed Out"),
        (ACOUSTIC_HEADBANGER,       "Edge Case 4 — Acoustic Headbanger"),
    ]

    for profile, label in runs:
        print_profile(profile, label)
        print_recommendations(recommend_songs(profile, songs, k=5))


if __name__ == "__main__":
    main()
