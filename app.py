import streamlit as st
import json
import os

# Load movies from JSON file
def load_movies(filename='movies.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

# Save movies to JSON file
def save_movies(movies, filename='movies.json'):
    with open(filename, 'w') as file:
        json.dump(movies, file)

# Calculate movie rating
def calculate_rating(cinematography, acting, storytelling, enjoyed):
    if not (1 <= cinematography <= 3 and 1 <= acting <= 3 and 1 <= storytelling <= 3):
        raise ValueError("Cinematography, acting, and storytelling points should be between 1 and 3.")
    return cinematography + acting + storytelling + (1 if enjoyed else 0)

# Validate user inputs
def validate_inputs(title, genre, actor, year, cinematography, acting, storytelling):
    if not (title and genre and actor and year):
        st.error("Please fill out all fields.")
        return False
    if not (1 <= cinematography <= 3 and 1 <= acting <= 3 and 1 <= storytelling <= 3):
        st.error("Cinematography, acting, and storytelling points should be between 1 and 3.")
        return False
    return True

# Create a movie entry
def create_movie_entry(title, genre, actor, year, rating):
    return {
        'title': title,
        'genre': genre,
        'actor': actor,
        'year': year,
        'rating': rating
    }

# Add a new movie
def add_movie(movies, title, genre, actor, year, cinematography, acting, storytelling, enjoyed):
    if not validate_inputs(title, genre, actor, year, cinematography, acting, storytelling):
        return

    rating = calculate_rating(cinematography, acting, storytelling, enjoyed)
    movie = create_movie_entry(title, genre, actor, year, rating)
    movies.append(movie)
    save_movies(movies)
    st.success(f"Movie '{title}' added successfully with a rating of {rating}/10.")

# Search for movies
def search_movies(movies, query):
    query = query.lower()
    return [movie for movie in movies if query in movie['title'].lower() or query in movie['genre'].lower()]

# Sort movies by rating
def sort_movies(movies):
    movies.sort(key=lambda movie: movie['rating'], reverse=True)
    save_movies(movies)
    st.success("Movies sorted by rating in descending order.")
    return movies

# Delete a movie
def delete_movie(movies, title):
    movies = [movie for movie in movies if movie['title'].lower() != title.lower()]
    save_movies(movies)
    st.success(f"Movie '{title}' deleted successfully.")
    return movies

# Recommend movies based on criteria
def recommend_movies(movies, actor=None, genre=None, min_rating=0):
    if actor:
        movies = [movie for movie in movies if actor.lower() in movie['actor'].lower()]
    if genre:
        movies = [movie for movie in movies if genre.lower() in movie['genre'].lower()]
    return [movie for movie in movies if movie['rating'] >= min_rating]

# Initialize movies list
movies = load_movies()

# Streamlit UI
st.title("Movie Recommendation System")

menu = ["Add Movie", "Search Movies", "Sort Movies", "Delete Movie", "Recommend Movies"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Movie":
    st.subheader("Add a New Movie")
    title = st.text_input("Title")
    genre = st.text_input("Genre")
    actor = st.text_input("Actor")
    year = st.number_input("Year", min_value=1800, max_value=2024, step=1)
    cinematography = st.slider("Cinematography (1-3)", 1, 3)
    acting = st.slider("Acting (1-3)", 1, 3)
    storytelling = st.slider("Storytelling (1-3)", 1, 3)
    enjoyed = st.checkbox("Did you enjoy the movie?")
    if st.button("Add Movie"):
        add_movie(movies, title, genre, actor, year, cinematography, acting, storytelling, enjoyed)

elif choice == "Search Movies":
    st.subheader("Search for Movies")
    query = st.text_input("Enter title or genre to search for")
    if st.button("Search"):
        results = search_movies(movies, query)
        st.write(f"Found {len(results)} movies:")
        for movie in results:
            st.write(f"Title: {movie['title']}, Genre: {movie['genre']}, Actor: {movie['actor']}, Year: {movie['year']}, Rating: {movie['rating']}/10")

elif choice == "Sort Movies":
    st.subheader("Sort Movies by Rating")
    if st.button("Sort"):
        sorted_movies = sort_movies(movies)
        st.write("Movies sorted by rating in descending order:")
        for movie in sorted_movies:
            st.write(f"Title: {movie['title']}, Genre: {movie['genre']}, Actor: {movie['actor']}, Year: {movie['year']}, Rating: {movie['rating']}/10")

elif choice == "Delete Movie":
    st.subheader("Delete a Movie")
    title = st.text_input("Enter the title of the movie to delete")
    if st.button("Delete"):
        movies = delete_movie(movies, title)

elif choice == "Recommend Movies":
    st.subheader("Recommend Movies")
    actor = st.text_input("Actor (optional)")
    genre = st.text_input("Genre (optional)")
    min_rating = st.slider("Minimum rating", 0, 10, 5)
    if st.button("Recommend"):
        recommendations = recommend_movies(movies, actor, genre, min_rating)
        st.write(f"Movies matching the criteria:")
        for movie in recommendations:
            st.write(f"Title: {movie['title']}, Genre: {movie['genre']}, Actor: {movie['actor']}, Year: {movie['year']}, Rating: {movie['rating']}/10")
