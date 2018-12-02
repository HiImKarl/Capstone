import numpy as np
import math


def monte_carlo(rf, psigma, length, nsim):
    """
    :param rf: portfolio's weekly return, scalar
    :param psigma: portfolio's weekly std dev, scalar
    :param length: number of weeks to simulate over, scalar
    :param nsim: number of simulations to run, scalar
    :return paths: nsim by length np array
    This function returns an array of nsim number of
    """

    paths = np.empty((nsim, length))

    for i in range(nsim):
        for j in range(length):
            if j == 0:
                # Initial week as 0 loss
                paths[i, j] = 0
            else:
                z = np.random.standard_normal(1)[0]
                # % change in portfolio value compared to last week
                paths[i, j] = math.exp((rf - ((psigma**2)/2)) + psigma*z) - 1

    return paths


def var_calc(rets, alpha):
    """
    :param rets:is an np.array((n,m)) from monte_carlo
    :param ret_type: determines the shape of the rets matrix, scalar
    :param alpha: The VaR returned will be the 1-alpha percentile of losses
    :return (var, cvar): the alpha var and alpha cvar of the porfolio in % of portfolio value
    """

    m = len(rets[:, 0])
    n = len(rets[0, :])
    new_dim = n*m

    new_rets = np.reshape(rets, (new_dim,))
    new_rets.sort()
    index = math.ceil(new_dim*alpha)
    var_set = new_rets[(index-1):(index+1)]
    cvar_set = new_rets[0:index]
    var = -np.average(var_set)*100
    cvar = -np.average(cvar_set)*100

    return var, cvar


def p_metrics (x, mu, q, rf):
    mu_p = np.dot(x, mu)
    sd_p = math.sqrt(np.matmul(np.matmul(np.transpose(x), q), x))
    sharpe_p = (mu_p - rf) / sd_p
    return mu_p, sd_p, sharpe_p


# test = monte_carlo(3.79e-02,math.pow(6.15e-03,0.5), 52, 1000)
# test2 = var_calc(test, 0.01)
# print(math.pow(52,0.5)*math.pow(6.15e-03,0.5))
