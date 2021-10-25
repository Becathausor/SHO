"""
Plot the distribution of the algorithms run in snp.py for evaluation
"""
import get_evaluation
import evaluation_representation
import plot_evaluation
import algo_comparison
import ExperimentDesign

if __name__ == "__main__":

    # PARAMETERS
    N_RUNS = 10
    METHOD_NAME = "num_annealing"
    RESOLUTION = 100
    DELTA = 650
    DELTAS = (600, 660, 675)
    METHOD_NAMES = ["num_annealing", "bit_annealing", "num_genetical", "bit_genetical"]
    PARAMETERS = [  {'nb-sensors': 3, 'sensor-range': 0.3, 'domain-width': 30},
                    {'nb-sensors': 4, 'sensor-range': 0.3, 'domain-width': 30}]
    BUDGET = 60

    # get_evaluation.create_evaluation(N_RUNS, METHOD_NAME)
    print(f"GATHER DATA AROUND THE {METHOD_NAME}")
    runs = get_evaluation.get_data(METHOD_NAME)

    # Visualize different trajectories
    print(f"PLOT TRAJECTORIES")
    plot_evaluation.plot_runs(runs, title=METHOD_NAME)

    # Plot eah
    print("PLOT EAH")
    eah = evaluation_representation.create_eah(runs, RESOLUTION, RESOLUTION)
    plot_evaluation.plot_eah(eah, title=METHOD_NAME + "_eah")

    # Plot ert according to the value of DELTA
    print("PLOT ERT")
    ert = evaluation_representation.create_ert(runs, DELTA)
    plot_evaluation.plot_ert(ert, title=METHOD_NAME + f"_ert, delta={DELTA}", y_label=f"P(Quality < {DELTA})")

    # Plot eaf
    print("PLOT EAF")
    costs, qualities, eaf = evaluation_representation.create_eaf(runs)
    plot_evaluation.plot_eaf(costs, qualities, eaf, title=METHOD_NAME + f"_eaf", y_label="Quality")

    # Plot erts
    print("PLOT ERT")
    algo_comparison.compare_ert(METHOD_NAMES, nb_runs=N_RUNS, deltas=DELTAS,
                                title="Comparison of algorithms", y_label="P[x > delta]",
                                name_save="")
    
    bench = ExperimentDesign.ExperimentDesign(METHOD_NAMES, PARAMETERS, BUDGET, N_RUNS)
    bench.evaluate_bench_median()
