import csv
import datetime
import requests
from dateutil.relativedelta import relativedelta
from instance.config import INTRINIO_API_KEYS
from app.util import limit_list_size

# rotate calls to our API keys LUL
intrinio_api_key_index = 0

# maximum number of data points we want to extract
MAX_NUMBER_DATA_POINTS = 500
INTRINIO_URL_BASE = 'https://api.intrinio.com/'
TODAY_DATETIME = datetime.datetime.now()
PAST_DATETIME = datetime.datetime.now() - relativedelta(years=10)

with open('data/stock_tickers.csv', 'r') as f:
    reader = csv.reader(f)
    STOCK_TICKERS = [ticker.strip() for ticker in list(reader)[0]]
    # FIXME
    STOCK_TICKERS = STOCK_TICKERS[0:10]

with open('data/etf_tickers.csv', 'r') as f:
    reader = csv.reader(f)
    ETF_TICKERS = [ticker.strip() for ticker in list(reader)[0]]

with open('data/factors.csv', 'r') as f:
    reader = csv.reader(f)
    FF_FACTORS = []
    for row in reader:
        # the first column is the date
        FF_FACTORS.append((float(row[1]), float(row[2]),
                           float(row[3]), float(row[4])))


def intrinio_historical_data(ticker, item):
    """
    :param: ticker: string stock ticker for query
    :item: string representing the data item, i.e. 'close_price' or 'marketcap'
    :return: a list from of the ticker's market cap
    from PAST_DATETIME to TODAY_DATETIME, with weekly frequency
    """

    params = {
        'item': item,
        'ticker': ticker,
        'start_date': PAST_DATETIME.strftime('%Y-%m-%d'),
        'end_date': TODAY_DATETIME.strftime('%Y-%m-%d'),
        'frequency': 'weekly',
        'api_key': INTRINIO_API_KEYS[intrinio_api_key_index]
    }

    # increment api key index LUL
    global intrinio_api_key_index
    intrinio_api_key_index += 1
    if intrinio_api_key_index == len(INTRINIO_API_KEYS):
        intrinio_api_key_index = 0

    # request json from intrinio
    response = requests.get(url=INTRINIO_URL_BASE + 'historical_data', params=params)
    json_data = response.json()
    data = [data_point['value'] for data_point in json_data['data']]

    # intrinio returns data from latest to earliest, want other way around
    data.reverse()
    return data


def get_sp500_data():
    """
    :return: a 3 element tuple: a dictionary that maps stock ticker to shares
    outstanding, and a dictionary that maps stock ticker to numpy array of stock prices,
    both for the time periods between TODAY_DATETIME, PAST_DATETIME
    """
    prices = {}
    market_cap = {}

    for TICKER in STOCK_TICKERS:
        price_array = intrinio_historical_data(TICKER, 'adj_close_price')
        market_cap_array = intrinio_historical_data(TICKER, 'marketcap')

        # ensure the arrays are the same size and not
        # greater than the maximum data point cap
        price_array = limit_list_size(price_array, MAX_NUMBER_DATA_POINTS)
        market_cap_array = limit_list_size(market_cap_array, MAX_NUMBER_DATA_POINTS)

        prices[TICKER] = price_array
        market_cap[TICKER] = market_cap_array

    print("Done grabbing stock data")
    return market_cap, prices
