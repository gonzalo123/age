#!/usr/bin/env python

import requests
from datetime import datetime, timedelta
import sys
import os

LANGUAGE = 'en-EN'
BASE = 'https://api.themoviedb.org/3'


def get(url, query=None):
    if query is None:
        query = {}
    query['api_key'] = os.getenv('API_KEY')
    query['language'] = LANGUAGE

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


def process_film(film):
    film_data = {'male': False, 'female': False}
    if 'release_date' in film:
        film_credits = get(f"{BASE}/movie/{film['id']}/credits")
        for cast in film_credits['cast']:
            gender = get_gender(cast)
            if gender and film_data[gender] is False:
                person = get(f"{BASE}/person/{cast['id']}")
                if person['birthday']:
                    birthday = datetime.strptime(person['birthday'], '%Y-%m-%d')
                    film_data[gender] = dict(
                        name=cast['name'],
                        birthday=birthday,
                        age=get_age_in_release_date(
                            release_date=datetime.strptime(film['release_date'], '%Y-%m-%d'),
                            birthday=birthday))
        return film_data


def get_data(query):
    films = get(f'{BASE}/search/movie', {'query': query})
    response_data = {}
    if len(films['results']) > 0:
        film = films['results'][0]
        release_date = datetime.strptime(film['release_date'], '%Y-%m-%d')
        film_data = process_film(film)
        title = film['title']
        male = film_data['male']
        female = film_data['female']
        if male and female:
            years = male['age'] - female['age']
            response_data['title'] = title
            response_data['year'] = release_date.strftime('%Y')
            response_data['female'] = {
                'name': female['name'],
                'age': female['age'],
                'year': female['birthday'].strftime('%Y'),
            }
            response_data['male'] = {
                'name': male['name'],
                'age': male['age'],
                'year': male['birthday'].strftime('%Y'),
            }
            response_data['diff'] = years
    return response_data


if __name__ == '__main__':
    data = get_data(sys.argv[1:][0])

    print("")
    print(f"{data['title']} ({data['year']})")
    print("")
    print(f"{data['female']['name']} - {data['female']['age']} years old ({data['female']['year']})")
    print(f"{data['male']['name']} - {data['male']['age']} years old ({data['male']['year']})")
    print(f"Years of difference: {data['diff']}")
    print("")
