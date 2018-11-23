import numpy as np
import pandas as pd
import statsmodels.api as sm


# estimate the optimization parameters using the generated factors
def ff3_return_estimates(returns, factors, rf, coefficients):
    # array to hold ff3 ret estimates
    # FIXME compute geometric mean instead of arithmetic
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


# estimate the asset variances using factor modelling
def ff3_cov_est(returns, factors, coefficients):
    ff3_cov = []
    
    # get factor variances and covariances
    sig_factors = np.cov(factors, rowvar=False)

    # generate co-variance matrix
    for i in range(len(returns[0])):
        ff3_cov_i = []
        for j in range(len(returns[0])):
            if i == j:
                ff3_cov_ij = 0

                for k in range(len(factors[0])):
                    for l in range(len(factors[0])):
                        ff3_cov_ij += coefficients[i, k] * coefficients[j, l] * sig_factors[k, l]

                ff3_cov_ij += np.cov(
                    np.array([returns[k][i]
                              for k in range(
                            len(returns))])) - np.dot(coefficients[i][1:] *
                                                      coefficients[i][1:],
                                                      np.array([sig_factors[l][l] for l in range(len(factors[0]))]))
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
        X = df[["Market", "HML", "SMB"]]

        # add constant for alpha
        X = sm.add_constant(X)
        y = target[indep_str]
        model = sm.OLS(y, X).fit()
        ff3_coefficient_i = [model.params.const, model.params.Market, model.params.SMB, model.params.HML]
        ff3_coefficient.append(ff3_coefficient_i)

    return np.array(ff3_coefficient)
