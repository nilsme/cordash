#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from sql.sql_queries import *


def execute_query(query):
    """
    Executing a SQL query on default postgres database.
    Setting up the connecting and closing it after the query. An empty query
    will default to query for a list of all tables in the database.

    :param query: An SQL query passed as a string.
    :return: 
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=postgres")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    print(query)
    cur.execute(query)

    # noinspection PyBroadException
    try:
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except:
        print('No rows were fetched.')

    finally:
        if conn:
            conn.close()


def main():
    execute_query(list_tables)


if __name__ == "__main__":
    main()
