
"""price_reader.py: Defines an abstract PriceReader class and two different data reader from JSON and SQLite database."""

__author__      = "Matias A. K. Schimuneck"
__copyright__   = "Copyright 2019, Blueface - Dublin"

import abc
import typing
import json

from lib.database import Database
from shoppingcart.product import Product

import logging
LOG_FILENAME = 'shoppingcart.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

class PriceReader(abc.ABC):
	"""
	Abstract class to define shopping data reader
	"""

	@abc.abstractmethod
	def __init__(self, file_path: str):
		pass

	@abc.abstractmethod
	def get_products(self) -> dict:
		pass


class JSONPriceReader(PriceReader):

	def __init__(self, file_path: str):
		""" CTOR
		:param file_path: json data file path
		"""
		self._file_path = file_path

	def get_products(self) -> dict:
		""" Method to read and return the shopping data from a JSON file
		:param 
		:return: dict
		"""
		products = dict()

		with open(self._file_path) as json_data:
			data = json.load(json_data)
			
			# ::TODO:: check data validity

			for product in data["data"]["products"]:
				if product["code"] not in products:

					# ::TODO:: Here I assumed that all the data was correctly parsed in the JSON file

					products[product["code"]] = Product(product["code"], product["price"], product["lastupdate"], product["currency"])

		return products

class SQLitePriceReader(PriceReader):

	def __init__(self, file_path: str):
		""" CTOR
		:param file_path: SQLite data file path
		"""
		self._file_path = file_path

	def get_products(self) -> dict:
		""" Method to read and return the shopping data from a SQLite file database
		:param 
		:return: dict
		"""
		products = dict()

		db = Database()
		db.create_connection(self._file_path)
		rows = db.get_products()
		db.close_connection()

		for row in rows:
			if row[0] not in products:
				try:
					products[row[0]] = Product(row[0], row[1], row[2], row[3]) # code, price, lastupdate, currency
				except Exception as e: 
					# IF the database was not correct parsed, the item will be discarted, 
					# the event will be logged in the log file and the program will continue
					logging.error(str(datetime.now())+': ' + e)
					continue

		return products