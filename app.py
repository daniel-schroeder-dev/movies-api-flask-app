from flask import Flask, render_template
from tmdbv3api import TMDb, Movie

with open("api_key.txt", mode="rt", encoding="utf-8") as api_key_file:
    api_key = api_key_file.read().strip()

app = Flask(__name__)

tmdb = TMDb()
tmdb.api_key = api_key
tmdb.language = "en"
tmdb.debug = True

movies_list = [
    "scarface",
    "goodfellas",
    "casino",
    "the godfather",
]

movie = Movie()

best_results = []
api_url = "https://image.tmdb.org/t/p/w500/"

for movie_title in movies_list:
    results = movie.search(movie_title)

    if not results:
        continue

    for result in results:
        if result.title.lower() == movie_title:
            best_result = {
                "title": result.title,
                "poster_path": api_url + result.poster_path,
                "slug": result.title.lower().replace(" ", "-"),
            }
            best_results.append(best_result)
            break


@app.route("/")
def home():
    return render_template("index.html", best_results=best_results)


@app.route("/movie/<slug>")
def movie(slug):
    movie = [
        best_result for best_result in best_results if best_result["slug"] == slug
    ][0]
    return render_template("movie.html", movie=movie)
