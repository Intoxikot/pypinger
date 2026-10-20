import os
import subprocess
from utility import *
from easycheck import *
from parallelcheck  import *

# Для тестов/демонстрации/отладки
# easycheck('ya.ru')
# easycheck("ya.ru", 10, 1000)

# Смена кодировки для читабельности
change_encode()

# Прочитать и вывести список хостов из файла
hosts = readfile('hosts.txt')
print('hosts:')
for host in hosts:
    print(host)
print()
multihostcheck(hosts)
os.system('pause')
