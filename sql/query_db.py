#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from sql_queries import *


def execute_query(query):

    conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=postgres")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute(query)

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
