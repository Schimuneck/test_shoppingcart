import typing

from . import abc


class ShoppingCart(abc.ShoppingCart):
    def __init__(self):
        self._items = dict()

    def add_item(self, product_code: str, quantity: int):
        if product_code not in self._items:
            self._items[product_code] = quantity
        else:
            q = self._items[product_code]
            self._items[product_code] = q + quantity

    def print_receipt(self) -> typing.List[str]:
        lines = []

        for item in self._items.items():
            price = self._get_product_price(item[0]) * item[1]

            price_string = "€%.2f" % price

            lines.append(item[0] + " - " + str(item[1]) + ' - ' + price_string)

        return lines

    def _get_product_price(self, product_code: str) -> float:
        price = 0.0

        if product_code == 'apple':
            price = 1.0

        elif product_code == 'banana':
            price = 1.1

        elif product_code == 'kiwi':
            price = 3.0

        return price
