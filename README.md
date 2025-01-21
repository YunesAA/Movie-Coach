# Movie-Recommender
Technologies: Python, SQLite, OMDb API 


## Overview
This Python-based application allows users to search for movies, manage a watchlist, view recommendations, and follow/unfollow other users. The application interacts with the OMDb API to fetch movie details and uses an SQLite database to store user data, movie details, ratings, and relationships.

---

## Features
1. **User Authentication**
   - Log in or sign up to create an account.
   - User credentials are securely stored in the `User` table.

2. **Movie Search**
   - Search for movies by title using the OMDb API.
   - View detailed movie information, including title, year, genre, director, actors, and IMDb rating.
   - Option to add movies to the watchlist.

3. **Watchlist Management**
   - View all movies in the user's watchlist.
   - Access detailed information about movies in the watchlist.

4. **Ratings and Comments**
   - Add ratings and comments for movies.
   - View ratings and comments from other users.

5. **Recommendations**
   - Get personalized movie recommendations based on the user's watchlist and highly-rated movies.

6. **Social Features**
   - Follow or unfollow other users.
   - View followers and following lists.

---

## Dependencies
- `sqlite3`: For database operations.
- `requests`: For interacting with the OMDb API.
- `time`: For adding delays in menu navigation.

---

## Setup Instructions
1. Install Python
2. Install required libraries using `pip install requests`.
3. Set up the database using the provided `database_maker.sql` file.
4. Replace `INSERT API KEY` with a valid [OMDb API](https://www.omdbapi.com/apikey.aspx) key.
5. Run the application using `python main.py`.

---

## Future Improvements
- Add a chat feature for users.
- Implement a graphical user interface (GUI).
- Add support for advanced search filters (e.g., genre, year).
- Improve the recommendations feature

---

## License
none.

