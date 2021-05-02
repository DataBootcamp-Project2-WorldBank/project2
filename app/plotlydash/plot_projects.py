#Dependencies
import pandas as pd
import re
import csv
#import matplotlib.pyplot as plt
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from .layout import html_layout

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def init_projectchart (server):
  dash_app = dash.Dash(  server=server,
        routes_pathname_prefix="/dashapp/")
  # ------------------------------------------------------------------------------
  # Import and clean data (importing csv into pandas)
  project_df=pd.read_csv('data/IEG_World_Bank_Project_Performance_Ratings.csv')
  project_df=project_df.loc[:,['Country Name','IEG_Outcome']]
  project_df.columns=['country', 'IEG_Outcome']
  project_df=project_df.assign(count=1)
  project_df = project_df.groupby(['country','IEG_Outcome'])['count'].sum().reset_index()
  #project_df.head(20)
  project_df= project_df.sort_values(by=['count'], ascending=False)
  list=project_df['country'].unique()
  list.sort()
  # Custom HTML layout
  dash_app.index_string = html_layout
  # ------------------------------------------------------------------------------
  # create layout
  fig = px.bar(project_df.set_index('country'), y="count", color="IEG_Outcome", title="World bank Project",height=600)
  jls_extract_var = id
  dash_app.layout = html.Div(children=[
    html.H1(children='Project Charts',style={'text-align': 'center'}),
    dcc.Graph(
        id='bar-chart1',
        figure=fig
    ),
    html.Br(),
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in list],
        value=list[0],
        clearable=False,
    ),
    dcc.Graph(
        id='bar-chart'
    )
  ])

  @dash_app.callback(
     Output("bar-chart", "figure"),
    [Input("dropdown", "value")])
  #create the fig
  def update_chart(country):
    df=project_df.copy()
    fig1 = px.bar(df.set_index('country').loc[country],
            x='IEG_Outcome',
            y='count',
            title= 'World Bank Project for Country:'+ country,
            text='count')
    return fig1

  return dash_app.server

