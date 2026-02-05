from src.visualization import (
    plot_error_distribution,
    plot_error_over_time,
    plot_prediction_vs_actual,
)
from src.analysis import calculate_performance_metrics
from src.analysis import detect_anomalies
from src.analysis import daily_energy_summary
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

###### Project 2 #######


data_path = "data/raw/Plant_1_Generation_Data.csv"

df = load_data(data_path)
df = clean_data(df)
daily_df = daily_energy_summary(df)

print(daily_df.head())

avg, threshold, anomalies = detect_anomalies(daily)
print("\nAverage Daily Energy:", avg)
print("Threshold Value:", threshold)
print("Anomalous Days:")
print(anomalies)

## performance ##
metrics = calculate_performance_metrics(daily, anomalies)
print("\nPerformance Metrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")

# Visualization for Project 2 ##

predicted = daily.rolling(window=3).mean().dropna()
actual = daily.loc[predicted.index]
errors = actual - predicted

plot_prediction_vs_actual(actual, predicted)
plot_error_distribution(errors)
plot_error_over_time(errors.index, errors)

## check##
print(actual.min(), actual.max())
print(predicted.min(), predicted.max())
