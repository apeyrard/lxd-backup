from lxd_backup.frequencies import should_backup
from lxd_backup.frequencies import Frequency

def test_when_daily_and_monday_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.weekday', return_value=0)
    assert should_backup(Frequency.DAILY)
    
def test_when_weekly_and_tuesday_then_should_not_backup(mocker):
    mocker.patch('lxd_backup.frequencies.weekday', return_value=1)
    assert not should_backup(Frequency.WEEKLY)

def test_when_weekly_and_monday_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.weekday', return_value=0)
    assert should_backup(Frequency.WEEKLY)

def test_when_daily_and_saturday_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.weekday', return_value=5)
    assert should_backup(Frequency.DAILY)
    
def test_when_weekly_and_wednesday_and_chosen_day_is_wednesday_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.weekday', return_value=2)
    assert should_backup(Frequency.WEEKLY, target=2)

def test_when_monthly_and_first_day_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.day', return_value=1)
    assert should_backup(Frequency.MONTHLY)
    
def test_when_monthly_and_15_day_then_should_not_backup(mocker):
    mocker.patch('lxd_backup.frequencies.day', return_value=15)
    assert not should_backup(Frequency.MONTHLY)

def test_when_monthly_and_26_and_chosen_day_is_26_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.day', return_value=26)
    assert should_backup(Frequency.MONTHLY, target=26)

def test_when_bianually_and_january_first_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.month', return_value=1)
    mocker.patch('lxd_backup.frequencies.day', return_value=1)
    assert should_backup(Frequency.BIANUALLY)

def test_when_bianually_and_november_5_then_should_not_backup(mocker):
    mocker.patch('lxd_backup.frequencies.month', return_value=11)
    mocker.patch('lxd_backup.frequencies.day', return_value=5)
    assert not should_backup(Frequency.BIANUALLY)

def test_when_bianually_and_july_first_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.month', return_value=7)
    mocker.patch('lxd_backup.frequencies.day', return_value=1)
    assert should_backup(Frequency.BIANUALLY)

def test_when_bianually_and_october_26_and_target_is_april_26_then_should_backup(mocker):
    mocker.patch('lxd_backup.frequencies.month', return_value=10)
    mocker.patch('lxd_backup.frequencies.day', return_value=26)
    assert should_backup(Frequency.BIANUALLY, target={'day': 26, 'month': 4})

def test_when_unknown_frequency_then_should_not_backup(mocker):
    assert not should_backup(42)
