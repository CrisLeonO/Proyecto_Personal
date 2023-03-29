import requests
from bs4 import BeautifulSoup


def scrap_top_25_movies_from():
    url = 'https://www.imdb.com/list/ls024149810/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    # iterando para encontrar los nombres de las peliculas
    movie_title = []
    for title in soup.findAll('h3', {'class': 'lister-item-header'}):
        titles = title.find('a', href=True).get_text()
        movie_title.append(titles)

    # iterando para encontrar los años de las peliculas
    year_movie = []
    for year in soup.findAll('h3', {'class': 'lister-item-header'}):
        years = year.find(
            'span', attrs={'class': 'lister-item-year text-muted unbold'}).text
        year_movie.append(years)
    for i in range(len(year_movie)):
        year_movie[i] = year_movie[i].replace('(', '').replace(')', '')

    # genero de las peliculas
    genre_list = []
    for genre in soup.findAll('span', attrs={'class': 'genre'}):
        genre = genre.get_text()
        genre_list.append(genre.strip())

    top_25 = [{'id': "", 'title': title, 'year': year, 'genre': genre, 'created_at': "", 'updated_at': ""}
              for title, year, genre in zip(movie_title, year_movie, genre_list)]

    return top_25
