from app import app
from flask import Flask, render_template, request, redirect, session, flash
from app.config.mysqlconnection import connectToMySQL
from app.models.movie import Movie
from app.models.user import User


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/main')
    data = {
        "id": session['user_id']
    }
    user = User.get_one_user(data)
    top_25_movies = Movie.get_top_25_movies()
    for movie in top_25_movies:
        data_movie = {
            'title': movie['title'],
            'year': movie['year'],
            'genre': movie['genre']
        }
        Movie.add_movie(data_movie)
    list_movies = Movie.get_all_movies()
    favorites = Movie.show_favorites(data)
    is_favorite = Movie.is_favorite(data)

    for movie in list_movies:
        if movie in favorites:
            movie['isfavorite'] = True
        else:
            movie['isfavorite'] = False

    return render_template("dashboard.html", user=user, list_movies=list_movies, favorites=favorites, isfavorite=is_favorite)


@app.route('/show_favorites', methods=['POST'])
def show_favorites():
    data = {
        'movie_id': request.form['id'],
        "user_id": session['user_id']
    }
    return redirect('/profile')


@app.route('/dashboard/remove/<int:id>')
def destroy(id):
    data = {
        'id': id,
        "user_id": session['user_id']
    }
    Movie.delete_favorite(data)
    return redirect('/dashboard')


@app.route('/add_to_favorites/<int:id>', methods=['POST'])
def add_to_favorites(id):
    data = {
        'movie_id': id,
        "user_id": session['user_id']
    }
    Movie.add_favorite(data)
    print(data)
    return redirect("/dashboard")
