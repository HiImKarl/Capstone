import requests

params = {
        'action': 'history',
        'symbol': 'MSFT',
        'interval': 'daily',
        'period': 10
        }

print(requests.get(url='http://api.kibot.com/', params=params).content.decode('utf-8'))

