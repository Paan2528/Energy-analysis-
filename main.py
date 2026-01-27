import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('/Users/yatoum/Documents/Solar-energy-project/data/raw/Plant_1_Generation_Data.csv')

# clear NaN values
df = df.dropna()

# change string to number
df['DC_POWER'] = pd.to_numeric(df['DC_POWER'], errors='coerce')


# convert 'DATE_TIME' column to datetime format
df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], dayfirst=True)
#only kepp day
df['day'] = df['DATE_TIME'].dt.date

# resample data to daily frequency, summing up 'DC_POWER' values
daily = df.groupby("day")['DC_POWER'].sum()

'graph daily data'
plt.figure(figsize=(12, 6))
plt.plot(daily.index, daily.values, label='Daily DC Power', color='blue') 
plt.legend()
plt.show()


print("daily:")
print(daily.describe())


print("min:", df['DC_POWER'].min())
print("max:", df['DC_POWER'].max())

# ====== Analysis =======

average_energy = daily.mean()
print("\nAverage daily energy generation:", average_energy)
print("\nDays with below-average energy:")
for day, value in daily.items():
    if value < average_energy:
        print(day, "->", value) 
