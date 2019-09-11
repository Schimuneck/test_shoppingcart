#!/usr/bin/env python

"""create_db.py: Script to populate simple SQLite database."""

__author__      = "Matias A. K. Schimuneck"
__copyright__   = "Copyright 2019, Blueface - Dublin"

import sys

sys.path.append('../')
from lib.database import Database


if __name__ == '__main__':

    db = Database()
    db.create_connection("../tests/data.db")


    sql_create_table = """CREATE TABLE IF NOT EXISTS products (
                            code text PRIMARY KEY,
                            price real NOT NULL,
                            lastupdate text,
                            currency text
                            );"""


    db.create_table(sql_create_table)

    product_a = ('a', 1.0, '10-09-2019', 'EUR')
    product_b = ('b', 1.1, '10-09-2019', 'EUR')
    product_c = ('c', 1.173, '10-09-2019', 'EUR')
    product_d = ('d', 2.233, '10-09-2019', 'EUR')
    product_e = ('e', 3.0, '10-09-2019', 'EUR')


    #create products
    print(db.add_product(product_a))
    print(db.add_product(product_b))
    print(db.add_product(product_c))
    print(db.add_product(product_d))
    print(db.add_product(product_e))


    print(db.get_products())

    db.close_connection()
