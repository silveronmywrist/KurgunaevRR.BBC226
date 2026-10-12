while True:
    print('Калькулятор')
    print('Введите число') #Принимаем на вход два числа и операцию над ними
    a = float(input())
    print('Введите операцию')
    b = str(input())
    print('Введите число')
    c = float(input())
    if b == '+': #Отдельно отрабатываем каждую операцию
        print(a + c)
    elif b == '-':
        print(a - c)
    elif b == '*':
        print(a * c)
    elif b == '/':
        if c != 0:
            print(a / c)
        else:
            print('Нельзя')
    else:
        print('Такой операции нет')