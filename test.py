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
    METHOD_NAME = "num_genetical"
    RESOLUTION = 100
    DELTA = 650
    DELTAS = (600, 660, 675)
    METHOD_NAMES = ["num_annealing",
                    "bit_annealing",
                    "num_genetical",
                    "bit_genetical"]
    PARAMETERS = [{'nb-sensors': 3, 'sensor-range': 0.3, 'domain-width': 30},
                  {'nb-sensors': 4, 'sensor-range': 0.3, 'domain-width': 30}]
    BUDGET = 90

    # CHOOSE WHAT TO RUN
    RUN_CREATE_DATA = True
    PLOT_TRAJECTORIES = True
    RUN_EAF = True
    RUN_ERT = True
    RUN_BENCH = True

    if RUN_CREATE_DATA:
        get_evaluation.create_evaluation(N_RUNS, method_name=METHOD_NAME)

    print(f"GATHER DATA AROUND THE {METHOD_NAME}")
    runs = get_evaluation.get_data(METHOD_NAME)

    if PLOT_TRAJECTORIES:
        # Visualize different trajectories
        print(f"PLOT TRAJECTORIES")
        plot_evaluation.plot_runs(runs, title=METHOD_NAME)

    if RUN_ERT:
        # Plot ert according to the value of DELTA
        print("PLOT ERT")
        ert = evaluation_representation.create_ert(runs, DELTA)
        plot_evaluation.plot_ert(ert, title=METHOD_NAME + f"_ert, delta={DELTA}", y_label=f"P(Quality < {DELTA})")

        # Plot erts for comparisons
        print("PLOT ERT")
        algo_comparison.compare_ert(METHOD_NAMES, nb_runs=N_RUNS, deltas=DELTAS,
                                    title="Comparison of algorithms", y_label="P[x > delta]",
                                    name_save="")

    if RUN_EAF:
        # Plot eaf
        print("PLOT EAF")
        eaf, extent = evaluation_representation.create_eaf(runs, RESOLUTION, RESOLUTION)
        plot_evaluation.plot_eaf(eaf, extent=extent, title=METHOD_NAME + "_eaf",
                                 x_label=f"Budget [{extent[0]};{extent[1]}]",
                                 y_label=f"Quality [{extent[2]};{extent[3]}]")

    if RUN_BENCH:
        bench = ExperimentDesign.ExperimentDesign(METHOD_NAMES, PARAMETERS, BUDGET, N_RUNS)
        medians = bench.evaluate_bench_median()
        print(medians)