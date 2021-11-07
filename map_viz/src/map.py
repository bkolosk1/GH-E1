import ast
import os
from dateutil.relativedelta import relativedelta as rd
from datetime import date, datetime, timedelta

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from scipy.special import softmax

from . import DATA_DIR

RAW_DF = pd.read_csv(os.path.join(DATA_DIR, "locations.csv"), index_col=0)

structure = html.Div(
    [
        dbc.Row(style={'height': 300},
                ),
        dbc.Row(dbc.Col(
            html.H3("Slovenia's Waste Management Tracker"), width={"size": 6, "offset": 3},
        ), style={'text-align': 'center', 'height': 200},
        ),
        dbc.Row(
            dbc.Col(
                dbc.Nav([
                    dbc.NavItem([
                        html.H5("Waste class"),
                        dcc.Dropdown(
                            id="waste_class",
                            options=[{"label": "All", "value": "All"}] + [{"label": el, "value": el} for el in
                                                                          ['Baterije', 'Medicinski odpadki', 'Olje',
                                                                           'Metalni odpadki', 'Nevarne snovi',
                                                                           'Električni odpadki', 'Gradbeni odpadki',
                                                                           'Plastika', 'Papir', 'Mešana embalaža',
                                                                           'Les', 'Bio', 'Steklo']],
                            value='All')]),
                    dbc.NavItem([
                        html.H5("Location"),
                        dcc.Dropdown(
                            id="city",
                            options=[
                                {"label": "Slovenia", "value": "(46.05108, 14.50513, 8)"},
                                {"label": "Ljubljana", "value": "(46.05108, 14.50513,12)"},
                                {"label": "Maribor", "value": "(46.55472, 15.64667,12)"},
                                {"label": "Celje", "value": "(46.23092, 15.26044,12)"},
                                {"label": "Kranj", "value": "(46.23887, 14.35561,12)"},
                                {"label": "Nova Gorica", "value": "(45.95604, 13.64837,12)"},
                                {"label": "Koper", "value": "(45.54694, 13.72944,12)"},
                                {"label": "Novo Mesto", "value": "(45.80397, 15.16886,12)"},
                                {"label": "Murska Sobota", "value": "(46.6625, 16.16639,12)"}
                            ], style={'width': 200},
                            value="(46.05108, 14.50513, 8)"), ], ),
                    dbc.NavItem([
                        html.H5("Date"),
                        dcc.DatePickerSingle(
                            id="Date",
                            min_date_allowed=date(2017, 1, 1),
                            max_date_allowed=date(2020, 8, 31),
                            initial_visible_month=date(2020, 8, 31),
                            date=date(2020, 8, 31)
                        )]),
                    dbc.NavItem(
                        dbc.Button(
                            "Plot",
                            id="trigger_plot",
                            n_clicks=0, style={'background-color': 'black'})),
                    dbc.NavItem([
                        html.H5("Hack it?"),
                        dcc.Checklist(
                            id="is_green",
                            options=[{'label': "YES!", 'value': "YES!"}],
                            value=["YES!"])]),

                ]),
                width={"size": 6, "offset": 4}, style={'text-align': 'center'}),
            style={'text-align': 'center'}),
        dbc.Row(
            [
                dbc.Col(dcc.Slider(
                    id='date_offset',
                    min=0,
                    max=30,
                    step=None,
                    marks={h: {'label': str(h - 30), 'style': {'color': 'black'}} for h in range(0, 31)},
                    # marks={i:{f"-{30-i-1}", 'style':{'color':'black'}} for i in range(0, 30)},
                    # marks={i:f"-{30-i-1}" for i in range(0, 30)},

                    value=30
                ), width={"size": 9, "offset": 1}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='map_graph')
                        , width={'size': 9, 'offset': 1}
                        )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='bar_graph')
                        , width={'size': 9, 'offset': 1}
                        )
            ]
        )
    ]
)

APP = dash.Dash(external_stylesheets=[dbc.themes.LUX])
APP.layout = html.Div([

    html.Div(structure),

], style={'background-image': 'url(https://wallpapercave.com/wp/wp3278004.jpg)', 'opacity': 0.75, 'height': '100%',
          'color': 'black'})

RAW_DF_CLUS = pd.read_csv(os.path.join(DATA_DIR, "EVL_boshko_done_DB-6700.csv"), index_col=0)
ALL_LOCS_OD = RAW_DF_CLUS[
    ['DB_CLUSTER_LOCATION_ODDAJA', 'DB_CLUSTER_LOCATION_ODDAJA_X', "DB_CLUSTER_LOCATION_ODDAJA_Y"]].drop_duplicates(
    subset=['DB_CLUSTER_LOCATION_ODDAJA']).sort_values(by='DB_CLUSTER_LOCATION_ODDAJA').reset_index(drop=True).rename(
    {"DB_CLUSTER_LOCATION_ODDAJA": "cluster_id"}, axis=1)
ALL_LOCS_DO = RAW_DF_CLUS[
    ['DB_CLUSTER_LOCATION_PREJEMA', 'DB_CLUSTER_LOCATION_PREJEMA_X', "DB_CLUSTER_LOCATION_PREJEMA_Y"]].drop_duplicates(
    subset=['DB_CLUSTER_LOCATION_PREJEMA']).sort_values(by='DB_CLUSTER_LOCATION_PREJEMA').reset_index(drop=True).rename(
    {"DB_CLUSTER_LOCATION_PREJEMA": "cluster_id"}, axis=1)
ALL_LOCS = ALL_LOCS_OD.merge(ALL_LOCS_DO, how='outer', on='cluster_id')
ALL_LOCS['X'] = ALL_LOCS[['DB_CLUSTER_LOCATION_PREJEMA_X', 'DB_CLUSTER_LOCATION_ODDAJA_X']].max(axis=1)
ALL_LOCS['Y'] = ALL_LOCS[['DB_CLUSTER_LOCATION_PREJEMA_Y', 'DB_CLUSTER_LOCATION_ODDAJA_Y']].max(axis=1)
ALL_LOCS = ALL_LOCS[['cluster_id', "X", "Y"]].set_index("cluster_id")

OLD_LOCS = pd.read_csv(os.path.join(DATA_DIR, "locations.csv"))


def filter_data(df: pd.DataFrame, filters: dict):
    ret_df = df.copy()
    for k, v in filters.items():
        print(k, v)
        if v == "All":
            continue
        ret_df = ret_df.loc[ret_df[k] == v]
    return ret_df


class MapPlot:

    def __init__(self) -> None:
        self.data_dir = DATA_DIR

    @APP.callback(
        dash.dependencies.Output("map_graph", 'figure'),
        [dash.dependencies.Input("trigger_plot", "n_clicks")],
        [dash.dependencies.State("waste_class", 'value'), dash.dependencies.State("city", 'value'),
         dash.dependencies.State("Date", "date"), dash.dependencies.State("date_offset", "value"),
         dash.dependencies.State("is_green", "value")]
    )
    def update_graph(*args):
        print("Updating graph..")

        waste_class = args[1]
        loc_info = ast.literal_eval(args[2])
        default_frame = {'lat': loc_info[0], 'lon': loc_info[1]}
        default_zoom = loc_info[2]
        curr_date = pd.Timestamp(args[3]).date()
        date_offset = rd(days=30 - args[4] - 1)
        print("------------" + str(date_offset))
        curr_date = curr_date - date_offset
        curr_date = f"{curr_date:%d.%m.%y}"
        is_green = args[5]
        filters = {'NAZIV_ODPADKA_MERGED': waste_class, "DAT_ODDAJA": curr_date}

        if len(is_green) == 0:
            t_df = OLD_LOCS.copy()
            fig = px.scatter_mapbox(t_df, mapbox_style="stamen-terrain", lon='lon', lat='lat', center=default_frame,
                                    zoom=default_zoom, hover_name="Lokacija")
            fig.update_layout(height=850)
            return fig

        ## SCATTER ##
        df = filter_data(RAW_DF_CLUS, filters)


        df_out = df.groupby(['DB_CLUSTER_LOCATION_ODDAJA', ]).agg({"KOLIČINA ODPADKA v kg": "sum"}).rename(
            {"KOLIČINA ODPADKA v kg": "kg"}, axis=1)
        df_in = df.groupby(['DB_CLUSTER_LOCATION_PREJEMA', ]).agg({"KOLIČINA ODPADKA v kg": "sum"}).rename(
            {"KOLIČINA ODPADKA v kg": "kg"}, axis=1)

        df_net = df_in.join(df_out, how='outer', lsuffix="_out", rsuffix="_in").fillna(0.0)
        df_net['net_kg'] = df_net['kg_in'] - df_net['kg_out']
        df_net['abs_net_kg'] = df_net['kg_in'] + df_net['kg_out']
        df_net['abs_net_kg_log'] = np.log2(df_net["abs_net_kg"])

        df_final = df_net.join(ALL_LOCS, how='inner')

        ## LINES ##
        df_lines = filter_data(RAW_DF_CLUS, filters).groupby(
            ["DB_CLUSTER_LOCATION_ODDAJA", "DB_CLUSTER_LOCATION_PREJEMA"]).agg(
            {"KOLIČINA ODPADKA v kg": "sum", "DB_CLUSTER_LOCATION_ODDAJA_X": "first",
             "DB_CLUSTER_LOCATION_ODDAJA_Y": "first", "DB_CLUSTER_LOCATION_PREJEMA_X": "first",
             "DB_CLUSTER_LOCATION_PREJEMA_Y": "first"}).rename(
            {"DB_CLUSTER_LOCATION_ODDAJA_X": "X1", "DB_CLUSTER_LOCATION_ODDAJA_Y": "Y1",
             "DB_CLUSTER_LOCATION_PREJEMA_X": "X2", "DB_CLUSTER_LOCATION_PREJEMA_Y": "Y2",
             "KOLIČINA ODPADKA v kg": "kg"}, axis=1)
        fig_map = px.scatter_mapbox(df_final, mapbox_style="stamen-terrain", lon='Y', lat='X', color='net_kg',
                                    size='abs_net_kg_log')

        fig_lines = go.Figure()
        for i in range(len(df_lines)):
            fig_lines.add_trace(
                go.Scattermapbox(
                    lat=[list(df_lines['X1'])[i], list(df_lines['X2'])[i]],
                    lon=[list(df_lines['Y1'])[i], list(df_lines['Y2'])[i]],
                    mode='lines',
                    line=dict(width=int(np.log10(list(df_lines['kg'])[i])), color='red'),
                    # text =[f"Total kg.: {list(df_lines['kg'])[i]}"],
                    # hoverinfo ='text'                    
                    # opacity = float(df_flight_paths['cnt'][i]) / float(df_flight_paths['cnt'].max()),
                )
            )

        fig3 = go.Figure(data=fig_map.data + fig_lines.data,
                         layout={"colorscale": go.layout.Colorscale(diverging='solar')})
        # fig3 = go.Figure(data= fig_lines.data, layout = { "colorscale": go.layout.Colorscale(diverging='solar')})
        fig3.update_layout({"showlegend": False, "mapbox_style": "stamen-terrain"},
                           mapbox={'center': default_frame, 'zoom': default_zoom}, height=850)

        return fig3

    @APP.callback(
        dash.dependencies.Output("bar_graph", 'figure'),
        [dash.dependencies.Input("trigger_plot", "n_clicks")],
        [dash.dependencies.State("waste_class", 'value'), dash.dependencies.State("Date", "date"),
         dash.dependencies.State("date_offset", "value")]
    )
    def update_graph(*args):
        print("Updating histogram..")

        waste_class = args[1]
        curr_date = pd.Timestamp(args[2]).date()
        date_offset = rd(days=30 - args[3] - 1)
        curr_date = curr_date - date_offset
        curr_date = f"{curr_date:%d.%m.%y}"
        filters = {"DAT_ODDAJA": curr_date}
        df = filter_data(RAW_DF_CLUS, filters)
        df = df.groupby("NAZIV_ODPADKA_MERGED").agg({"KOLIČINA ODPADKA v kg": "sum"}).rename(
            {"KOLIČINA ODPADKA v kg": "kg"}, axis=1)
        df['Waste type'] = df.index
        #
        fig = px.pie(df, values='kg', names='Waste type', color='Waste type',
                     template='plotly_white')
        fig.update_layout(height=600)

        print("Done")
        return fig

    def run(self):
        APP.run_server(debug=True, host="0.0.0.0", port=8050)
