import pandas as pd
from sqlalchemy import create_engine
from sql.query_db import execute_query
from sql.sql_queries import *


def etl_corona_data():
    """
    Load corona data to default postgres database.

    :return: None
    """
    # load data
    df = pd.read_csv('https://raw.githubusercontent.com/RamiKrispin/coronavirus/master/csv/coronavirus.csv')

    # clean data
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])

    # drop existing table
    execute_query(coronavirus_table_drop)

    # create table
    execute_query(coronavirus_table_create)

    # insert data into table
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    df.to_sql('coronavirus', engine, index=False, if_exists='append')

    # preview
    table_preview = execute_query(preview)
    table_nrows = execute_query("SELECT COUNT(*) FROM coronavirus;")

    return None


def main():
    etl_corona_data()


if __name__ == "__main__":
    main()
