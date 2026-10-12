def f(n1, n2, op): #принимает два числа и операцию над ними
    if str(op) == '+': return n1 + n2 #в зависимости от выбранной операции совершает её
    elif str(op) == '-': return n1 - n2
    elif str(op) == '*': return n1 * n2
    elif str(op) == '/':
        if n2 != 0: #дополнительно проверяет возможность выполнения операции
            return n1 / n2
        else:
            return 'Нельзя'
    elif str(op) == '^':
        return n1 ** n2
    else:
        return 'Такой операции нет'

while True: #позволяет калькулятору работать бесконечно, не требует повторного запуска
    print('Введите число')
    a = float(input())
    print('Введите операцию')
    b = str(input())
    print('Введите число')
    c = float(input())
    print(f(a, c, b))