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
        conn = psycopg2.connect('host=127.0.0.1 dbname=postgres user=postgres password=postgres')
        df = pd.read_sql(query, conn)

    except psycopg2.DatabaseError as e:
        return print(f'Error {e}')

    finally:
        # close connection
        if conn:
            conn.close()

    return df


def query_country(country, options):
    df = pd.DataFrame()

    for option in options:
        query = f"""SELECT date, type, cases, sum(cases) OVER (ORDER BY date, type) as ccases FROM coronavirus \
                    WHERE (country = '{country}' AND cases > 0 AND type = '{option}');"""

        df_option = query_db(query)
        df = df_option.append(df, ignore_index=True)

    # clean data column
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])

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
app.layout = html.Div([

    html.Div([
        html.H1(children='Corona Dash'),
        html.Div(children='''
        A dashboard with corona data.
        '''),

        html.Label('Country'),
        dcc.Dropdown(
            id='country-dropdown',
            options=list_countries,
            value='Germany'),

        html.Label('Tpye'),
        dcc.Checklist(
            id='type-checkbox',
            options=[
                {'label': 'confirmed', 'value': 'confirmed'},
                {'label': 'recovered', 'value': 'recovered'},
                {'label': 'death', 'value': 'death'}],
            value=['confirmed', 'recovered', 'death'])
    ], style={'width': '20%', 'float': 'left', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='daily-cases-graph',
                  responsive=True)
    ], style={'width': '40%', 'float': 'center', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='daily-cases-csum-graph',
                  responsive=True)
    ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'})

])


@app.callback(
    Output('daily-cases-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('type-checkbox', 'value'))
def update_daily_graph(country_value, type_value):
    country = country_value
    options = type_value

    df = query_country(country, options)

    # bar chart with daily cases
    fig = px.line(df, x='date', y='cases', color='type',
                  labels={'date': '', 'cases': ''},
                  title='New Cases per Day',
                  template='simple_white')
    fig.update_layout(showlegend=False)

    return fig


@app.callback(
    Output('daily-cases-csum-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('type-checkbox', 'value'))
def update_daily_csum(country_value, type_value):
    country = country_value
    options = type_value

    df = query_country(country, options)

    # bar chart with daily cases
    fig = px.line(df, x='date', y='ccases', color='type',
                  labels={'date': '', 'ccases': ''},
                  title='Cumulated Cases per Day',
                  template='simple_white')
    fig.update_layout(showlegend=False)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
