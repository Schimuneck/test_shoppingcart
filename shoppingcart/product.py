
"""product.py: Defines a representation of a product of a shoppint cart."""

__author__      = "Matias A. K. Schimuneck"
__copyright__   = "Copyright 2019, Blueface - Dublin"

import datetime
from currency_converter import CurrencyConverter

class Product():
	""" 
	"""

	def __init__(self, code: str, price: float):
		""" Simplified CTOR
        :param string product code, float product price
        """
		self.__code = code  	# private attributes 
		self.__price = price 	 
		self.__lastupdate = ""	
		self.__currency = ""	
		self.__converter = CurrencyConverter()

	def __init__(self, code: str, price: float, lastupdate: str, currency: str):
		""" CTOR
        :param string product code, float product price, string product last data update, string [EUR, GBP, USD] currency type
        """
		self.__code = code 		# private attributes 
		self.__price = price
		self.__lastupdate = datetime.datetime.strptime(lastupdate, '%d-%m-%Y')
		self.__currency = currency
		self.__converter = CurrencyConverter()


	def get_code(self) -> str:
		return self.__code

	def get_price(self) -> float:
		return self.__price

	def set_price(self, price: float):
		self.__price = price

	def get_lastupdate(self) -> datetime:
		""" Usefull to validate the newest data if the same data are duplicated in different sources
        :param 
        :return: Return the date when the item was insert in the dataset
        """
		return self.lastupdate

	def set_last_update(self, lastupdate: datetime):
		self.__lastupdate = datetime.datetime.strptime(lastupdate, '%d-%m-%Y')

	def get_currency(self) -> str:
		return self.lastupdate

	def set_currency(self, currency: str):
		self.__currency = currency

	def get_price_in_other_currency(self, currency: str) -> float:
		""" Use CurrencyConverter with uptodate money data converter from the European Central Bank
        :param currency: the required currency to return the price
        :return: float price value in the new currency
        """
		return self.__converter.convert(round(self.__price, 2), self.__currency, currency)  #Round the price to guarantee consistency
