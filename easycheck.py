from utility import *

# Пинг с параметрами в режиме реального времени
def ping(host, packets='4', size='32'):
    execute_os(f'ping {host} -n {packets} -l {size}')

# Простая проверка, последовательно выполняет трассировку/пинги/резолв
# Выводит результат сразу на экран, но нет многопоточности, долгое выполнение команд, нет вывода в файл
# Прим. Количество пакетов и размер используются только в случае, если пинги проходят
def easycheck(host, packets='60', size='1000'):

    execute_os(f'nslookup {host}')
    execute_os(f'tracert {host}')

    # Проверка на icmp, выводит результат в переменную для анализа, но без вывода на экран
    print('checking ' + host + ' for icmp... ', end='')
    result = subprocess.run(
        'ping ' + host, capture_output=True, text=True, shell=True
    )
    # Если хост отвечает на icmp, отправляем много пакетов и разного размера
    if 'Reply' in result.stdout:
        print('success!')
        ping(host, packets)
        ping(host, packets, size)
    else:
        # В противном случае, все равно нужно вывести для наглядности + исключить ошибку
        print('failure!')
        ping(host)

    # Как оказалось, нужно видеть подключения и таблицу маршрутов, чтобы избежать некорректный результат
    execute_os('ipconfig /all')
    execute_os('route print')

    print()
    print(colortext('Execution complete', TEXT_BLUE))
    os.system('pause')
