from datetime import datetime

import age


def test_gender():
    assert age.get_gender({'gender': 2}) == 'male'
    assert age.get_gender({'gender': 1}) == 'female'
    assert age.get_gender({'gender': 0}) is False


def test_get_age_in_release_date():
    assert age.get_age_in_release_date(
        release_date=datetime.strptime('1999-6-11', '%Y-%m-%d'),
        birthday=datetime.strptime('1964-10-10', '%Y-%m-%d')
    ) == 34
    assert age.get_age_in_release_date(
        release_date=datetime.strptime('1999-6-11', '%Y-%m-%d'),
        birthday=datetime.strptime('1967-10-10', '%Y-%m-%d')
    ) == 31
