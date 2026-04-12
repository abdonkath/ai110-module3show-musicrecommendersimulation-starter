"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, UserProfile

def printProfile(user_profile):
    print(f"Music Recommender Simulation")
    print(f"Taste Profile: The Focused Coder")
    print(f"  • Genre preference: {user_profile.favorite_genre}")
    print(f"  • Mood preference: {user_profile.favorite_mood}")
    print(f"  • Energy level: {user_profile.target_energy}")
    print(f"  • Valence (positivity): {user_profile.target_valence}")
    print(f"  • Danceability: {user_profile.target_danceability}")
    print(f"  • Likes acoustic: {user_profile.likes_acoustic}")



def main() -> None:
    songs = load_songs("data/songs.csv")

    # calm, lofi beats
    user_profile1 = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill", 
        target_energy=0.40,
        target_valence=0.55,
        target_danceability=0.45,
        likes_acoustic=True
    )
    
    printProfile(user_profile1)
    
    recommendations = recommend_songs(user_profile1, songs, k=5)

    print("Top 5 recommendations:\n")
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title']} - {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"   Score: {score:.2f}/1.00")
        print(f"   Why: {explanation}")
        print()


if __name__ == "__main__":
    main()
