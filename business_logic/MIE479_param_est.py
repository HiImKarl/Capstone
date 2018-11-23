import math
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import pandas as pd
import statsmodels.api as sm

# first let's read the data we need to test on
#stock price data
stock_dat = 'Project1_Data_adjClose.csv'
stock_tab = []
with open(stock_dat, 'rb') as csvfile:
    stockreader = csv.reader(csvfile, delimiter = ' ')
    for row in stockreader:
        stock_tab.append(row)

stock_tab2 = []
for i in range(0, len(stock_tab)):
    stock_tab2.append(stock_tab[i][0].split(','))

#convert stock data to float type
for i in range(1, len(stock_tab2)):
    #stock_tab2[i][0] = int(stock_tab2[i][0])
    for j in range(1, len(stock_tab2[i])):
        stock_tab2[i][j] = float(stock_tab2[i][j])

#factors data
ff_dat = 'Project1_Data_FF_factors.csv'
ff_tab = []
with open(ff_dat, 'rb') as csvfile:
    ffreader = csv.reader(csvfile, delimiter = ' ')
    for row in ffreader:
        ff_tab.append((row))

ff_tab2 = []
for i in range(0, len(ff_tab)):
    ff_tab2.append(ff_tab[i][0].split(','))

#convert ff data to float type
for i in range(1, len(ff_tab2)):
    for j in range(1, len(ff_tab2[i])):
        ff_tab2[i][j] = float(ff_tab2[i][j])

#keep dates as strings for now
#will hardcode period length in - for this sample data it is weekly
#variables to hold number of periods of data + number of stocks
periods = len(stock_tab2) - 1
stocks = len(stock_tab2[0]) - 1
#first get numpy matrix of price data
price = np.array([stock_tab2[i][1:(stocks + 1)] for i in range(1, periods + 1)],\
                 dtype = np.float64)
#get return data

#get return as (P[i] - P[i-1])/P[i-1]
rets = (price[1:periods,:] - price[0:(periods-1),:])/price[0:(periods-1)]
#now get mean returns
#axis 0 pertains to columns, which is what I am looking for (i.e. mean return of each stock)
mu = np.mean(rets, axis = 0)

#get covariance matrix
Q = np.cov(rets, rowvar = False)

#Attempt to do factor modelling now...
#ff_tab2 contains the the factors data
#get matrix of just the data for the factors
factors = np.array([ff_tab2[i][1:4] for i in range(1, periods)],\
                   dtype = np.float64)
#risk free
rf = np.array([ff_tab2[i][4] for i in range(1, periods)],\
                   dtype = np.float64)

#next get the expectation and variance of the factors
mu_factors = np.mean(factors, axis = 0)
sig_factors = np.cov(factors, rowvar = False)

#function to estimate the factor co-efficients
def ff3coeff_gen(rets, factors, rf):
    #
    ff3coeff = []
    #excess returns
    excess_rets = rets - np.tile(rf, (len(rets[0]), 1)).transpose()
    #mean
    mu = np.mean(excess_rets, axis = 0)
    mu_factors = np.mean(factors, axis = 0)
    #covariance of factors
    sig_factors = np.cov(factors, rowvar = False)
    #now we will start the computation of the factors
    for i in range(0, len(rets[0])):
        A = []
        b = []
        #loop over factors
        #set up system of linear equations
        for j in range(0, len(factors[0])):
            sig_ret_factor = np.cov(excess_rets[:,i], factors[:,j])
            b.append(sig_ret_factor[0,1])
            A.append([sig_factors[j,k] for k in range(0, len(factors[0]))])

        beta_i = np.linalg.solve(np.array(A), np.array(b))
        alpha_i = mu[i] - np.dot(beta_i, mu_factors)
        ff3coeff_i = np.concatenate((np.array([[alpha_i]]),\
                                     np.expand_dims(beta_i, axis = 0)),axis = 1)
        ff3coeff.append(ff3coeff_i)

    #now to return output
    return np.squeeze(np.array(ff3coeff))


#test factor generating function more rigorously later
#first let's estimate the optimization parameters using the generated factors
def ff3_ret_ests(rets, factors, rf, est_mode = 0):
    #array to hold ff3 ret ests
    ff3_ret = []
    #mean of risk-free
    mu_rf = np.mean(rf)
    #factor means
    mu_factors = np.mean(factors, axis = 0)
    #get factor co-efficients
    if est_mode == 0:
        ff3coeff = ff3coeff_gen(rets, factors, rf)
    elif est_mode == 1:
        ff3coeff = ff3_OLS(rets, factors, rf)
    else:
        #use Luenberger method as default
        ff3coeff = ff3coeff_gen(rets, factors, rf)

    for i in range(0,len(rets[0])):
        ff3_ret_i = mu_rf + ff3coeff[i, 0] + np.dot(ff3coeff[i,1:],mu_factors)
        ff3_ret.append(ff3_ret_i)

    return np.array(ff3_ret)

#estimated returns generated are the same as the mean rets...
#in hindsight, this makes sense b/c of the algebra
#so does this only save on computation?
#try linear estimation approach - see if same values are generated...

#before trying this out though, let's estimate the asset variances using factor modelling
def ff3_cov_est(rets, factors, rf, est_mode = 0):
    #ff3 cov
    ff3_cov = []
    #get factor co-efficients
    if est_mode == 0:
        ff3coeff = ff3coeff_gen(rets, factors, rf)
    elif est_mode == 1:
        ff3coeff = ff3_OLS(rets, factors, rf)
    else:
        #use Luenberger method as default
        ff3coeff = ff3coeff_gen(rets, factors, rf)
    #get factor variances and covariances
    sig_factors = np.cov(factors, rowvar=False)
    #now generate co-variance matrix
    for i in range(0, len(rets[0])):
        #row i
        ff3_cov_i = []
        for j in range(0, len(rets[0])):
            if i == j:
                ff3_cov_ij = 0
                for k in range(0, len(factors[0])):
                    for l in range(0, len(factors[0])):
                        ff3_cov_ij += ff3coeff[i, k]*ff3coeff[j, l]*sig_factors[k,l]
                ff3_cov_ij += np.cov(np.array([rets[k][i] for k in range(0, len(rets))])) - \
                              np.dot(ff3coeff[i][1:]*ff3coeff[i][1:], \
                                     np.array([sig_factors[l][l] for l in range(0, len(factors[0]))]))
            else:
                ff3_cov_ij = 0
                for k in range(0, len(factors[0])):
                    for l in range(0, len(factors[0])):
                        ff3_cov_ij += ff3coeff[i, k]*ff3coeff[j, l]*sig_factors[k,l]
            ff3_cov_i.append(ff3_cov_ij)
        ff3_cov.append(ff3_cov_i)
    return np.array(ff3_cov)

#ok i have something, now to return and do something with linear regression...
def ff3_OLS(rets, factors, rf):
    #variable to hold vals to return
    ff3coeff = []
    #excess returns is the dependent variable
    excess_rets = rets - np.tile(rf, (len(rets[0]), 1)).transpose()
    #the idea is to perform linear regression for each asset
    #the slope will be the factor co-efficients and y-intercept will be the alpha

    #dependent variable dictionary for setting up pd data frame
    dep_var = {'Market': [factors[j][0] for j in range(0, len(factors))],\
               'SMB': [factors[j][1] for j in range(0, len(factors))], \
               'HML': [factors[j][2] for j in range(0, len(factors))]}
    #pandas data frame
    df = pd.DataFrame(data=dep_var)
    #looping through each stock/asset
    for i in range(0, len(rets[0])):
        #independent var dictionary for setting up pd data frame
        indep_str = 'r ' + str((i + 1))
        indep_var ={indep_str: [rets[j][i] for j in range(0, len(rets))]}
        #set up a pandas data frame
        target = pd.DataFrame(data=indep_var)
        #do linear regression
        X = df[["Market", "HML", "SMB"]]
        #add constant for alpha
        X = sm.add_constant(X)
        y = target[indep_str]
        model = sm.OLS(y, X).fit()
        ff3coeff_i = [model.params.const, model.params.Market, \
                      model.params.SMB, model.params.HML]
        ff3coeff.append(ff3coeff_i)

    return np.array(ff3coeff)

#maybe add a function that plots the return estimate values... - in the interest of time...
#let's leave this for later...

#ok... what about BL?  Can we write up something in relation to that?

#Ignore this for now... was just testing out plotting in python...
def plotrets (tickers, mu, Q):
    mupsd = []
    mumsd = []
    tkrs = tkr.FixedFormatter(["", ""] + tickers)
    for i in range(0, len(mu)):
        sd = math.sqrt(Q[i][i])
        mupsd.append(mu[i] + sd)
        mumsd.append(mu[i] - sd)

    fig = plt.figure(figsize = (12,8))
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(tkr.MultipleLocator(1.0))
    ax.xaxis.set_major_formatter(tkrs)

    ax.scatter(range(0,len(tickers)),  mu, s=10, c='b', marker="s", label='mu')
    ax.scatter(range(0,len(tickers)),mupsd, s=10, c='r', marker="o", label='mu + sd')
    ax.scatter(range(0,len(tickers)),mumsd, s=10, c='g', marker="o", label='mu - sd')
    plt.legend(loc='upper left');
    plt.show()


