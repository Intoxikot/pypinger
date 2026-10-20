# Вспомогательные системные функции
import os
import queue
import subprocess
import threading
from queue import Queue
from typing import TextIO

"""
Консольные теги для окрашивания текста, стоило бы выделить в отдельный модуль, нашел и более занимательные вариации, но это лишнее
91 - red, 92 - green, 93 - yellow, 94 - blue
"""
COLOR_CH = '\033'
CLOSE_CH = '[0m'
TEXT_RED = '[91m'
TEXT_GREEN = '[92m'
TEXT_YELLOW = '[93m'
TEXT_BLUE = '[94m'

# Главный по локдаунам, можно везде засунуть по своей переменной, но не настолько высока нагрузка
lock = threading.Lock()

# Кракозябрен ахтунг. Смена кодировки в консоли (запустить вначале один раз), utf-8 на win-1251
def change_encode():
    print('change encode')
    os.system('chcp 65001')
    print()

# Построчное чтение файла с косметикой
def readfile(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    return lines

# Косметичка, окрашивает текст в консоли
def colortext(text, color):
    return COLOR_CH + color + text + COLOR_CH + CLOSE_CH

# Выполнение системной команды + вывод самой команды
# Вариант через os.system, исполнение команды в реальном времени
def execute_os(cmd):
    #print(cmd)
    print(colortext(cmd, TEXT_GREEN))
    os.system(cmd)

# Выполнение системной команды через subprocess (работает как альтернатива os.system). Здесь предназначен для использования в потоках и исполнения в фоне
# Отследить прогресс выполнения команды нельзя или получить промежуточный вывод, но имеет уведомления о выполнении/завершении команды (можно отключить)
def execute_subprocess(cmd, value=None, notify=True, filename=None):
    if notify:
        with lock:
            print(f"execution started: {cmd}")
    result = subprocess.run(
        cmd, capture_output=True, text=True, shell=True
    )
    # Результат выполнения пишется во вспомогательную переменную
    # Нововведение: она создается в любом случае и передается как результат
    if value is None:
        value = queue.Queue()
    value.put(result.stdout)
    # Добавляет поддержку вывода в файл (если требуется), отчасти костыль
    if filename is not None:
        with lock:
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(result.stdout + '\n')
    if notify:
        with lock:
            print(f"execution complete: {cmd}")
    return value

# Запуск команды в потоке. Поток добавляется в цепочку, потом с ней можно делать всякое
# Сейчас это уже просто удобная заготовка
def execute_thread(cmd: str, filename):
    thread = threading.Thread(target=execute_subprocess, args=(cmd,None,True,filename,))
    # thread_chain.append(thread)
    # thread.start() # что лучше - мгновенный или централизованный запуск?
    return thread

def run_chain(thread_chain: list):
    for thread in thread_chain:
        thread.start()
    for thread in thread_chain:
        thread.join()
