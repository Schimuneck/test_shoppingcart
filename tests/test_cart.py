#!/usr/bin/env python

"""test_cart.py: Defines test routines."""

__author__      = "Matias A. K. Schimuneck"
__copyright__   = "Copyright 2019, Blueface - Dublin"

import unittest
import sys
import typing

sys.path.append('../')
from shoppingcart.cart import ShoppingCart
from readers.price_reader import PriceReader, JSONPriceReader, SQLitePriceReader
from currency_converter import CurrencyConverter

## CURRENCY DEFINITIONS ##
EURcurrency = 'EUR'
USDcurrency = 'USD'
GBPcurrency = 'GBP'

converter = CurrencyConverter()
def convert_wrapup(value, newcurrency):
    return round(converter.convert(value, EURcurrency, newcurrency), 2)

class TestShopping(unittest.TestCase):

    def test_add_item(self):
        self.add_item(SQLitePriceReader("../tests/data.db"))
        self.add_item(JSONPriceReader("../tests/data.json"))

    def add_item(self, reader: PriceReader):
        
        cart = ShoppingCart(reader)
        cart.add_item("a", 1)

        receipt = cart.print_receipt()

        self.assertEqual(receipt[0],"a - 1 - €1.00 - $%.2f - £%.2f" % (convert_wrapup(1.00, USDcurrency), convert_wrapup(1.00, GBPcurrency)), "Erro in test_add_item()")
        self.assertEqual(receipt[1],"Total: €1.00 - $%.2f - £%.2f" % (convert_wrapup(1.00, USDcurrency), convert_wrapup(1.00, GBPcurrency)))


    def test_add_item_with_multiple_quantity(self):
        self.add_item_with_multiple_quantity(SQLitePriceReader("../tests/data.db"))
        self.add_item_with_multiple_quantity(JSONPriceReader("../tests/data.json"))

    def add_item_with_multiple_quantity(self, reader: PriceReader):
        cart = ShoppingCart(reader)
        cart.add_item("a", 2)

        receipt = cart.print_receipt()

        self.assertEqual(receipt[0],"a - 2 - €2.00 - $%.2f - £%.2f" % (convert_wrapup(2.00, USDcurrency), convert_wrapup(2.00, GBPcurrency)))
        self.assertEqual(receipt[1],"Total: €2.00 - $%.2f - £%.2f" % (convert_wrapup(2.00, USDcurrency), convert_wrapup(2.00, GBPcurrency)))


    def test_add_same_item_multiple_times(self):
        self.add_same_item_multiple_times(SQLitePriceReader("../tests/data.db"))
        self.add_same_item_multiple_times(JSONPriceReader("../tests/data.json"))

    def add_same_item_multiple_times(self, reader: PriceReader):
        cart = ShoppingCart(reader)
        cart.add_item("a", 1)
        cart.add_item("a", 1) # add same item two times

        receipt = cart.print_receipt()

        self.assertEqual(receipt[0],"a - 2 - €2.00 - $%.2f - £%.2f" % (convert_wrapup(2.00, USDcurrency), convert_wrapup(2.00, GBPcurrency)))
        self.assertEqual(receipt[1],"Total: €2.00 - $%.2f - £%.2f" % (convert_wrapup(2.00, USDcurrency), convert_wrapup(2.00, GBPcurrency)))

    def test_add_different_items(self):
        self.add_different_items(SQLitePriceReader("../tests/data.db"))
        self.add_different_items(JSONPriceReader("../tests/data.json"))

    def add_different_items(self, reader: PriceReader):
        cart = ShoppingCart(reader)
        cart.add_item("a", 1)
        cart.add_item("b", 2)
        cart.add_item("c", 1)
        cart.add_item("d", 5)
        cart.add_item("e", 3)

        receipt = cart.print_receipt()

        self.assertEqual(receipt[0],"a - 1 - €1.00 - $%.2f - £%.2f" % (convert_wrapup(1.00, USDcurrency), convert_wrapup(1.00, GBPcurrency)))
        self.assertEqual(receipt[1],"b - 2 - €2.20 - $%.2f - £%.2f" % (convert_wrapup(2.20, USDcurrency), convert_wrapup(2.20, GBPcurrency)))
        self.assertEqual(receipt[2],"c - 1 - €1.17 - $%.2f - £%.2f" % (convert_wrapup(1.17, USDcurrency), convert_wrapup(1.17, GBPcurrency)))
        self.assertEqual(receipt[3],"d - 5 - €11.15 - $%.2f - £%.2f" % (convert_wrapup(11.15, USDcurrency), convert_wrapup(11.15, GBPcurrency)))
        self.assertEqual(receipt[4],"e - 3 - €9.00 - $%.2f - £%.2f" % (convert_wrapup(9.00, USDcurrency), convert_wrapup(9.00, GBPcurrency)))
        self.assertEqual(receipt[5],"Total: €24.52 - $%.2f - £%.2f" % (convert_wrapup(24.52, USDcurrency), convert_wrapup(24.52, GBPcurrency)))

    def test_add_invalid_items(self):
        self.add_invalid_items(SQLitePriceReader("../tests/data.db"))
        self.add_invalid_items(JSONPriceReader("../tests/data.json"))

    def add_invalid_items(self, reader: PriceReader):
        cart = ShoppingCart(reader)
        cart.add_item("a", 1)
        cart.add_item("b", 2)
        cart.add_item("x", 1) # add not defined item

        receipt = cart.print_receipt()

        print (receipt)
        self.assertEqual(receipt[0],"a - 1 - €1.00 - $%.2f - £%.2f" % (convert_wrapup(1.00, USDcurrency), convert_wrapup(1.00, GBPcurrency)))
        self.assertEqual(receipt[1],"b - 2 - €2.20 - $%.2f - £%.2f" % (convert_wrapup(2.20, USDcurrency), convert_wrapup(2.20, GBPcurrency)))
        self.assertEqual(receipt[2],"Total: €3.20 - $%.2f - £%.2f" % (convert_wrapup(3.20, USDcurrency), convert_wrapup(3.20, GBPcurrency)))

    def test_add_items_with_negative_quantity(self):
        self.add_items_with_negative_quantity(SQLitePriceReader("../tests/data.db"))
        self.add_items_with_negative_quantity(JSONPriceReader("../tests/data.json"))

    def add_items_with_negative_quantity(self, reader: PriceReader):
        cart = ShoppingCart(reader)
        cart.add_item("a", 1)
        cart.add_item("b", 2)
        cart.add_item("c", -2) # add negative quantity item

        receipt = cart.print_receipt()

        print (receipt)
        self.assertEqual(receipt[0],"a - 1 - €1.00 - $%.2f - £%.2f" % (convert_wrapup(1.00, USDcurrency), convert_wrapup(1.00, GBPcurrency)))
        self.assertEqual(receipt[1],"b - 2 - €2.20 - $%.2f - £%.2f" % (convert_wrapup(2.20, USDcurrency), convert_wrapup(2.20, GBPcurrency)))
        self.assertEqual(receipt[2],"Total: €3.20 - $%.2f - £%.2f" % (convert_wrapup(3.20, USDcurrency), convert_wrapup(3.20, GBPcurrency)))

if __name__ == '__main__':
    unittest.main()
