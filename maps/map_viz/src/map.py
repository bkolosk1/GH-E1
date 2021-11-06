import ast
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datetime import date, datetime, timedelta

from . import DATA_DIR

APP = dash.Dash(__name__)
APP.layout = html.Div([
    html.Div([
            html.H5("Waste class"),
            html.Div(
                [
                    dcc.Dropdown(
                        id="waste_class",
                        options=[{"label":"Glass", "value":"Glass"}, {"label":"Plastic", "value":"Plastic"}],
                        value='Glass'),
                ],



            )], style={'width': '15%',
                       'display': 'inline-block', 'vertical-align': 'top'
                       }),
        html.Div([
            html.H5("City"),
            html.Div(
                [
                    dcc.Dropdown(
                        id="city",
                        options=[
                                {"label":"Slovenia",     "value":"(46.05108, 14.50513, 8)"}, 
                                {"label":"Ljubljana",     "value":"(46.05108, 14.50513,12)"}, 
                                {"label":"Maribor",       "value":"(46.55472, 15.64667,12)"},
                                {"label":"Celje",         "value":"(46.23092, 15.26044,12)"},
                                {"label":"Kranj",         "value":"(46.23887, 14.35561,12)"},
                                {"label":"Nova Gorica",   "value":"(45.95604, 13.64837,12)"},
                                {"label":"Koper",         "value":"(45.54694, 13.72944,12)"},
                                {"label":"Novo Mesto",    "value":"(45.80397, 15.16886,12)"},
                                {"label":"Murska Sobota", "value":"(46.6625, 16.16639,12)"}
                        ],
                        value="(46.05108, 14.50513, 8)"),
                ],

            )], style={'width': '15%',
                       'display': 'inline-block', 'vertical-align': 'top'
                       }),
        html.Div(
            [
                html.H5("Date"),
                dcc.DatePickerSingle(
                    id="Date",
                    min_date_allowed=date(2017, 1, 1),
                    max_date_allowed=date(2021, 8, 31),
                    initial_visible_month=date(2021, 8, 31),
                    date=date(2021, 8, 31)
                ),
            ],

                style={'width': '20%',
                    'display': 'inline-block', 'vertical-align': 'top'
                    }),
        html.Div([
            html.Div(
                [
                    html.Button(
                        "Plot",
                        id="trigger_plot",
                        n_clicks=0)
                ],
            )], style={'width': '5%',
                       'display': 'inline-block', 'vertical-align': 'top'
                       }),
    html.Div([
            # html.H5("City"),
            html.Div(
                [
                    dcc.Slider(
                        min=0,
                        max=30,
                        step=None,
                        marks={i:f"-{30-i-1}" for i in range(0, 30)},
                            
                        value=5
                        )
                ],

            )], style={'width': '100%',
                       'display': 'inline-block', 'vertical-align': 'top'
                       }),

    html.Div([
            dcc.Graph(id='map_graph')
        ]
                       ),

])


RAW_DF =  pd.read_csv(os.path.join(DATA_DIR, "locations.csv"), index_col=0)
class MapPlot:

    def __init__(self) -> None:
        self.data_dir = DATA_DIR
        # self.raw_df =
    
    @APP.callback(
        dash.dependencies.Output("map_graph", 'figure'),
        [dash.dependencies.Input("trigger_plot", "n_clicks")],
        [dash.dependencies.State("waste_class", 'value'), dash.dependencies.State("city", 'value')]
    )
    def update_graph(*args):
        print("Updating graph..")

        waste_class = args[1]
        loc_info = ast.literal_eval(args[2])
        default_frame = {'lat': loc_info[0], 'lon':loc_info[1]}
        default_zoom = loc_info[2]

        #TODO: ADD FILTERS FOR DF ACCORING TO TEXT FIELDS
        df = RAW_DF.copy()
        # breakpoint()
        # fig = px.scatter_mapbox(df, mapbox_style="stamen-terrain", lon='lon', lat='lat', animation_frame='year', size='pop', center=default_frame, zoom=default_zoom)
        fig = px.scatter_mapbox(df, mapbox_style="stamen-terrain", lon='lon', lat='lat', center=default_frame, zoom=default_zoom, hover_name="Lokacija")
        fig.update_layout(width = 1750, height=850)
        return fig


    def run(self):
        APP.run_server(debug=True, host="0.0.0.0", port=8050)

    



    