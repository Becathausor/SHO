"""
Plot the distribution of the algorithms run in snp.py for evaluation
"""
import get_evaluation
import evaluation_representation
import plot_evaluation
import algo_comparison

if __name__ == "__main__":
    N_RUNS = 10
    METHOD_NAME = "num_annealing"
    RESOLUTION = 100
    DELTA = 650
    DELTAS = (600, 660, 675)
    METHOD_NAMES = ["num_annealing", "bit_annealing"]

    # get_evaluation.create_evaluation(N_RUNS, METHOD_NAME)
    runs = get_evaluation.get_data(METHOD_NAME)

    # Visualize different trajectories
    plot_evaluation.plot_runs(runs, title=METHOD_NAME)

    # Plot eah
    eah = evaluation_representation.create_eah(runs, RESOLUTION, RESOLUTION)
    plot_evaluation.plot_eah(eah, title=METHOD_NAME + "_eah")

    # Plot ert according to the value of DELTA
    ert = evaluation_representation.create_ert(runs, DELTA)
    plot_evaluation.plot_ert(ert, title=METHOD_NAME + f"_ert, delta={DELTA}", y_label=f"P(Quality < {DELTA})")

    # Plot eaf
    costs, qualities, eaf = evaluation_representation.create_eaf(runs)
    plot_evaluation.plot_eaf(costs, qualities, eaf, title=METHOD_NAME + f"_eaf", y_label="Quality")

    # Plot erts
    algo_comparison.compare_ert(METHOD_NAMES, nb_runs=N_RUNS, deltas=DELTAS)
