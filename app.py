# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import psycopg2


def query_db(query):

    conn = None

    try:
        # open connection
        conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=postgres")
        df = pd.read_sql(query, conn)

    except psycopg2.DatabaseError as e:
        return print(f'Error {e}')

    finally:
        # close connection
        if conn:
            conn.close()

    return df


def query_country(country, options):
    # query db
    df = query_db(f"""SELECT date, country, type, cases FROM coronavirus \
                      WHERE (country = '{country}' AND cases > 0 );""")
    # clean data column
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])

    # select types
    df = df.loc[df['type'].isin(options)]

    return df


def country_list():
    df = query_db("SELECT DISTINCT country FROM coronavirus;")
    df = df.sort_values(by=['country'])
    return df


list_countries = [{'label': i, 'value': i} for i in country_list()['country']]

# set dash style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# set app layout
app.layout = html.Div(children=[
    html.H1(children='Corona Dash'),

    html.Div(children='''
        A dashboard with corona data.
    '''),

    html.Label('Country'),
    dcc.Dropdown(
        id='country-dropdown',
        options=list_countries,
        value='Germany'
    ),
    html.Label('Tpye'),
    dcc.Checklist(
        id='type-checkbox',
        options=[
            {'label': 'confirmed', 'value': 'confirmed'},
            {'label': 'recovered', 'value': 'recovered'},
            {'label': 'death', 'value': 'death'}
        ],
        value=['confirmed', 'recovered', 'death']
    ),
    dcc.Graph(id='daily-cases-graph'),
    dcc.Graph(id='daily-cases-cum-graph')

], style={'columnCount': 3})


@app.callback(
    Output('daily-cases-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('type-checkbox', 'value'))
def update_daily_graph(country_value, type_value):
    country = country_value
    options = type_value

    df = query_country(country, options)

    # bar chart with daily cases
    fig_daily = px.line(df, x="date", y="cases", color='type')

    return fig_daily


@app.callback(
    Output('daily-cases-cum-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('type-checkbox', 'value'))
def update_daily_cum(country_value, type_value):
    country = country_value
    options = type_value

    df = query_country(country, options)

    # bar chart with daily cases
    fig_daily_cum = px.line(df, x="date", y="cases", color='type')
    return fig_daily_cum


if __name__ == '__main__':
    app.run_server(debug=True)
