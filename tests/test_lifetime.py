import arrow

from lxd_backup.time import (today,
                             day,
                             weekday,
                             month,
                             get_date_from_lifetime)


def test_today(mocker):
    date = arrow.get('2018-12-07')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert today() == '2018-12-07'


def test_today_other_case(mocker):
    date = arrow.get('1992-02-28')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert today() == '1992-02-28'


def test_day(mocker):
    date = arrow.get('1992-02-08')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert day() == 8


def test_day_other_case(mocker):
    date = arrow.get('2000-01-31')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert day() == 31


def test_tuesday_is_1(mocker):
    date = arrow.get('2018-09-25')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert weekday() == 1


def test_monday_is_0(mocker):
    date = arrow.get('2018-09-24')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert weekday() == 0


def test_month(mocker):
    date = arrow.get('1992-02-08')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert month() == 2


def test_month_other_case(mocker):
    date = arrow.get('2000-11-30')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert month() == 11


def test_when_given_days_then_lifetime_is_current_date_plus_days(mocker):
    date = arrow.get('2018-12-07')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert get_date_from_lifetime({'days': 1}) == '2018-12-08'


def test_when_given_0_days_then_lifetime_is_current_date(mocker):
    date = arrow.get('1999-05-28')
    mocker.patch('lxd_backup.time.Arrow.utcnow', return_value=date)
    assert get_date_from_lifetime({'days': 0}) == '1999-05-28'
