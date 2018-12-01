import cvxpy as cvx
import numpy as np


def cov_to_cor(covariances):
    """
    :param covariances: a 2d numpy array of covariances
    :return: a 2d numpy array of correlations
    """
    correlations = np.zeros(covariances.shape, dtype=np.float64)
    for i in range(covariances.shape[0]):
        for j in range(covariances.shape[1]):
            correlations[i, j] = covariances[i, j] / (covariances[i, i] * covariances[j, j])

    return correlations


def md_mvo(corr, card):
    '''
    :param card: The number of assets to be chosen (not including the rf asset (integer)
    :param corr: The nxn correlation matrix (np.array)
    '''
    n = len(corr[:, 0])
    z = cvx.Variable((n, n), boolean=True)
    y = cvx.Variable(n, boolean=True)
    cons = []
    for i in range(n):
        for j in range(n):
            cons.append(z[i][j] <= y[i])
        cons.append(cvx.sum(z[:, i]) == 1)

    cons.append(cvx.sum(y, axis=0) == card)
    obj = cvx.Maximize(cvx.sum(corr * z))
    prob = cvx.Problem(obj, cons)
    prob.solve()
    buckets = np.round(y.value)
    return buckets
