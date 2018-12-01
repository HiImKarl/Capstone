import csv
import datetime
import requests
import io
from dateutil.relativedelta import relativedelta
from instance.config import INTRINIO_API_KEYS
from app.util import limit_list_size

# rotate calls to our API keys LUL
intrinio_api_key_index = 0

# maximum number of data points we want to extract
MAX_NUMBER_DATA_POINTS = 600

# urls
INTRINIO_URL_BASE = 'https://api.intrinio.com/'
KIBOT_URL_BASE = 'http://api.kibot.com/'

# start end dates in datetime format
TODAY_DATETIME = datetime.datetime.now()
PAST_DATETIME = datetime.datetime.now() - relativedelta(years=10)

with open('data/stock_tickers.csv', 'r') as f:
    reader = csv.reader(f)
    STOCK_TICKERS = [ticker.strip() for ticker in list(reader)[0]]
    # FIXME
    STOCK_TICKERS = STOCK_TICKERS[0:10]

# FIXME can't find data for etf market cap, so just assume
# constant shares outstanding...
with open('data/etf_tickers.csv', 'r') as f:
    reader = csv.reader(f)
    ETF_TICKERS = [ticker.strip() for ticker in list(reader)[0]]

TICKERS = STOCK_TICKERS + ETF_TICKERS

with open('data/etf_shares.csv') as f:
    reader = csv.reader(f)
    ETF_SHARES_OUTSTANDING = {}
    shares_outstanding = list(reader)[0]
    assert len(shares_outstanding) == len(ETF_TICKERS)
    for i in range(len(shares_outstanding)):
        ETF_SHARES_OUTSTANDING[ETF_TICKERS[i]] = float(shares_outstanding[i])

with open('data/factors.csv', 'r') as f:
    reader = csv.reader(f)
    FF_FACTORS = []
    RISK_FREE = []
    for row in reader:
        # the first column is the date
        FF_FACTORS.append((float(row[1]), float(row[2]),
                           float(row[3])))
        RISK_FREE.append(float(row[4]))


def intrinio_historical_data(ticker, item):
    """
    :param: ticker: string stock ticker for query
    :item: string representing the data item, i.e. 'adj_close_price' or 'marketcap'
    :return: a list from of the ticker's item
    from PAST_DATETIME to TODAY_DATETIME, with weekly frequency
    """

    global intrinio_api_key_index

    params = {
        'item': item,
        'ticker': ticker,
        'start_date': PAST_DATETIME.strftime('%Y-%m-%d'),
        'end_date': TODAY_DATETIME.strftime('%Y-%m-%d'),
        'frequency': 'weekly',
        'api_key': INTRINIO_API_KEYS[intrinio_api_key_index]
    }

    # increment api key index LUL
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


def kibot_historical_price(ticker):
    """
    :param: ticker: string stock ticker for query
    :return: a list from of the ticker's market cap
    from PAST_DATETIME to TODAY_DATETIME, with weekly frequency
    """
    params = {
        'action': 'history',
        'symbol': ticker,
        'interval': 'weekly',
        'period': 3650
    }

    content = requests.get(url=KIBOT_URL_BASE, params=params).content.decode('utf-8')
    content = csv.reader(io.StringIO(content))
    # data is given from earliest to latest, which is what we want
    # column 4 is the adjusted_close price

    data = []
    for point in content:
        data.append(float(point[4]))

    return data


def log_into_kibot():
    """
    logins into kibot with guest credentials
    :return: None
    """
    params = {
        'action': 'login',
        'user': 'guest',
        'password': 'guest'
    }

    requests.get(KIBOT_URL_BASE, params=params)


def get_asset_data():
    """
    :return: a 2 element tuple: a dictionary that maps stock ticker to market
    cap, and a dictionary that maps stock ticker to numpy array of stock prices,
    both for the time periods between TODAY_DATETIME, PAST_DATETIME
    """

    # necessary to make API calls to kibot
    log_into_kibot()

    prices = {}
    market_cap = {}

    # find the smallest number of data points and limit all other data sets
    # to this number; date synchronization would be preferable but YOLO

    smallest_length = MAX_NUMBER_DATA_POINTS

    for TICKER in STOCK_TICKERS:
        price_array = intrinio_historical_data(TICKER, 'adj_close_price')
        market_cap_array = intrinio_historical_data(TICKER, 'marketcap')

        if smallest_length > len(price_array):
            smallest_length = len(price_array)

        if smallest_length > len(market_cap_array):
            smallest_length = len(market_cap_array)

        prices[TICKER] = price_array
        market_cap[TICKER] = market_cap_array

    for TICKER in ETF_TICKERS:
        price_array = kibot_historical_price(TICKER)
        market_cap_array = [ETF_SHARES_OUTSTANDING[TICKER] * price for price in price_array]

        if smallest_length > len(price_array):
            smallest_length = len(price_array)

        if smallest_length > len(market_cap_array):
            smallest_length = len(market_cap_array)

        prices[TICKER] = price_array
        market_cap[TICKER] = market_cap_array

    # ensure the arrays are the same size and not
    # greater than the maximum data point cap

    for key in prices.keys():
        prices[key] = limit_list_size(prices[key], smallest_length)

    for key in market_cap.keys():
        market_cap[key] = limit_list_size(market_cap[key], smallest_length)

    return market_cap, prices

