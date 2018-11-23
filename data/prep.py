filt = ['ABBV', 'AYI', 'ALLE', 'GOOG', 'ANDV', 'APTV', 'BHGE', 'BKNG', 'BHF', 'AVGO', 'CBOE', 'CBRE', 'CHTR', 'CFG', 'ED', 'COTY', 'CSRA', 'DG', 'DWDP', 'DPS', 'DXC', 'ETN', 'EVHC', 'ESRX', 'FB', 'FTV', 'FBHS', 'GM', 'HCA', 'HPE', 'HLT', 'HII', 'INFO', 'INCY', 'ICE', 'IPGP', 'IQV', 'KMI', 'KHC', 'LUK', 'LYB', 'MPC', 'KORS', 'MU', 'MYL', 'NAVI', 'NKTR', 'NWSA', 'NWS', 'NLSN', 'NCLH', 'PYPL', 'PRGO', 'PSX', 'PPG', 'QRVO', 'SPGI', 'SYF', 'TPR', 'FTI', 'TRV', 'TRIP', 'ULTA', 'UAA', 'UA', 'URI', 'VRSK', 'WELL', 'WRK', 'WLTW', 'WYN','XYL','ZTS']

with open('stock_tickers.csv') as f:
    p = f.read().split(',')
    print(len(p))
    filtered = []
    for ticker in p:
        if not ticker in filt:
            filtered.append(ticker)
        else:
            print(ticker)

    print(len(filtered))
    out_f = open("output.csv", "w")
    out_f.write(",".join(filtered))
