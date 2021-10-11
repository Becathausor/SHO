import numpy as np
import matplotlib.pyplot as plt


def plot_runs(runs, title):
    """
    Plot every runs on the same figure
    """
    for run in runs:
        costs, qualities = run
        plt.plot(costs, qualities)
    plt.xlabel("Budget")
    plt.ylabel("Quality")
    plt.title(title)
    plt.show()
