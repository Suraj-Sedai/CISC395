I am building a Movie Watchlist CLI app.

The project structure is:
movie_watchlist/
├── src/
│   ├── models.py
│   ├── storage.py
│   └── main.py
└── data/

Create src/models.py with:

1. Import dataclass and field from dataclasses.
2. Define a Movie dataclass:
   - title: str
   - genre: str
   - rating: float (0.0 to 10.0)
   - watched: bool = False
3. Define a Watchlist collection class:
   - __init__(): initializes an empty list of movies in self._movies.
   - add(movie: Movie): adds a movie to the list.
   - get_all() -> list[Movie]: returns all movies.
   - get_unwatched() -> list[Movie]: returns movies where watched == False.
   - get_top_rated(n: int = 5) -> list[Movie]: returns the top n movies sorted by rating (highest first).
   - mark_watched(index: int): sets self._movies[index].watched = True.
   - get_random_unwatched() -> Movie: returns a random movie from the unwatched list (use random.choice). Handle empty list by returning None.
   - __len__(): returns the number of movies.
   - get_by_index(index: int): returns the movie at the given index.

Do not add an if __name__ == "__main__" block.
Write the file directly to src/models.py.
