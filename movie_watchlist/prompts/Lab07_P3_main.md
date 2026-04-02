I am building a Movie Watchlist CLI app.

The project structure is:
movie_watchlist/
├── src/
│   ├── models.py
│   ├── storage.py
│   └── main.py
└── data/

Read src/models.py and src/storage.py first, then create src/main.py.

src/main.py must:
1. Fix the import path at the top so it works when run from the movie_watchlist/ root:
       import sys, os
       sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

2. Import Movie, Watchlist from src.models.
   Import load_movies, save_movies from src.storage. (Assume storage.py exists and works like the one in trip_notes).

3. On startup: watchlist = load_movies().

4. Show this menu in a loop until the user quits:
       === Movie Watchlist ===
       [1] Add movie
       [2] View all movies
       [3] View unwatched movies
       [4] Mark movie as watched
       [5] Get random recommendation
       [6] View top rated
       [7] Quit

5. Implement each option:
   [1] Add movie: input title, genre, rating (float) -> Movie -> watchlist.add() -> save_movies()
   [2] View all: list all movies with their status and rating.
   [3] View unwatched: list only movies not yet watched.
   [4] Mark as watched: show numbered list of unwatched, user picks one, update and save.
   [5] Random recommendation: show one random unwatched movie.
   [6] Top rated: show top 5 movies by rating.
   [7] Quit: print "Goodbye!" and exit.

Handle invalid inputs gracefully with print statements.
Write the file directly to src/main.py.
