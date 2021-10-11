import math
import numpy as np

from . import pb


########################################################################
# Objective functions
########################################################################

# Decoupled from objective functions, so as to be used in display.
def to_sensors(sol):
    """Convert a vector of n*2 dimension to an array of n 2-tuples.

    >>> to_sensors([0,1,2,3])
    [(0, 1), (2, 3)]
    """
    assert (len(sol) > 0)
    sensors = []
    for i in range(0, len(sol), 2):
        sensors.append((int(math.floor(sol[i])), int(math.floor(sol[i + 1]))))
    return sensors


def cover_sum(sol, domain_width, sensor_range, dim):
    """Compute the coverage quality of the given vector."""
    assert (0 < sensor_range <= math.sqrt(2))
    assert (0 < domain_width)
    assert (dim > 0)
    assert (len(sol) >= dim)
    domain = np.zeros((domain_width, domain_width))
    sensors = to_sensors(sol)
    cov = pb.coverage(domain, sensors, sensor_range * domain_width)
    s = np.sum(cov)
    assert (s >= len(sensors))
    return s


########################################################################
# Initialization, generation
########################################################################

def rand(dim, scale):
    """Draw a random vector in [0,scale]**dim."""
    return np.random.random(dim) * scale


def gaussian(params, test=False, dim=None, scale=None):
    """Draw a random vector according to a gaussian model"""
    mean, cov = params
    if test:
        print(f"mean: {mean.shape}")
        print(f"covariance: {cov.shape}")
    return np.random.multivariate_normal(mean, cov)


########################################################################
# Neighborhood
########################################################################

def neighb_square(sol, scale, domain_width):
    """Draw a random vector in a square of witdh `scale` in [0,1]
    as a fraction of the domain width around the given solution."""
    assert (0 < scale <= 1)
    side = domain_width * scale;
    new = sol + (np.random.random(len(sol)) * side - side / 2)
    return new


########################################################################
# Constraint management
########################################################################


def reparation(X, maxi, mini=0):
    Y = (X - maxi) * ((X - maxi) <= 0) + maxi
    Y = (Y + mini) * ((Y + mini) >= 0) - mini
    return Y


def penalization(x, x_repaired, method="Mean_Square"):
    if method == "Mean_Square":
        loss = np.sum((x - x_repaired) ** 2)
    elif method == "Lasso":
        loss = np.sum(np.abs(x - x_repaired))
    else:
        raise NotImplementedError
    return loss


