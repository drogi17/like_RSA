from random import randint
import math, sys, pickle, os

# Ссылка на материал: http://enisey.name/umk/pzis/ch18s07.html

def prost(chislo):
    if chislo % 2 == 0:
        return False
    else:
        for n in range(3, round(chislo/2)):
            if chislo % n == 0:
                return False
    return True


def get_e(n, fi):
    #подбор числа е, которое должно соответствовать двум критериям: 
    #           быть меньше n и не иметь общих множителей с fi(n)
    for e_m in range(round(n/2), n-1):
        if not fi%e_m == 0:
            return e_m

def get_d(e, n):
    d = 3
    while True:
        if (e*d-1)%n == 0 and d != e:
            return d
        d += 1

def p_and_q():
    rand_q = randint(100, 1000)
    rand_p = randint(100, 1000)
    while not prost(rand_q):
        rand_q -= 1
    while not prost(rand_p):
        rand_p -= 1
    return rand_p, rand_q


def cripting(e, n, m_str):
    message_int = 0
    for char in m_str:
        message_int = int(str(message_int) + str(ord(char)) + '00000')
    message_int = int(str(message_int) + str(ord(char)) + '000100')
    full_cycles = message_int // n
    c = (message_int ** e) % n
    return g, c

def encripting(c, d, n, g):
    get_m = ((c ** d) % n) + (n*g)
    str_to_print = ''
    num = 0
    while num <= len(str(get_m).split('00000'))-2:
        char = str(get_m).split('00000')[num]
        if not char == '':
            str_to_print += chr(int(char))
        num += 1
    return str_to_print


def check_for_files(action):
    if action == 'read':  
        if not os.path.exists('secret'):
            return False
        else:
            return True
    elif action == 'write':
        if not os.path.exists('publick'):
            return False
        else:
            return True




if '--create-keys' in sys.argv:
    p, q = p_and_q()    # Пара простых чисел для генерации ключей
    n   = p*q           # Модуль сравнения
    fi  = (p-1)*(q-1)   # Функция Эйлера
    e   = get_e(n, fi)  
    d   = get_d(e, n)
    with open('publick', 'wb') as f:
       pickle.dump([e, n], f)
    with open('secret', 'wb') as f:
       pickle.dump([d, n], f)


elif '--encrypt' in sys.argv:
    if not check_for_files('write'):
        print('ERROR[0]: generate keys or get a key to open.')
        sys.exit()
    index = sys.argv.index('--encrypt') + 1
    with open('publick', 'rb') as f:
       get_data = pickle.load(f)
    e, n = get_data
    g, c = cripting(e, n, sys.argv[index])
    with open('message', 'w') as f:
        f.write(str(c) + ':' + str(g))
    print('finish')

elif '--decrypt' in sys.argv:
    if not check_for_files('read'):
        print('ERROR[0]: generate keys or get a key to open.')
        sys.exit()
    index = sys.argv.index('--decrypt') + 1
    try:
        if os.path.exists(sys.argv[index]):
            with open(sys.argv[index], 'r') as f:
                sys.argv[index] = f.read()
        text = sys.argv[index].split(':')
    except IndexError:
        print('ERROR[1]: Incorrect data')
        sys.exit()
    if len(text) != 2:
        print('ERROR[1]: Incorrect data')
        sys.exit()
    c = int(text[0])
    g = int(text[1])
    with open('secret', 'rb') as f:
       get_data = pickle.load(f)
    d, n = get_data
    result = encripting(c, d, n, g)
    with open('result', 'w') as f:
        f.write(result)
    print('finish')

else:
    print('''Generate keys:      --create-keys
Encrypting message: --encrypt
Decrypting message: --decrypt''')