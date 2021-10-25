import matplotlib.pyplot as plt
from matplotlib import cm
from time import sleep


def context_plot(plotter):
    def wrapped(*args, x_label="Budget", y_label="Quality", title="", name_save="", **kwargs):
        plotter(*args, **kwargs)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if name_save:
            plt.savefig(f"images_evaluation\\{name_save}")
        plt.show()
        return None

    return wrapped


@context_plot
def plot_runs(runs):
    """
    Plot every runs on the same figure
    """
    for run in runs:
        costs, qualities = run
        plt.plot(costs, qualities)


@context_plot
def plot_eah(eah):
    plt.imshow(eah, cmap="Oranges", origin="lower")


@context_plot
def plot_ert(ert):
    plt.plot(ert)


@context_plot
def plot_eaf(X, Y, eaf):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(X, Y, eaf,
                           linewidth=0, cmap=cm.coolwarm, antialiased=False)
    fig.colorbar(surf)
