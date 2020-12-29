import requests
from datetime import datetime, timedelta
import os
import settings


def get(url, query=None):
    if query is None:
        query = {}
    query['api_key'] = os.getenv('API_KEY')
    query['language'] = settings.LANGUAGE

    response = requests.request("GET", url, params=query)
    return response.json()


def get_age_in_release_date(release_date, birthday):
    return int((release_date - birthday) / timedelta(days=365))


def get_gender(cast):
    gender = False
    if cast['gender'] == 2:
        gender = 'male'
    elif cast['gender'] == 1:
        gender = 'female'
    return gender


def get_film_data(film):
    film_data = {'male': False, 'female': False}
    film_credits = get(f"{settings.BASE}/movie/{film['id']}/credits")
    for cast in film_credits['cast']:
        gender = get_gender(cast)
        if gender and film_data[gender] is False:
            person = get(f"{settings.BASE}/person/{cast['id']}")
            if person['birthday']:
                birthday = datetime.strptime(person['birthday'], '%Y-%m-%d')
                film_data[gender] = dict(
                    name=cast['name'],
                    birthday=birthday,
                    age=get_age_in_release_date(
                        release_date=datetime.strptime(film['release_date'], '%Y-%m-%d'),
                        birthday=birthday))
    return film_data


def process_film(film):
    response_data = {}
    release_date = datetime.strptime(film['release_date'], '%Y-%m-%d')
    if 'release_date' in film:
        film_data = get_film_data(film)
        if film_data['male'] and film_data['female']:
            response_data['title'] = film['title']
            response_data['year'] = release_date.strftime('%Y')
            response_data['female'] = {
                'name': film_data['female']['name'],
                'age': film_data['female']['age'],
                'year': film_data['female']['birthday'].strftime('%Y'),
            }
            response_data['male'] = {
                'name': film_data['male']['name'],
                'age': film_data['male']['age'],
                'year': film_data['male']['birthday'].strftime('%Y'),
            }
            response_data['diff'] = film_data['male']['age'] - film_data['female']['age']
    return response_data


def get_data(query):
    films = get(f'{settings.BASE}/search/movie', {'query': query})
    if len(films['results']) > 0:
        return process_film(films['results'][0])
