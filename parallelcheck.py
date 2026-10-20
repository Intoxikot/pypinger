import queue
from threading import Thread
from utility import *

# Директория, куда пишется результат
output_dir = 'output/' #
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Повторяет функционал и содержимое easycheck, но со значительными модификациями

# Многопоточный вариант выполнения пинга, с необязательным выводом в файл
def ping(thread_chain, host, filename=None, packets='4', size='32'):
    thread_chain.append(execute_thread(f'ping {host} -n {packets} -l {size}', filename))

# Здесь логика следующая - команд много, выполняться могут долго, но результат надо видеть и писать сразу
def parallelcheck(thread_chain: list, host: str, packets='80', size='1000'):
    # Пересоздаем файл, иначе будут перемешиваться старые и новые результаты
    # Можно улучшить через временную метку - добавлять в сам файл, в имя файла или саму директорию (пока не знаю как лучше, сейчас проще)
    filename = f"{output_dir}{host}.txt"
    open(filename, 'w').close()

    thread_chain.append(execute_thread(f'nslookup {host}', filename))
    thread_chain.append(execute_thread(f'tracert {host}', filename))

    # Проверка на icmp, выводит результат в переменную для анализа, но без вывода на экран
    # Многопоточность здесь страдает, от результата зависит итоговая цепочка потоков, но небольшая экономия в том, что отправка идет по одному пакету
    print('checking ' + colortext(host, TEXT_YELLOW) + ' for icmp... ', end='')
    icmp = False
    for i in range(2):
        check = execute_subprocess(f"ping {host} -n 1", value=None, notify=False, filename=None)
        if 'Reply' in check.get():
            icmp = True
            break

    ping(thread_chain, host, filename) # это все равно в файл пишем (чтобы СРАЗУ видеть результаты пингов)
    # а тут допом больше пакетов и разного размера
    if icmp:
        print(colortext('success!', TEXT_BLUE))
        ping(thread_chain, host, filename, packets)
        ping(thread_chain, host, filename, packets, size)
    else:
        print(colortext('failure!', TEXT_RED))

    return thread_chain # пока не запускаем, передаем в "центр управления полетами"

# Вспомогательная функция, выводит информацию о системе
def systemcheck(thread_chain: list):
    filename = f"{output_dir}netinfo.txt"
    thread_chain.append(execute_thread('ipconfig /all', filename))
    thread_chain.append(execute_thread('route print', filename))
    return thread_chain

# Распараллеливает для списка хостов
def multihostcheck(hosts: list):
    thread_chain = []
    systemcheck(thread_chain)
    for host in hosts:
        parallelcheck(thread_chain, host)
    run_chain(thread_chain)
    print(colortext('execution complete', TEXT_BLUE))
