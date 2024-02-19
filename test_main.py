from main import check_balance
from main import stat_expected_amount
from main import filter_transaction_sub
from main import filter_transaction
from main import pass_try



transactions_data = {}
transactions_data_2 = {'авдлав': 300}



def test_pass_try():
    assert True == pass_try('123', 150124950)


def test_pass_try():
    assert False == pass_try('143', 150124950)


def test_password_int(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: 123)
    check_balance(2000, '150124950')
    out, err = capfd.readouterr()
    assert out == 'Ваш баланс: 2000\n'


def test_password_not_True(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "123")
    check_balance(2000, '1')
    out, err = capfd.readouterr()
    assert out == 'Неверный пароль! Попробуйте ещё раз.\n'


def test_stat_expected_amount_no_operations(capfd):
    stat_expected_amount(transactions_data)
    out, err = capfd.readouterr()
    assert out == 'Нет запланированных операций! \n'


def test_stat_expected_amount_operations(capfd):
    stat_expected_amount(transactions_data_2)
    out, err = capfd.readouterr()
    assert out == '300 руб: 1 платеж(а)\n'


def test_filter_transaction_sub():
    for i in filter_transaction_sub(transactions_data_2):
        assert i == ('авдлав', 300)


def test_filter_transaction(mocker, monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: int(300))
    mocker.patch('main.filter_transaction_sub', return_value=[('fdfdf', 2000), (',g,g,', 3000)])
    filter_transaction(transactions_data)
    out, err = capfd.readouterr()
    assert out == ('\nДанная операция выведет все отложенные пополнения которые больше введенного числа.\n'
                   '\n'
                   'Транзакция больше 300 рублей.: fdfdf  2000 р.\n'
                   'Транзакция больше 300 рублей.: ,g,g,  3000 р.\n')
