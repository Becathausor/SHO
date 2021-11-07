########################################################################
# Algorithms
########################################################################
import numpy as np
from sho import num


def random(func, init, again):
    """Iterative random search template."""
    best_sol = init()
    best_val = func(best_sol)
    val, sol = best_val, best_sol
    i = 0
    while again(i, best_val, best_sol):
        sol = init()
        val = func(sol)
        if val >= best_val:
            best_val = val
            best_sol = sol
        i += 1
    return best_val, best_sol


def greedy(func, init, neighb, again):
    """Iterative randomized greedy heuristic template."""
    best_sol = init()
    best_val = func(best_sol)
    val, sol = best_val, best_sol
    i = 1
    while again(i, best_val, best_sol):
        sol = neighb(best_sol)
        val = func(sol)
        # Use >= and not >, so as to avoid random walk on plateus.
        if val >= best_val:
            best_val = val
            best_sol = sol
        i += 1
    return best_val, best_sol


def simu_annealing(func, init, neighb, again, T_init=2000, alpha=50, beta=1.1, evaluation=True):
    """Iterative randomized greedy heuristic template."""
    best_sol = init()
    best_val = func(best_sol)
    val, sol = best_val, best_sol
    T = T_init
    i = 1
    if evaluation:
        L_val = [best_val]

    # Fonction de recui simulé
    def test_recui(f0, f1, t_instant):
        """
        print(f"numérateur: {-(f1 - f0)}")
        print(f"dénominateur: {t_instant}")
        print(f"exponentielle: {np.exp(-(f1 - f0) / t_instant)}")
        print(f"bien calculé")
        print(f"\n")
        """
        return np.exp(-(f1 - f0) / t_instant) < alpha

    while again(i, best_val, best_sol):
        # Mise à jour de la bonne solution
        sol = neighb(best_sol)
        val = func(sol)
        # Use >= and not >, so as to avoid random walk on plateus.
        if val >= best_val:
            best_val = val
            best_sol = sol

        elif test_recui(best_val, val, T):
            # print("Recuisson")
            best_val, best_sol = val, sol

        if evaluation:
            L_val.append(best_val)

        i += 1
        T /= beta

    if evaluation:
        return L_val, best_sol

    return best_val, best_sol


def genetical_population(func, init, neighb, again, pop_size=15, selection_size=5):
    """Population-based stochastic heuristic template"""
    pop = [init() for k in range(pop_size)]
    pop_val = [func(individual) for individual in pop]
    idx = np.argmax(np.array(pop_val))
    best_val, best_sol = pop_val[idx], pop[idx]
    val,sol = best_val,best_sol
    i = 1
    while again(i, best_val, best_sol):

        ## SELECTION ##
        # Random selection of k individuals in population
        total_val = np.sum(pop_val)
        indices = np.random.choice(len(pop), selection_size, replace=False, p=[(pop_val[j]/total_val) for j in range(len(pop_val))])
        selected_population = np.array(pop)[indices]
        selected_population = list(selected_population)

        ## MUTATION ##
        # Selection of close neighbors for each individual
        # TODO: Crossover to be implemented
        mutation_population = [neighb(individual) for individual in selected_population]

        ## REPLACEMENT AND FITNESS ##
        pop += mutation_population                                       # Adds the mutated population to the population
        pop_val = [func(individual) for individual in pop]               # Applies the function to each of them and then sort them.
        index_order = sorted(range(len(pop_val)), key=lambda k: pop_val[k])
        pop = [pop[i] for i in index_order]
        pop_val = [pop_val[i] for i in index_order]
        pop = pop[selection_size:]                                # Removes the k less worst individuals
        pop_val = pop_val[selection_size:]

        # Keeping track of the best elements for evaluation
        idx = np.argmax(np.array(pop_val))
        val, sol = pop_val[idx], pop[idx]
        if val > best_val:
            best_val, best_sol = val, sol
        i += 1
    return best_val, best_sol


def stochastic_heuristic(func, init, neighb, again, n_pop=100, n_select=10, new_generation=num.gaussian):
    """Iterative randomized greedy heuristic template."""

    # First Generation
    pop = np.array([init() for i in range(n_pop)])
    scores = np.array(list(map(func, pop)))

    # Select best individuals
    best_ind = argmax_k(scores, k=n_select)
    best_sol = pop[best_ind]
    best_val = scores[best_ind]

    # Keep track of the best result
    repr_val = best_val[0]
    repr_sol = best_sol[0]

    # Prepare next generation
    print(f"best_sol: {best_sol.shape}")
    mean_hat = (1 / n_select) * sum(best_sol)
    best_sol_bar = best_sol - mean_hat
    print(f"best_sol_bar.shape: {best_sol_bar.shape}")
    cov_hat = (1 / n_select) * np.sum([np.dot(sol, sol.T) for sol in best_sol_bar], axis=1)
    params_neigh = (mean_hat, cov_hat)
    i = 1

    while again(i, repr_val, repr_sol):
        # Next Generation
        pop = np.array([neighb(params_neigh) for i in range(n_pop)])

        scores = np.array(list(map(func, pop)))

        # Select best individuals
        best_ind = argmax_k(scores, k=n_select)
        best_sol = pop[best_ind]
        best_val = scores[best_ind]

        # Keep track of the best elements
        repr_val = best_val[0]
        repr_sol = best_sol[0]

        # Prepare next generation
        mean_hat = (1 / n_select) * sum(best_sol)
        cov_hat = np.cov(best_sol)
        params_neigh = (mean_hat, cov_hat)

        i += 1
    return repr_val, repr_sol


########################################################################
# Additional functions
########################################################################


def argmax_k(list_iter: np.ndarray, k: int, new=True):
    """
    Compute the indices of the k highest elements of the list l.
    :param list_iter: list
    :param k: int
    :return: bests_ind: list
    """
    return sorted(range(len(list_iter)), key=lambda index: list_iter[index])

