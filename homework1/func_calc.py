def plus(a, b): #Вводим операции через функции отдельно каждую
    return a + b
def minus(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    return a / b
while True: #Зацикливаем работу калькулятора, чтобы не запускать заново
    print('Введите число')
    a = float(input())
    print('Введите операцию')
    b = str(input())
    print('Введите число')
    c = float(input())
    if b == '+': #Проверяем введенную операцию и присваиваем нужной свою функцию
        print(plus(a, c))
    elif b == '-':
        print(minus(a, c))
    elif b == '*':
        print(multiply(a, c))
    elif b == '/':
        if b != 0:
            print(divide(a, c))
        else:
            print('Нельзя')
    else:
        print('Такой операции нет')

