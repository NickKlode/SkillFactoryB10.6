import requests
import json
from config import currencies

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = currencies[base.title()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = currencies[quote.title()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}")
        resp = json.loads(r.content)
        new_price = resp[currencies[quote]] * float(amount)
        new_price = round(new_price, 3)
        return new_price
