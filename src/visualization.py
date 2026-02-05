import matplotlib.pyplot as plt

# Graph daily data


def plot_daily_energy(daily_data):
    plt.figure(figsize=(12, 6))
    plt.plot(daily_data.index, daily_data.values, marker='o', linestyle='-')
    plt.title('Daily Energy Generation')
    plt.xlabel('Day')
    plt.ylabel('Total DC Power')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

## Project 2 ##

## graph 1 : predicted vs actual ##


def plot_prediction_vs_actual(actual, predicted):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 6))
    plt.scatter(actual.values, predicted.values, alpha=0.6)

    # ideal Line
    min_val = min(actual.min(), predicted.min())
    max_val = max(actual.max(), predicted.max())
    plt.plot([min_val, max_val], [min_val, max_val], linestyle='--',
             linewidth=2, color='red', label="Ideal line( y=x)", zorder=10)

    plt.xlim(min_val, max_val)
    plt.ylim(min_val, max_val)

    plt.xlabel("Actual Energy")
    plt.ylabel("Predicted Energy")
    plt.title("Predicted vs Actual Daily Energy")

    plt.show()

## graph 2: Error Distribution ##


def plot_error_distribution(errors):
    plt.figure(figsize=(8, 6))
    plt.hist(errors, bins=30)

    plt.xlabel("Prediction Error")
    plt.ylabel("Frequency")
    plt.title("Errors Distribution")

    plt.show()

## graph 3: Error over time ##


def plot_error_over_time(dates, errors):
    plt.figure(figsize=(12, 6))

    plt.plot(dates, errors)

    plt.xlabel("Date")
    plt.ylabel("Prediction Error")
    plt.title("Prediction Error Over Time")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
