import matplotlib.pyplot as plt

'graph daily data'
def plot_daily_energy(daily_data):
    plt.figure(figsize=(12, 6))
    plt.plot(daily_data.index, daily_data.values, marker='o', linestyle='-')
    plt.title('Daily Energy Generation')
    plt.xlabel('Day')
    plt.ylabel('Total DC Power')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    