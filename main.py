transactions_data = {}
user_data = {}


def hash_pass(login_save, password_hash):
    h = 0
    hh = 1
    num = 1234001651
    for i in password_hash:
        h += ord(i)
        hh *= ord(i)
    h = h % num
    hh = hh % num
    hashed_pass = str(h) + str(hh)
    with open(f'login.passwordhash.txt', 'a', encoding='UTF=8') as file:
        file.write(f'{login_save} {hashed_pass}\n')
    return login_save, hashed_pass


def pass_try(user_pass, password_now):
    h = 0
    hh = 1
    num = 1234001651
    for i in user_pass:
        h += ord(i)
        hh *= ord(i)
    h = h % num
    hh = hh % num
    user_pass = str(h) + str(hh)
    if str(user_pass) == str(password_now):
        return True
    else:
        return False


def create_user():
    year = 2024
    balance = 0
    name = input('Введите ФИО: ')
    try:
        age = int(input('Внимание: Год рождения должен состоять только из цифр!' + '\nВведите год рождения: '))
        login = str(input('Придумайте LOGIN: '))
        password = str(input('Придумайте пароль: '))
        print(f'Создан аккаунт: {name}  ({str(year - age)} лет)')
    except ValueError:
        age = int(input('Год рождения должен состоять из цифр, введите число:'))
        login = str(input('Придумайте LOGIN: '))
        password = str(input('Придумайте пароль: '))
        print(f'Создан аккаунт: {name}  ({str(year - age)} лет)')
    print('Аккаунт успешно зарегистрирован!')
    login, password = hash_pass(login, password)
    with open(f'{login}_data_user.txt', 'w', encoding='UTF-8') as file:
        file.write('name.' + str(name) + '\n' + 'age.' + str(age) + '\n')
    with open(f'{login}_balance.txt', 'w', encoding='UTF-8') as file:
        file.write('balance ' + str(balance))
    with open(f'{login}_transaction.txt', 'w', encoding='UTF-8') as file_data_transaction:
        file_data_transaction.write('')
    with open(f'{login}_limit_data.txt', 'w', encoding='UTF-8') as file:
        file.write('limite 0')
    with open(f'{login}_future_pay.txt', 'w', encoding='UTF-8') as file:
        file.write('')
    return login, password, balance


def money_up(balance, login_to_up):
    try:
        cash_up = int(input('Введите сумму пополнения: '))
        balance += cash_up
        print('Счет успешно пополнен!')
        with open(f'{login_to_up}_balance.txt', 'w', encoding='UTF-8') as file_user_balance:
            file_user_balance.write('balance ' + str(balance))
        return balance

    except ValueError:
        print()
        print('Возможно вы пытаетесь ввести буквы!')
        print()
        return balance


def money_to_cash(balance, password, login_to_cash):
    try:
        user_password = input('Введите пароль: ')
        if pass_try(user_password, password):
            cash_down = int(input('Ваш баланс: ' + str(balance) + 'руб. Введите сумму для снятия: '))
            if cash_down > balance:
                print('Недостаточно средств для снятия.')
            elif cash_down <= 0:
                print('Сумма указана некорректно, попробуйте ещё раз! ')
            else:
                balance -= cash_down
                print('Снятие успешно завершено, ваш баланс: ' + str(balance))
                return balance
        else:
            print('Неверный пароль! Попробуйте ещё раз.')

        with open(f'{login_to_cash}_balance.txt', 'w', encoding='UTF-8') as file_user_balance:
            file_user_balance.write('balance ' + str(balance))
        return balance
    except ValueError:
        print()
        print('Чтобы снять денежные средства, необходимо указать верную сумму, возможно вы пытаетесь ввести слово!')
        print()


def check_balance(balance, password):
    try:
        user_password = str(input('Введите пароль: '))
        if pass_try(user_password, password):
            print('Ваш баланс: ' + str(balance))
        else:
            print('Неверный пароль! Попробуйте ещё раз.')
    except:
        print('Непредвиденная ошибка!')
        print()


def transaction(transactions, login_tran):
    try:
        expected_amount = int(input('Введите сумму ожидаемого пополнения: '))
        comment = str(input('Уточните пожалуйста назначение пополнения: '))
        transactions[comment] = expected_amount
        count_tran = len(transactions)
        print('Ожидается ' + str(count_tran) + ' операций(я)')
        with open(f'{login_tran}_transaction.txt', 'a', encoding='UTF=8') as file_transaction:
            file_transaction.write(str(comment) + ' ' + str(expected_amount) + '\n')
    except ValueError:
        print()
        print('Вы вводите буквы, нужно ввести число!! ')
        print()


def max_limite(login_limit):
    try:
        limite = int(input('Введите максимально допустимую сумму которая должна быть на счету: '))
        with open(f'{login_limit}_limit_data.txt', 'w', encoding='UTF-8') as file:
            file.write('limite ' + str(limite))
        return limite
    except ValueError:
        print()
        print('Вы вводите буквы, нужно ввести число!! ')
        print()


def ran_transactions(transactions, limite, login_tran):
    summ = 0
    try:
        for comment, expected_amount in list(transactions.items()):
            if int(expected_amount) < limite:
                summ += int(expected_amount)
                print(f'Транзакция {comment} на сумму {expected_amount} руб. успешно применена.')
                del transactions[comment]
            else:
                print(
                    f'Транзакция {comment} на сумму {expected_amount} руб. Не может быть применена(превышен лимит или '
                    f'не установлен).')
        with open(f'{login_tran}_transaction.txt', 'w', encoding='UTF=8') as file_transaction:
            for comment, expected_amount in list(transactions.items()):
                file_transaction.write(str(comment) + ' ' + str(expected_amount) + '\n')
        return summ
    except:
        print('Непредвиденная ошибка!')


def stat_expected_amount(transactions):
    rub = {}
    try:
        for comment, expected_amount in transactions.items():
            if expected_amount in rub:
                rub[expected_amount] += 1
            else:
                rub[expected_amount] = 1
        if rub != {}:
            for summ, num_payments in rub.items():
                print(str(summ) + ' руб: ' + str(num_payments) + ' платеж(а)')
        else:
            print('Нет запланированных операций! ')
    except:
        print('Непредвиденная ошибка!')


def filter_transaction_sub(transactions):
    for key, value in transactions.items():
        yield key, value


def filter_transaction(transactions):
    print()
    print('Данная операция выведет все отложенные пополнения которые больше введенного числа.')
    print()
    threshold = int(input('Введите число от которого будем проверять сумму транзакций: '))
    for transactions in filter_transaction_sub(transactions):
        if int(transactions[1]) >= threshold:
            print(f'Транзакция больше {threshold} рублей.: {transactions[0]}  {transactions[1]} р.')


def future_pay(user_password, balance_user):
    login = str(input('Введите логин : '))
    if login == user_data['login']:
        password = (input('Введите пароль : '))
        if pass_try(password, user_password):
            login_to_pay = str(input('Введите логин на который хотите отправить деньги: '))
            summ = int(input('Введите сумму пополнения: '))
            if summ <= balance_user:
                with open(f'{login_to_pay}_balance.txt', encoding='UTF-8') as file:
                    for line in file:
                        name, balance = line.split()
                        balance = int(balance)
                        balance += summ
                        balance_user -= summ
                        balance = str(balance)
                with open(f'{login_to_pay}_balance.txt', 'w', encoding='UTF-8') as file:
                    file.write(f'balance {balance}')
                with open(f'{login}_balance.txt', 'w', encoding='UTF-8') as file:
                    file.write(f'balance {balance_user}')
                print(f'Отложенный платеж успешно выполнен на сумму {summ}, отправлен на логин: {login_to_pay}')
                print(f'На вашем счету осталось {balance_user}')
                return balance_user
            else:
                with open(f'{login}_future_pay.txt', 'a', encoding='UTF-8') as file:
                    file.write(f'{login_to_pay} {summ}\n')
                print(f'Не удалось пополнить указанный логин! операция будет выполнина, как только на балансе будет'
                      f' достаточно средств')
                return balance_user
        else:
            print('Неверный пароль! ')
    else:
        print('Неверный логин')


def future_pay_act(user_balance, user_login):
    try:
        with open(f'{user_login}_future_pay.txt') as file:
            for line in file:
                if line:
                    login_to_pay, summ = line.split()
                    if int(summ) <= user_balance:
                        with open(f'{login_to_pay}_balance.txt', encoding='UTF-8') as file1:
                            for line1 in file1:
                                name, balance = line1.split()
                            balance = int(balance)
                            balance += int(summ)
                            user_balance -= int(summ)
                            balance = str(balance)
                            with open(f'{login_to_pay}_balance.txt', 'w', encoding='UTF-8') as file:
                                file.write(f'balance {balance}')
                            with open(f'{user_login}_balance.txt', 'w', encoding='UTF-8') as file:
                                file.write(f'balance {user_balance}')
                            print(f'Отложенный платеж выполнен на сумму {summ}, отправлен на логин: {login_to_pay}')
                            print(f'На вашем счету осталось {user_balance}')
                            with open(f'{user_login}_future_pay.txt', 'w', encoding='UTF-8') as file:
                                file.write('')
                            return user_balance
                else:
                    print('Недостаточно средств для перевода! ')
                    return user_balance
    except:
        print()


def recover_data_YES(user_login, transactions, user_data_func):
    with open(f'{user_login}_transaction.txt', encoding='UTF-8') as file_data_transaction:
        for line in file_data_transaction:
            if line == '\n':
                continue
            else:
                comment, expected_amount = line.split()
                transactions[comment] = expected_amount

    with open(f'{user_login}_data_user.txt', encoding='UTF-8') as file_user_data:
        for line in file_user_data:
            if line == '\n':
                continue
            else:
                key, valume = line.split('.')
                user_data_func[key] = valume

    with open(f'{user_login}_balance.txt', encoding='UTF-8') as file_user_balance:
        for line in file_user_balance:
            key, valume = line.split()
            user_data_func[key] = valume

    with open(f'{user_login}_limit_data.txt', encoding='UTF-8') as file:
        for line in file:
            if line != '':
                key, valume = line.split()
                user_data_func[key] = valume
            else:
                continue

    with open(f'login.passwordhash.txt', encoding='UTF-8') as file_hash:
        for line in file_hash:
            if user_login in line:
                key, valume = line.split()
                user_data_func[key] = valume
            else:
                continue

    print(f'С возвращением {user_data_func['name']} !')
    print(f'Ваш баланс: {user_data_func['balance']} р.')
    return user_data_func


def recover_login(transactions, user_data_func):
    v = {}
    while True:
        login = input('Введите логин: ')
        password = input('Введите пароль: ')
        try:
            with open(f'login.passwordhash.txt', encoding='UTF-8') as file_hash:
                for line in file_hash:
                    key, valume = line.split()
                    v[key] = valume
                if login in v:
                    if pass_try(password, v[login]):
                        user_data = recover_data_YES(login, transactions, user_data_func)
                        user_data['login'] = login
                        return user_data
                else:
                    print()
                    print('Неверный пароль или логин!')
                    print()
        except:
            print("Аккаунт с таким логином не найден")
            exit()


def recover_sign_in():
    login, password, balance = create_user()
    return login, password, balance


def operation_user():
    print('-----------------Банковское приложение-----------------')
    print('Меню:')
    print('1.Положить деньги на счет')
    print('2.Снять деньги')
    print('3.Вывести баланс на экран')
    print('4.Выставление ожидаемого пополнения')
    print('5.Установить максимальный лимит')
    print('6.Выполнить запланированные транзакции')
    print('7.Статистика по ожидаемым пополнениям')
    print('8.Фильтрация отложенных пополнений')
    print('9.отложенный платеж')
    print('10.Выйти из программы')
    operation_in = int(input('Введите номер операции: '))
    return operation_in


if __name__ == "__main__":
    try:
        Bank_login = input('Добро пожаловать, вы хотите зарегистрироваться или войти в аккаунт?(Войти/Рег): ')
        if Bank_login == 'Войти':
            user_data = recover_login(transactions_data, user_data)
            login = user_data['login']
            password = user_data[str(login)]
            balance = int(user_data['balance'])
            limite = int(user_data['limite'])
        else:
            login, password, balance = recover_sign_in()
            user_data['login'] = login
    except ValueError:
        print('Некорректный ввод!!')

    while True:
        try:
            future_pay_act(balance, login)
            operation = operation_user()
            if operation == 1:
                balance = money_up(balance, login)
                print()

            elif operation == 2:
                balance = money_to_cash(balance, password, login)
                print()

            elif operation == 3:
                check_balance(balance, password)
                print()

            elif operation == 4:
                transaction(transactions_data, login)
                print()

            elif operation == 5:
                limite = max_limite(login)
                print()

            elif operation == 6:
                balance += ran_transactions(transactions_data, limite, login)
                with open(f'{login}_balance.txt', 'w', encoding='UTF=8') as file_user_balance:
                    file_user_balance.write('balance ' + str(balance))
                print()

            elif operation == 7:
                stat_expected_amount(transactions_data)
                print()

            elif operation == 8:
                filter_transaction(transactions_data)
                print()

            elif operation == 9:
                balance = future_pay(password, balance)

            elif operation == 10:
                print('Спасибо за пользование нашей программой, до свидания!')
                break
            else:
                print('Некорректный номер операции, попробуйте снова :(')
        except ValueError:
            print('Некорректный ввод!')
