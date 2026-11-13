import pandas as pd
import numpy as np

df = pd.read_csv("/Users/radmirkurgunaev/Documents/devs/python/homework4/tested.csv")
df = pd.DataFrame(df)

result1 = df.groupby(["Pclass", "Sex"]).agg(
    passenger_count=("Pclass", "size"),
    mean_age=("Age", "mean"),
    survived_percent=("Survived", lambda x: x.mean() * 100),
    mean_fare=("Fare", "mean")
).round(2)

print(result1)

result2 = df.groupby("Embarked").agg(
    passenger_count=("Pclass", "size"),
    survived_percent=("Survived", lambda x: x.mean() * 100)
).round(2)

print(result2)

survived_classes = df.groupby("Pclass")["Survived"].mean() * 100

most_survivors = survived_classes.idxmax()

print(f"Больше всего выживших в классе {most_survivors}")

result1.to_csv("titanic_statistics.csv", index=True)