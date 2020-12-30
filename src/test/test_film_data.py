import age
import settings


def test_get_film_data(monkeypatch):
    film = {
        'id': 111,
        'release_date': '1999-6-11',
        'title': 'Fake title'
    }

    film_credits = {
        'cast': [
            {'gender': 1, 'id': 1, 'name': 'Actress Name'},
            {'gender': 2, 'id': 2, 'name': 'Actor Name'}
        ]
    }

    person1 = {
        'birthday': '1964-10-10',
    }

    person2 = {
        'birthday': '1967-10-10',
    }

    fake_responses = {
        f"{settings.BASE}/movie/111/credits": film_credits,
        f"{settings.BASE}/person/1": person1,
        f"{settings.BASE}/person/2": person2,
    }

    monkeypatch.setattr(age, "get", lambda url, query=None: fake_responses[url])

    data = age.get_film_data(film)
    assert data['female']['name'] == 'Actress Name'
    assert data['male']['name'] == 'Actor Name'
    assert data['female']['birthday'].year == 1964
    assert data['male']['birthday'].year == 1967
    assert data['female']['age'] == 34
    assert data['male']['age'] == 31
