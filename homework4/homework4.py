import pandas as pd
import numpy as np

data = pd.read_csv("/Users/radmirkurgunaev/Documents/devs/python/homework4/tested.csv")
df = pd.DataFrame(data)
n = int(input("Количество строк: "))
print(df.head(n))
print(df.tail(5))
rows, columns = df.shape
print(rows, columns)
print(df.columns)
print(df.dtypes)

num_features = ["Age", "SibSp", "Parch", "Fare"]
cat_features = ["Survived", "Pclass", "Sex", "Embarked"]

stats = df[num_features].agg([
    "mean", "median", 'min', 'max', 'std'
])

print(stats)

print(df["Pclass"].value_counts().sort_index())

print(df["Embarked"].nunique())