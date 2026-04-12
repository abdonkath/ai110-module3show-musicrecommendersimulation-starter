"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
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


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Pop / happy — upbeat party listener
    user_profile = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.80,
        target_valence=0.85,
        target_danceability=0.75,
        likes_acoustic=False
    )

    print_profile(user_profile, "The Party Starter")
    print_recommendations(recommend_songs(user_profile, songs, k=5))


if __name__ == "__main__":
    main()
