from dash import Dash, html, dcc, dependencies
import plotly.express as px
import pandas as pd
import os
import datetime as dt

app = Dash(__name__)
last_modified = 0
df = None
df_weekly = None

def load_data():
    df = pd.read_csv("data.csv",sep=";", parse_dates=["Date"], dayfirst=True)
    #Agregate data by week and call it df_weekly, the aggregation is done on the column "Date" and the aggregated column is called week
    df_weekly = df.resample('W', on='Date').agg({'+bas': 'mean', '+haut': 'mean'})
    df_weekly = df_weekly.reset_index()
    df_weekly.columns = ['Week', '+bas', '+haut']
    last_modified = os.path.getmtime("data.csv")
    return df,df_weekly

def figure_cours():
    fig = px.line(df, x="Date", y="Dernier", title='Prix de fermeture au cours du temps')
    return fig

def figure_semaine():
    bas  = px.bar(df_weekly, x="Week", y="+bas", title='Valeur basse journalière moyenne par semaine')
    haut = px.bar(df_weekly, x="Week", y="+haut", title='Valeur haute journalière moyenne par semaine')
    return bas,haut

@app.callback(dependencies.Output('graphique_cours', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def mise_a_jour_cours(n):
    if last_modified != os.path.getmtime("data.csv"):
        df,_ = load_data()
        fig = figure_cours()
        return fig
    return fig
@app.callback(dependencies.Output('graphique_bas_semaine', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def mise_a_jour_semaine_bas(n):
    if last_modified != os.path.getmtime("data.csv"):
        _,df_weekly = load_data()
        bas,_ = figure_semaine()
        return bas
    return bas

@app.callback(dependencies.Output('graphique_haut_semaine', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def mise_a_jour_semaine_haut(n):
    if last_modified != os.path.getmtime("data.csv"):
        _,df_weekly = load_data()
        _,haut = figure_semaine()
        return haut
    return haut

if __name__ == '__main__':
    df,df_weekly = load_data()
    fig = figure_cours()
    bas,haut = figure_semaine()

    app.layout = html.Div(children=[
        html.H1(children='Dashboard LVMH'),

        dcc.Graph(
            id='graphique_cours',
            figure=fig
        ),

        dcc.Graph(
            id='graphique_bas_semaine',
            figure=bas
        ),

        dcc.Graph(
            id='graphique_haut_semaine',
            figure=haut
        ),


        dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
        )
    ])
    app.run_server(debug=True, host='172.31.2.170', port=8050)
