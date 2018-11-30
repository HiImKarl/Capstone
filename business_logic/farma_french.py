import numpy as np
import pandas as pd
import statsmodels.api as sm


# estimate the optimization parameters using the generated factors
def ff3_return_estimates(returns, factors, rf, coefficients):

    # array to hold ff3 ret estimates
    ff3_ret = []
    # mean of risk-free
    mu_rf = np.mean(rf)
    # factor means
    mu_factors = np.mean(factors, axis=0)
    # get factor co-efficients

    for i in range(len(returns[0])):
        ff3_ret_i = mu_rf + np.dot(coefficients[i, 1:], mu_factors)
        ff3_ret.append(ff3_ret_i)

    return np.array(ff3_ret)


def err_var(rets, factors, rf, beta):
    # get excess returns
    excess_rets = rets - np.tile(rf, (len(rets[0]), 1)).transpose()
    # now get matrix of residuals
    # factors is n X 3; beta is pX3; rets is n X p
    # so do rets - matmul(factors, beta^T)
    residuals = excess_rets - np.matmul(factors, np.transpose(beta))
    sigma_eps = np.cov(residuals, rowvar=False)

    return sigma_eps


# estimate the asset variances using factor modelling
def ff3_cov_est(returns, factors, rf, coefficients):
    ff3_cov = []
    
    # get factor variances and covariances
    sig_factors = np.cov(factors, rowvar=False)

    sigma_eps = err_var(returns, factors, rf,
                        [coefficients[i, 1:] for i in range(len(returns[0]))])

    # generate co-variance matrix
    for i in range(len(returns[0])):
        ff3_cov_i = []
        for j in range(len(returns[0])):
            if i == j:
                ff3_cov_ij = 0

                for k in range(len(factors[0])):
                    for l in range(len(factors[0])):
                        ff3_cov_ij += coefficients[i, k] * coefficients[j, l] * sig_factors[k, l]

                ff3_cov_ij += sigma_eps[i][i]

            else:
                ff3_cov_ij = 0
                for k in range(len(factors[0])):
                    for l in range(len(factors[0])):
                        ff3_cov_ij += coefficients[i, k] * coefficients[j, l] * sig_factors[k, l]

            ff3_cov_i.append(ff3_cov_ij)
        ff3_cov.append(ff3_cov_i)
    return np.array(ff3_cov)


def ff3_ols(returns, factors, rf):
    # variable return coefficients
    ff3_coefficient = []
    # excess returns 
    excess_returns = returns - np.tile(rf, (len(returns[0]), 1)).transpose()

    # perform linear regression for each asset
    # slope is factor co-efficients, y-intercept is alpha

    # dependent variable dictionary for setting up pd data frame

    dep_var = {
                'Market': [factors[j][0] for j in range(len(factors))],
                'SMB': [factors[j][1] for j in range(len(factors))],
                'HML': [factors[j][2] for j in range(len(factors))]
              }
    df = pd.DataFrame(data=dep_var)

    for i in range(len(returns[0])):
        # dictionary for setting up pd data frame
        indep_str = 'r ' + str((i + 1))
        indep_var = {indep_str: [excess_returns[j][i] for j in range(len(returns))]}
        target = pd.DataFrame(data=indep_var)

        # linear regression
        x = df[["Market", "HML", "SMB"]]

        # add constant for alpha
        x = sm.add_constant(x)
        y = target[indep_str]
        model = sm.OLS(y, x).fit()
        ff3_coefficient_i = [model.params.const, model.params.Market, model.params.SMB, model.params.HML]
        ff3_coefficient.append(ff3_coefficient_i)

    return np.array(ff3_coefficient)
