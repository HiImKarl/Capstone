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

    return correlations.tolist()


def md_mvo(corr, card):
    '''
    :param card: The number of assets to be chosen (not including the rf asset (integer)
    :param corr: The nxn correlation matrix (np.array)
    '''

    rho = np.array(corr)
    n = len(rho[:, 0])

    z = cvx.Variable((n, n), boolean=True)
    y = cvx.Variable(n, boolean=True)

    cons = []
    for i in range(n):
        for j in range(n):
            cons += [
                z[i, j] <= y[i]
            ]
        cons += [cvx.sum(z, axis=0) == 1]

    cons += [cvx.sum(y, axis=0) == card]
    obj_mat = np.empty((n, n), dtype=np.float64)

    for i in range(n):
        for j in range(n):
            obj_mat[i, j] = rho[i, j] * z[i, j]

    obj = cvx.Maximize(cvx.sum(obj_mat))
    prob = cvx.Problem(obj, cons)
    prob.solve()
    return y.value
