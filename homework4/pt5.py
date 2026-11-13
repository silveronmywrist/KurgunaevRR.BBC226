import pandas as pd
import numpy as np

data = pd.read_csv("/Users/radmirkurgunaev/Documents/devs/python/homework4/tested.csv")
df = pd.DataFrame(data)
df = df.drop(columns="Cabin")
select = df[
    (df['Sex'] == 'male') & 
    (df["Age"] > 30) &
    (df["Pclass"] == 1)]

fare = df["Fare"].to_numpy

print(f"Количество мужчин старше 30 в первом классе: {len(select)}")
print(select.head(10).to_string(index=False))

select2 = df[
    ((df["Age"] < 18) | (df["Sex"] == "female")) &
    (df["Survived"] == 1)
]

print(f"Количество женщин или моложе 18 которые выжили: {len(select2)}")

mean_fare_3 = df.loc[df["Pclass"] == 3, "Fare"].mean()

select3 = df.loc[(df["Pclass"] == 3) & (df["Fare"] > mean_fare_3)]

print("Пассажиры третьего класса, стоимость билета которых больше стоимости билета средней")
print(select3)

select4 = df.loc[(df["Age"].between(20, 40, inclusive="both")) & (df["Embarked"] == "S")]

print("Пассажиры старше 20, но моложе 40, отправившиеся из S")
print(select4)