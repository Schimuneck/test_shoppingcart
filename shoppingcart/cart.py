
"""cart.py: Shopping cart routines to generate receipt."""

__author__      = "Matias A. K. Schimuneck"
__copyright__   = "Copyright 2019, Blueface - Dublin"

import typing
import json
import collections

from . import abc
from readers.price_reader import PriceReader
from datetime import datetime

import logging
LOG_FILENAME = 'shoppingcart.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

## CURRENCY DEFINITIONS ##
EURcurrency = 'EUR'
USDcurrency = 'USD'
GBPcurrency = 'GBP'

class ShoppingCart(abc.ShoppingCart):
    def __init__(self, reader: PriceReader):
        """ CTOR
        :param reader: receive a reader that will provide the product price data
        """
        self._items = collections.OrderedDict() #protected attributes
        self._products = reader.get_products()
        ### DEBUG ###
        logging.debug(str(datetime.now())+': New shopping car created')
       

    def add_item(self, product_code: str, quantity: int):
        """ Add an item (if valid) to the shopping list
        :param string product code and integer quantity
        :return: 
        """
        if quantity > 0:
            # IF is a new item
            if product_code not in self._items and product_code in self._products:
                self._items[product_code] = quantity
                ### DEBUG ###
                logging.debug(str(datetime.now())+': Adding item ' + product_code + ' with quantity ' + str(quantity))
            # IF is to increment an existent item 
            elif product_code in self._products:
                q = self._items[product_code]
                self._items[product_code] = q + quantity
                ### DEBUG ###
                logging.debug(str(datetime.now())+': Updating item ' + product_code + ' with more ' + str(quantity))
            # IF product code is not valid
            else:
                ### DEBUG ###
                logging.warning(str(datetime.now())+': Invalid product code.')
        else:
            ### DEBUG ###
            logging.warning(str(datetime.now())+': Invalid product quantity.')

    def print_receipt(self) -> typing.List[str]:
        """ Generete the shopping receipt with the pre added product itens
        :param 
        :return: String list with each line of the receipt including the last Total line
        """
        lines = []

        total_price = 0.0
        total_usd_price = 0.0
        total_gbp_price = 0.0

        ### DEBUG ###
        logging.debug(str(datetime.now())+': Printing receipt')

        for item in self._items.items():
            price = round(self._products[item[0]].get_price(), 2) * item[1] #Round the price to guarantee consistency in the recepit Total value and itens products sum
            # Try to make the cast of the price of the value from EUR to USD and GBP currencies
            try:
                price_usd = self._products[item[0]].get_price_in_other_currency(USDcurrency) * item[1]
                price_gbp = self._products[item[0]].get_price_in_other_currency(GBPcurrency)* item[1]
            except Exception as e: 
                ### DEBUG ###
                logging.error(str(datetime.now())+': ' + e)


            # Sum individualy the total price of the receipt for each supported currency
            total_price += price
            total_usd_price += price_usd
            total_gbp_price += price_gbp

            # Parse prices to print in the receipt
            price_string = "€%.2f" % price
            price_usd_string = "$%.2f" % price_usd
            price_gbp_string = "£%.2f" % price_gbp

            # Add the item generated data to the receipt lines
            lines.append(item[0] + " - " + str(item[1]) + ' - ' + price_string + ' - ' + price_usd_string + ' - ' + price_gbp_string)
            
            ### DEBUG ###
            list_lisnes_length = len(lines)
            logging.debug(str(datetime.now())+': Receipt line ' + str(list_lisnes_length) + ': ' + lines[list_lisnes_length-1])

        # Parse prices to print the Total line in the receipt
        total_price_string = "€%.2f" % total_price
        total_usd_price_string = "$%.2f" % total_usd_price
        total_gbp_price_string = "£%.2f" % total_gbp_price

        # Add the Total generated data to the receipt as the last line
        lines.append("Total: " + total_price_string + ' - ' + total_usd_price_string + ' - ' + total_gbp_price_string)
        
        ### DEBUG ###
        list_lisnes_length = len(lines)
        logging.debug(str(datetime.now())+': Receipt final line ' + str(list_lisnes_length) + ': ' + lines[list_lisnes_length-1])
        
        return lines


        
