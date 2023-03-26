from dash import Dash, html, dcc, dependencies
import plotly.express as px
import pandas as pd
import os
import datetime as dt

app = Dash(__name__)
last_modified = 0
df = None
fig = None

def load_data():
    df = pd.read_csv("data.csv",sep=";", parse_dates=["Date"], dayfirst=True)
    last_modified = os.path.getmtime("data.csv")
    return df

def create_figure():
    fig = px.line(df, x="Date", y="Dernier", title='Prix de fermeture au cours du temps')
    return fig

@app.callback(dependencies.Output('example-graph', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    if last_modified != os.path.getmtime("data.csv"):
        df = load_data()
        fig = create_figure()
        return fig
    return fig

if __name__ == '__main__':
    df = load_data()
    fig = create_figure()

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        ),

        dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
        )
    ])
    app.run_server(debug=True)
