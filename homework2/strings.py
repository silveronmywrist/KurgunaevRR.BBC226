def lvl1(string):
    print('Этот метод возвращает введенную строку в трех форматах: только заглавными буквами, только строчными буквами и с первой заглавной')
    a = string.upper()
    b = string.lower()
    c = string.capitalize()
    return f'метод upper: {a}. метод lower: {b}. метод capitalize: {c}'
    
#print(lvl1('пРиВет МИР'))

def lvl2(string):
    print('Этот метод ищет слова, меняет слова и считает количество букв')
    a = str(input('Введите слово, первое вхождение которого вы хотите найти: '))
    b = str(input('Введите слово, на которое вы хотите заменить слово "круто": '))
    c = str(input('Введите букву, количество которой вы хотите посчитать: '))
    c.lower()
    first = string.find(a)
    second = string.replace('круто', b)
    third = string.lower().count(c)
    return f'первое вхождение слова {a}: {first}. Измененная строка: {second}. Количество букв {c}: {third}'

#print(lvl2('Ботать это круто. Очень круто'))

def lvl3(string):
    print('Этот метод выделяет все символы строки, а затем меняет разделитель на пробел')
    splitter = str(input('Введите разделитель: '))
    a = string.split(splitter)
    newsplitter = str(input('Введите новый разделитель: ' ))
    b = newsplitter.join(a)
    return f'все символы строки: {a}, а строка с новым разделителем: {b}'

#print(lvl3('1, 2, 3, 4'))

def lvl4(string):
    print('Этот метод анализирует строку')
    newstr = r"string"
    a = newstr.isdigit()
    b = newstr.isalpha()
    c = str(input('Введите символы, которые вы хотите убрать: '))
    c1 = newstr.strip(c)
    print('Для ответа нужно решить пример: 3 + 5 = ')
    print(int(input('Введите ответ: ')))
    print('Верно, {a} + {b} = {ans}'.format(a=3, b=5, ans = 8))

    return f'В строке все символы - цифры: {a}. В строке все символы - буквы: {b}. Новая строка: {c1}'

#print(lvl4('1234*&%$'))

def lvl5(string):
    print('Этот метод делает из непонятной строки понятную')
    s = string.strip().strip(';').lower().capitalize().replace(';', ' ')
    return f'Новая строка: {s}'
    

print(lvl5('     pYtHon;is;AWESome;    '))
