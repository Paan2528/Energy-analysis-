import pandas as pd


def calculate_daily_energy(df):
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], dayfirst=True)
    df['day'] = df['DATE_TIME'].dt.date
    daily = df.groupby("day")['DC_POWER'].sum()
    return daily


def find_below_average_days(daily_series):
    avg = daily_series.mean()
    below_avg = daily_series[daily_series < avg]
    return avg, below_avg

##### Project 2 ######


def daily_energy_summary(df):
    daily = df.groupby("date")["energy_kWh"].sum().reset_index()
    return daily
