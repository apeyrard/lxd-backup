from lxd_backup.lifetime import get_date_from_lifetime

def test_when_given_days_then_lifetime_is_current_date_plus_days(mocker):
    mocker.patch('lxd_backup.lifetime.today', return_value='2018-12-7')
    assert get_date_from_lifetime({'days': 1}) == '2018-12-8'
