import numpy as np
import scipy.optimize as opt


def variance(x, stats):
    q, mu, mu_goal, rf = stats
    # X is a row-vector
    # Q is the covariance matrix
    z = np.array(x)
    z = z[:-1]
    var = (1/2)*(np.matmul(z, np.matmul(q, np.transpose(z))))
    return var


def ret_goal(x, stats):
    q, mu, mu_goal, rf = stats

    # x and mu are row vectors
    z = np.array(x)

    # add the risk free return
    z_mu = np.append(np.array(mu), rf)
    val = np.matmul(z, np.transpose(z_mu)) - mu_goal
    return val


def budget(x):
    return np.sum(x)-1


def mvo(q, mu, mu_goal, rf, short_selling_allowed=False):
    """
    :param q: 2d numpy covariance matrix
    :param mu: numpy returns vector
    :param mu_goal: return value goal
    :param rf: risk free rate
    :param short_selling_allowed: set to True if shorting should be allowed
    :return: a tuple: np array of weights, the variance, and the return
    of the optimized portfolio
    """

    # arg structure
    data = [q, mu, mu_goal, rf]

    # constraint structure
    cons = [{'type': 'eq', 'fun': budget, 'args': (data,)},
            {'type': 'ineq', 'fun': ret_goal, 'args': (data,)}]
    
    # initial guess construction
    x0 = np.zeros(len(mu)+1)
    x0[0] = 1

    # no short selling condition
    bounds = [(0, np.inf) for _ in x0]

    # short selling condition
    if short_selling_allowed:
        bounds = [(-np.inf, np.inf) for _ in x0]
    
    # optimization
    res = opt.minimize(variance, x0, args=(data,), method='SLSQP',
                       constraints=cons, options={'ftol': 1e-9, 'disp': True},
                       bounds=bounds)
    
    port_var = res.fun
    port_weights = res.x
    port_ret = np.matmul(np.array(res.x), np.transpose(np.append(mu,rf)))
    
    return port_weights, port_var, port_ret

