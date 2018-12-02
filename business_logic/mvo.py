import numpy as np
import scipy.optimize as opt


def variance(x, stats):
    q, mu, mu_goal = stats
    # X is a row-vector
    # Q is the covariance matrix
    z = np.array(x)
    var = np.matmul(z, np.matmul(q, np.transpose(z)))
    return var


def ret_goal(x, stats):
    q, mu, mu_goal  = stats

    # x and mu are row vectors
    z = np.array(x)

    # add the risk free return
    val = np.matmul(z, np.transpose(mu)) - mu_goal
    return val


def budget(x, data):
    return np.sum(x)-1


def mvo(q, mu, mu_goal,  short_selling_bound=-np.inf):
    """
    n = # assets
    :param q: 2d n x n numpy covariance matrix
    :param mu: numpy returns vector: n x 1
    :param mu_goal: return scalar value goal
    :param rf; the scalar risk free rate
    :param short_selling_bound set to maximum % allowed to short sell, from (-np.inf, 0]
    :return: a tuple: np array of weights, the variance, and the return
    of the optimized portfolio
    """

    # arg structure
    data = [q, mu, mu_goal]

    # constraint structure
    cons = [{'type': 'eq', 'fun': budget, 'args': (data,)},
            {'type': 'ineq', 'fun': ret_goal, 'args': (data,)}]
    
    # initial guess construction
    x0 = np.zeros(len(mu))
    x0[0] = 1

    # short selling condition
    bounds = [(short_selling_bound, np.inf) for _ in x0]
    
    # optimization
    res = opt.minimize(variance, x0, args=(data,), method='SLSQP',
                       constraints=cons, options={'ftol': 1e-9, 'disp': True},
                       bounds=bounds)
    
    port_var = res.fun
    port_weights = res.x
    port_ret = np.matmul(np.array(res.x), np.transpose(mu))
    return port_weights, port_var, port_ret

