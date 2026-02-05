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

### Performance ###


def calculate_performance_metrics(daily_series, anomaly_series=None):

    metrics = {}

# besic metrics
    metrics['average_energy'] = daily_series.mean()
    metrics['total_energy'] = daily_series.sum()
    metrics['max_energy'] = daily_series.max()
    metrics['min_energy'] = daily_series.min()
    metrics['std_deviation'] = daily_series.std()
# find which day had min/max
    metrics['day_with_max_energy'] = daily_series.idxmax()
    metrics['day_with_min_energy'] = daily_series.idxmin()

# anomaly metrics
    if anomaly_series is not None:
        metrics['num_anomalies'] = len(anomaly_series)
        metrics['anomaly_percentage'] = (
            len(anomaly_series) / len(daily_series)) * 100
    else:
        metrics['num_anomalies'] = 0
        metrics['anomaly_percentage'] = 0.0
    return metrics
