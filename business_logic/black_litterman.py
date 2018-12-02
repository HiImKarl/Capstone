import math
import numpy as np
import csv
import pandas as pd
import statsmodels.api as sm
import random


# note that at the moment I am just writing skeletal barebones
# will refine later
# function that computes lambda
def bl_lambda(mkt_cap, mu, q, rf):
    x_mkt = mkt_cap / np.sum(mkt_cap)
    var_mkt = np.matmul(np.matmul(x_mkt.transpose(), q), x_mkt)
    mu_mkt = sum(mu * x_mkt)
    return (mu_mkt - rf) / var_mkt


# function that compute equilibrium returns
def bl_pi(mkt_cap, mu, q, rf):
    rav_coeff = bl_lambda(mkt_cap, mu, q, rf)
    x_mkt = mkt_cap / np.sum(mkt_cap)
    return rav_coeff * np.matmul(q, x_mkt)


# with views done, now need omega
def omega_gen(p, q, tau):
    omega = []
    for i in range(len(p)):
        omega_i = []
        for j in range(len(p)):
            if i == j:
                omega_i.append(tau*np.matmul(np.matmul(p[i].transpose(), q), p[i]))
            else:
                omega_i.append(0)
        omega.append(omega_i)
    return omega


# need a function to compute the combined return vector
# for now use K, where K is the number of views need
def bl_cr(mkt_cap, mu, q, rf, views, tau):
    pi = bl_pi(mkt_cap, mu, q, rf)
    view_matrix = np.identity(len(mu), dtype=np.float64)
    view_vector = mu * views
    omega = omega_gen(view_matrix, q, tau)
    x1 = np.linalg.inv(tau * q)
    x2 = np.matmul(np.matmul(view_matrix.transpose(), np.linalg.inv(omega)), view_matrix)
    x3 = np.linalg.inv(x1 + x2)
    x4 = np.matmul(x1, pi)
    x5 = np.matmul(np.matmul(view_matrix.transpose(), np.linalg.inv(omega)), view_vector)
    x6 = x4 + x5
    return np.matmul(x3, x6)


def bl_weights_normalized(returns, rac, q):
    w = np.matmul(np.linalg.inv(rac * q), returns)
    return w / np.sum(w)


# put everything together to make a function
# need rets, factors, risk free and market cap probably
def black_litterman(mu, q, rf, mkt_cap, views, tau=0.02):
    """
    Where n = # assets, m = # periods
    :param mu:  n x 1
    :param q:   n x n
    :param rf:  1 x 1
    :param mkt_cap: n x 1
    :param views: investor views
    :param tau: [0.01, 0.05]
    :return: n x 1 portfolio weights
    """
    rac = bl_lambda(mkt_cap, mu, q, rf)
    cr = bl_cr(mkt_cap, mu, q, rf, views, tau)
    w = bl_weights_normalized(cr, rac, q)
    return w
