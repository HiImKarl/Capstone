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
    mu_mkt = sum(mu*x_mkt)
    return mu_mkt-np.mean(rf) / var_mkt


# function that compute equilibrium returns
def bl_pi(mkt_cap, mu, q, rf):
    rav_coeff = bl_lambda(mkt_cap, mu, q, rf)
    x_mkt = mkt_cap / np.sum(mkt_cap)
    return rav_coeff * np.matmul(q, x_mkt)


# tutorialer function for view gen
def in_flags(flags, flags_i):
    for i in range(len(flags)):
        if flags[i] == flags_i:
            return True
    return False


# generates view matrices and vectors for us
# returns views of various types
# provides the imlied equilibrium assets of the views
# centres views around factor model estimates for now
# k is number of views
def view_gen(stocks, mu, k, mkt_cap,  type = 0):
    # view matrix; # last column will be view
    p = []
    q = []
    # type 0 are the absolute views
    if type == 0:
        flags = []
        for i in range(stocks):
            flags.append(False)
        for i in range(k):
            # need to add some sort of way to confirm if asset has already been chosen or not
            # idea flags
            asset = int(math.floor(random.random()*stocks))
            # if collision use linear probing to get next chosen asset
            while flags[asset]:
                asset = (asset + 1)%stocks
            flags[asset] = True
            pi = []
            for j in range(stocks):
                if j == asset:
                    pi.append(1)
                else:
                    pi.append(0)
            p.append(pi)
            q.append(mu[asset])
    elif type == 1:
        # type 1 will cover relative views
        # for this will need a flags matrix to cover pair combinations
        flags = []
        for i in range(stocks):
            flags_i = []
            for j in range(stocks):
                # we will not one two assets in a pair to be same
                if i == j:
                    flags_i.append(True)
                flags_i.append(False)
            flags.append(flags_i)
        # now to generate views
        for i in range(k):
            asset_r = int(math.floor(random.random()*stocks))
            asset_c = int(math.floor(random.random()*stocks))
            # like before use linear probing to handle collisions
            while flags[asset_r][asset_c]:
                toss = random.random()
                if toss > 0.5:
                    asset_r = (asset_r + 1)%stocks
                else:
                    asset_c = (asset_c + 1)%stocks
            flags[asset_r][asset_c] = True
            flags[asset_c][asset_r] = True
            # now create row for view
            pi = []
            for j in range(stocks):
                if j == asset_r:
                    pi.append(1)
                elif j == asset_c:
                    pi.append(-1)
                else:
                    pi.append(0)
            p.append(pi)
            q.append(mu[asset_r] - mu[asset_c])
    elif type == 2:
        # by far the most complex... this will feature compound views
        # since the amount of assets to feature will show lot of variance...
        # flags probably not as useful as before... so what can I do?!
        # idea: can still use flags but need to structure it a bit differently...
        flags = []
        for i in range(k):
            # number of assets to form compound view on
            flags_i = [False]*stocks
            comp_assets = int(math.ceil(random.random()*stocks/2))
            # ok...
            assets = []
            for j in range(comp_assets*2):
                asset = int(math.floor(random.random()*stocks))
                while flags_i[asset]:
                    asset = (asset + 1)%stocks
                flags_i[asset] = True
                assets.append(asset)
            # use tutorialer function here
            # keep repeating the asset generation step until it is not a duplicate:
            while in_flags(flags, flags_i):
                # number of assets to form compound view on
                flags_i = [False]*stocks
                comp_assets = int(math.ceil(random.random()*stocks/2))
                # ok...
                assets = []
                for j in range(comp_assets*2):
                    asset = int(math.floor(random.random()*stocks))
                    while flags_i[asset]:
                        asset = (asset + 1)%stocks
                    flags_i[asset] = True
                    assets.append(asset)
            # update flags
            flags.append(flags_i)
            # construct view
            mkt_capi = 0
            for j in range(len(assets)):
                mkt_capi += mkt_cap[assets[j]]
            pi = [0]*stocks
            qi = 0
            for j in range(len(assets)):
                if j < comp_assets:
                    pi[assets[j]] = mkt_cap[assets[j]]/mkt_capi
                    qi += pi[assets[j]] * mu[assets[j]]
                else:
                    pi[assets[j]] = -mkt_cap[assets[j]]/mkt_capi
                    qi += pi[assets[j]] * mu[assets[j]]
            p.append(pi)
            q.append(qi)
    elif type == 3:
        # type 3 will cover a hybrid of all three variations
        flags1 = [False]*stocks
        flags2 = []
        for i in range(stocks):
            flags2i = []
            for j in range(stocks):
                if j == i:
                    flags2i.append(True)
                else:
                    flags2i.append(False)
            flags2.append(flags2i)
        flags3 = []

        # generate views
        for i in range(k):

            # randomly decide which type to use
            currType = int(math.floor(random.random()*3))
            if currType == 0:
                asset = int(math.floor(random.random()*stocks))

                # if collision use linear probing to get next chosen asset
                while flags1[asset]:
                    asset = (asset + 1)%stocks
                flags1[asset] = True
                pi = []
                for j in range(stocks):
                    if j == asset:
                        pi.append(1)
                    else:
                        pi.append(0)
                p.append(pi)
                q.append(mu[asset])
            elif currType == 1:
                asset_r = int(math.floor(random.random()*stocks))
                asset_c = int(math.floor(random.random()*stocks))

                # like before use linear probing to handle collisions
                while flags2[asset_r][asset_c]:
                    toss = random.random()
                    if toss > 0.5:
                        asset_r = (asset_r + 1)%stocks
                    else:
                        asset_c = (asset_c + 1)%stocks
                flags2[asset_r][asset_c] = True
                flags2[asset_c][asset_r] = True
                
                # create row for view
                pi = []
                for j in range(stocks):
                    if j == asset_r:
                        pi.append(1)
                    elif  j == asset_c:
                        pi.append(-1)
                    else:
                        pi.append(0)
                p.append(pi)
                q.append(mu[asset_r] - mu[asset_c])
            elif currType == 2:
                # number of assets to form compound view on
                flags_i = [False]*stocks
                comp_assets = int(math.ceil(random.random()*stocks/2))
                assets = []
                for j in range(comp_assets*2):
                    asset = int(math.floor(random.random()*stocks))
                    while flags_i[asset]:
                        # print "Stuck here"
                        asset = (asset + 1)%stocks
                    flags_i[asset] = True
                    assets.append(asset)
                # keep repeating the asset generation step until it is not a duplicate:
                while in_flags(flags3, flags_i):
                    # number of assets to form compound view on
                    # print "Stuck here"
                    flags_i = [False]*stocks
                    comp_assets = int(math.ceil(random.random()*stocks/2))
                    # ok...
                    assets = []
                    for j in range(comp_assets*2):
                        asset = int(math.floor(random.random()*stocks))
                        while flags_i[asset]:
                            asset = (asset + 1)%stocks
                        flags_i[asset] = True
                        assets.append(asset)

                # update flags
                flags3.append(flags_i)

                # construct view
                mkt_capi = 0
                for j in range(len(assets)):
                    mkt_capi += mkt_cap[assets[j]]
                pi = [0]*stocks
                qi = 0
                for j in range(len(assets)):
                    if j < comp_assets:
                        pi[assets[j]] = mkt_cap[assets[j]]/mkt_capi
                        qi += pi[assets[j]] * mu[assets[j]]
                    else:
                        pi[assets[j]] = -mkt_cap[assets[j]]/mkt_capi
                        qi += pi[assets[j]] * mu[assets[j]]
                p.append(pi)
                q.append(qi)
    return np.array(p), np.array(q)
    

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
def bl_cr(mkt_cap, mu, q, rf, tau, k):
    pi = bl_pi(mkt_cap, mu, q, rf)
    view_matrix, views_vector = view_gen(len(mu), mu - np.mean(rf), k, mkt_cap, 3)
    omega = omega_gen(view_matrix, q, tau)
    x1 = np.linalg.inv(tau * q)
    x2 = np.matmul(np.matmul(view_matrix.transpose(), np.linalg.inv(omega)), view_matrix)
    x3 = np.linalg.inv(x1 + x2)
    x4 = np.matmul(x1, pi)
    x5 = np.matmul(np.matmul(view_matrix.transpose(), np.linalg.inv(omega)), view_vector)
    x6 = x4 + x5
    return np.matmul(x3, x6)


def bl_weights_normalized(retvec, rac, q):
    w = np.matmul(np.linalg.inv(rac * q), retvec)
    return w / np.sum(w)


# put everything together to make a function
# need rets, factors, risk free and market cap probably
def blacklitterman(mu, q, rf, mkt_cap, tau = 0.02, K = 10):
    # use factor modelling to get estimates
    rac = bl_lambda(mkt_cap, mu, q, rf)
    cr = bl_cr(mkt_cap, mu, q, rf, tau, K)
    w = bl_weights_normalized(cr, rac, q)

    return w
