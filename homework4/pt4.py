import pandas as pd
import numpy as np

data = pd.read_csv("/Users/radmirkurgunaev/Documents/devs/python/homework4/tested.csv")
df = pd.DataFrame(data)

survived = df["Survived"].to_numpy()
sex = df["Sex"].to_numpy()
age = df["Age"].to_numpy()
fare = df["Fare"].to_numpy()

survived_percent =  np.mean(survived) * 100
male_survived = np.mean(survived[sex == 'male']) * 100
women_survived = np.mean(survived[sex == 'female']) * 100

print(f"Процент выживших мужчин: {male_survived:.2f}\nПроцент выживших женщин: {women_survived:.2f}")
print(survived_percent)

men_age = np.nanmean(age[sex == 'male'])
women_age = np.nanmean(age[sex == 'female'])
print(f"Мужчины: {men_age:.2f}, Женщины: {women_age:.2f}")

min_fare = np.nanmin(fare)
med_fare = np.nanmean(fare)
max_fare = np.nanmax(fare)
print(f"Минимальная стоимость: {min_fare:.2f}, Средняя стоимость: {med_fare:.2f}, Максимальная стоимость: {max_fare:.2f}")

age_std = np.nanstd(age, ddof = 1)
print(f"Стандартное отклонение: {age_std:.2f}")
