import pandas as pd
import numpy as np

data = pd.read_csv("/Users/radmirkurgunaev/Documents/devs/python/homework4/tested.csv")
df = pd.DataFrame(data)

missing = df.isna().sum()
print(missing)

missing_p = df.isna().sum() / df.shape[0] * 100
print(missing_p)

print("Столбец с макисмальным количеством пропусков: ", missing.idxmax())
print("Количество пропусков: ", max(missing))

age_stats = df["Age"].agg([
    "mean", "median", "min", "max", "std", "count"
])
print(age_stats)

median_age = df["Age"].median()
df["Age"] = df["Age"].fillna(median_age)
print(df["Age"].isna().sum())

age_stats_after = df["Age"].agg([
    "mean", "median", "min", "max", "std", "count"
])

print(age_stats_after)

comparison = pd.DataFrame({
    "До обработки": age_stats,
    "После обработки": age_stats_after
})

print(comparison)

df = df.dropna(subset=["Embarked"])

missing_cabin = df["Cabin"].isna().sum() / df.shape[0]
print(missing_cabin)
if missing_cabin > 0.5:
    df = df.drop(columns=["Cabin"])
    print("Cabin удалена")

print(df[df["Fare"].isna()])

df.to_csv("titanic-processed.csv", index=False)