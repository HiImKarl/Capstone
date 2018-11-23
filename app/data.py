import csv
import quandl
import datetime
import requests
from dateutil.relativedelta import relativedelta
from instance.config import INTRINIO_API_KEY_DAVID, QUANDL_API_KEY
from app.util import limit_list_size, synchronize_list

# maximum number of data points we want to extract
MAX_NUMBER_DATA_POINTS = 500


with open('data/stock_tickers.csv', 'r') as f:
    reader = csv.reader(f)
    STOCK_TICKERS = [ticker.strip() for ticker in list(reader)[0]]
    # FIXME
    STOCK_TICKERS = STOCK_TICKERS[0:10]

with open('data/etf_tickers.csv', 'r') as f:
    reader = csv.reader(f)
    ETF_TICKERS = [ticker.strip() for ticker in list(reader)[0]]

with open('data/factors.csv') as f:
    reader = csv.reader(f)
    FF_FACTORS = []
    for count, row in enumerate(reader):
        # the first column is the date
        FF_FACTORS.append((float(row[1]), float(row[2]),
                           float(row[3]), float(row[4])))

        if count == MAX_NUMBER_DATA_POINTS:
            break

QUANDL_US_STOCK_DB_NAME = 'WIKI'
quandl.ApiConfig.api_key = QUANDL_API_KEY

INTRINIO_URL_BASE = 'https://api.intrinio.com/'

TODAY_DATETIME = datetime.datetime.now()
PAST_DATETIME = datetime.datetime.now() - relativedelta(years=10)


def intrinio_historical_market_cap(ticker):
    """
    :param ticker: string stock ticker for query
    :return: a list from of the ticker's market cap
    from PAST_DATETIME to TODAY_DATETIME, with weekly frequency
    """

    params = {
        'item': 'marketcap',
        'ticker': ticker,
        'start_date': PAST_DATETIME.strftime('%Y-%m-%d'),
        'end_date': TODAY_DATETIME.strftime('%Y-%m-%d'),
        'frequency': 'weekly',
        'api_key': INTRINIO_API_KEY_DAVID
    }

    response = requests.get(url=INTRINIO_URL_BASE + 'historical_data', params=params)
    json_data = response.json()
    data = [data_point['value'] for data_point in json_data['data']]

    return data


def get_sp500_data():
    """
    :return: a 3 element tuple: a dictionary that maps stock ticker to shares
    outstanding, and a dictionary that maps stock ticker to numpy array of stock prices,
    both for the time periods between TODAY_DATETIME, PAST_DATETIME
    """
    prices = {}
    market_cap = {}

    # FIXME
    for i in range(len(STOCK_TICKERS)):
        # tenth column is adjusted close
        raw_data = quandl.get(QUANDL_US_STOCK_DB_NAME + '/' + STOCK_TICKERS[i],
                              start_date=PAST_DATETIME.strftime('%Y-%m-%d'),
                              collapse='weekly',
                              end_date=TODAY_DATETIME.strftime('%Y-%m-%d'),
                              returns='pandas')

        price_array = raw_data.iloc[:, [10]].values
        price_array = [price[0] for price in price_array]

        # quandl returns data from earliest to latest, want other way around
        price_array.reverse()

        market_cap_array = intrinio_historical_market_cap(STOCK_TICKERS[i])

        # ensure the arrays are the same size and not
        # greater than the maximum data point cap
        price_array = limit_list_size(price_array, MAX_NUMBER_DATA_POINTS)
        market_cap_array = limit_list_size(market_cap_array, MAX_NUMBER_DATA_POINTS)
        price_array, market_cap_array = synchronize_list(price_array, market_cap_array)

        prices[STOCK_TICKERS[i]] = price_array
        market_cap[STOCK_TICKERS[i]] = market_cap_array

    print("Done grabbing stock data")
    return market_cap, prices
