import json
import requests
import requests_cache
from cachecontrol import CacheControl


class LocalbitcoinsPublic:

    def __init__(self, caching=True):
        self.__session = requests.session()
        self.__cached_sess = CacheControl(self.__session)
        self.__sql_caching = caching

    def get_url(self, endpoint):
        return 'https://localbitcoins.com' + endpoint

    def get_fiat_symbols(self):
        endpoint = '/api/currencies/'
        response = self.__cached_sess.get(self.get_url(endpoint))
        try:
            if response.status_code == 200:
                d = response.json()
            else:
                d = []
        except json.decoder.JSONDecodeError:
            print("JSON decode error: {}".format(endpoint))
            d = []
        return d

    def get_payment_methods(self):
        endpoint = '/api/payment_methods/'
        response = self.__cached_sess.get(self.get_url(endpoint))
        try:
            if response.status_code == 200:
                d = response.json()
            else:
                d = []
        except json.decoder.JSONDecodeError:
            print("JSON decode error: {}".format(endpoint))
            d = []
        return d

    def get_service_fees(self):
        endpoint = '/api/fees/'
        response = self.__cached_sess.get(self.get_url(endpoint))
        try:
            if response.status_code == 200:
                d = response.json()
            else:
                d = []
        except json.decoder.JSONDecodeError:
            print("JSON decode error: {}".format(endpoint))
            d = []
        return d

    def get_averaged_data(self):
        endpoint = '/bitcoinaverage/ticker-all-currencies/'
        response = self.__cached_sess.get(self.get_url(endpoint))
        try:
            if response.status_code == 200:
                d = response.json()
            else:
                d = []
        except json.decoder.JSONDecodeError:
            print("JSON decode error: {}".format(endpoint))
            d = []
        return d

    def get_online_offers(self, currency, side="buy", page=0):
        if page != 0:
            endpoint = '/{}-bitcoins-online/{:s}/.json?page={}'.format(side, currency, page)
        else:
            endpoint = '/{}-bitcoins-online/{:s}/.json'.format(side, currency)
        response = self.__cached_sess.get(self.get_url(endpoint))
        try:
            if response.status_code == 200:
                d = response.json()
            else:
                d = []
        except json.decoder.JSONDecodeError:
            print("JSON decode error: {}".format(endpoint))
            d = []
        return d

    def get_trades(self, currency, last=0):

        if self.__sql_caching:
            requests_cache.install_cache('trades_history', expire_after=900)

        if last != 0:
            endpoint = '/bitcoincharts/{:s}/trades.json?since={}'.format(currency, last)
        else:
            endpoint = '/bitcoincharts/{:s}/trades.json'.format(currency)
        response = self.__cached_sess.get(self.get_url(endpoint))
        try:
            if response.status_code == 200:
                d = response.json()
            elif response.status_code != 400:
                print("HTTP {}. Repeating...".format(response.status_code))
                response = self.__cached_sess.get(self.get_url(endpoint))
                d = response.json()
            elif response.status_code == 400:
                print("lbapi get_trades 400: {}".format(response.text))
                endpoint = '/bitcoincharts/{:s}/trades.json'.format(currency)
                response = self.__cached_sess.get(self.get_url(endpoint))
                trades = response.json()
                idx = next((index for (index, row) in enumerate(trades) if int(row["tid"]) == last), 0)
                d = trades[idx+1:]
            else:
                d = []
            return d
        except json.decoder.JSONDecodeError:
            print("JSON decode error: {}".format(endpoint))
            d = []
        return d

    def get_orderbook(self, currency):
        endpoint = '/bitcoincharts/{:s}/orderbook.json'.format(currency)
        response = self.__cached_sess.get(self.get_url(endpoint))
        try:
            if response.status_code == 200:
                d = response.json()
            else:
                d = []
        except json.decoder.JSONDecodeError:
            print("JSON decode error: {}".format(endpoint))
            d = []
        return d



