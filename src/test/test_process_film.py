from datetime import datetime

import age


def test_process_film(monkeypatch):
    film = {
        'id': 111,
        'release_date': '1999-6-11',
        'title': 'Fake title'
    }

    film_data = {
        'male': {'name': 'Actor Name', 'birthday': datetime.strptime('1964-10-10', '%Y-%m-%d'), 'age': 34},
        'female': {'name': 'Actress Name', 'birthday': datetime.strptime('1967-10-10', '%Y-%m-%d'), 'age': 31},
    }
    monkeypatch.setattr(age, "get_film_data", lambda url, query=None: film_data)

    data = age.process_film(film)
    assert data['diff'] == 3
    assert data['title'] == 'Fake title'
    assert data['year'] == '1999'
    assert data['female']['name'] == 'Actress Name'
    assert data['male']['name'] == 'Actor Name'
    assert data['female']['year'] == '1967'
    assert data['male']['year'] == '1964'
    assert data['female']['age'] == 31
    assert data['male']['age'] == 34
