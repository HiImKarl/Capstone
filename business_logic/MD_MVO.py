import cvxpy as cvx
import numpy as np


def MD_MVO(correl, card):
    '''

    :param card: The number of assets to be chosen (not including the rf asset (integer)
    :param correl: The nxn correlation matrix (np.array)
    '''

    rho = np.array(correl)
    n = len(rho[:,0])

    z = cvx.Variable((n,n), boolean=True)
    y = cxv.Variable(n, boolean=True)

    ones = np.ones(n)


    cons = []

    for i in range (n):
        for j in range(n):
            cons += [
                z[i,j] <= y[i]
            ]
        cons += [cvx.sum_entries(z, axis=0) ==1
        ]

    cons += [cvx.sum_entries(y, axis = 0) == card]


    obj_mat = np.(n)

    for i in range(n):
        for j in range(n):
            obj_mat[i,j] = rho[i,j]*z[i,j]

    obj = cvx.Maximixe(cvx.sum_array(obj_mat))

    prob. = cvx.Problem(obj, cons)

    prob.solve()

    print (y.value)

    return()
