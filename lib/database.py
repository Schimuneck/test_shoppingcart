
"""database.py: Defines simple database methods to connect in SQLite file."""

__author__      = "Matias A. K. Schimuneck"
__copyright__   = "Copyright 2019, Blueface - Dublin"

import sqlite3
from sqlite3 import Error

import logging
LOG_FILENAME = 'shoppingcart.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

class Database():
    def __init__(self):
        """ CTOR
        :param 
        """
        self.conn = None # Connection with the SQLite database

    def create_connection(self, file_path: str):
        """ Create a database connection to a SQLite database
        :param file_path: SQLite database path
        :return: 
        """
        if self.conn:
            self.conn.close()

        try:
            self.conn = sqlite3.connect(file_path)

        except Error as e:
            print(e)

    def create_table(self, create_table_sql: str):
        """ Create a table difined in the create_table_sql param to the SQLite database
        :param create_table_sql: SQL string that defines the new table to be created
        :return: 
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            # Any problem in the creation of the table will be logged
            logging.error(str(datetime.now())+': ' + e)

    def add_product(self, product):
        """ Create insert a new product line in the PRODUCTS table to the SQLite database """
        sql = ''' INSERT INTO products(code,price,lastupdate,currency)
                  VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, product)
        return cur.lastrowid

    def get_products(self):
        """ Get all rows with all atributes af PRODUCTS table in the SQLite database
        :param 
        :return: Return a products list 
        """
        cur = self.conn.cursor()
        cur.execute("SELECT code, price, lastupdate, currency FROM products")
     
        rows = cur.fetchall()
        return rows

    def close_connection(self):
        """ Commit and finish the conection with the SQLite database
        :param 
        :return: 
        """
        if self.conn:
            self.conn.commit()
            self.conn.close()