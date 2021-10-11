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


def simu_annealing(func, init, neighb, again, T_init=2, alpha=0.5, beta=2):
    """Iterative randomized greedy heuristic template."""
    best_sol = init()
    best_val = func(best_sol)
    val, sol = best_val, best_sol
    T = T_init
    i = 1

    # Fonction de recui simulé
    def test_recui(f0, f1, t_instant):
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
            best_val, best_sol = val, sol
        i += 1
        T /= beta

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
    cov_hat = (1 / n_select) * np.sum(np.dot(sol, sol.T) for sol in best_sol_bar)
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


def argmax_k(list_iter: np.ndarray, k: int):
    """
    Compute the indices of the k highest elements of the list l.
    :param list_iter: list
    :param k: int
    :return: bests_ind: list
    """
    l_ = list_iter.copy()
    bests_ind = []
    mini = min(l_) - 1
    for i in range(k):
        if i >= len(l_):
            return bests_ind
        ind = np.argmax(l_)
        bests_ind.append(ind)
        l_[ind] = mini
    return bests_ind