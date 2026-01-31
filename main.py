from src.analysis import find_below_average_days
from src.visualization import plot_daily_energy
from src.analysis import calculate_daily_energy
from src.data_cleaning import clean_data
import pandas as pd
import matplotlib.pyplot as plt
# Load data
from src.data_loader import load_data
df = load_data(
    '/Users/yatoum/Documents/Solar-energy-project/data/raw/Plant_1_Generation_Data.csv')

# clear NaN values
df = clean_data(df)

# change string to number
df['DC_POWER'] = pd.to_numeric(df['DC_POWER'], errors='coerce')


# convert 'DATE_TIME' column to datetime format
df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], dayfirst=True)
# only kepp day
df['day'] = df['DATE_TIME'].dt.date

# resample data to daily frequency, summing up 'DC_POWER' values

daily = calculate_daily_energy(df)

# graph daily data
plot_daily_energy(daily)

print("daily:")
print(daily.describe())

# ====== Analysis =======

avg, below_avg_days = find_below_average_days(daily)

print("\nAverage daily energy generation:", avg)
print("\nDays with below-average energy:")
print(below_avg_days)
