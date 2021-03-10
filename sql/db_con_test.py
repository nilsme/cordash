#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import sys


def main():
    """
    Test connection to postgres DB

    :return: String with postgres DB version.
    """

    conn = None

    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute('SELECT version()')

        version = cur.fetchone()[0]
        print(version)

    except psycopg2.DatabaseError as e:\

        print(f'Error {e}')
        sys.exit(1)

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
