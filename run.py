import json
import logging
import graphyte
import requests
from dateutil import parser as dt_parser


logging.getLogger().setLevel(logging.INFO)


BASE_URL = 'https://api.solcast.com.au/weather_sites/dbc7-55a4-c43f-60ac/{}'
API_KEY = 'MlDW_Fxq226KaAxd5qro9FIEP6u3Sm3e'


def fetch_data(info_type):
    result = requests.get(
        BASE_URL.format(info_type),
        params={'format': 'json', 'api_key': API_KEY},
    ).json()[info_type]
    result = list(map(
        lambda info: (info['ghi'], dt_parser.parse(info['period_end']).timestamp()),
        result,
    ))
    return result


def get_current_radiation():
    return fetch_data('estimated_actuals')


def get_forecast():
    return fetch_data('forecasts')


GRAPHITE_HOST = 'graphite'


def send_metrics(radiation, info_type):
    sender = graphyte.Sender(GRAPHITE_HOST, prefix='radiation')
    for r in radiation:
        sender.send(info_type, r[0], timestamp=r[1] - 10000)


def main():
    current_radiation = get_current_radiation()
    forecast = get_forecast()
    logging.info(forecast[:10])
    send_metrics([current_radiation[0]], 'real')
    send_metrics(forecast, 'forecast')


if __name__ == '__main__':
    main()
