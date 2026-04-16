"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: a late-night study session listener
    # Wants calm, acoustic lofi with low energy to stay focused
    user_prefs = {
        "favorite_genre": "ambient",     # strong genre loyalty — wants lo-fi texture
        "favorite_mood":  "peaceful",  # current context: studying, not relaxing
        "target_energy":  0.35,       # low energy — nothing jarring or loud
        "likes_acoustic": True,       # prefers organic, warm sounds over synthetic
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # ── Header ────────────────────────────────────────────────────────────────
    width = 60
    print()
    print("=" * width)
    print("  Music Recommender -- Top 5 Recommendations")
    print(
        f"  Profile:  genre={user_prefs['favorite_genre']}"
        f"  |  mood={user_prefs['favorite_mood']}"
        f"  |  energy={user_prefs['target_energy']}"
    )
    print("=" * width)

    # ── Results ───────────────────────────────────────────────────────────────
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled  = round((score / 4.0) * 20)
        score_bar   = "[" + "#" * bar_filled + "-" * (20 - bar_filled) + "]"

        print()
        print(f"  #{rank}  {song['title']}  by {song['artist']}")
        print(f"       Score: {score:.2f} / 4.0  {score_bar}")
        for reason in explanation.split(" · "):
            print(f"       - {reason}")
        print("  " + "-" * (width - 2))

    print()


if __name__ == "__main__":
    main()
