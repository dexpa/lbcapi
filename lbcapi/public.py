import requests, requests_cache
from cachecontrol import CacheControl


class LocalbitcoinsPublic:

    def __init__(self):
        self.__session = requests.session()
        self.__cached_sess = CacheControl(self.__session)

    def get_url(self, endpoint):
        return 'https://localbitcoins.com' + endpoint

    def get_fiat_symbols(self):
        endpoint = '/api/currencies/'
        response = self.__cached_sess.get(self.get_url(endpoint))
        return response.json()

    def get_payment_methods(self):
        endpoint = '/api/payment_methods/'
        response = self.__cached_sess.get(self.get_url(endpoint))
        return response.json()

    def get_service_fees(self):
        endpoint = '/api/fees/'
        response = self.__cached_sess.get(self.get_url(endpoint))
        return response.json()

    def get_averaged_data(self):
        endpoint = '/bitcoinaverage/ticker-all-currencies/'
        response = self.__cached_sess.get(self.get_url(endpoint))
        return response.json()

    def get_buying_offers(self, currency):
        endpoint = '/sell-bitcoins-online/{:s}/.json'.format(currency)
        response = self.__cached_sess.get(self.get_url(endpoint))
        return response.json()

    def get_selling_offers(self, currency):
        endpoint = '/buy-bitcoins-online/{:s}/.json'.format(currency)
        response = self.__cached_sess.get(self.get_url(endpoint))
        return response.json()

    def get_trades(self, currency):
        endpoint = '/bitcoincharts/{:s}/trades.json'.format(currency)
        response = self.__cached_sess.get(self.get_url(endpoint))
        return response.json()

    def get_orderbook(self, currency):
        endpoint = '/bitcoincharts/{:s}/orderbook.json'.format(currency)
        response = self.__cached_sess.get(self.get_url(endpoint))
        return response.json()



