import pandas as pd
def calculate_daily_energy(df):
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], dayfirst=True)
    df['day'] = df['DATE_TIME'].dt.date
    daily = df.groupby("day")['DC_POWER'].sum()
    return daily