from math import *
class Calculator: #Создаем класс калькулятора

    def __init__(self, tempo): #Вводим переменную, которая вручную будет добавляться к объектам класса
        self.tempo = tempo

    def calc(self): #Расчитываем нужные параметры
        bpm = 60000/self.tempo #Длительность одного удара в мс
        short_decay = bpm
        medium_decay = bpm * 2
        long_decay = bpm * 4
        predelay = bpm/4
        print('predelay = ', round(predelay), 'мс')
        print('короткий реверб = ', round(short_decay), 'мс')
        print('средний реверб = ', round(medium_decay), 'мс')
        print('длинный реверб = ', round(long_decay), 'мс')

bpm = int(input('Введите темп: ')) #Вводим переменную вручную
reverbcalc = Calculator(bpm)
reverbcalc.calc()
