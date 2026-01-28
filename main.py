import pandas as pd
import matplotlib.pyplot as plt
# Load data
from src.data_loader import load_data
df = load_data('/Users/yatoum/Documents/Solar-energy-project/data/raw/Plant_1_Generation_Data.csv')

# clear NaN values
from src.data_cleaning import clean_data
df = clean_data(df)

# change string to number
df['DC_POWER'] = pd.to_numeric(df['DC_POWER'], errors='coerce')


# convert 'DATE_TIME' column to datetime format
df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], dayfirst=True)
#only kepp day
df['day'] = df['DATE_TIME'].dt.date

# resample data to daily frequency, summing up 'DC_POWER' valuesit 

from src.analysis import calculate_daily_energy
daily = calculate_daily_energy(df)

'graph daily data'
from src.visualization import plot_daily_energy
plot_daily_energy(daily)

print("daily:")
print(daily.describe())

# ====== Analysis =======

average_energy = daily.mean()
print("\nAverage daily energy generation:", average_energy)
print("\nDays with below-average energy:")
for day, value in daily.items(): 
    if value < average_energy:
        print(day, "->", value) 
