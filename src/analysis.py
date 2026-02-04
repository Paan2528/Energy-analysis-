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
    daily = df.groupby("DATE_TIME")["DC_POWER"].sum().reset_index()
    return daily

### Threshold anomaly detection ####


def detect_anomalies(daily_series, threshold_ratio=0.5):
    """Detect anomalies based on a threshold ratio.

    Parameters:
     daily_series (pd.Series): Series with daily energy values.
     threshold_ratio (float): Ratio of the average energy (default is 0.5)

    Returns:
      averge_energy
      threshold_value
      anomaly_day(Series)
    """
    average_energy = daily_series.mean()
    threshold_value = average_energy * threshold_ratio
    anomaly_days = daily_series[daily_series < threshold_value]
    return average_energy, threshold_value, anomaly_days
